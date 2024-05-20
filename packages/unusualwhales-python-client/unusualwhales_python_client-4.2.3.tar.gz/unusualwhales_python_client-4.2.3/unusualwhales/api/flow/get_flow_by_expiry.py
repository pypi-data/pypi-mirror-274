from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import UnusualWhalesClient
from ...models.flow_per_expiry_results import FlowPerExpiryResults
from ...types import Response


def _get_kwargs(
    ticker: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/stock/{ticker}/flow-per-expiry",
    }

    return _kwargs


def _parse_response(
    *, client: UnusualWhalesClient, response: httpx.Response
) -> Optional[FlowPerExpiryResults]:
    response_json = response.json()
    if response_json.get("data") is not None:
        response_json = response_json["data"]
    if response.status_code == HTTPStatus.OK:
        response_200 = FlowPerExpiryResults.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: UnusualWhalesClient, response: httpx.Response
) -> Response[FlowPerExpiryResults]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticker: str,
    *,
    client: UnusualWhalesClient,
) -> Response[FlowPerExpiryResults]:
    """Option Order Flow for a Ticker Grouped by Expiry

     Returns all option orders grouped by expiry for a given ticker for the last Trading Day

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlowPerExpiryResults]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticker: str,
    *,
    client: UnusualWhalesClient,
) -> Optional[FlowPerExpiryResults]:
    """Option Order Flow for a Ticker Grouped by Expiry

     Returns all option orders grouped by expiry for a given ticker for the last Trading Day

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlowPerExpiryResults
    """

    return sync_detailed(
        ticker=ticker,
        client=client,
    ).parsed


async def asyncio_detailed(
    ticker: str,
    *,
    client: UnusualWhalesClient,
) -> Response[FlowPerExpiryResults]:
    """Option Order Flow for a Ticker Grouped by Expiry

     Returns all option orders grouped by expiry for a given ticker for the last Trading Day

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlowPerExpiryResults]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticker: str,
    *,
    client: UnusualWhalesClient,
) -> Optional[FlowPerExpiryResults]:
    """Option Order Flow for a Ticker Grouped by Expiry

     Returns all option orders grouped by expiry for a given ticker for the last Trading Day

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlowPerExpiryResults
    """

    return (
        await asyncio_detailed(
            ticker=ticker,
            client=client,
        )
    ).parsed
