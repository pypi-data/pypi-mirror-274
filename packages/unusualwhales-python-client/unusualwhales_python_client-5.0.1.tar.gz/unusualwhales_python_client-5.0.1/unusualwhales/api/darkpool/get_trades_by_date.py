from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import UnusualWhalesClient
from ...models.darkpool_trade_response import DarkpoolTradeResponse
from ...models.error_message import ErrorMessage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = UNSET,
    date: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    # Dictionary of query parameters to be sent with the request.
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["date"] = date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/darkpool/recent",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: UnusualWhalesClient, response: httpx.Response
) -> Optional[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    response_json = response.json()
    if response_json.get("data") is not None:
        response_json = response_json["data"]
    if response.status_code == HTTPStatus.OK:
        response_200 = DarkpoolTradeResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ErrorMessage.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = response.text
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: UnusualWhalesClient, response: httpx.Response
) -> Response[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: UnusualWhalesClient,
    limit: Union[Unset, int] = UNSET,
    date: Union[Unset, str] = UNSET,
) -> Response[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    """Darkpool trades for a given date. All Symbols.

     Returns the latest darkpool trades.

    Args:
        limit (Union[Unset, int]): How many items to return. Default: 100. Max: 200. Min: 1.
            Example: 10.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DarkpoolTradeResponse, ErrorMessage, str]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        date=date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: UnusualWhalesClient,
    limit: Union[Unset, int] = UNSET,
    date: Union[Unset, str] = UNSET,
) -> Optional[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    """Darkpool trades for a given date. All Symbols.

     Returns the latest darkpool trades.

    Args:
        limit (Union[Unset, int]): How many items to return. Default: 100. Max: 200. Min: 1.
            Example: 10.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DarkpoolTradeResponse, ErrorMessage, str]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        date=date,
    ).parsed


async def asyncio_detailed(
    *,
    client: UnusualWhalesClient,
    limit: Union[Unset, int] = UNSET,
    date: Union[Unset, str] = UNSET,
) -> Response[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    """Darkpool trades for a given date. All Symbols.

     Returns the latest darkpool trades.

    Args:
        limit (Union[Unset, int]): How many items to return. Default: 100. Max: 200. Min: 1.
            Example: 10.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DarkpoolTradeResponse, ErrorMessage, str]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        date=date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: UnusualWhalesClient,
    limit: Union[Unset, int] = UNSET,
    date: Union[Unset, str] = UNSET,
) -> Optional[Union[DarkpoolTradeResponse, ErrorMessage, str]]:
    """Darkpool trades for a given date. All Symbols.

     Returns the latest darkpool trades.

    Args:
        limit (Union[Unset, int]): How many items to return. Default: 100. Max: 200. Min: 1.
            Example: 10.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DarkpoolTradeResponse, ErrorMessage, str]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            date=date,
        )
    ).parsed
