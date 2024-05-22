from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import UnusualWhalesClient
from ...models.error_message import ErrorMessage
from ...models.spot_gex_exposures_per_1_min_results import SpotGEXExposuresPer1MinResults
from ...types import UNSET, Response, Unset


def _get_kwargs(
    ticker: str,
    *,
    date: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    # Dictionary of query parameters to be sent with the request.
    params: Dict[str, Any] = {}

    params["date"] = date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/stock/{ticker}/spot-exposures",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: UnusualWhalesClient, response: httpx.Response
) -> Optional[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
    response_json = response.json()
    if response_json.get("data") is not None:
        response_json = response_json["data"]
    if response.status_code == HTTPStatus.OK:
        response_200 = SpotGEXExposuresPer1MinResults.from_dict(response.json())

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
) -> Response[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
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
    date: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
    """Spot GEX exposures per 1min

     Returns the spot GEX exposures for the given ticker per minute.

    Spot GEX is the assumed $ value of the given greek (ie. gamma) exposure that market makers need to
    hedge per 1% change of the underlying stock's price movement. A positive value is long and a
    negative value is short.

    Investors and large funds lower risk and protect their money by selling calls and buying puts.
    Market makers provide the liquidity to facilitate these trades.

    GEX assumes that market makers are part of every transaction and that the bulk of their transactions
    are buying calls and selling puts to investors hedging their portfolios.

    If a market maker has one contract open with a gamma value of 0.05, then if the underlying stock
    price moves by 1%, that market maker is exposed to $[0.05 * 100 shares * 0.01 * stock price *
    underlying parameter of the greek variable (for gamma this variable is the stock price)]. The total
    market maker spot exposure is calculated by summing up the spot exposure of all open contracts
    determined by the daily open interest or by volume.

    Market makers profit from the bid-ask spreads and as such, they constantly gamma hedge (they buy and
    sell shares to keep their positions delta neutral).

    Long call positions are positive gamma - as the stock price increases and delta rises (approaches
    1), market makers hedge by selling shares, and they buy shares if the stock price decreases and
    delta falls.

    Short put positions are negative gamma - as the stock price increases and delta falls (approaches
    -1), market makers hedge by buying shares, and they sell shares if the stock price decreases and
    delta rises.

    As such, in the event of large positive gamma, volatility is suppressed as market makers will hedge
    by buying as the stock price decreases and selling as the stock price increases. And in the event of
    large negative gamma, volatility is amplified as market makers will hedge by buying as the stock
    price increases and selling as the stock price decreases.

    Args:
        ticker (str): A single ticker Example: AAPL.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
        date=date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticker: str,
    *,
    client: UnusualWhalesClient,
    date: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
    """Spot GEX exposures per 1min

     Returns the spot GEX exposures for the given ticker per minute.

    Spot GEX is the assumed $ value of the given greek (ie. gamma) exposure that market makers need to
    hedge per 1% change of the underlying stock's price movement. A positive value is long and a
    negative value is short.

    Investors and large funds lower risk and protect their money by selling calls and buying puts.
    Market makers provide the liquidity to facilitate these trades.

    GEX assumes that market makers are part of every transaction and that the bulk of their transactions
    are buying calls and selling puts to investors hedging their portfolios.

    If a market maker has one contract open with a gamma value of 0.05, then if the underlying stock
    price moves by 1%, that market maker is exposed to $[0.05 * 100 shares * 0.01 * stock price *
    underlying parameter of the greek variable (for gamma this variable is the stock price)]. The total
    market maker spot exposure is calculated by summing up the spot exposure of all open contracts
    determined by the daily open interest or by volume.

    Market makers profit from the bid-ask spreads and as such, they constantly gamma hedge (they buy and
    sell shares to keep their positions delta neutral).

    Long call positions are positive gamma - as the stock price increases and delta rises (approaches
    1), market makers hedge by selling shares, and they buy shares if the stock price decreases and
    delta falls.

    Short put positions are negative gamma - as the stock price increases and delta falls (approaches
    -1), market makers hedge by buying shares, and they sell shares if the stock price decreases and
    delta rises.

    As such, in the event of large positive gamma, volatility is suppressed as market makers will hedge
    by buying as the stock price decreases and selling as the stock price increases. And in the event of
    large negative gamma, volatility is amplified as market makers will hedge by buying as the stock
    price increases and selling as the stock price decreases.

    Args:
        ticker (str): A single ticker Example: AAPL.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]
    """

    return sync_detailed(
        ticker=ticker,
        client=client,
        date=date,
    ).parsed


async def asyncio_detailed(
    ticker: str,
    *,
    client: UnusualWhalesClient,
    date: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
    """Spot GEX exposures per 1min

     Returns the spot GEX exposures for the given ticker per minute.

    Spot GEX is the assumed $ value of the given greek (ie. gamma) exposure that market makers need to
    hedge per 1% change of the underlying stock's price movement. A positive value is long and a
    negative value is short.

    Investors and large funds lower risk and protect their money by selling calls and buying puts.
    Market makers provide the liquidity to facilitate these trades.

    GEX assumes that market makers are part of every transaction and that the bulk of their transactions
    are buying calls and selling puts to investors hedging their portfolios.

    If a market maker has one contract open with a gamma value of 0.05, then if the underlying stock
    price moves by 1%, that market maker is exposed to $[0.05 * 100 shares * 0.01 * stock price *
    underlying parameter of the greek variable (for gamma this variable is the stock price)]. The total
    market maker spot exposure is calculated by summing up the spot exposure of all open contracts
    determined by the daily open interest or by volume.

    Market makers profit from the bid-ask spreads and as such, they constantly gamma hedge (they buy and
    sell shares to keep their positions delta neutral).

    Long call positions are positive gamma - as the stock price increases and delta rises (approaches
    1), market makers hedge by selling shares, and they buy shares if the stock price decreases and
    delta falls.

    Short put positions are negative gamma - as the stock price increases and delta falls (approaches
    -1), market makers hedge by buying shares, and they sell shares if the stock price decreases and
    delta rises.

    As such, in the event of large positive gamma, volatility is suppressed as market makers will hedge
    by buying as the stock price decreases and selling as the stock price increases. And in the event of
    large negative gamma, volatility is amplified as market makers will hedge by buying as the stock
    price increases and selling as the stock price decreases.

    Args:
        ticker (str): A single ticker Example: AAPL.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
        date=date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticker: str,
    *,
    client: UnusualWhalesClient,
    date: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]]:
    """Spot GEX exposures per 1min

     Returns the spot GEX exposures for the given ticker per minute.

    Spot GEX is the assumed $ value of the given greek (ie. gamma) exposure that market makers need to
    hedge per 1% change of the underlying stock's price movement. A positive value is long and a
    negative value is short.

    Investors and large funds lower risk and protect their money by selling calls and buying puts.
    Market makers provide the liquidity to facilitate these trades.

    GEX assumes that market makers are part of every transaction and that the bulk of their transactions
    are buying calls and selling puts to investors hedging their portfolios.

    If a market maker has one contract open with a gamma value of 0.05, then if the underlying stock
    price moves by 1%, that market maker is exposed to $[0.05 * 100 shares * 0.01 * stock price *
    underlying parameter of the greek variable (for gamma this variable is the stock price)]. The total
    market maker spot exposure is calculated by summing up the spot exposure of all open contracts
    determined by the daily open interest or by volume.

    Market makers profit from the bid-ask spreads and as such, they constantly gamma hedge (they buy and
    sell shares to keep their positions delta neutral).

    Long call positions are positive gamma - as the stock price increases and delta rises (approaches
    1), market makers hedge by selling shares, and they buy shares if the stock price decreases and
    delta falls.

    Short put positions are negative gamma - as the stock price increases and delta falls (approaches
    -1), market makers hedge by buying shares, and they sell shares if the stock price decreases and
    delta rises.

    As such, in the event of large positive gamma, volatility is suppressed as market makers will hedge
    by buying as the stock price decreases and selling as the stock price increases. And in the event of
    large negative gamma, volatility is amplified as market makers will hedge by buying as the stock
    price increases and selling as the stock price decreases.

    Args:
        ticker (str): A single ticker Example: AAPL.
        date (Union[Unset, str]): A trading date in the format of YYYY-MM-DD.
            This is optional and by default the last trading date.
             Example: 2024-01-18.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorMessage, SpotGEXExposuresPer1MinResults, str]
    """

    return (
        await asyncio_detailed(
            ticker=ticker,
            client=client,
            date=date,
        )
    ).parsed
