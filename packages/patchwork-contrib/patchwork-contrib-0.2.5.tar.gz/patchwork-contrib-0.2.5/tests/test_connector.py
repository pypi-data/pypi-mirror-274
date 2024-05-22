# -*- coding: utf-8 -*-
import asyncio

from typing import List, AsyncIterable

from aiohttp import web, StreamReader
from pydantic import BaseModel

import pytest

from patchwork.contrib.common import HTTPConnector
from patchwork.contrib.common.connector import ConnectorError, ConnectorPreconditionFailed


class TestModel(BaseModel):
    pass


@pytest.mark.asyncio
async def test_response_no_content(aiohttp_raw_server):

    async def handler(request):
        return web.Response(status=204)

    data_endpoint = await aiohttp_raw_server(handler)
    await data_endpoint.start_server()

    connector = HTTPConnector(endpoint_url=str(data_endpoint.make_url('/')))

    async with connector:
        response = await connector.send('get', '/', response_model=None)
        assert response is None

        with pytest.raises(ConnectorError):
            # expected model, got No content response
            response = await connector.send('get', '/', response_model=TestModel)


@pytest.mark.asyncio
async def test_expected_model(aiohttp_raw_server):

    async def handler(request):
        return web.json_response({})

    data_endpoint = await aiohttp_raw_server(handler)
    await data_endpoint.start_server()

    connector = HTTPConnector(endpoint_url=str(data_endpoint.make_url('/')))

    async with connector:
        response = await connector.send('get', '/', response_model=TestModel)
        assert isinstance(response, TestModel)

        with pytest.raises(ConnectorError):
            # empty response expected, got content
            response = await connector.send('get', '/', response_model=None)


@pytest.mark.asyncio
async def test_expected_list(aiohttp_raw_server):

    async def handler(request):
        return web.json_response([{}, {}])

    data_endpoint = await aiohttp_raw_server(handler)
    await data_endpoint.start_server()

    connector = HTTPConnector(endpoint_url=str(data_endpoint.make_url('/')))

    async with connector:
        response = await connector.send('get', '/', response_model=List[TestModel])
        assert isinstance(response, list)
        assert len(response) == 2
        assert isinstance(response[0], TestModel) and isinstance(response[1], TestModel)


@pytest.mark.asyncio
async def test_expected_stream(aiohttp_raw_server):

    class AIter:
        async def __aiter__(self):
            for x in range(5):
                await asyncio.sleep(0)
                yield b'content'
    async def handler(request):
        resp = web.StreamResponse(headers={'Content-Length': "35"})
        await resp.prepare(request)
        await asyncio.sleep(0.01)
        async for c in AIter():
            await resp.write(c)
            await asyncio.sleep(0.01)

        await resp.write_eof()
        return resp

    data_endpoint = await aiohttp_raw_server(handler)
    await data_endpoint.start_server()

    connector = HTTPConnector(endpoint_url=str(data_endpoint.make_url('/')))

    async with connector:
        response = await connector.send('get', '/', response_model=AsyncIterable)
        assert isinstance(response, StreamReader)
        await asyncio.sleep(0.1)
        async for chunk, _ in response.iter_chunks():
            assert chunk == b'content'


@pytest.mark.asyncio
async def test_api_version_exact(aiohttp_raw_server):
    async def handler(request):
        return web.json_response({}, headers={'X-API-Version': '2'})

    data_endpoint = await aiohttp_raw_server(handler)
    await data_endpoint.start_server()

    connector = HTTPConnector(endpoint_url=str(data_endpoint.make_url('/')))
    async with connector:
        assert await connector.send('get', '/', response_model=TestModel, api_version='=2'), "exact version"
        assert await connector.send('get', '/', response_model=TestModel, api_version='>1'), "greater than version"
        assert await connector.send('get', '/', response_model=TestModel, api_version='<3'), "lower than version"

        with pytest.raises(ConnectorPreconditionFailed):    # exact not match
            await connector.send('get', '/', response_model=TestModel, api_version='=1')

        with pytest.raises(ConnectorPreconditionFailed):    # greater not match
            await connector.send('get', '/', response_model=TestModel, api_version='>2')

        with pytest.raises(ConnectorPreconditionFailed):    # lower not match
            await connector.send('get', '/', response_model=TestModel, api_version='<2')

        with pytest.raises(ValueError): #   invalid version
            assert await connector.send('get', '/', response_model=TestModel, api_version='1')
