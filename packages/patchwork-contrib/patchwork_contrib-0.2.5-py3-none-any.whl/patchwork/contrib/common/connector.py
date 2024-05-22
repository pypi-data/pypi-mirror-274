# -*- coding: utf-8 -*-
from collections import abc
from importlib.metadata import version

import aiohttp
import json
import sys
from pydantic import BaseModel
from typing import Literal, Union, Type, Any, TypeVar, List, get_args, get_origin, AsyncIterable

from patchwork.core import Component
from patchwork.core.stubs.prometheus import DummyMetric

try:
    from prometheus_client import Histogram, Info
except ImportError:
    from patchwork.core.stubs.prometheus import Histogram, Info


request_time = Histogram('connector_request_time', "Connector endpoint time", ["method", "url", "user_agent", "version"])
conn_info = Info("connector_endpoint_info", "Connector endpoint info")


class ConnectorError(Exception):
    pass


class ConnectorResponseError(ConnectorError):
    def __init__(self, code):
        self.code = code


class ConnectorBadData(ConnectorResponseError):
    def __init__(self, response):
        self.response = response
        super().__init__(code=422)


class ConnectorForbidden(ConnectorResponseError):
    def __init__(self):
        super().__init__(code=403)


class ConnectorNotFound(ConnectorResponseError):
    def __init__(self):
        super().__init__(code=404)


class ConnectorPreconditionFailed(ConnectorResponseError):
    def __init__(self, version: int = None, supported: int = None):
        self.version = version
        self.version_compatible = supported
        super().__init__(code=412)


class ConnectorTooManyAttempts(ConnectorResponseError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(code=429)


T = TypeVar('T')


def int_or_none(value: Union[str, int, None]) -> Union[int, None]:
    if value is None:
        return None
    elif isinstance(value, int):
        return value
    else:
        try:
            return int(value)
        except ValueError:
            return None


def match_version(requested_version: str, current_version: int, min_supported: int) -> Union[int, bool, None]:

    if requested_version[0] == '>':
        greater_than = int_or_none(requested_version[1:])
        if not greater_than or current_version <= greater_than:
            return False
        return current_version

    elif requested_version[0] == '<':
        lower_than = int_or_none(requested_version[1:])
        if not lower_than or min_supported >= lower_than:
            return False
        return max(lower_than - 1, current_version)

    elif requested_version[0] == '=':
        version = int_or_none(requested_version[1:])
        if not version or not (min_supported <= version <= current_version):
            return False
        else:
            return max(version, current_version)

    return None

class PrometheusMixin:

    settings: Any
    connector_version: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Histogram is DummyMetric:
            raise RuntimeError("unable to use prometheus metrics mixin without Prometheus Client installed")

        conn_info.info({
            "version": self.connector_version,
            "user_agent": self.settings.user_agent,
            "endpoint_url": self.settings.endpoint_url,
            "timeout": self.settings.timeout
        })

    async def send(
            self,
            method: Literal['get', 'head', 'post', 'put', 'patch', 'delete'],
            url: str = '/',
            **kwargs
    ) -> Union[T, None]:
        with request_time.labels(
            method=method,
            url=url,
            user_agent=self.settings.user_agent,
            version=self.connector_version
        ).time():
            return await super().send(method, url, **kwargs)


class HTTPConnector(Component):

    class Config(Component.Config):
        timeout: int = 60
        max_conn_limit: int = 100
        user_agent: str = None
        endpoint_url: str

    session: aiohttp.ClientSession
    connector_version = version('patchwork-contrib') if 'patchwork-contrib' in sys.modules else ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeout = aiohttp.ClientTimeout(total=self.settings.timeout)

    async def _start(self) -> bool:
        connector = aiohttp.TCPConnector(limit=self.settings.max_conn_limit)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.settings.user_agent:
            headers['user-agent'] = self.settings.user_agent

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self._timeout,
            headers=headers,
            base_url=self.settings.endpoint_url,
            raise_for_status=False,
            cookie_jar=aiohttp.DummyCookieJar()     # do not store any cookies for inter-services communication
        )
        return True

    async def _stop(self) -> bool:
        await self.session.close()
        return False

    async def send(
            self,
            method: Literal['get', 'head', 'post', 'put', 'patch', 'delete'],
            url: str = '/',
            *,
            payload: BaseModel = None,
            response_model: Type[T] = Any,
            data=None,
            api_version: str=None,
            **options,
    ) -> Union[T, None]:

        options.setdefault('headers', {})
        if api_version is not None:
            # validate API version request
            if __debug__:
                # check version format only in debug to catch programmer mistakes
                if api_version[0] not in {'<', '>', '='} or int_or_none(api_version[1:]) is None:
                    raise ValueError(f'invalid API version requested: {api_version}')

            options['headers']['X-API-Version'] = api_version

        if data is None:
            if payload is not None:
                # use pydantic JSON encoder instead of aiohttp, as pydantic one supports all types
                # supported by pydantic
                data = payload.model_dump_json().encode('utf-8')

        if method == 'get':
            assert data is None, \
                'payload forbidden on GET method'
            response = await self.session.get(url, **options)
        elif method == 'head':
            assert data is None, \
                'payload forbidden on HEAD method'
            response = await self.session.head(url, **options)
        elif method == 'post':
            response = await self.session.post(url, data=data, **options)
        elif method == 'put':
            response = await self.session.put(url, data=data, **options)
        elif method == 'patch':
            response = await self.session.patch(url, data=data, **options)
        elif method == 'delete':
            assert data is None, \
                "payload is forbidden on DELETE method"
            response = await self.session.delete(url, **options)
        else:
            raise NotImplementedError('not supported HTTP method')

        if api_version and response.ok:
            resp_version = int_or_none(response.headers.get('X-API-Version'))

            if not resp_version or not match_version(api_version, resp_version, resp_version):
                # API version requested but no version returned or unsupported version returned
                raise ConnectorPreconditionFailed(
                    version=resp_version,
                    supported=int_or_none(response.headers.get('X-API-Version-Compatible'))
                )

        try:
            return await self._handle_response(response, response_model)
        except ConnectorResponseError:
            # response errors just re-raise
            if not response.closed:
                response.close()
            raise
        except Exception as e:
            if not response.closed:
                response.close()
            raise ConnectorError() from e

    async def _handle_response(
            self,
            response: aiohttp.ClientResponse,
            response_model: Union[Type[BaseModel], Any, None, List[BaseModel], AsyncIterable]
    ) -> Union[BaseModel, List[BaseModel], None, AsyncIterable]:

        if response.status in {200, 201, 202}:
            if response_model is Any:
                return None
            elif response_model is None:
                if response.content_length is not None:
                    raise ValueError('empty response expected')
                return None

            if not response.content_length:
                raise ValueError('missing data')

            orig = get_origin(response_model)

            if orig is abc.AsyncIterable:
                return response.content

            data = await response.read()
            if response.content_type == 'application/json':
                data = json.loads(data)

            if orig is list:
                if not isinstance(data, list):
                    raise ValueError("list is expected, but endpoint returned not a list")

                model = get_args(response_model)[0]
                return [model(**d) for d in data]

            return response_model(**data)
        elif response.status == 204:
            if response_model is not Any and response_model is not None:
                raise ValueError('response data expected, but 204 No Content response received')
            return None
        elif response.status == 403:
            raise ConnectorForbidden()
        elif response.status == 404:
            raise ConnectorNotFound()
        elif response.status == 412:
            raise ConnectorPreconditionFailed(
                version=int_or_none(response.headers.get('X-API-Version')),
                supported=int_or_none(response.headers.get('X-API-Version-Compatible'))
            )
        elif response.status == 422:
            raise ConnectorBadData(await response.json())
        elif response.status == 429:
            raise ConnectorTooManyAttempts(int(response.headers.get('Retry-After', '0')))
        else:
            raise ConnectorResponseError(code=response.status)
