# easyoanda

An easy way to trade your [&copy;OANDA](https://www.oanda.com/) account.

<p>&nbsp;</p>

# Legal  Disclaimer
#### Disclaimer:
> This Python module, `easyoanda`, utilizes a RESTful API provided by &copy;OANDA for accessing financial data, managing accounts, and trading financial instruments. While the &copy;OANDA API is publicly available [here](https://developer.oanda.com/rest-live-v20/introduction/), and clearly lays out best practices [here](https://developer.oanda.com/rest-live-v20/best-practices/) and [here](https://developer.oanda.com/rest-live-v20/development-guide/), it's important to note that using this module without explicit permission from &copy;OANDA may potentially infringe upon their terms of service or acceptable use policies as provided for United States account holders [here](https://www.oanda.com/us-en/legal/) (non-US account holders, please see IMPORTANT DISCLAIMER DETAILS, item #2).

<details>
    <summary><b>IMPORTANT DISCLAIMER DETAILS (click me)</b></summary>

1) ###### Unauthorized Usage: <i>The use of the `easyoanda` module with &copy;OANDA's API without explicit permission may be in violation of &copy;OANDA's terms of service or acceptable use policies. Users are solely responsible for ensuring compliance with all legal and contractual obligations related to the use of the API.</i>

2) ###### Non-US Account Holders: <i>Non-US account holders are advised to refer to their own terms of service or acceptable use policies provided by &copy;OANDA or their respective financial institutions. Different regions may have different terms and conditions governing the use of &copy;OANDA's API and, by proxy, the `easyoanda` module. It is the responsibility of users outside the US to ensure compliance with applicable regulations.</i>

3) ###### Risk Disclosure: <i>Unauthorized use of &copy;OANDA's API may result in legal consequences, including but not limited to termination of access to the API, legal action, or financial penalties. Users should carefully consider the potential risks and consequences before using the `easyoanda` module with the API.</i>

4) ###### No Endorsement: <i>The creator of the `easyoanda` module does not endorse or condone unauthorized access to APIs or any other form of infringement of &copy;OANDA's rights. This module is provided for educational and informational purposes only, and users are encouraged to obtain proper authorization before using it in conjunction with &copy;OANDA's API.</i>

5) ###### Liability Limitation: <i>The creator of the `easyoanda` module shall not be held liable for any losses, damages, legal consequences, or other liabilities arising from the unauthorized use of &copy;OANDA's API or any other actions taken by users in connection with this module.</i>

6) ###### Software Functionality: <i>The `easyoanda` module may or may not work as intended due to factors including, but not limited to, changes in the &copy;OANDA API, errors in implementation, or system compatibility issues. The creator of the `easyoanda` module bears no responsibility for any malfunction or failure of the software.</i>

7) ###### Financial Responsibility: <i>The creator of the `easyoanda` module bears no responsibility for how users choose to trade their accounts or manage their financial instruments using this module. Users are solely responsible for their trading decisions, and any gains or losses incurred as a result of using the `easyoanda` module are the responsibility of the user.</i>

8) ###### No Association with &copy;OANDA: <i>The creator of the `easyoanda` module has no association with &copy;OANDA. This module is an independent creation and is not officially supported or endorsed by &copy;OANDA. Any reference to &copy;OANDA is for informational purposes only.</i>

8) ###### Legal Advice: <i>This disclaimer does not constitute legal advice. Users of the `easyoanda` module are strongly advised to seek legal counsel to determine their rights and obligations regarding the use of &copy;OANDA's API or any other third-party APIs.</i>

</details>

#### User Agreement:

>  By using the `easyoanda` Python module, you acknowledge that you have read, understood, and agreed to the terms and conditions outlined in this disclaimer, to include those listed under "IMPORTANT DISCLAIMER DETAILS". If you do not agree with these terms, you should refrain from using the `easyoanda` module.

<p>&nbsp;</p>

<!--- ===================================================================== ---> 

# Installation
#### <i>Windows:</i>
```cmd
> pip install easyoanda
```
#### <i>MacOS / Unix / Linux:</i>
```bash
$ pip3 install easyoanda
```

| Requirements | Versions   |
| ------------ | ---------- |
| Python       | >= 3.11    |
| requests     | >= 2.28.1  |
| pandas       | >= 1.5.3   |


<details>
    <summary><b><i>Meeting Requirements (click me)</i></b></summary>

1) ## <b>Updating Versions</b>

    - ### Download Python 3.11+ [here](https://www.python.org/downloads/)
        - ***Note:*** Ensure download is a stable release

    - ### Upgrade `requests` and `pandas` packages (will be installed if not present):

        #### <i>Windows:</i>
        ```cmd
        > pip install --upgrade requests pandas
        ```
        #### <i>MacOS / Unix / Linux:</i>
        ```bash
        $ pip3 install --upgrade requests pandas
        ```
2) ## <b>Reinstalling</b> `easyoanda`
    #### <i>Windows:</i>
    ```cmd
    > pip install easyoanda --ignore-installed --no-cache-dir
    ```
    #### <i>MacOS / Unix / Linux:</i>
    ```bash
    $ pip3 install easyoanda --ignore-installed --no-cache-dir
    ```

</details>

<p>&nbsp;</p>

<!--- ===================================================================== ---> 

# Basic Usage
> This section covers basic `easyoanda` use cases - for more advanced functionality,
please see the <b>Full Capabilities</b> section at the bottom of this page.

- ***Note:*** The `pretty()` function will be used to print `dictionary`
data structures within <b><i>"example (click me)"</i></b> portions of this guide. This is done purely for 
the reader's benefit and it not required in any capacity by the `easyoanda`
module. A "one-liner" is provided below for those of you who wish to 
follow along:

    ```python
    >>> import json; pretty = lambda x: print(json.dumps(x, default=str, indent=4))
    ```

    <details>
            <summary><b><i>example (click me)</i></b></summary>

    ```python 
    >>> # WITHOUT pretty()
    >>> myDict
    {'name': 'John Doe', 'timezone': 'America/New York', 'currentDate': datetime.datetime(2024, 5, 15, 13, 3, 40, 844525), 'about': {'age': 100, 'occupation': 'trader', 'speciality': 'forex'}}
    >>>
    >>> 
    >>> # pretty() "one-liner"
    >>> import json; pretty = lambda x: print(json.dumps(x, default=str, indent=4))
    >>>
    >>>
    >>> # WITH pretty()
    >>> pretty(myDict)
    {
        "name": "John Doe",
        "timezone": "America/New York",
        "currentDate": "2024-05-15 13:03:40.844525",
        "about": {
            "age": 100,
            "occupation": "trader",
            "speciality": "forex"
        }
    }
    >>>
    ```
    </details>

<p>&nbsp;</p>


1) ## **Start a session**
    > A session must be started with `easyoanda.start_session()` prior to accessing any of &copy;OANDA's endpoints: 

    ```python
    # import easyoanda
    from easyoanda import easyoanda
    
    # start a session
    session = easyoanda.start_session(sessionType="paper",
                                      accountID="123-123-12345678-123", 
                                      token="abcdefg1234567-abcdefg1234567")
    ```
    
    <details>
        <summary><b><i>example (click me)</i></b></summary>
    
    ```python
    >>> from easyoanda import easyoanda
    >>>
    >>> session = easyoanda.start_session(sessionType="paper", accountID="123-123-12345678-123", token="abcdefg1234567-abcdefg1234567")
    >>>
    ```

    </details>

    <p>&nbsp;</p>

    - `sessionType` may be "paper" or "live" depending on the account type you have with &copy;OANDA:
        - Open an &copy;OANDA  Account [here](https://www.oanda.com/us-en/trading/how-open-account/)
    - `accountID` can be found on your &copy;OANDA Hub Dashboard [here](https://hub.oanda.com)
        (account IDs are formatted as "XXX-XXX-XXXXXXXX-XXX").
        - ***Note:*** *Cryptocurrency accounts are not currently supported*
    - `token` must be generated for your account by &copy;OANDA - ensure it matches the `sessionType` specified:
        - Generate a PAPER (DEMO) Account Token [here](https://www.oanda.com/demo-account/tpa/personal_token)
        - Generate a LIVE Account Token [here](https://www.oanda.com/account/tpa/personal_token)

    <p>&nbsp;</p>

2) ## **Review account details**
    > Account details can be retrieved using the key session object `session.account`.
    A snapshot of your account is created as soon as the session begins, but 
    must be periodically updated throughout the trading day to keep your 
    account details up-to-date (in future releases, this will be automated):

    - ### **Full Snapshot:**
        ```python
        ''' always update your snapshots! '''

        # update snapshot
        session.account.update_fullDetails()

        # review your financial summary, pending orders, open positions, and open trades
        session.account.fullDetails
        ```
        <details>
            <summary><i><b>example (click me)</b></i></summary>

        ```python
        >>> session.account.update_fullDetails()
        >>> 
        >>> pretty(session.account.fullDetails)
        {
            "account": {
                "guaranteedStopLossOrderMode": "DISABLED",
                "hedgingEnabled": false,
                "id": "<REDACTED>",
                "createdTime": "2024-03-18 19:26:50.083009+00:00",
                "currency": "USD",
                "createdByUserID": "<REDACTED>",
                "alias": "Primary",
                "marginRate": 0.01,
                "lastTransactionID": 236,
                "balance": 102543.0386,
                "openTradeCount": 3,
                "openPositionCount": 1,
                "pendingOrderCount": 12,
                "pl": 2543.0386,
                "resettablePL": 2543.0386,
                "resettablePLTime": 0,
                "financing": -126.6018,
                "commission": 0.0,
                "dividendAdjustment": 0,
                "guaranteedExecutionFees": 0.0,
                "orders": [
                    {
                        "id": 188,
                        "createTime": "2024-04-23 23:38:23.027537+00:00",
                        "type": "TRAILING_STOP_LOSS",
                        "tradeID": 184,
                        "distance": 0.05,
                        "timeInForce": "GTC",
                        "triggerCondition": "DEFAULT",
                        "triggerMode": "TOP_OF_BOOK",
                        "state": "PENDING",
                        "trailingStopValue": 1.03888
                    },
                    
                    # ... truncated for brevity ...

                ],
                "positions": [
                    {
                        "instrument": "EUR_USD",
                        "long": {
                            "units": 10400,
                            "averagePrice": 1.07707,
                            "pl": 2479.4385,
                            "resettablePL": 2479.4385,
                            "financing": -126.9873,
                            "dividendAdjustment": 0.0,
                            "guaranteedExecutionFees": 0.0,
                            "tradeIDs": [
                                "184",
                                "195",
                                "227"
                            ],
                            "unrealizedPL": 121.6635
                        },
                        "short": {
                            "units": 0,
                            "pl": 63.6001,
                            "resettablePL": 63.6001,
                            "financing": 0.3855,
                            "dividendAdjustment": 0.0,
                            "guaranteedExecutionFees": 0.0,
                            "unrealizedPL": 0.0
                        },
                        "pl": 2543.0386,
                        "resettablePL": 2543.0386,
                        "financing": -126.6018,
                        "commission": 0.0,
                        "dividendAdjustment": 0.0,
                        "guaranteedExecutionFees": 0.0,
                        "unrealizedPL": 121.6635,
                        "marginUsed": 226.4787
                    }
                ],
                "trades": [
                    {
                        "id": 184,
                        "instrument": "EUR_USD",
                        "price": 1.07014,
                        "openTime": "2024-04-23 23:38:23.027537+00:00",
                        "initialUnits": 350,
                        "initialMarginRequired": 7.4904,
                        "state": "OPEN",
                        "currentUnits": 350,
                        "realizedPL": 0.0,
                        "financing": -0.3853,
                        "dividendAdjustment": 0.0,
                        "trailingStopLossOrderID": 188,
                        "unrealizedPL": 6.5205,
                        "marginUsed": 7.6219
                    },

                    # ... truncted for brevity...

                ],
                "unrealizedPL": 121.6635,
                "NAV": 102543.0386,
                "marginUsed": 226.4787,
                "marginAvailable": 102543.5444,
                "positionValue": 11323.936,
                "marginCloseoutUnrealizedPL": 122.408,
                "marginCloseoutNAV": 102543.7676,
                "marginCloseoutMarginUsed": 226.4787,
                "marginCloseoutPositionValue": 11323.936,
                "marginCloseoutPercent": 0.00116,
                "withdrawalLimit": 102543.5444,
                "marginCallMarginUsed": 226.4787,
                "marginCallPercent": 0.00232
            },
            "lastTransactionID": 236
        } 
        >>> 
        ```
        </details>
        <p>&nbsp;</p>

    - ### **Partial Snapshots:**
        ```python
        ''' always update your snapshots! '''

        # financial summary
        session.account.update_summary()
        session.account.summary

        # pending orders
        session.orders.update_pending()
        session.orders.pendingOrders

        # open positions
        session.positions.update_open()
        session.positions.openPositions

        # open trades
        session.trades.update_open()
        session.trades.openTrades
        ```
        <details>
            <summary><i><b>example (click me)</b></i></summary>

        ```python
        >>> session.account.update_summary()
        >>> pretty(session.account.summary)
        {
            "account": {
                "guaranteedStopLossOrderMode": "DISABLED",
                "hedgingEnabled": false,
                "id": "<REDACTED>",
                "createdTime": "2024-03-18 19:26:50.083009+00:00",
                "currency": "USD",
                "createdByUserID": <REDACTED>,
                "alias": "Primary",
                "marginRate": 0.01,
                "lastTransactionID": 236,
                "balance": 102543.3596,
                "openTradeCount": 3,
                "openPositionCount": 1,
                "pendingOrderCount": 12,
                "pl": 2543.0386,
                "resettablePL": 2543.0386,
                "resettablePLTime": 0,
                "financing": -126.6018,
                "commission": 0.0,
                "dividendAdjustment": 0,
                "guaranteedExecutionFees": 0.0,
                "unrealizedPL": 121.6635,
                "NAV": 102543.0231,
                "marginUsed": 226.4787,
                "marginAvailable": 102543.5444,
                "positionValue": 11323.936,
                "marginCloseoutUnrealizedPL": 122.408,
                "marginCloseoutNAV": 102543.7676,
                "marginCloseoutMarginUsed": 226.4787,
                "marginCloseoutPositionValue": 11323.936,
                "marginCloseoutPercent": 0.00116,
                "withdrawalLimit": 102543.5444,
                "marginCallMarginUsed": 226.4787,
                "marginCallPercent": 0.00232
            },
            "lastTransactionID": 236
        }
        >>>
        >>> session.orders.update_pending()
        >>> pretty(session.orders.pendingOrders)
        {
            "orders": [
                {
                    "id": 235,
                    "createTime": "2024-05-14 21:07:09.274182+00:00",
                    "type": "LIMIT",
                    "instrument": "EUR_USD",
                    "units": 10000,
                    "timeInForce": "GTC",
                    "price": 1.025,
                    "triggerCondition": "DEFAULT",
                    "partialFill": "DEFAULT_FILL",
                    "positionFill": "DEFAULT",
                    "state": "PENDING"
                },

                # ... truncated for brevity ...
            
            ],
            "lastTransactionID": 236
        }
        >>>
        >>> session.positions.update_open()
        >>> pretty(session.positions.openPositions)
        {
            "positions": [
                {
                    "instrument": "EUR_USD",
                    "long": {
                        "units": 10400,
                        "averagePrice": 1.07707,
                        "pl": 2479.4385,
                        "resettablePL": 2479.4385,
                        "financing": -126.9873,
                        "dividendAdjustment": 0.0,
                        "guaranteedExecutionFees": 0.0,
                        "tradeIDs": [
                            "184",
                            "195",
                            "227"
                        ],
                        "unrealizedPL": 121.6635
                    },
                    "short": {
                        "units": 0,
                        "pl": 63.6001,
                        "resettablePL": 63.6001,
                        "financing": 0.3855,
                        "dividendAdjustment": 0.0,
                        "guaranteedExecutionFees": 0.0,
                        "unrealizedPL": 0.0
                    },
                    "pl": 2543.0386,
                    "resettablePL": 2543.0386,
                    "financing": -126.6018,
                    "commission": 0.0,
                    "dividendAdjustment": 0.0,
                    "guaranteedExecutionFees": 0.0,
                    "unrealizedPL": 121.6635,
                    "marginUsed": 226.4787
                }
            ],
            "lastTransactionID": 236
        }
        >>>
        >>> session.trades.update_open()
        >>> pretty(session.trades.openTrades)
        {
            "trades": [
                {
                    "id": 227,
                    "instrument": "EUR_USD",
                    "price": 1.07735,
                    "openTime": "2024-05-13 01:30:59.541236+00:00",
                    "initialUnits": 10000,
                    "initialMarginRequired": 215.456,
                    "state": "OPEN",
                    "currentUnits": 10000,
                    "realizedPL": 0.0,
                    "financing": -2.1979,
                    "dividendAdjustment": 0.0,
                    "unrealizedPL": 114.2,
                    "marginUsed": 217.768,
                    "takeProfitOrder": {
                        "id": 228,
                        "createTime": "2024-05-13 01:30:59.541236+00:00",
                        "type": "TAKE_PROFIT",
                        "tradeID": 227,
                        "price": 1.12735,
                        "timeInForce": "GTC",
                        "triggerCondition": "DEFAULT",
                        "state": "PENDING"
                    },
                    "stopLossOrder": {
                        "id": 229,
                        "createTime": "2024-05-13 01:30:59.541236+00:00",
                        "type": "STOP_LOSS",
                        "tradeID": 227,
                        "price": 1.02,
                        "timeInForce": "GTC",
                        "triggerCondition": "DEFAULT",
                        "triggerMode": "TOP_OF_BOOK",
                        "state": "PENDING"
                    }
                },
                # ... truncated for brevity ...
            ],
            "lastTransactionID": 236
        }
        >>>
        ```
        </details>
        <p>&nbsp;</p>

    - ***Note:*** ALWAYS UPDATE YOUR SNAPSHOTS - if you've entered a trade or instrument
    prices have fluctuated within your portfolio, it will not be reflected 
    in your snapshot until an `update_*()` method is called 
    again (changes will always be properly reflected on &copy;OANDA's 
    servers, calling an `update_*()` function just ensures these changes are 
    reflected on your local machine, as well).

    <p>&nbsp;</p>


3) ## **Load historic data**
    >  &copy;OANDA provides granular access to historic instrument prices - 
    the key session object for accessing this data is `session.instruments`:
    - ### **Candles by Count:**
        ```python
        # retrieve candles
        session.instruments.update_candles(instrument="USD_JPY",    # USD/JPY
                                           price="M",               # the standard "mid" quote (avg. of bid-ask)
                                           granularity="H4",        # 4-hour candles
                                           count=20)                # last 20 candles available

        # review candles directly
        session.instruments.candles

        # or copy them out as a `pandas.DataFrame`
        USDJPY = session.instruments.copy_candles()
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> session.instruments.update_candles(instrument="USD_JPY", price="M", granularity="H4", count=20)
        >>>
        >>> pretty(session.instruments.candles)
        {
            "instrument": "USD_JPY",
            "granularity": "H4",
            "candles": [
                {
                    "complete": true,
                    "volume": 22005,
                    "time": "2024-05-14 13:00:00+00:00",
                    "mid": {
                        "o": 156.584,
                        "h": 156.658,
                        "l": 156.231,
                        "c": 156.486
                    }
                },

                # ... truncated for brevity ...
            
            ]
        }
        >>>
        >>> USDJPY = session.instruments.copy_candles()
        >>>
        >>> USDJPY
                                         o        h        l        c  volume
        datetime                                                             
        2024-05-14 13:00:00+00:00  156.584  156.658  156.231  156.486   22005
        2024-05-14 17:00:00+00:00  156.480  156.520  156.383  156.431    7036
        2024-05-14 21:00:00+00:00  156.425  156.562  156.386  156.392    7003
                            ...
        2024-05-17 17:00:00+00:00  155.626  155.724  155.585  155.642   11730
        >>>
        ```

        </details>
        <p>&nbsp;</p>

    - ### **Candles by Date Range:**
        ```python
        import datetime

        # two arbitrary dates: datetime.datetime(YYYY, MM, DD, <HH>, <MM>, <SS>)
        oneMonthAgo = datetime.datetime(2024, 4, 18)
        today = datetime.datetime.today()

        # retrieve the candles
        session.instruments.update_candles(instrument="EUR_USD",    # EUR/USD
                                           price="MBA",             # quotes for the mid (avg), bid, and ask
                                           granularity="D",         # daily candles
                                           fromTime=oneMonthAgo,    # from 1 month ago
                                           toTime=today)            # to today

        # review the candles directly
        session.instruments.candles

        # or copy them out as a `pandas.DataFrame`
        EURUSD = session.instruments.copy_candles()
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> import datetime
        >>>
        >>> oneMonthAgo = datetime.datetime(2024, 4, 18)
        >>>
        >>> today = datetime.datetime.today()
        >>>
        >>> session.instruments.update_candles(instrument="EUR_USD", price="MBA", granularity="D", fromTime=oneMonthAgo, toTime=today)
        >>>
        >>> pretty(session.instruments.candles)
        {
            "instrument": "EUR_USD",
            "granularity": "D",
            "candles": [
                {
                    "complete": true,
                    "volume": 67238,
                    "time": "2024-04-17 21:00:00+00:00",
                    "bid": {
                        "o": 1.06722,
                        "h": 1.06894,
                        "l": 1.06407,
                        "c": 1.06431
                    },
                    "mid": {
                        "o": 1.06729,
                        "h": 1.06901,
                        "l": 1.06415,
                        "c": 1.06439
                    },
                    "ask": {
                        "o": 1.06736,
                        "h": 1.06908,
                        "l": 1.06423,
                        "c": 1.06447
                    }
                },

                # ... truncated for brevity ...

            ]
        }
        >>>
        >>> EURUSD = session.instruments.copy_candles()
        >>>
        >>> EURUSD
                                        o        h        l        c    o_bid    h_bid    l_bid    c_bid    o_ask    h_ask    l_ask    c_ask  volume
        datetime                                                                                                                                     
        2024-04-17 21:00:00+00:00  1.06729  1.06901  1.06415  1.06439  1.06722  1.06894  1.06407  1.06431  1.06736  1.06908  1.06423  1.06447   67238
        2024-04-18 21:00:00+00:00  1.06451  1.06776  1.06104  1.06564  1.06427  1.06769  1.06097  1.06554  1.06475  1.06783  1.06112  1.06575   99058
        2024-04-21 21:00:00+00:00  1.06535  1.06708  1.06240  1.06538  1.06491  1.06701  1.06233  1.06531  1.06579  1.06716  1.06248  1.06545   55822
                                ...
        2024-05-16 21:00:00+00:00  1.08668  1.08786  1.08358  1.08697  1.08631  1.08779  1.08351  1.08687  1.08706  1.08793  1.08365  1.08707   42795
        >>>
        ```
        
        </details>
        <p>&nbsp;</p>

    - ***Note:*** `session.instruments.update_candles()` parameters are highly configurable -
    users are encouraged to explore the various options with `help(session.instruments.update_candles)`.

    <p>&nbsp;</p>


4) ## **Stream live quotes**
    >  Real-time quotes can be streamed using the key session 
    object `session.pricing`. Once the stream begins, `session.pricing.pricingStream`
    will be continuously updated with &copy;OANDA's most recent bid-ask spread - 
    if there's even the slightest change in an instrument's price, it will 
    automatically be reflected here.

    ```python
    # begin a price stream for EUR/USD
    session.pricing.start_stream("EUR_USD")

    # the current "EUR/USD" bid-ask spread
    session.pricing.pricingStream

    # a few moments later, a new "EUR/USD" bid-ask spread (automatically populated)
    session.pricing.pricingStream
    ```

    <details>
        <summary><i><b>example (click me)</b></i></summary>

    ```python
    >>> session.pricing.start_stream("EUR_USD")
    >>>
    >>> pretty(session.pricing.pricingStream)
    [
        {
            "type": "PRICE",
            "time": "2024-05-15 22:40:23.430277+00:00",
            "bids": [
                {
                    "price": 1.08889,
                    "liquidity": 10000000
                }
            ],
            "asks": [
                {
                    "price": 1.08904,
                    "liquidity": 10000000
                }
            ],
            "closeoutBid": 1.08889,
            "closeoutAsk": 1.08904,
            "status": "tradeable",
            "tradeable": true,
            "instrument": "EUR_USD"
        }
    ]
    >>>
    >>> pretty(session.pricing.pricingStream)
    [
        {
            "type": "PRICE",
            "time": "2024-05-15 22:40:28.528008+00:00",     # a few seconds later
            "bids": [
                {
                    "price": 1.08888,                       # bid has changed by .00001
                    "liquidity": 10000000
                }
            ],
            "asks": [
                {
                    "price": 1.08904,
                    "liquidity": 10000000
                }
            ],
            "closeoutBid": 1.08888,
            "closeoutAsk": 1.08904,
            "status": "tradeable",
            "tradeable": true,
            "instrument": "EUR_USD"
        }
    ]
    >>>
    ```

    </details>
    <p>&nbsp;</p>

    - ***Note 1:*** Don't forget to stop your stream with `session.pricing.stop_stream()` 
    before starting another stream. You may need to set 
    `session.streamMonitor.doNotResusitate = 0` beforehand to avoid the stream 
    from automatically being restarted (a built-in `easyoanda` failsafe for automation).
    - ***Note 2:*** If your program hangings on `quit()`, it's likely because
    there's a stream (or monitor thread) still running - ensure you run
    `session.quit()` to cleanly close out your session prior to exiting the
    session's parent program.

    <p>&nbsp;</p>

5) ## **Place an order**
    > Placing orders follows a general flow, regardless of order type: <b>(1)</b> 
    create an order using `easyoanda`, <b>(2)</b> configure the order using `*.set()`, 
    <b>(3)</b> place the order using key session object `session.orders`, and <b>(4)</b>
    <i>optionally</i> confirm order placement.
    - ### Base Orders
        > <b>Base Orders</b> enter trades, exit trades, and everything in 
        between. Please see `help()` on the following <b>Base Orders</b>:
        - `easyoanda.StopOrder()`
        - `easyoanda.LimitOrder()`
        - `easyoanda.MarketOrder()`
        - `easyoanda.MarketIfTouchedOrder()`
        ```python
        # (1) create the order
        marketOrder = easyoanda.MarketOrder()

        # (2) configure the order (long 10000 units of the instrument's base currency; a negative number would be short)
        marketOrder.set(instrument="EUR_USD", units=10000)

        # (3) place the order
        session.orders.place_order(marketOrder)

        # (4) (optional) confirm order placement
        session.orders.rcode                    # return code 888 is "order accepted"
        session.orderMonitor.logs[-1]           # verify order receipt
        ```
        <details>
            <summary><i><b>example (click me)</b></i></summary>

        ```python
        >>> marketOrder = easyoanda.MarketOrder()
        >>> 
        >>> marketOrder.set(instrument="EUR_USD", units=10000)
        >>> 
        >>> session.orders.place_order(marketOrder) 
        >>> 
        >>> session.orders.rcode
        888
        >>>
        >>> pretty(session.orderMonitor.logs[-1])
        {
            "entryID": 12,
            "datetime": "2024-05-15T23:07:35.962772Z",
            "originClass": "Orders",
            "confirmationDetails": {
                "orderCreateTransaction": {
                    "id": 256,
                    "accountID": "<REDACTED>",
                    "userID": <REDACTED>,
                    "batchID": 256,
                    "requestID": <REDACTED>,
                    "time": "2024-05-15 23:07:41.644279+00:00",
                    "type": "MARKET_ORDER",
                    "instrument": "EUR_USD",
                    "units": 10000,
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT",
                    "reason": "CLIENT_ORDER"
                },
                "orderFillTransaction": {
                    "id": 257,
                    "accountID": "<REDACTED>",
                    "userID": <REDACTED>,
                    "batchID": 256,
                    "requestID": <REDACTED>,
                    "time": "2024-05-15 23:07:41.644279+00:00",
                    "type": "ORDER_FILL",
                    "orderID": 256,
                    "instrument": "EUR_USD",
                    "units": 10000,
                    "requestedUnits": 10000,
                    "price": 1.08884,
                    "pl": 0.0,
                    "quotePL": 0,
                    "financing": 0.0,
                    "baseFinancing": 0,
                    "commission": 0.0,
                    "accountBalance": 102452.0191,
                    "gainQuoteHomeConversionFactor": 1,
                    "lossQuoteHomeConversionFactor": 1,
                    "guaranteedExecutionFee": 0.0,
                    "quoteGuaranteedExecutionFee": 0,
                    "halfSpreadCost": 0.7,
                    "fullVWAP": 1.08884,
                    "reason": "MARKET_ORDER",
                    "tradeOpened": {
                        "price": 1.08884,
                        "tradeID": 257,
                        "units": 10000,
                        "guaranteedExecutionFee": 0.0,
                        "quoteGuaranteedExecutionFee": 0,
                        "halfSpreadCost": 0.7,
                        "initialMarginRequired": 217.754
                    },
                    "fullPrice": {
                        "closeoutBid": 1.0887,
                        "closeoutAsk": 1.08884,
                        "timestamp": "2024-05-15 23:07:37.762451+00:00",
                        "bids": [
                            {
                                "price": 1.0887,
                                "liquidity": 10000000
                            }
                        ],
                        "asks": [
                            {
                                "price": 1.08884,
                                "liquidity": 10000000
                            }
                        ]
                    },
                    "homeConversionFactors": {
                        "gainQuoteHome": {
                            "factor": 1
                        },
                        "lossQuoteHome": {
                            "factor": 1
                        },
                        "gainBaseHome": {
                            "factor": 1.08332615
                        },
                        "lossBaseHome": {
                            "factor": 1.09421385
                        }
                    }
                },
                "relatedTransactionIDs": [
                    "256",
                    "257"
                ],
                "lastTransactionID": 257
            }
        }
        >>>
        ```
        </details>
        <p>&nbsp;</p>

    - ### Dependent Orders
        > <b>Dependent Orders</b> are attached to a <b>Base Order</b> that 
        has <i>already been filled</i> by &copy;OANDA (identifed by a `tradeID`) - 
        they're used to exit trades based on a trigger condition and only 
        close out the <b>Base Order</b> that they've been attached to. A <b>Base
        Order</b> may have multiple <b>Dependent Orders</b> attached - as soon as
        one is triggered, the rest are cancelled. Please see `help()` on the 
        following <b>Dependent Orders</b>:
        - `easyoanda.StopLossOrder()`
        - `easyoanda.TakeProfitOrder()`
        - `easyoanda.TrailingStopLossOrder()`
        - `easyoanda.GuaranteedStopLossOrder()`

        ```python
        # (1) create the order
        stopLossOrder = easyoanda.StopLossOrder()

        # (2) configure the order (close the trade if prices hit 1.045)
        stopLossOrder.set(tradeID=257, price=1.045)

        # (3) place the order
        session.orders.place_order(stopLossOrder)

        # (4) (optional) confirm order placement
        session.orders.rcode                    # return code 888 is "order accepted"
        session.orderMonitor.logs[-1]           # verify order receipt
        ```
        <details>
            <summary><i><b>example (click me)</b></i></summary>

        ```python
        >>> stopLossOrder = easyoanda.StopLossOrder()
        >>>
        >>> stopLossOrder.set(tradeID=257, price=1.045)
        >>>
        >>> session.orders.place_order(stopLossOrder)
        >>>
        >>> session.orders.rcode 
        888
        >>>
        >>> pretty(session.orderMonitor.logs[-1])
        {
            "entryID": 13,
            "datetime": "2024-05-15T23:13:59.267312Z",
            "originClass": "Orders",
            "confirmationDetails": {
                "orderCreateTransaction": {
                    "id": 259,
                    "accountID": "<REDACTED>",
                    "userID": <REDACTED>,
                    "batchID": 259,
                    "requestID": <REDACTED>,
                    "time": "2024-05-15 23:14:04.960575+00:00",
                    "type": "STOP_LOSS_ORDER",
                    "tradeID": 257,
                    "timeInForce": "GTC",
                    "triggerCondition": "DEFAULT",
                    "triggerMode": "TOP_OF_BOOK",
                    "price": 1.045,
                    "reason": "CLIENT_ORDER"
                },
                "relatedTransactionIDs": [
                    "259"
                ],
                "lastTransactionID": 259
            }
        }
        >>>
        ```

        </details>
        <p>&nbsp;</p>

        - ***Note:*** Potential `tradeID`(s) can be found in `session.trades.openTrades` 
        (don't forget to `update_openTrades()` first)
        
        <p>&nbsp;</p>

    - ### Complete Orders
        > <b>Complete Orders</b> are <b>Base Orders</b> with one or more 
        <b>Dependent Orders</b> attached to them <i>prior to being placed</i> 
        with &copy;OANDA. Any <b>Base Order</b> can call the following functions 
        to attach a corresponding <b>Dependent Order</b>:
        - `*.set_takeProfit()`
        - `*.set_stopLoss()`
        - `*.set_trailingStop()`
        - `*.set_guaranteedStop()`
        ```python
        # (1) create the order
        marketOrder = easyoanda.MarketOrder()

        # (2.a) configure the order
        marketOrder.set(instrument="EUR_USD", units=10000)

        # (2.b) configure the dependent orders
        marketOrder.set_stopLoss(price=1.0450)
        marketOrder.set_takeProfit(price=1.750)

        # (3) place the order
        session.orders.place_order(marketOrder)
        
        # (4) (optional) confirm order placement
        session.orders.rcode                    # return code 888 is "order accepted"
        session.orderMonitor.logs[-1]           # verify order receipt
        ```
        <details>
            <summary><i><b>example (click me)</b></i></summary>

        ```python
        >>> marketOrder = easyoanda.MarketOrder()
        >>>
        >>> marketOrder.set(instrument="EUR_USD", units=10000)
        >>>
        >>> marketOrder.set_stopLoss(price=1.0450)
        >>>
        >>> marketOrder.set_takeProfit(price=1.750)
        >>>
        >>> session.orders.place_order(marketOrder)
        >>>
        >>> session.orders.rcode
        888
        >>>
        >>> pretty(session.orderMonitor.logs[-1])
        {
            "entryID": 16,
            "datetime": "2024-05-15T23:29:26.566192Z",
            "originClass": "Orders",
            "confirmationDetails": {
                "orderCreateTransaction": {
                    "id": 265,
                    "accountID": "<REDACTED>",
                    "userID": <REDACTED>,
                    "batchID": 265,
                    "requestID": <REDACTED>,
                    "time": "2024-05-15 23:29:32.274985+00:00",
                    "type": "MARKET_ORDER",
                    "instrument": "EUR_USD",
                    "units": 10000,
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT",
                    "takeProfitOnFill": {
                        "price": 1.75,
                        "timeInForce": "GTC"
                    },
                    "stopLossOnFill": {
                        "price": 1.045,
                        "timeInForce": "GTC",
                        "triggerMode": "TOP_OF_BOOK"
                    },
                    "reason": "CLIENT_ORDER"
                },
                "orderFillTransaction": {
                    "id": 266,
                    "accountID": "<REDACTED>",
                    "userID": <REDACTED>,
                    "batchID": 265,
                    "requestID": <REDACTED>,
                    "time": "2024-05-15 23:29:32.274985+00:00",
                    "type": "ORDER_FILL",
                    "orderID": 265,
                    "instrument": "EUR_USD",
                    "units": 10000,
                    "requestedUnits": 10000,
                    "price": 1.08903,
                    "pl": 0.0,
                    "quotePL": 0,
                    "financing": 0.0,
                    "baseFinancing": 0,
                    "commission": 0.0,
                    "accountBalance": 102452.8191,
                    "gainQuoteHomeConversionFactor": 1,
                    "lossQuoteHomeConversionFactor": 1,
                    "guaranteedExecutionFee": 0.0,
                    "quoteGuaranteedExecutionFee": 0,
                    "halfSpreadCost": 0.8,
                    "fullVWAP": 1.08903,
                    "reason": "MARKET_ORDER",
                    "tradeOpened": {
                        "price": 1.08903,
                        "tradeID": 266,
                        "units": 10000,
                        "guaranteedExecutionFee": 0.0,
                        "quoteGuaranteedExecutionFee": 0,
                        "halfSpreadCost": 0.8,
                        "initialMarginRequired": 217.79
                    },
                    "fullPrice": {
                        "closeoutBid": 1.08887,
                        "closeoutAsk": 1.08903,
                        "timestamp": "2024-05-15 23:29:31.736132+00:00",
                        "bids": [
                            {
                                "price": 1.08887,
                                "liquidity": 10000000
                            }
                        ],
                        "asks": [
                            {
                                "price": 1.08903,
                                "liquidity": 10000000
                            }
                        ]
                    },
                    "homeConversionFactors": {
                        "gainQuoteHome": {
                            "factor": 1
                        },
                        "lossQuoteHome": {
                            "factor": 1
                        },
                        "gainBaseHome": {
                            "factor": 1.08350525
                        },
                        "lossBaseHome": {
                            "factor": 1.09439475
                        }
                    }
                },
                "relatedTransactionIDs": [
                    "265",
                    "266",
                    "267",
                    "268"
                ],
                "lastTransactionID": 268
            }
        }
        >>>
        ```

        </details>
        <p>&nbsp;</p>

    - ***Note 1:*** There are many ways to trade your account with `easyoanda` - 
    it is <i>highly recommended</i> that users explore all their
    available options with `help(session.orders)`, `help(session.trades)`, and 
    `help(session.positions)`.

    - ***Note 2:*** A word on &copy;OANDA verbiage: You place <b>orders</b>. All
    <b>orders</b> have a unique <b>order ID</b>. A <b>trade</b> is created when
    a <b>Base Order</b> is <i>filled</i>. Once a <b>trade</b> is created (<b>Base Order</b> 
    is filled), the <b>Base Order</b> and its associated <b>Dependent Orders</b> 
    (if present) will be classified under a <b>trade ID</b>. A <i>pending</i> 
    <b>Dependent Order</b> may be associated with a <b>trade ID</b> if its 
    <b>Base Order</b> has been filled. A <i>pending</i> <b>Base Order</b> will never 
    be associated with a <b>trade ID</b>. Finally, a <b>position</b> is the sum
    of all <i>open</i> <b>trades</b> that share a single instrument. You can interact with
    all <b>orders</b>, <b>trades</b>, and <b>positions</b> independently (see ***Note 1***).

    - ***Note 3:*** &copy;OANDA complies with &copy;National Futures Association 
    (NFA) [FIFO regulations](https://www.investopedia.com/terms/n/nfa-compliance-rule-2-43b.asp) - 
    it may be useful to understand how &copy;OANDA implements "FIFO" regulations 
    [here](https://help.oanda.com/us/en/faqs/fifo-requirement.htm). 
    Orders that violate "FIFO" regulations will deceptively return an 888 
    confirmation return code. ***You*** did everything correctly if you've
    receive an 888, so if you're not seeing an order on the books, a "FIFO" 
    violation may be involved: when in doubt, check `session.orderMonitor.logs` 
    (see <b>Section 9</b> below).



    <p>&nbsp;</p>

6) ## **Size an Order**
    > When placing orders, an order's size must <b>(1)</b> be units of the 
    target instruments's base currency to buy / sell and <b>(2)</b> be 
    placed as an integer. These constraints result in order sizes that are 
    rarely exact equivalents to a preferred order sized in your home currency. 
    Working within these constraints, `easyoanda` has simplified the roder 
    sizing process:
    - ### Converting to Base Currency Units
        > Converting an order size in an account's home currency to an order size
        in the target instrument's base currency is relatively simple:
        (1) gather the target instrument's conversion rates, then (2) provide
        `easyoanda.to_baseUnits()` the rates and your preferred order size. 
        Below is an example where a USD account trades CHF/JPY - our preferred 
        order size is 10000USD (the account's home currency), and our "best-fit" 
        order size (units of CHF to buy) is saved to the `orderSize` variable:
        - ***Note:*** The equivalent value of the "best-fit" order size in the base 
        currency will always be slightly less than the preferred order size in 
        the home currency - this is due to rounding base currency units down 
        to meet the previously mentioned integer requirements when placing orders.
        ```python
        # (1) gather the target instrument's conversion rates
        session.pricing.update_pricing("CHF_JPY")

        # (2) calculate the order size in base currency units
        orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, 
                                           homeUnits=10000,             # 10000USD
                                           truncate=True)               # rounds base units to integers

        # (optional) verify the equivalent "best-fit" order size in your home currency
        easyoanda.to_homeUnits(currentQuotes=session.pricing.pricing, 
                               baseUnits=orderSize)
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> session.pricing.update_pricing("CHF_JPY")
        >>>
        >>> orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, homeUnits=10000, truncate=True)
        >>>
        >>> orderSize
        9097
        >>> easyoanda.to_homeUnits(currentQuotes=session.pricing.pricing, baseUnits=orderSize)
        9999.340544602695
        >>>
        ```
        </details>

    - ### Measuring Price Changes
        > Conversion factors in FOREX markets make price volatility a little 
        less intuitive than in domestically priced instruments - traders
        should be aware of how a given currency pair's price fluctuations may 
        impact their trade:
        ```python
        # (1) calculate order size
        session.pricing.update_pricing("AUD_CAD")
        orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, 
                                           homeUnits=15000,
                                           truncate=True)
        
        
        # (2) calculate impact (in the account's home currency) of a single pip change
        easyoanda.get_pip_impact(currentQuotes=session.pricing.pricing,
                                 baseUnits=orderSize)

        # (3) calculate impact (in the account's home currency) of a change between two price levels
        easyoanda.get_price_impact(currentQuotes=session.pricing.pricing,
                                   baseUnits=orderSize,
                                   exitPrice = .8165,
                                   entryPrice = .9116)      # *Note* if entryPrice omitted, will use current market prices
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> session.pricing.update_pricing("AUD_CAD")
        >>>
        >>> orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, homeUnits=15000, truncate=True)
        >>>
        >>> orderSize
        22478
        >>>
        >>> easyoanda.get_pip_impact(currentQuotes=session.pricing.pricing, baseUnits=orderSize)
        1.6503004701099573
        >>>
        >>> easyoanda.get_price_impact(currentQuotes=session.pricing.pricing, baseUnits=orderSize, exitPrice = .8165, entryPrice = .9116)
        -1569.4357470745688
        >>> 
        ```
        </details>

        <p>&nbsp;</p>

7) ## Managing Risk
    > There are many ways to limit a trade's potential downside - below are two 
    methods to assist in your preservation of capital:
    - ### Selecting an optimal stop-loss:
        > If an order size has already been decided on and the trader has 
        a maximum allowable loss in mind, `easyoanda` can calculate the 
        optimal stop-loss price level for your trade: 
        ```python
        # (1) set preferences (enter with 10000 units of home currency, risk no more than 1% of account)
        preferredSize = 10000
        preferredMaxLoss = session.account.summary["account"]["balance"] * .01

        # (2) get conversion factors and calculate order size
        session.pricing.update_pricing("EUR_USD")
        orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, 
                                           homeUnits=preferredSize,
                                           truncate=True)

        # (3) find optimal stop-loss price level
        stopLossAt = easyoanda.find_optimal_stop(currentQuotes=session.pricing.pricing,
                                                 baseUnits=orderSize,
                                                 maxLoss=preferredMaxLoss)
                                                 # by omitting entryPrice, calculation uses current market prices

        # (4) (optional) view "best-fit" max loss in home currency units
        easyoanda.get_price_impact(currentQuotes=session.pricing.pricing,
                                   baseUnits=orderSize,
                                   exitPrice=stopLossAt)
                                   # by omitting entryPrice, calculation uses current market prices
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> preferredSize = 10000
        >>>
        >>> preferredMaxLoss = session.account.summary["account"]["balance"] * .01
        >>>
        >>> session.pricing.update_pricing("EUR_USD")
        >>>
        >>> orderSize = easyoanda.to_baseUnits(currentQuotes=session.pricing.pricing, homeUnits=preferredSize, truncate=True)
        >>>
        >>> stopLossAt = easyoanda.find_optimal_stop(currentQuotes=session.pricing.pricing, baseUnits=orderSize, maxLoss=preferredMaxLoss)
        >>>
        >>> orderSize
        9204
        >>>
        >>> preferredMaxLoss
        1000.000077
        >>>
        >>> stopLossAt
        0.97783
        >>> 
        >>> easyoanda.get_price_impact(currentQuotes=session.pricing.pricing, baseUnits=orderSize, exitPrice=stopLossAt)
        -999.9225600000007
        >>>
        ```
        </details>

    - ### Selecting an optimal trade size:
        > If a stop-loss price level has already been decided on and the 
        trader has a maximum allowable loss in mind, `easyoanda` can calculate
        the optimal order size in the target instrument's base currency for 
        your trade:
        ```python
        # (1) set preferences (stop out if prices drop to 1.05, risk no more than 1% of account)
        stopLoss = 1.05
        preferredMaxLoss = session.account.summary["account"]["balance"] * .01

        # (2) get conversion factors
        session.pricing.update_pricing("EUR_USD")

        # (3) find optimal order size in base currency units
        orderSize = easyoanda.find_optimal_size(currentQuotes=session.pricing.pricing,
                                                maxLoss=preferredMaxLoss,
                                                exitPrice=stopLoss)
                                                # omitting entryPrice, uses current market prices

        # (4) (optional) view "best-fit" max loss in home currency units
        easyoanda.get_price_impact(currentQuotes=session.pricing.pricing,
                                   baseUnits=orderSize,
                                   exitPrice=stopLoss)
                                   # by omitting entryPrice, calculation uses current market prices
        ```
        <details>
            <summary><b><i>example (click me)</i></b></summary>

        ```python
        >>> stopLoss = 1.05
        >>>
        >>> preferredMaxLoss = session.account.summary["account"]["balance"] * .01
        >>>
        >>> session.pricing.update_pricing("EUR_USD")
        >>>
        >>> orderSize = easyoanda.find_optimal_size(currentQuotes=session.pricing.pricing, maxLoss=preferredMaxLoss, exitPrice=stopLoss)
        >>>
        >>> stopLoss
        1.05
        >>>
        >>> preferredMaxLoss
        1000.000077
        >>>
        >>> orderSize
        27419.0
        >>> 
        >>> easyoanda.get_price_impact(currentQuotes=session.pricing.pricing, baseUnits=orderSize, exitPrice=stopLoss)
        -999.9709300000001
        >>>
        ```
        </details>

        <p>&nbsp;</p>

        - ***Note*** "Best-fit" max losses will always be slightly less than
        a trader's preferred max loss - this is due to either (1) rounding order
        sizes down to integers (see <b>Section 6</b>) or (2) rounding instrument 
        prices up / down to their nearest 5th decimal (another order placement
        requirement). These subtle changes typically have a negligible effect on a 
        trade's hypothetical value, and become even less relevant once market 
        volatility is taken into account - nonetheless, they are considerations 
        worth noting.

<p>&nbsp;</p>

8) ## **Review account transactions**
    > &copy;OANDA records nearly everything that happens in your account - 
    the key session object to access these records is `session.transactions`. 
    There are many options to filter by, but for the sake of trade history 
    analysis, "ORDER" will likely be your preferred single filter:

    ```python
    # update your snapshot (all order-related transactions since your account was opened)
    session.transactions.update_since(sinceID=1, transactionTypes=["ORDER"])

    # view the transactions
    session.transactions.sinceID
    ```
    <details>
        <summary><i><b>example (click me)</b></i></summary>

    ```python
    >>> session.transactions.update_since(sinceID=1, transactionTypes=["ORDER"])
    >>>
    >>> pretty(session.transactions.sinceID)
    {
        "transactions": [
            {
                "id": 4,
                "accountID": "<REDACTED>",
                "userID": <REDACTED>,
                "batchID": 4,
                "requestID": <REDACTED>,
                "time": "2024-03-18 19:34:01.021741+00:00",
                "type": "MARKET_ORDER",
                "instrument": "EUR_USD",
                "units": 100,
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
                "reason": "CLIENT_ORDER"
            },

            # ... truncated for brevity ...
        
        ],
        "lastTransactionID": 268
    }
    >>>
    ```
    </details>
    <p>&nbsp;</p>

    - ***Note 1:*** Please see `help(session.transactions.update_transactions)` for
    an exhaustive list of potential `transactionTypes`.

    - ***Note 2:*** Setting `sinceID=session.account._firstTransactionID` will
    filter transactions to the start of your session.

    <p>&nbsp;</p>

9) ## **View important logs**
    > Beyond &copy;OANDA's thorough transaction records (see <b>Section 8</b> above), 
    local logging is also built in for `easyoanda` users. Logs are always accessible
    within the program, but may also be configured to <b>(1)</b> print to `stdout`, 
    or <b>(2)</b> save to a file locally - these setting must be configured at 
    the beginning of a session. Please see `help(easyoanda.start_session)` 
    for more details.
    
    - ### Error Logs
        > <b>Error Logs</b> are managed by the key session object `session.errorMonitor` - 
        this object records malformed &copy;OANDA requests and (less common) 
        client-server network errors:
        ```python
        # error example: miss-type an instrument name (added too many 'D's)
        marketOrder = easyoanda.MarketOrder()
        marketOrder.set(instrument="EUR_USDDD", units=10000)
        session.orders.place_order(marketOrder)

        # view the error log
        session.errorMonitor.logs
        ```    

        <details>
            <summary><i><b>example (click me)</b></i></summary>
        
        ```python
        >>> marketOrder = easyoanda.MarketOrder()
        >>>
        >>> marketOrder.set(instrument="EUR_USDDD", units=10000)
        >>>
        >>> session.orders.place_order(marketOrder)
        >>>
        >>> pretty(session.errorMonitor.logs)
        [
            {
                "entryID": 0,
                "datetime": "2024-05-16T01:48:34.523512Z",
                "originClass": "Orders",
                "errorDetails": {
                    "url": "https://api-fxpractice.oanda.com/v3/accounts/<REDACTED>/orders",
                    "headers": {
                        "Authorization": "<REDACTED>",
                        "Content-Type": "application/json",
                        "AcceptDatetimeFormat": "RFC3339"
                    },
                    "parameters": null,
                    "payload": {
                        "order": {
                            "type": "MARKET",
                            "instrument": "EUR_USDDD",
                            "units": "10000",
                            "timeInForce": "FOK",
                            "positionFill": "DEFAULT"
                        }
                    },
                    "code": 400,
                    "message": {
                        "errorMessage": "Invalid value specified for 'order.instrument'",
                        "errorCode": "oanda::rest::core::InvalidParameterException"
                    }
                }
            }
        ]
        >>> 
        ```
        </details>

    <p>&nbsp;</p>

    - ### Order Logs
        > <b>Order Logs</b> are managed by the key session object `session.orderMonitor` -
        this object records successfully placed orders and their corresponding 
        confirmation receipts:
        ```python
        # order example: short 10000 units of EUR
        marketOrder = easyoanda.MarketOrder()
        marketOrder.set(instrument="EUR_USD", units=-10000)
        session.orders.place_order(marketOrder)

        # view the order log
        session.orderMonitor.logs
        ```

        <details>
            <summary><i><b>example (click me)</b></i></summary>
            
        ```python
        >>> marketOrder = easyoanda.MarketOrder()
        >>> 
        >>> marketOrder.set(instrument="EUR_USD", units=-10000)
        >>> 
        >>> session.orders.place_order(marketOrder)
        >>> 
        >>> pretty(session.orderMonitor.logs)
        [
            {
                "entryID": 0,
                "datetime": "2024-05-16T01:51:27.054254Z",
                "originClass": "Orders",
                "confirmationDetails": {
                    "orderCreateTransaction": {
                        "id": 273,
                        "accountID": "<REDACTED>",
                        "userID": <REDACTED>,
                        "batchID": 273,
                        "requestID": <REDACTED>,
                        "time": "2024-05-16 01:51:32.777478+00:00",
                        "type": "MARKET_ORDER",
                        "instrument": "EUR_USD",
                        "units": -10000,
                        "timeInForce": "FOK",
                        "positionFill": "DEFAULT",
                        "reason": "CLIENT_ORDER"
                    },
                    "orderFillTransaction": {
                        "id": 274,
                        "accountID": "<REDACTED>",
                        "userID": <REDACTED>,
                        "batchID": 273,
                        "requestID": <REDACTED>,
                        "time": "2024-05-16 01:51:32.777478+00:00",
                        "type": "ORDER_FILL",
                        "orderID": 273,
                        "instrument": "EUR_USD",
                        "units": -10000,
                        "requestedUnits": -10000,
                        "price": 1.08857,
                        "pl": 0.0,
                        "quotePL": 0,
                        "financing": 0.0,
                        "baseFinancing": 0,
                        "commission": 0.0,
                        "accountBalance": 102447.9191,
                        "gainQuoteHomeConversionFactor": 1,
                        "lossQuoteHomeConversionFactor": 1,
                        "guaranteedExecutionFee": 0.0,
                        "quoteGuaranteedExecutionFee": 0,
                        "halfSpreadCost": 0.7,
                        "fullVWAP": 1.08857,
                        "reason": "MARKET_ORDER",
                        "tradeOpened": {
                            "price": 1.08857,
                            "tradeID": 274,
                            "units": -10000,
                            "guaranteedExecutionFee": 0.0,
                            "quoteGuaranteedExecutionFee": 0,
                            "halfSpreadCost": 0.7,
                            "initialMarginRequired": 217.728
                        },
                        "fullPrice": {
                            "closeoutBid": 1.08857,
                            "closeoutAsk": 1.08871,
                            "timestamp": "2024-05-16 01:51:27.611898+00:00",
                            "bids": [
                                {
                                    "price": 1.08857,
                                    "liquidity": 10000000
                                }
                            ],
                            "asks": [
                                {
                                    "price": 1.08871,
                                    "liquidity": 10000000
                                }
                            ]
                        },
                        "homeConversionFactors": {
                            "gainQuoteHome": {
                                "factor": 1
                            },
                            "lossQuoteHome": {
                                "factor": 1
                            },
                            "gainBaseHome": {
                                "factor": 1.0831968
                            },
                            "lossBaseHome": {
                                "factor": 1.0940832
                            }
                        }
                    },
                    "relatedTransactionIDs": [
                        "273",
                        "274"
                    ],
                    "lastTransactionID": 274
                }
            }
        ]
        >>> 
        ```
        </details>
    
    <p>&nbsp;</p>
    
    - ***Note:*** Users are advised to print error logs and order logs
    to `stdout` when first developing their strategies, but to later set
    logging to <i>only</i> files once a strategy is complete. If a strategy
    is run continuously throughout the day (or longer), this allows for 
    perforance reviews and edge-case troubleshooting at the user's convenience. 
    Once again, please see `help(easyoanda.start_session)` for logging
    configuration details. 

    <p>&nbsp;</p>

<!--- ===================================================================== ---> 


# Examples
> ***Note:*** Full implementations examples to come!

<p>&nbsp;</p>

<!--- ===================================================================== ---> 



# Full Capabilities
> Click on any following capability to exand its details:
- ***ALERT:*** Capabilities tagged with `***` execute financial transactions.

### <i>Starting a Session:</i>
> Start an `easyoanda` session. (required for most capabilities)
<details>
    <summary><b>session = easyoanda.start_session()</b></summary>

```python
easyoanda.start_session(sessionType : str,
                        accountID : str,
                        token : str,
                        errorLog : str | None = None,
                        errorPrint : bool = False,
                        orderLog : str | None = None,
                        orderPrint : bool = False,
                        streamBeats : int = 10,
                        streamRetries : int = 3,
                        streamReset : int = 60
                        ) -> None
    
    '''
    
    Instantiates an OandaSession object with API access to Oanda trading 
    endpoints.
    

    Parameters
    ----------
    `sessionType` : str
        Determines which oanda servers to send all subsequent communication
        to:
            sessionType="paper" : Paper account
            sessionType="live" : Live account

    `accountID` : str
        Unique Account ID for the account to trade with (identify
        within Oanda portal).
    
    `token` : str
        Unique token generated for Oanda account. *Note* All "live" accounts
        share the same token, but "paper" accounts have their own unique
        token - make sure you're providing the correct one for the 
        `sessionType` started.
    
    `errorLog` : str | None = None
        (Optional) Full path to log file on disk for recording errors. If
        provided, will attempt to load any pre-existing logs to memory
        before error logging begins. [Default=None]
    
    `errorPrint` : bool = False
        Whether to print errors to stdout. [Default=False]
    
    `orderLog` : str | None = None
        (Optional) Full path to log file on disk for recording confirmations. 
        If provided, will attempt to load any pre-existing logs to memory
        before confirmation logging begins. [Default=None]
    
    `orderPrint` : bool = False
        Whether to print order confirmations to stdout. [Default=False]
    
    `streamBeats` : int = 10
        Number of seconds between heartbeats before a stream is considered dead. [Default=10]
    
    `streamRetries` : int = 3
        Number of times to attempt to restart a dead stream. [Default=3]
    
    `streamReset` : int = 60
        Number of minutes before resetting `streamRetries` counters back to zero for each endpoint. [Default=60]
    
    Returns
    -------
    `OandaSession`
        Custom class object with API access to Oanda trading endpoints.
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Stopping a Session:</i>
> Gracefully exit an `easyoanda` session.
<details>
    <summary><b>session.quit()</b></summary>

```python
session.quit() -> None

    '''

    Gracefully stops the given session's sub-threads (monitors and streams),
    allowing the parent program to cleanly exit. If your program hangs 
    on exit, having not run this is likely the cause - simply press
    <CTRL>+'C' to regain control of your terminal if this happens.


    Parameters
    ----------
    None

    Returns
    -------
    `None`

    '''
```
</details>

<p>&nbsp;</p>

### <i>Account Management:</i>
> View account details, track profit-and-loss changes, set new margin rates.
<details>
    <summary><b>session.account</b></summary>

``` python
session.account : object

    ''' 
    
    Your OANDA account interface. 
    
    '''
```
</details>

<details>
    <summary><b>session.account.fullDetails</b></summary>

```python
session.account.fullDetails : dict

    ''' 
    
    Full details on the given account. Full pending Order, open Trade and 
    open Position representations are provided.

    '''
```
</details>

<details>
    <summary><b>session.account.summary</b></summary>

```python
session.account.summary : dict

    ''' 
    
    Summary of the given account. 
    
    '''
```
</details>

<details>
    <summary><b>session.account.instruments</b></summary>

```python
session.account.instruments : dict

    ''' 
    
    List of tradeable instruments and their respective details for the 
    given Account. The list of tradeable instruments is dependent on 
    the regulatory division that the Account is located in, thus should be 
    the same for all Accounts owned by a single user.
    
    '''
```
</details>

<details>
    <summary><b>session.account.changes</b></summary>

```python
session.account.changes : dict
    
    '''

    Current state and changes in an account since a specified
    point in time (by TransactionID).

    '''
```
</details>

<details>
    <summary><b>session.account.update_fullDetails()</b></summary>

```python
session.account.update_fullDetails() -> None

    ''' 

    Updates `session.account.fullDetails` attribute.


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.account.update_summary()</b></summary>

```python
session.account.update_summary() -> None

    '''

    Updates `session.account.summary` attribute.


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.account.update_changes()</b></summary>

```python
session.account.update_changes(transactionID : int | str | None = None) -> None

    '''

    Updates `session.account.changes` attribute using provided argument filters.


    Parameters
    ----------------
    `transactionID` : int | str | None = None
        ID of the Transaction to get Account changes since - if
        `None`, will update from the beginning of the session.

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>*** session.account.set_margin()</b></summary>

```python
session.account.set_margin(marginRate : float | str) -> None

    '''

    Sets the margin rate for an account. *Note* Know your account's
    maximum allowable margin rate - typically .02 (50:1) - to avoid failed
    requests.


    Parameters
    ----------
    `marginRate` : float | str
        New margin rate to set for account (represented as a decimal).

    Returns
    -------
    `None`

    '''
```
</details>

<p>&nbsp;</p>

### <i>Instrument Data:</i>
> View historic instrument data, track an instrument's order book, view other trader's positions. 
<details>
    <summary><b>session.instruments</b></summary>

```python
session.instruments : object

    '''

    Your OANDA instrument interface.

    '''
```
</details>

<details>
    <summary><b>session.instruments.candles</b></summary>

```python
session.instruments.candles : None | dict = None

    '''

    Candle stick data for an instrument. `None` until populated by
    `session.instruments.update_candles()`.

    '''
```
</details>

<details>
    <summary><b>session.instruments.orderBook</b></summary>

```python
session.instruments.orderBook : None | dict = None

    '''

    Snapshot of an instrument's order book at a given point in time.
    `None` until populated by `session.instruments.update_orderBook()`.

    '''
```
</details>

<details>
    <summary><b>session.instruments.positionBook</b></summary>

```python

    '''

    Snapshot of an instrument's position book at a given point in time.
    `None` until populated by `session.instruments.update_positionBook()`.

    '''
```
</details>

<details>
    <summary><b>session.instruments.update_candles()</b></summary>

```python
session.instruments.update_candles(instrument : str,
                                   price : str = "M",
                                   granularity : str = "D",
                                   count : int | str | None = None,
                                   fromTime : datetime.datetime | str | None = None,
                                   toTime : datetime.datetime | str | None = None,
                                   smooth : bool = False,
                                   includeFirst : bool | None = None,
                                   dailyAlignment : int | str = 17,
                                   alignmentTimezone : str = "America/New_York",
                                   weeklyAlignment : str = "Friday"
                                   ) -> None

    '''

    Updates `session.instruments.candles` attribute using provided argument filters.


    Parameters
    ----------
    `instrument` : str
        Name of the Instrument to request candles for. *Note* if
        `Account()` object present, can check `account.instruments` for
        appropriate names.

    `price` : str = "M"
        The Price component(s) to get candlestick data for. [default=M]
            "M" : Midpoint candles
            "B" : Bid candles
            "A" : Ask candles
            "BA" : Bid and Ask candles
            "MBA" : Mid, Bid, and Ask candles
    
    `granularity` : str = "D"
        The granularity of the candlesticks to fetch [default=S5]
            "S5"	: 5 second candlesticks, minute alignment\n
            "S10"	: 10 second candlesticks, minute alignment\n
            "S15"	: 15 second candlesticks, minute alignment\n
            "S30"	: 30 second candlesticks, minute alignment\n
            "M1"	: 1 minute candlesticks, minute alignment\n
            "M2"	: 2 minute candlesticks, hour alignment\n
            "M4"	: 4 minute candlesticks, hour alignment\n
            "M5"	: 5 minute candlesticks, hour alignment\n
            "M10"	: 10 minute candlesticks, hour alignment\n
            "M15"	: 15 minute candlesticks, hour alignment\n
            "M30"	: 30 minute candlesticks, hour alignment\n
            "H1"	: 1 hour candlesticks, hour alignment\n
            "H2"	: 2 hour candlesticks, day alignment\n
            "H3"	: 3 hour candlesticks, day alignment\n
            "H4"	: 4 hour candlesticks, day alignment\n
            "H6"	: 6 hour candlesticks, day alignment\n
            "H8"	: 8 hour candlesticks, day alignment\n
            "H12"	: 12 hour candlesticks, day alignment\n
            "D" 	: 1 day candlesticks, day alignment\n
            "W"	    : 1 week candlesticks, aligned to start of week\n
            "M" 	: 1 month candlesticks, aligned to first day of the month\n

    `count` : int | str | None = None
        The number of candlesticks to return in the response. `count` 
        should not be specified if both the `fromTime` and `toTime` 
        parameters are provided, as the time range combined with the 
        granularity will determine the number of candlesticks to return.
        `count` may be specified if only one `(from or to)Time` is provided. 
        [Default=500 if `None`, or only one of `fromTime` or `toTime`
        is set]. (Max 5000)
    
    `fromTime` : datetime.datetime | str | None = None
        The start of the time range to fetch candlesticks for. 
        *Note* Strings must be RFC3339 format.
    
    `toTime` : datetime.datetime | str | None = None
        The end of the time range to fetch candlesticks for.
        *Note* Strings must be RFC3339 format.
    
    `smooth` : bool = False
        A flag that controls whether the candlestick is “smoothed” or 
        not. A smoothed candlestick uses the previous candles close 
        price as its open price, while an un-smoothed candlestick uses 
        the first price from its time range as its open price. 
        [default=False]
    
    `includeFirst` : bool | None = None
        A flag that controls whether the candlestick that is covered by 
        the from time should be included in the results. This flag 
        enables clients to use the timestamp of the last completed 
        candlestick received to poll for future candlesticks but avoid 
        receiving the previous candlestick repeatedly. [default=True, 
        if using 'fromTime' argument and left as `None`]
    
    `dailyAlignment` : int | str = 17
        The hour of the day (in the specified timezone) to use for 
        granularities that have daily alignments. [default=17, 
        minimum=0, maximum=23]
    
    `alignmentTimezone` : str = "America/New_York"
        The timezone to use for the dailyAlignment parameter. 
        Candlesticks with daily alignment will be aligned to the 
        dailyAlignment hour within the alignmentTimezone. Note that the 
        returned times will still be represented in UTC. 
        [default=America/New_York].
        List of "TZ Identifiers": https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    
    `weeklyAlignment` : str = "Friday"
        The day of the week used for granularities that have weekly 
        alignment. [default=Friday]
            "Monday"	: Monday\n
            "Tuesday"	: Tuesday\n
            "Wednesday"	: Wednesday\n
            "Thursday"	: Thursday\n
            "Friday"	: Friday\n
            "Saturday"	: Saturday\n
            "Sunday"	: Sunday\n
        
    Returns
    -------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.instruments.update_orderBook()</b></summary>

```python
session.instruments.update_orderBook(instrument : str, 
                                     time : datetime.datetime | str | None = None) -> None:

    '''

    Updates `session.instruments.orderBook` attribute using provided argument filters.

    
    Parameters
    ----------
    `instrument` : str
        Name of the instrument.

    `time` : datetime.datetime | str | None = None
        The time of the snapshot to fetch. This time is only customizable
        up to "hours" - all minutes and seconds should be zero-ed out.
        If not specified, then the most recent snapshot is fetched. 
        *Note* Ensure strings are RCF3339 formatted.

    Returns
    -------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.instruments.update_positionBook()</b></summary>

```python
session.instruments.update_positionBook(instrument : str, 
                                        time : datetime.datetime |  str | None = None) -> None

    '''

    Updates `session.instruments.positionBook` attribute using provided argument filters.
        

    Parameters
    ----------
    `instrument` : str
        Name of the instrument.

    `time` : datetime.datetime | str | None = None
        The time of the snapshot to fetch. This time is only customizable
        up to "hours" - all minutes and seconds should be zero-ed out.
        If not specified, then the most recent snapshot is fetched. 
        *Note* Ensure strings are RCF3339 formatted.

    Returns
    -------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.instruments.pretty_candles()</b></summary>

```python
session.instruments.pretty_candles(spread : bool = False) -> pandas.DataFrame

    '''
    
    Returns copy of candles in `session.instruments.candles` as a 
    `pandas.DataFrame`. No error checking is done prior to conversion - 
    ensure `session.instruments.candles` have  been successfully retrieved first 
    by confirming `session.instruments.rcode` == 200. *Note*: "o", "h", "l", and
    "c" will be appended with a suffix to indicate quote type:

        "<no suffix>"      : the average ("mid") of the bid-ask quotes (standard quote)
        "_bid"             : the bid
        "_ask"             : the ask
        "_spread"          : the bid-ask spread (if requested)


    Parameters
    ----------
    `spread` : bool = False
        If set to `True` and both the bid and ask were requested in your 
        `update_candles()` command, the spread will be appended to the
        returned DataFrame on your behalf. [default=False]

    Returns
    -------
    `pandas.DataFrame`
        Candles in `pandas.DataFrame` format.
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Order Management:</i>
> Create, place, replace, cancel, and track orders.
<details>
    <summary><b>session.orders</b></summary>

```python
session.orders : object

    '''

    Your OANDA order interface.

    '''
```
</details>

<details>
    <summary><b>session.orders.orders</b></summary>

```python
session.orders.orders :  None | dict = None

    '''

    Filtered orders of an account. `None` until populated by
    `session.orders.update_orders()`.

    '''
```
</details>

<details>
    <summary><b>session.orders.pendingOrders</b></summary>

```python
session.orders.pendingOrders : dict

    '''

    All pending orders in an account.

    '''
```
</details>

<details>
    <summary><b>session.orders.specificOrder</b></summary>

```python
session.orders.specificOrder : None | dict = None

    '''

    Details of a single order in a given account. `None` until
    populated by `session.orders.update_specific()`.

    '''
```
</details>

<details>
    <summary><b>session.orders.update_orders()</b></summary>

```python
session.orders.update_orders(instrument : str | None = None,
                             state : str = "PENDING",
                             ids : list[str | int] | None = None,
                             beforeID : str | int | None = None,
                             count : int = 50) -> None

    '''

    Updates `session.orders.orders` attribute by filtering the given account's 
    order book by specified parameters (max 500).


    Parameters
    ----------------
    `instrument` : str | None
        The instrument to filter the requested orders by
    
    `state` : None | str = "PENDING"
        The state to filter the requested Orders by [default=PENDING]

        "PENDING"\n
        "FILLED"\n
        "TRIGGERED"\n
        "CANCELLED"\n
        "ALL"
    
    `ids` : list[int, str] | None = None
        List of Order IDs to retrieve. Ensure `state="ALL"` if any of the
        orders are not "PENDING".

        Example:
        [51, 56, 60]

    `beforeID` : str | int | None = None
        The maximum Order ID to return. If not provided, the most recent 
        Order in the Account is used as the maximum Order ID to return.

    `count` : int = 50
        The maximum number of Orders to return [default=50, maximum=500].

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.orders.update_pending()</b></summary>

```python
session.orders.update_pending() -> None
        
    ''' 
    
    Updates `session.orders.pendingOrders` (no filtering required).


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.orders.update_specific()</b></summary>

```python
session.orders.update_specific(orderID : int | str) -> None

    ''' 
    
    Updates `session.orders.specificOrder` attribute by populating full details of
    a  single order via a given `orderID` ("orderSpecifier").


    Parameters
    ----------------
    `orderID` : int | str
        Specific order to collect details on. `orderID` may be index (int)
        or "Client ID" (string) (Example: 6372 or "@my_order_100")

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>*** session.orders.replace_order()</b></summary>

```python
session.orders.replace_order(orderID: int | str,
                             newOrder : dict | MarketOrder | LimitOrder | StopOrder
                             | MarketIfTouchedOrder | TakeProfitOrder | StopLossOrder |
                             GuaranteedStopLossOrder | TrailingStopLossOrder) -> None

    ''' 
    
    Replaces an order in an account by simultaneously cancelling it
    and creating a new order.


    Parameters
    ----------
    `orderID`: int | str
        Specific order to replace. `orderID` may be index (int)
        or "Client ID" (string) (Example: 6372 or "@my_order_100")
    
    `newOrder` : dict | MarketOrder | LimitOrder | StopOrder
                | MarketTouchOrder | TakeProfitOrder | StopLossOrder |
                    GuaranteedStopLossOrder | TrailingStopLossOrder
        
        A custom dictionary or prebuilt order object from one of the `prebuild` 
        module classes - help(prebuild.<class>.set_entry) -
        which contains all required order specifications to 
        pass to the endpoint. 
        
        If building the dictionary manually, specific Attributes / formatting 
        can be found on the Oanda API documentation page under 
        "PUT /v3/accounts/{accountID}/orders/{orderSpecifier}" 
        -> "Request Body Schema (application/json)":
            https://developer.oanda.com/rest-live-v20/order-ep/
        
        *Note* Within this program, some arguments are converted to their
        appropriate datatypes prior to sending requests to the server - if
        building your own `newOrder` requests, ensure the values you're
        using conform to the Oanda API documentation.

    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>*** session.orders.cancel_order()</b></summary>

```python
session.orders.cancel_order(orderID: int | str) -> None

    ''' 
    
    Cancels a pending order in an account.


    Parameters
    ----------
    `orderID`: int | str
        Specific order to cancel. `orderID` may be index (int)
        or "Client ID" (string) (Example: 6372 or "@my_order_100")

    Returns
    -------
    `None`

    '''
```
</details>

<details>
    <summary><b>*** session.orders.place_order()</b></summary>

```python
session.orders.place_order(newOrder : dict | MarketOrder | LimitOrder | StopOrder
                           | MarketIfTouchedOrder | TakeProfitOrder | StopLossOrder |
                           GuaranteedStopLossOrder | TrailingStopLossOrder) -> None

    '''
    
    Places an order for an account.


    Parameters
    ----------
    `newOrder` : dict | MarketOrder | LimitOrder | StopOrder
                | MarketTouchOrder | TakeProfitOrder | StopLossOrder |
                    GuaranteedStopLossOrder | TrailingStopLossOrder
        
        A custom dictionary or prebuilt order object : help(easyoanda.<order type>). 
        Contains all required order specifications to pass to the endpoint. 
        
        If building the dictionary manually, specific Attributes / formatting 
        can be found on the Oanda API documentation page under 
        "PUT /v3/accounts/{accountID}/orders/{orderSpecifier}" 
        -> "Request Body Schema (application/json)":
            https://developer.oanda.com/rest-live-v20/order-ep/
        
        *Note* Within this program, some arguments are converted to their
        appropriate datatypes prior to sending requests to the server - if
        building your own `newOrder` requests, ensure the values you're
        using conform to the Oanda API documentation.

    Returns
    -------
    `None`
    
    '''
```
</details>

- #### <i><u>Base Orders:</u></i>
    > Create traditional orders.
    <details>
        <summary><b>marketOrder = easyoanda.MarketOrder()</b></summary>

    ```python
    easyoanda.MarketOrder() : object

        '''

        A market order template.

        '''
    ```
    </details>

    <details>
        <summary><b>marketOrder.set()</b></summary>

    ```python
    marketOrder.set(instrument : str,
                    units : int,
                    priceBounds : float | None = None,
                    timeInForce : str = "FOK",
                    positionFill : str = "DEFAULT") -> None

        ''' 
        
        Sets required Market Order specifications. 
        

        Parameters
        ----------
        `instrument` : str
            The order's target instrument.

        `units` : int
            The quantity requested to be filled by the order. A positive
            number of units results in a long Order, and a negative number of units
            results in a short Order.

        `priceBound` : float | None = None
            (Optional) The worst price that the client is willing to have the Order
            filled at.

        `timeInForce` : str = "FOK"
            The time-in-force requested for the Order. TimeInForce describes
            how long an Order should remain pending before automaticaly being
            cancelled by the execution system. Must be "FOK" or "IOC" for
            Market Orders [Default=FOK]:

            "FOK"	: The Order must be immediately “Filled Or Killed”\n
            "IOC"	: The Order must be “Immediately partially filled Or Cancelled”

        `positionFill` : str = "DEFAULT"
            Specification of how Positions in the Account are modified when the Order
            is filled [Default=DEFAULT]:

            "OPEN_ONLY"	: When the Order is filled, only allow Positions to be 
                opened or extended.
            "REDUCE_FIRST"	: When the Order is filled, always fully reduce an 
                existing Position before opening a new Position.
            "REDUCE_ONLY"	: When the Order is filled, only reduce an existing 
                Position.
            "DEFAULT"	: When the Order is filled, use REDUCE_FIRST behaviour 
                for non-client hedging Accounts, and OPEN_ONLY behaviour for 
                client hedging Accounts.

        Returns
        -------
        `None`

        '''
    ```
    </details>

    <details>
        <summary><b>limitOrder = easyoanda.LimitOrder()</b></summary>

    ```python
    easyoanda.LimitOrder() : object

        '''

        A limit order template.

        '''
    ```
    </details>

    <details>
        <summary><b>limitOrder.set()</b></summary>

    ```python
    limitOrder.set(instrument : str,
                units : int,
                price : float,
                timeInForce : str = "GTC",
                gtdTime : datetime.datetime | str | None = None,
                positionFill : str = "DEFAULT",
                triggerCondition : str = "DEFAULT") -> None

        '''
        
        Sets required Limit Order specifications. *Note* A general note on LimitOrders:

        If POSITIVE units provided (Going Long / Closing Short)...
            AND Current Price < Order Price: 
                order will be filled immediately at CURRENT market prices (if not
                enough market liquidity and markets move UPWARD, will continue to be 
                filled only at prices LESS THAN or EQUAL TO the ORDER price)
            
            AND Current Price = Order Price: 
                order will be filled immediately at ORDER / CURRENT price or LESS 
                (if enough market liquidity)

            AND Current Price > Order Price: 
                order will sit at ORDER price until CURRENT price FALLS to ORDER price,
                at which point the order will be filled at ORDER price or LESS (if 
                enough market liquidity)
            
        If Negative Units Provided (Going Short / Closing Long) and...
            AND Current Price < Order Price: 
                order will sit at ORDER price until CURRENT price RISES to ORDER price,
                at which point the order will be filled at ORDER price or GREATER 
                (if enough market liquidity)

            AND Current Price = Order Price: 
                order will be filled immediately at ORDER / CURRENT price or GREATER
                (if enough market liquidity)
            
            AND Current Price > Order Price: 
                order will be filled immediately at CURRENT market prices (if not
                enough market liquidity and markets move DOWNWARD, will continue to
                be filled  only at prices GREATER THAN or EQUAL TO the ORDER price)
            

        Parameters
        ----------
        `instrument` : str
            The order's target instrument.

        `units` : int
            The quantity requested to be filled by the order. A positive
            number of units results in a long Order, and a negative number of units
            results in a short Order.

        `price` : float | None = None
            The price threshold specified for the Order. The Limit Order will 
            only be filled by a market price that is equal to or better than 
            this price.

        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce describes
            how long an Order should remain pending before automaticaly being
            cancelled by the execution system [Default=GTC]:

            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time
            "FOK"	: The Order must be immediately “Filled Or Killed”
            "IOC"	: The Order must be “Immediately partially filled Or Cancelled”

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce="GTD") The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.

        `positionFill` : str = "DEFAULT"
            Specification of how Positions in the Account are modified when the Order
            is filled [Default=DEFAULT]:

            "OPEN_ONLY"	: When the Order is filled, only allow Positions to be 
                opened or extended.
            "REDUCE_FIRST"	: When the Order is filled, always fully reduce an 
                existing Position before opening a new Position.
            "REDUCE_ONLY"	: When the Order is filled, only reduce an existing 
                Position.
            "DEFAULT"	: When the Order is filled, use REDUCE_FIRST behaviour 
                for non-client hedging Accounts, and OPEN_ONLY behaviour for 
                client hedging Accounts.

        `triggerCondition` : str = "DEFAULT"
            Specification of which price component should be evaluated when
            determining if an Order should be triggered and filled [Default=DEFAULT]. 

            "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                to the ask for long Orders and bid for short Orders.
            "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                compare its price the bid for long Orders and ask for short Orders.
            "BID"	: Trigger an Order by comparing its price to the bid 
                regardless of whether it is long or short.
            "ASK"	: Trigger an Order by comparing its price to the ask 
                regardless of whether it is long or short.
            "MID"	: Trigger an Order by comparing its price to the midpoint 
                regardless of whether it is long or short.

                
        Returns
        -------
        `None`

        '''
    ```
    </details>

    <details>
        <summary><b>stopOrder = easyoanda.StopOrder()</b></summary>

    ```python
    easyoanda.StopOrder() : object

        '''

        A stop order template.

        '''
    ```
    </details>

    <details>
        <summary><b>stopOrder.set()</b></summary>

    ```python
    stopOrder.set(instrument : str,
                units : int,
                price : float,
                priceBound : float | None = None,
                timeInForce : str = "GTC",
                gtdTime : datetime.datetime | str | None = None,
                positionFill : str = "DEFAULT",
                triggerCondition : str = "DEFAULT") -> None

        ''' 
        
        Sets required stop order specifications. *Note* A general note on StopOrders:

        If POSITIVE units provided (Going Long / Closing Short)...
            AND Current Price < Order Price: 
                order will sit at ORDER price until CURRENT price RISES to ORDER price,
                at which point the order will be filled at the ORDER price or
                GREATER (if enough market liquidity)

            AND Current Price = Order Price: 
                order will be filled immediately at ORDER / CURRENT price or GREATER
                (if enough market liquidity)
            
            AND Current Price > Order Price: 
                order will be filled immediately at CURRENT market prices (if not
                enough market liquidity and markets move DOWNWARD, will continue to
                be filled only at prices GREATER THAN or EQUAL TO the ORDER price).
            
        If Negative Units Provided (Going Short / Closing Long)...
            AND Current Price > Order Price:
                order will sit at ORDER price until CURRENT prices FALL to ORDER price,
                at which point the order will be filled at the ORDER price or LESS
                (if enough market liquidity)

            AND Current Price = Order Price: 
                order will be filled immediately at ORDER / CURRENT price or LESS
                (if enough market liquidity)
            
            AND Current Price < Order Price: 
                order will be filled immediately at CURRENT market prices (if not
                enough market liquidity and markets move UPWARD, will continue to
                be filled only at prices LESS THAN or EQUAL TO the ORDER price)


        Parameters
        ----------
        `instrument` : str
            The order's target instrument.

        `units` : int
            The quantity requested to be filled by the order. A positive
            number of units results in a long Order, and a negative number of units
            results in a short Order.

        `price` : float
            The price threshold specified for the Order. The Stop Order will 
            only be filled by a market price that is equal to or worse than this 
            price.

        `priceBound` : float | None = None
            (Optional) The worst price that the client is willing to have the Order
            filled at.

        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce describes
            how long an Order should remain pending before automaticaly being
            cancelled by the execution system [Default=GTC]:

            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time
            "FOK"	: The Order must be immediately “Filled Or Killed”
            "IOC"	: The Order must be “Immediately partially filled Or Cancelled”

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce="GTD") The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.

        `positionFill` : str = "DEFAULT"
            Specification of how Positions in the Account are modified when the Order
            is filled [Default=DEFAULT]:

            "OPEN_ONLY"	: When the Order is filled, only allow Positions to be 
                opened or extended.
            "REDUCE_FIRST"	: When the Order is filled, always fully reduce an 
                existing Position before opening a new Position.
            "REDUCE_ONLY"	: When the Order is filled, only reduce an existing 
                Position.
            "DEFAULT"	: When the Order is filled, use REDUCE_FIRST behaviour 
                for non-client hedging Accounts, and OPEN_ONLY behaviour for 
                client hedging Accounts.

        `triggerCondition` : str = "DEFAULT"
            Specification of which price component should be evaluated when
            determining if an Order should be triggered and filled [Default=DEFAULT]. 

            "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                to the ask for long Orders and bid for short Orders.
            "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                compare its price the bid for long Orders and ask for short Orders.
            "BID"	: Trigger an Order by comparing its price to the bid 
                regardless of whether it is long or short.
            "ASK"	: Trigger an Order by comparing its price to the ask 
                regardless of whether it is long or short.
            "MID"	: Trigger an Order by comparing its price to the midpoint 
                regardless of whether it is long or short.

                
        Returns
        -------
        `None`

        '''
    ```
    </details>

    <details>
        <summary><b>marketIfTouchedOrder = easyoanda.MarketIfTouchedOrder()</b></summary>

    ```python
    easyoanda.MarketIfTouchedOrder() : object

        '''

        A "market-if-touched" order template.

        '''
    ```
    </details>

    <details>
        <summary><b>marketIfTouchedOrder.set()</b></summary>

    ```python
    marketIfTouchedOrder.set(instrument : str,
                            units : int,
                            price : float,
                            priceBound : float | None = None,
                            timeInForce : str = "GTC",
                            gtdTime : datetime.datetime | str | None = None,
                            positionFill : str = "DEFAULT",
                            triggerCondition : str = "DEFAULT") -> None

        ''' 
        
        Sets required MarketIfTouched Order specifications. *Note* A general 
        note on MarketIfTouchedOrders:

        Think of a MarketIfTouchedOrder as taking ONE direction at a specific
        price point no matter where the market price comes from before hand.

        If POSITIVE units provided (Going Long / Closing Short)...
            AND Current Price < Order Price: 
                [Acts as Long Stop] order will sit at ORDER price until CURRENT price 
                RISES to ORDER price, at which point the order will be filled at the 
                ORDER price or GREATER (if enough market liquidity)

            AND Current Price = Order Price: 
                N/A
            
            AND Current Price > Order Price: 
                [Acts as Long Limit]  order will sit at ORDER price until CURRENT price 
                FALLS to ORDER price, at which point the order will be filled at 
                ORDER price or LESS (if enough market liquidity)
            
        If Negative Units Provided (Going Short / Closing Long)...
            AND Current Price > Order Price: 
                [Acts as Short Stop] order will sit at ORDER price until CURRENT price
                FALLS to ORDER price, at which point the order will be filled at the
                ORDER price or LESS (if enough market liquidity)

            AND Current Price = Order Price: 
                N/A

            AND Current Price < Order Price:
                [Acts as Short Limit] order will sit at ORDER price until CURRENT price 
                RISES to ORDER price, at which point the order will be filled at 
                ORDER price or GREATER (if enough market liquidity)
            

        Parameters
        ----------
        `instrument` : str
            The order's target instrument.

        `units` : int
            The quantity requested to be filled by the order. A positive
            number of units results in a long Order, and a negative number of units
            results in a short Order.

        `price` : float
            The price threshold specified for the Order. The MarketIfTouched 
            Order will only be filled by a market price that crosses this price 
            from the direction of the market price at the time when the Order 
            was created (the initialMarketPrice). Depending on the value of the 
            Orders price and initialMarketPrice, the MarketIfTouchedOrder will 
            behave like a Limit or a Stop Order.

        `priceBound` : float | None = None
            (Optional) The worst price that the client is willing to have the Order
            filled at.

        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce describes
            how long an Order should remain pending before automaticaly being
            cancelled by the execution system. Restricted to “GTC”, “GFD” and 
            “GTD” for MarketIfTouched Orders [Default=GTC]:

            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce="GTD") The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.

        `positionFill` : str = "DEFAULT"
            Specification of how Positions in the Account are modified when the Order
            is filled [Default=DEFAULT]:

            "OPEN_ONLY"	: When the Order is filled, only allow Positions to be 
                opened or extended.
            "REDUCE_FIRST"	: When the Order is filled, always fully reduce an 
                existing Position before opening a new Position.
            "REDUCE_ONLY"	: When the Order is filled, only reduce an existing 
                Position.
            "DEFAULT"	: When the Order is filled, use REDUCE_FIRST behaviour 
                for non-client hedging Accounts, and OPEN_ONLY behaviour for 
                client hedging Accounts.

        `triggerCondition` : str = "DEFAULT"
            Specification of which price component should be evaluated when
            determining if an Order should be triggered and filled [Default=DEFAULT]. 

            "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                to the ask for long Orders and bid for short Orders.
            "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                compare its price the bid for long Orders and ask for short Orders.
            "BID"	: Trigger an Order by comparing its price to the bid 
                regardless of whether it is long or short.
            "ASK"	: Trigger an Order by comparing its price to the ask 
                regardless of whether it is long or short.
            "MID"	: Trigger an Order by comparing its price to the midpoint 
                regardless of whether it is long or short.

                
        Returns
        -------
        `None`

        '''
    ```
    </details>

    <p></p>

    <details>
        <summary><b>ANY_BASE_ORDER.get_payload()</b></summary>

    ```python
    ANY_BASE_ORDER.get_payload() -> dict

        ''' 
        
        Returns a base order's configurations, formatted for placement with OANDA.


        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''
    ```
    </details>

- #### <i><u>Dependent Orders:</u></i> 
    > Create orders that can be attached to live trades.
    <details>
        <summary><b>takeProfitOrder = easyoanda.TakeProfitOrder()</b></summary>

    ```python
    easyoanda.TakeProfitOrder()

        '''

        A take-profit order template.

        '''
    ```
    </details>

    <details>
        <summary><b>takeProfitOrder.set()</b></summary>

    ```python
    takeProfitOrder.set(tradeID : int,
                        price : float | None = None,
                        distance : float | None = None,
                        timeInForce : str = "GTC",
                        gtdTime : datetime.datetime | str | None = None,
                        triggerCondition : str = "DEFAULT") -> None

        ''' 
        
        Sets required TakeProfit Order requirements.
        

        Parameters
        ----------
        `tradeID` : int
                The ID of the Trade to close when the price threshold is breached.

        `price` : float | None = None
            The associated Trade will be closed by a market price that is equal 
            to or better than this threshold (acts as Limit Order). Only 
            `price` OR `distance` may be specified - if both are input, 
            `price` will be given preference.

        `distance` : float | None = None
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            by a market price that is equal to or better than this threshold 
            (acts as Limit Order). If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it). Only 
            `price` OR `distance` may be specified - if both are input, `price` 
            will be given preference.

        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for TakeProfit Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.

        `triggerCondition` : str = "DEFAULT"
            Specification of which price component should be evaluated when
            determining if an Order should be triggered and filled [Default=DEFAULT]. 

            "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                to the ask for long Orders and bid for short Orders.
            "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                compare its price the bid for long Orders and ask for short Orders.
            "BID"	: Trigger an Order by comparing its price to the bid 
                regardless of whether it is long or short.
            "ASK"	: Trigger an Order by comparing its price to the ask 
                regardless of whether it is long or short.
            "MID"	: Trigger an Order by comparing its price to the midpoint 
                regardless of whether it is long or short.

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

    <details>
        <summary><b>stopLossOrder = easyoanda.StopLossOrder()</b></summary>

    ```python
    easyoanda.StopLossOrder()

        '''

        A stop-loss order template.

        '''
    ```
    </details>

    <details>
        <summary><b>stopLossOrder.set()</b></summary>

    ```python
    stopLossOrder.set(tradeID : int,
                    price : float | None = None,
                    distance : float | None = None,
                    timeInForce : str = "GTC",
                    gtdTime : datetime.datetime | str | None = None,
                    triggerCondition : str = "DEFAULT") -> None

            ''' 
            
            Sets required StopLoss Order requirements.
            

            Parameters
            ----------
            `tradeID` : int
                The ID of the Trade to close when the price threshold is breached.

            `price` : float | None = None
                The associated Trade will be closed by a market price that is equal 
                to or worse than this threshold (acts as Stop Order). Only 
                `price` OR `distance` may be specified - if both are input, 
                `price` will be given preference.

            `distance` : float | None = None
                Specifies the distance (in positive price units) from the trade's current 
                price to use as the Order price. The associated Trade will be closed
                by a market price that is equal to or better than this threshold 
                (acts as Limit Order). If the Trade is short the Instruments BID 
                price is used to calculated the price (and filled once ASK hits it), and 
                for long Trades the ASK is used (and filled once BID hits it). Only 
                `price` OR `distance` may be specified - if both are input, `price` 
                will be given preference.

            `timeInForce` : str = "GTC"
                The time-in-force requested for the Order. TimeInForce 
                describes how long an Order should remain pending before automaticaly 
                being cancelled by the execution system. Restricted to
                “GTC”, “GFD” and “GTD” for StopLoss Orders [Default=GTC]:
            
                "GTC"	: The Order is “Good unTil Cancelled”
                "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                    the provided time
                "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                    New York time

            `gtdTime` : datetime.datetime | str | None = None
                (Required if timeInForce=GTD) The date/time when the Order will be 
                cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
                RCF3339 formatted.

            `triggerCondition` : str = "DEFAULT"
                Specification of which price component should be evaluated when
                determining if an Order should be triggered and filled [Default=DEFAULT]. 

                "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                    to the ask for long Orders and bid for short Orders.
                "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                    compare its price the bid for long Orders and ask for short Orders.
                "BID"	: Trigger an Order by comparing its price to the bid 
                    regardless of whether it is long or short.
                "ASK"	: Trigger an Order by comparing its price to the ask 
                    regardless of whether it is long or short.
                "MID"	: Trigger an Order by comparing its price to the midpoint 
                    regardless of whether it is long or short.

            Returns
            -------
            `None`
            
            '''
    ```
    </details>

    <details>
        <summary><b>guaranteedStopLossOrder = easyoanda.GuaranteedStopLossOrder()</b></summary>

    ```python
    easyoanda.GuaranteedStopLossOrder()

        '''

        A guaranteed stop-loss order template.

        '''
    ```
    </details>

    <details>
        <summary><b>guaranteedStopLossOrder.set()</b></summary>

    ```python
    guaranteedStopLossOrder.set(tradeID : int,
                                price : float | None = None,
                                distance : float | None = None,
                                timeInForce : str = "GTC",
                                gtdTime : datetime.datetime | str | None = None,
                                triggerCondition : str = "DEFAULT") -> None

            ''' 
            
            Sets required GuaranteedStopLoss Order requirements.
            

            Parameters
            ----------
            `tradeID` : int
                The ID of the Trade to close when the price threshold is breached.

            `price` : float | None = None
                The associated Trade will be closed at this price. Only 
                `price` OR `distance` may be specified - if both are input, 
                `price` will be given preference.

            `distance` : float | None = None
                Specifies the distance (in positive price units) from the trade's current 
                price to use as the Order price. The associated Trade will be closed
                by a market price that is equal to or better than this threshold 
                (acts as Limit Order). If the Trade is short the Instruments BID 
                price is used to calculated the price (and filled once ASK hits it), and 
                for long Trades the ASK is used (and filled once BID hits it). Only 
                `price` OR `distance` may be specified - if both are input, `price` 
                will be given preference.

            `timeInForce` : str = "GTC"
                The time-in-force requested for the Order. TimeInForce 
                describes how long an Order should remain pending before automaticaly 
                being cancelled by the execution system. Restricted to
                “GTC”, “GFD” and “GTD” for GuaranteedStopLoss Orders [Default=GTC]:
            
                "GTC"	: The Order is “Good unTil Cancelled”
                "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                    the provided time
                "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                    New York time

            `gtdTime` : datetime.datetime | str | None = None
                (Required if timeInForce=GTD) The date/time when the Order will be 
                cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
                RCF3339 formatted.

            `triggerCondition` : str = "DEFAULT"
                Specification of which price component should be evaluated when
                determining if an Order should be triggered and filled [Default=DEFAULT]. 

                "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                    to the ask for long Orders and bid for short Orders.
                "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                    compare its price the bid for long Orders and ask for short Orders.
                "BID"	: Trigger an Order by comparing its price to the bid 
                    regardless of whether it is long or short.
                "ASK"	: Trigger an Order by comparing its price to the ask 
                    regardless of whether it is long or short.
                "MID"	: Trigger an Order by comparing its price to the midpoint 
                    regardless of whether it is long or short.

            Returns
            -------
            `None`
            
            '''
    ```
    </details>

    <details>
        <summary><b>trailingStopLossOrder = easyoanda.TrailingStopLossOrder()</b></summary>

    ```python
    easyoanda.TrailingStopLossOrder()

        '''

        A trailing stop-loss order template.

        '''
    ```
    </details>

    <details>
        <summary><b>trailingStopLossOrder.set()</b></summary>

    ```python
    trailingStopLossOrder.set(tradeID : int,
                            distance : float,
                            timeInForce : str = "GTC",
                            gtdTime : datetime.datetime | str | None = None,
                            triggerCondition : str = "DEFAULT") -> None

        '''
        
        Sets required TrailingStopLoss Order requirements.
        
        
        Parameters
        ----------
        `tradeID` : int
                The ID of the Trade to close when the price threshold is breached.
                
        `distance` : float
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            by a market price that is equal to or worse than this threshold 
            (acts as Stop Order). If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it).

        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for GuaranteedStopLoss Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.

        `triggerCondition` : str = "DEFAULT"
            Specification of which price component should be evaluated when
            determining if an Order should be triggered and filled [Default=DEFAULT]. 

            "DEFAULT"	: Trigger an Order the “natural” way: compare its price 
                to the ask for long Orders and bid for short Orders.
            "INVERSE"	: Trigger an Order the opposite of the “natural” way: 
                compare its price the bid for long Orders and ask for short Orders.
            "BID"	: Trigger an Order by comparing its price to the bid 
                regardless of whether it is long or short.
            "ASK"	: Trigger an Order by comparing its price to the ask 
                regardless of whether it is long or short.
            "MID"	: Trigger an Order by comparing its price to the midpoint 
                regardless of whether it is long or short.

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

    <p></p>

    <details>
        <summary><b>ANY_DEPENDENT_ORDER.get_payload()</b></summary>

    ```python
    ANY_DEPENDENT_ORDER.get_payload() -> None

        '''

        Returns a dependent order's configurations, formatted for placement with OANDA.


        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''
    ```
    </details>

- #### <i><u>Complete Orders:</u></i>
    > Attach "Dependent Orders" to "Base Orders" before they're even placed.
    <details>
        <summary><b>ANY_BASE_ORDER.set_takeProfit()</b></summary>

    ```python
    ANY_BASE_ORDER.set_takeProfit(price : float | None = None,
                                distance : float | None = None,
                                timeInForce : str = "GTC",
                                gtdTime : datetime.datetime | str | None = None) -> None
            
        ''' 
        
        Creates and sets a base order's TakeProfit dependent order.


        Parameters
        ----------
        `price` : float | None = None
            The associated Trade will be closed by a market price that is equal 
            to or better than this threshold (acts as Limit Order). Only 
            `price` OR `distance` may be specified - if both are input, 
            `price` will be given preference.

        `distance` : float | None = None
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            by a market price that is equal to or better than this threshold 
            (acts as Limit Order). If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it). Only 
            `price` OR `distance` may be specified - if both are input, `price` 
            will be given preference.
        
        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for TakeProfit Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.
        

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

    <details>
        <summary><b>ANY_BASE_ORDER.set_stopLoss()</b></summary>

    ```python
    ANY_BASE_ORDER.set_stopLoss(price : float | None = None,
                                distance : float | None = None,
                                timeInForce : str = "GTC",
                                gtdTime : datetime.datetime | str | None = None) -> None

        ''' 
        
        Creates and sets a base order's StopLoss dependent order.


        Parameters
        ----------
        `price` : float | None = None
            The associated Trade will be closed by a market price that is equal 
            to or worse than this threshold (acts as Stop Order). Only 
            `price` OR `distance` may be specified - if both are input, 
            `price` will be given preference.

        `distance` : float | None = None
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            by a market price that is equal to or worse than this threshold 
            (acts as Stop Order). If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it). Only 
            `price` OR `distance` may be specified - if both are input, `price` 
            will be given preference.
        
        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for StopLoss Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.
        

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

    <details>
        <summary><b>ANY_BASE_ORDER.set_trailingStop()</b></summary>

    ```python
    ANY_BASE_ORDER.set_trailingStop(distance : float,
                                    timeInForce : str = "GTC",
                                    gtdTime : datetime.datetime | str | None = None) -> None

        ''' 
        
        Creates and sets a base order's TrailingStopLoss dependent order.


        Parameters
        ----------
        `distance` : float | None = None
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            by a market price that is equal to or worse than this threshold 
            (acts as Stop Order). If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it).
        
        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for TrailingStopLoss Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.
        

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

    <details>
        <summary><b>ANY_BASE_ORDER.set_guaranteedStop()</b></summary>

    ```python
    ANY_BASE_ORDER.set_guaranteedStop(self,
                            price : float | None = None,
                            distance : float | None = None,
                            timeInForce : str = "GTC",
                            gtdTime : datetime.datetime | str | None = None) -> None

        ''' 
        
        Creates and sets a base order's GuarnateedStopLoss dependent order.


        Parameters
        ----------
        `price` : float | None = None
            The associated Trade will be closed at this price. Only 
            `price` OR `distance` may be specified - if both are input, 
            `price` will be given preference.

        `distance` : float | None = None
            Specifies the distance (in positive price units) from the trade's current 
            price to use as the Order price. The associated Trade will be closed
            at this price. If the Trade is short the Instruments BID 
            price is used to calculated the price (and filled once ASK hits it), and 
            for long Trades the ASK is used (and filled once BID hits it). Only 
            `price` OR `distance` may be specified - if both are input, `price` 
            will be given preference.
        
        `timeInForce` : str = "GTC"
            The time-in-force requested for the Order. TimeInForce 
            describes how long an Order should remain pending before automaticaly 
            being cancelled by the execution system. Restricted to
            “GTC”, “GFD” and “GTD” for GuarnateedStopLoss Orders [Default=GTC]:
        
            "GTC"	: The Order is “Good unTil Cancelled”
            "GTD"	: The Order is “Good unTil Date” and will be cancelled at 
                the provided time
            "GFD"	: The Order is “Good For Day” and will be cancelled at 5pm 
                New York time

        `gtdTime` : datetime.datetime | str | None = None
            (Required if timeInForce=GTD) The date/time when the Order will be 
            cancelled if its timeInForce is “GTD”. If string, ensure UTC in 
            RCF3339 formatted.
        

        Returns
        -------
        `None`
        
        '''
    ```
    </details>

- #### <i><u>Sizing a Position:</u></i>
    > Convert home currency units to target instrument's base currency units, 
    evaluate a trade's price sensitivity
    <details>
        <summary><b>easyoanda.to_baseUnits()</b></summary>

    ```python
    easyoanda.to_baseUnits(currentQuotes : dict,
                           homeUnits : float,
                           truncate : bool = False) -> float | int

        '''
        
        Convert units of the account's home currency to equivalent units of an 
        instrument's base currency.


        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().
        
        `homeUnits` : float
            Units of the account's home currency to convert.

        `truncate` : bool = False
            Whether to truncate the equivalent units of the base currency. Set this
            value to `True` when calculating units for an order - OANDA order units 
            are the number of the target instrument's base currency that you'd like 
            to buy or sell - these units must be INTEGERS! When `truncate=True`, if the 
            equivalent units of a base currency contain decimals, the units will be 
            "floored" to the nearest integer (decimals will be dropped) to comply 
            with OANDA order specifications. This will result in an equivalent order 
            size that is slightly smaller than that requested in `homeUnits`. 
            To verify the true value of the base currency units after truncating, use 
            `easyoanda.calc_home()`. [default=False]

        Returns
        -------
        float | int
            The equivalent units of the target instrument's base currency.
        
        '''
    ```
    </details>

    <details>
        <summary><b>easyoanda.to_homeUnits()</b></summary>

    ```python
    easyoanda.to_homeUnits(currentQuotes : dict,
                           baseUnits : float | int) -> float

        '''
        
        Convert units of an instrument's base currency to equivalent units of  
        the account's home currency.


        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().
        
        `baseUnits` : float
            Units of the instrument's base currency to convert.

        Returns
        -------
        float
            The equivalent units of the account's home currency.
        
        '''
    ```
    </details>
    
    <details>
        <summary><b>easyoanda.get_pip_impact()</b></summary>

    ```python
    easyoanda.get_pip_impact(currentQuotes : dict,
                             baseUnits : float) -> None

        '''
        
        Calculate the price impact of a single pip change (as measured in the 
        account's home currency), given a number of units of the target instrument's 
        base currency. *Note* A "pip" for instrumented quoted in "JPY" or "HUF" is 
        .01, whereas for all others, a "pip" is .0001.

        
        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().
        
        `baseUnits` : float
            Units of the instrument's base currency.

        Returns
        -------
        float
            The price impact a single pip change has (as measured in the 
            account's home currency)
        
        '''
    ```
    </details>

    <details>
        <summary><b>easyoanda.get_price_impact()</b></summary>

    ```python
    easyoanda.get_price_impact(currentQuotes : dict,
                               baseUnits : float,
                               entryPrice : float,
                               exitPrice : float) -> None

        '''
        
        Calculate the price impact of movements between two price levels within an 
        instrument (as measured in the account's home currency), given a number of 
        units of the target instrument's base currency.
        
        
        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().

        `baseUnits` : float
            Units of the instrument's base currency. Positive for long position,
            negative for short position.

        `entryPrice` : float | None = None
            The instrument's starting price level. If `None`, will assume entry
            price level is based on current bid/ask quotes (evaluated by sign of 
            `baseUnits`). [default=None]
        
        `exitPrice` : float
            The instrument's ending price level


        Returns
        -------
        float
            The price impact of changes between the two price levels (as measured
            in the account's home currency).

        '''
    ```
    </details>

- #### <i><u>Managing Risk:</u></i>
    > Calculate optimal stop loss levels and optimal trade sizes.
    <details>
        <summary><b>easyoanda.find_optimal_stop()</b></summary>

    ```python
    easyoanda.find_optimal_stop(currentQuotes : dict,
                                baseUnits : int,
                                maxLoss : float,
                                entryPrice : float | None = None) -> None

        '''
        
        Calculates the optimal stop-loss price level given an order's units
        (quoted in the target instrument's base currency) and trader's 
        maximum loss threshold (quoted in the account's home currency). *Note*
        OANDA requires stop-loss price levels be rounded to their 5th decimal place - 
        this is an industry standard. Due to this rounding, potential losses from
        the optimal stop-loss price level are slightly smaller than those 
        requested in `maxLoss`. To verify the true value of potential losses in 
        the account's home currency, use `easyoanda.get_price_impact()`.

        
        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().

        `baseUnits` : int
            The order size of the trade (quoted in the target instrument's base
            currency units). Positive units indicate a long position, negative 
            units indicate a short position. *Reminder* OANDA order units must be 
            INTEGERS.

        `maxLoss` : float
            The maximum allowable loss a trader is willing to take on the position
            (quoted in the account's home currency).
        
        `entryPrice` : float | None = None
            The trade's projected entry price. If `None`, will assume trade is 
            a market order and will use most recently quoted bid / ask provided
            within `currentQuotes` (depending on sign of `baseUnits`). [default=None]

        Returns
        -------
        float
            The target instrument's optimal stop-loss price level.

        '''
    ```
    </details>

    <details>
        <summary><b>easyoanda.find_optimal_size()</b></summary>

    ```python
    easyoanda.find_optimal_size(currentQuotes : dict,
                                maxLoss : float,
                                exitPrice : float,
                                entryPrice : float | None = None) -> None

        '''

        Calculate the optimal order size for a trade (in the target instrument's base 
        currency), given a target stop-loss price level and trader's maximum loss 
        threshold (quoted in the account's home currency). *Note* OANDA order units 
        are the number of the target instrument's base currency that you'd like 
        to buy or sell - these units must be INTEGERS! After the optimal units
        are calculated, if they contain decimals, the units will be 
        "floored" to the nearest integer (decimals will be dropped) to comply 
        with OANDA order specifications. This will result in an order size that is 
        slightly less than optimal - a "best-fit", if you will. This "best-fit" size 
        is the closest to the optimal size while still keeping potential losses below 
        the trader's maximum loss threshold. To verify the true value of the 
        optimal order size in the account's home currency, use `easyoanda.calc_home()`.


        Parameters
        ----------
        `currentQuotes` : dict
            The current `session.pricing.pricing` details of the target
            instrument. *Note* Pricing data must include home conversion factors 
            - this is the default in session.pricing.update_pricing().

        `exitPrice` : float
            The trade's target stop-loss price level.

        `maxLoss` : float | None = None
            The maximum allowable loss a trader is willing to take on the position
            (quoted in the account's home currency).
        
        `entryPrice` : float | None = None
            The order's projected entry price. If `None`, will assume the order is 
            a market order and will use the most recently quoted bid / ask provided
            within `currentQuotes`. The average of the bid-ask is used as a 
            benchmark to evaluate the `exitPrice` against to determine if the
            position is long or short - if your market order stops are 
            extremely close to the bid/ask (anything less than half the spread), 
            it may be worthwhile to enter this parameter manually. [default=None]

        
        Returns
        -------
        int
            The optimal order size for the trade in the target instrument's base
            currency.

        '''
    ```
    </details>

<p>&nbsp;</p>

### <i>Trade Management:</i>
> Close, modify, and track open trades.
<details>
    <summary><b>session.trades</b></summary>

```python
session.trades : object

    '''

    Your OANDA trades interface.

    '''
```
</details>

<details>
    <summary><b>session.trades.trades</b></summary>

```python
session.trades.trades : None | dict = None

    '''
    
    Filtered trades of a given account. `None` until populated by
    `session.trades.update_trades()`.
    
    '''
```
</details>

<details>
    <summary><b>session.trades.openTrades</b></summary>

```python
session.trades.openTrades : dict
    
    '''

    All open trades in an account.

    '''
```
</details>

<details>
    <summary><b>session.trades.specificTrade</b></summary>

```python
session.trades.specificTrade : None | dict = None

    '''

    Details of a single trade in a given account. `None` until
    populated by `session.trades.update_specific()`.

    '''
```
</details>

<details>
    <summary><b>session.trades.update_trades()</b></summary>

```python
session.trades.update_trades(instrument : str | None = None,
                             state : str = "OPEN",
                             ids : list[str, int] | None = None,
                             beforeID : str | int | None = None,
                             count : int = 50) -> None

    ''' 
    
    Updates `session.trades.trades` attribute using provided argument filters.


    Parameters
    ----------------
    `instrument` : None | str = None
        Instrument to filter trades by.
    
    `state` : None | str = "PENDING"
        The state to filter the requested Trades by. [default=OPEN]

        "OPEN"\n
        "CLOSED"\n
        "CLOSE_WHEN_TRADEABLE"\n
        "ALL"
    
    `ids` : None | list = None
        List of trade ids to filter by. Ensure `state="ALL"` if any of the
        trades are not "OPEN".

        [51, 56, 60]

    `beforeID` : None | str = None
        The maximum Trade ID to return. If not provided, the most recent 
        Trade in the Account is used as the maximum Trade ID to return.

    `count` : int = 50
        The maximum number of Trades to return. [default=50, maximum=500]

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.trades.update_open()</b></summary>

```python
session.trades.update_open() -> None

    '''
    
    Updates `session.trades.openTrades` (no filtering required).


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.trades.update_specific()</b></summary>

```python
session.trades.update_specific(tradeID : int | str) -> None

    '''
    
    Updates `session.trades.specificTrade` attribute by populating full details 
    of a single trade via a given trade id ("tradeSpecifier").


    Parameters
    ----------------
    `tradeID` : int | str
        Specific trade to collect details on. `tradeID` may be index (int)
        or "Client ID" (string) (Example: 6395 or "@my_eur_usd_trade")

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>*** session.trades.close_trade()</b></summary>

```python
session.trades.close_trade(tradeID : int | str, 
                           units : int | str = "ALL") -> None:

    ''' 
    
    Close (partially or fully) a specified open trade in an account.


    Parameters
    ----------
    `tradeID` : int | str
        Specific trade to close (partially or fully). `tradeID` may be index
        (int) or "Client ID" (string) (Example: 6395 or "@my_eur_usd_trade")


    `units` : int | str = "ALL"
        Indication of how much of the Trade to close. Either the string “ALL”
        (indicating that all of the Trade should be closed), or an integer
        representing the number of units of the open Trade to Close using a
        TradeClose MarketOrder. The units specified must always be positive, and
        the magnitude of the value cannot exceed the magnitude of the Trade's
        open units.
    
    Returns
    -------
    `None`

    
    '''
```
</details>

<details>
    <summary><b>*** session.trades.modify_trade()</b></summary>

```python
session.trades.modify_trade(tradeID : int | str,
                            preBuilt : dict | None = None,
                            cancelTP : bool = False,
                            modifyTP : bool = False,
                            tpPrice : float | None = None,
                            tpDistance : float | None = None,
                            tpTimeInForce : str | None = None,
                            tpGtdTime : datetime.datetime | str | None = None,
                            cancelSL : bool = False,
                            modifySL : bool = False,
                            slPrice : float | None = None,
                            slDistance : float | None = None,
                            slTimeInForce : str | None = None,
                            slGtdTime : datetime.datetime | str | None = None,
                            cancelTSL : bool = False,
                            modifyTSL : bool = False,
                            tslDistance : float | None = None,
                            tslTimeInForce : str | None = None,
                            tslGtdTime : datetime.datetime | str | None = None,
                            cancelGSL : bool = False,
                            modifyGSL : bool = False,
                            gslPrice : float | None = None,
                            gslDistance : float | None = None,
                            gslTimeInForce : str | None = None,
                            gslGtdTime : datetime.datetime | str | None= None) -> None
    ''' 
    
    Create, replace, or cancel a trade's dependent orders (Take Profit,
    Stop Loss, Trailing Stop Loss, and / or Guaranteed Stop Loss). 
    All dependent orders are set to their default fill types 
    (TakeProfit=LimitOrder, StopLoss=StopOrder, TrailingStopLoss=StopOrder, 
    GuaranteedStopLoss=N/A).
    
    *Note* Can change multiple of the listed  dependents at once.

                        *** NOTES ON TRIGGERING ***
    Dependent orders are evaluated off of their respective position types - 
    ie: if a position is short, stops / profits are evaluated off of the 
    current ASK price; if a position is long, stops / profits are evaluated 
    off of the current BID price.
    
    If `distance` is used to set any dependent order price thresholds, that 
    price is calculated off of the ENTRY PRICE TYPE - ie: if the position was 
    opened long, the exit price will be calculated from the current ASK price; 
    if the position was opened short, the price will be calculated from the 
    current BID price. This price will then be evaluated against the EXIT PRICE 
    TYPE - ie. BID to close long, or ASK to close short - to close a position.
    
    If more specific trigger requirements are needed, considered creating
    a completely new dependent order and cancelling / replacing the old
    one instead of modifying dependents directly with this implementation - 
    this implementation is an intuitive, quick way to modify dependent 
    orders without going through the trouble of creating an entire new 
    order, there are just limits to its trigger granularity.
    
    
    Parameters
    ----------
    `tradeID` : int | str
        Specific trade to modify. `tradeID` may be index (int | str) or 
        "Client ID" (string) (Example: 6395, "6293" or "@my_eur_usd_trade")
    
    `preBuilt` : dict | None = None
        (Optional) A prebuilt dictionary of all required trade arguments to
        pass to the endpoint. Attributes / formatting can be found on the Oanda
        API documentation page under "PUT /v3/accounts/{accountID}/trades/{tradeSpecifier}/orders"
        -> "Request Body Schema (application/json)":
            https://developer.oanda.com/rest-live-v20/trade-ep/
        
        *Note* Within this program, some arguments are converted to their
        appropriate datatypes prior to sending requests to the server - if
        building your own `preBuilt` requests, ensure the values you're
        using conform to the Oanda API documentation.

    ***** TAKE PROFIT *****\n
    The specification of the Take Profit to create/modify/cancel. If
    both `cancelTP` and `modifyTP` are set to False (by default they are),
    no modifications to the existing Take Profit order will happen. If 
    `cancelTP` = True, the dependent order is cancelled. If `modifyTP` = True,
    the new parameters (`tpPrice` or `tpDistance`, `tpTimeInForce`, and 
    (potentially) `tpGtdTime`) will be 
    applied to the trade (this will create a new dependent order if no other
    Take Profits exists within the trade, otherwise only the specified parameters 
    will be replaced) - `modifyTP` MUST be set to True to have these new
    parameters applied. *Note* `cancelTP` supercedes `modifyTP` if both flags
    are set.

    `cancelTP` : bool = False
        Flag that cancels the associated Take Profit dependent order.
    
    `modifyTP` : bool = False
        Flag that allows modifications to the Take Profit dependent order.  
    
    `tpPrice` : float | None = None
        The price that the Take Profit Order will be triggered at. Only one of
        the `tpPrice` and `tpDistance`  fields may be specified. (if both are set,
        `tpPrice` is given preference).

    `tpDistance` : float | None = None
        Specifies the distance (in positive price units) from the Trade's
        open price to use as the Take Profit price. If position is short,
        positive values translate to their short equivalents. Only one of the
        distance and price fields may be specified. *Note* This option isn't
        explicitly listed on the Oanda TakeProfitDetails API docs, but is 
        supported in testing.
        
    `tpTimeInForce` : str | None = None
        The time in force for the created Take Profit Order. This may
        only be "GTC", "GTD" or "GFD". If omitted, will inherit whatever the existing
        time-in-force configurations are if a corresponding dependent order already 
        exists - if omitted with NO pre-existing dependent order already attached,
        will set the new dependent order to "GTC".
    
    `tpGtdTime` : datetime.datetime | str | None = None
        The date when the Take Profit Order will be cancelled on if timeInForce
        is GTD.
    
        
    ***** STOP LOSS *****\n
    The specification of the Stop Loss to create/modify/cancel. If
    both `cancelSL` and `modifySL` are set to False (by default they are),
    no modifications to the existing Stop Loss order will happen. If 
    `cancelSL` = True, the dependent order is cancelled. If `modifySL` = True,
    the new parameters (`slPrice` or `slDistance`, `slTimeInForce`, and 
    (potentially) `slGtdTime`) will be 
    applied to the trade (this will create a new dependent order if no other
    Stop Losses exists within the trade, otherwise only the specified parameters 
    will be replaced) - `modifySL` MUST be set to True to have these new
    parameters applied. *Note* `cancelSL` supercedes `modifySL` if both flags
    are set.

    `cancelSL` : bool = False
        Flag that cancels the associated Stop Loss dependent order.
    
    `modifySL` : bool = False
        Flag that allows modifications to the Stop Loss dependent order. 
    
    `slPrice` : float | None = None
        The price that the Stop Loss Order will be triggered at. Only one of the
        `slPrice` and `slDistance`  fields may be specified. (if both are set,
        `slPrice` is given preference).
    
    `slDistance` : float | None = None
        Specifies the distance (in positive price units) from the Trade's open 
        price to use as the Stop Loss Order price.  If position is short,
        positive values translate to their short equivalents.
        Only one of the distance and price fields may be specified.
    
    `slTimeInForce` : str | None = None
        The time in force for the created Stop Loss Order. This may
        only be "GTC", "GTD" or "GFD". If omitted, will inherit whatever the existing
        time-in-force configurations are if a corresponding dependent order already 
        exists - if omitted with NO pre-existing dependent order already attached,
        will set the new dependent order to "GTC".
    
    `slGtdTime` : datetime.datetime | str | None = None
        The date when the Stop Loss Order will be cancelled on if timeInForce 
        is GTD.
    
        
    ***** TRAILING STOP LOSS *****\n
    The specification of the Trailing Stop Loss to create/modify/cancel. If
    both `cancelTSL` and `modifyTSL` are set to False (by default they are),
    no modifications to the existing Trailing Stop Loss order will happen. If 
    `cancelTSL` = True, the dependent order is cancelled. If `modifyTSL` = True,
    the new parameters (`tslDistance`, `tslTimeInForce`, and (potentially) `tslGtdTime`)
    will be 
    applied to the trade (this will create a new dependent order if no other
    Trailing Stop Losses exists within the trade, otherwise only the specified 
    parameters will be replaced) - `modifyTSL` MUST be set to True to have these new
    parameters applied. *Note* `cancelTSL` supercedes `modifyTSL` if both flags
    are set.

    `cancelTSL` : bool = False
        Flag that cancels the associated Trailing Stop Loss dependent order.
    
    `modifyTSL` : bool = False
        Flag that allows modifications to the Trailing Stop Loss dependent order. 
    
    `tslDistance` : float | None = None
        The distance (in positive price units) from the Trades fill price that the
        Trailing Stop Loss Order will be triggered at.  If position is short,
        positive values translate to their short equivalents.
    
    `tslTimeInForce` : str | None = None
        The time in force for the created Trailing Stop Loss Order. This may
        only be "GTC", "GTD" or "GFD". If omitted, will inherit whatever the existing
        time-in-force configurations are if a corresponding dependent order already 
        exists - if omitted with NO pre-existing dependent order already attached,
        will set the new dependent order to "GTC".
    
    `tslGtdTime` : datetime.datetime | str | None = None
        The date when the Trailing Stop Loss Order will be cancelled on if
        timeInForce is GTD.
    
        
    ***** GUARANTEED STOP LOSS *****\n
    The specification of the Guaranteed Stop Loss to create/modify/cancel. If
    both `cancelGSL` and `modifyGSL` are set to False (by default they are),
    no modifications to the existing Guaranteed Stop Loss order will happen. If 
    `cancelGSL` = True, the dependent order is cancelled. If `modifyGSL` = True,
    the new parameters (`gslPrice` or `gslDistance`, `gslTimeInForce`, and 
    (potentially) `gslGtdTime`) will be 
    applied to the trade (this will create a new dependent order if no other
    Guaranteed Stop Losses exists within the trade, otherwise only the specified 
    parameters will be replaced) - `modifyGSL` MUST be set to True to have these new
    parameters applied. *Note* `cancelGSL` supercedes `modifyGSL` if both flags
    are set.

    `cancelGSL` : bool = False
        Flag that cancels the associated Guaranteed Stop Loss dependent order.
    
    `modifyGSL` : bool = False
        Flag that allows modifications to the Guaranteed Stop Loss dependent order. 

    `gslPrice` : float | None = None
        The price that the Guaranteed Stop Loss Order will be triggered at. Only
        one of the `gslPrice` and `gslDistance` fields may be specified. (if both 
        are set, `gslPrice` is given preference).

    `gslDistance` : float | None = None
        Specifies the distance (in positive price units) from the Trades open price to
        use as the Guaranteed Stop Loss Order price. Only one of the `gslPrice` 
        and `gslDistance`  fields may be specified.  If position is short, positive 
        values translate to their short equivalents.
    
    `gslTimeInForce` : str | None = None
        The time in force for the created Guaranteed Stop Loss Order. This may
        only be "GTC", "GTD" or "GFD". If omitted, will inherit whatever the existing
        time-in-force configurations are if a corresponding dependent order already 
        exists - if omitted with NO pre-existing dependent order already attached,
        will set the new dependent order to "GTC".

    `gslGtdTime` : datetime.datetime | str | None = None
        The date when the Guaranteed Stop Loss Order will be cancelled on if
        timeInForce is "GTD".
    
    
    Returns
    -------
    `None`
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Position Management:</i>
> Close entire positions, view current position details, view historic position details.
<details>
    <summary><b>session.positions</b></summary>

```python
sessions.positions : object

    '''

    Your OANDA positions interface.

    '''

```
</details>

<details>
    <summary><b>session.positions.positions</b></summary>

```python
session.positions.positions : dict

    '''
    
    All positions for an account. Positions listed are for every 
    instrument that has had a position during the lifetime of the account.

    '''
```
</details>

<details>
    <summary><b>session.positions.openPositions</b></summary>

```python
session.positions.openPositions : dict

    '''

    All open positions for an account. An open position is a position in an
    account that currently has a trade opened for it. *Note* If a trade has
    a state of "CLOSE_WHEN_TRADEABLE", it MAY NOT be included here
    (testing to come).

    '''
```
</details>

<details>
    <summary><b>session.positions.specificPosition</b></summary>

```python
session.positions.specificPosition : None | dict = None
    '''

    Details of a single instrument's position in the account. The position
    may or may not be open. `None` until populated by 
    `session.positions.update_specific()`.

    '''
```
</details>

<details>
    <summary><b>session.positions.update_positions()</b></summary>

```python
session.positions.update_positions() -> None

    ''' 
    
    Updates `session.positions.positions` attribute (no arguments required).


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.positions.update_open()</b></summary>

```python
session.positions.update_open() -> None

    ''' 
    
    Updates `session.positions.openPositions` attribute (no arguments required).


    Parameters
    ----------------
    None

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.positions.update_specific()</b></summary>

```python
session.positions.update_specific(instrument : str) -> None

    '''
    
    Updates `session.positions.specificPosition` attribute by populating full 
    details of a single position (open or closed) via a given instrument.


    Parameters
    ----------------
    `instrument` : str
        Instrument name to get position details on.

    Returns
    -----------
    `None`

    '''
```
</details>

<details>
    <summary><b>*** session.positions.close_position()</b></summary>

```python
session.positions.close_position(instrument : str,
                                 longUnits : str | int = "NONE",
                                 shortUnits : str | int = "NONE") -> None
                                 
    ''' 
    
    Fully or partially closes out an open position for a specific 
    instrument in an account using a non-optional "market order" (this is a
    server-side configuration).


    Parameters
    ----------
    `instrument` : str
        Name of the instrument to close out.
    
    `longUnits` : str | int = "NONE"
        Indication of how much of the long Position to closeout. Either the
        string “ALL”, the string “NONE”, or an integer representing how many
        units of the long position to close using a PositionCloseout MarketOrder.
        The units specified must always be positive. If hedging is permitted 
        on the account, you may send `shortUnits` argument as well
        ("ALL" or integer) - otherwise `shortUnits` must remain "NONE" if passing
        "ALL" or integer `longUnits` parameter.

    `shortUnits` : str | int = "NONE"
        Indication of how much of the short Position to closeout. Either the
        string “ALL”, the string “NONE”, or a integer representing how many
        units of the short position to close using a PositionCloseout
        MarketOrder. The units specified must always be positive. If hedging 
        is permitted on the account, you may send `longUnits` argument as well
        ("ALL" or integer) - otherwise `longUnits` must remain "NONE" if passing
        "ALL" or integer `shortUnits` parameter.
    
    Returns
    -------
    `None`
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Transaction Records:</i>
> Review &copy;OANDA transactional records.
<details>
    <summary><b>session.transactions</b></summary>

```python
session.transactions : object

    '''

    Your OANDA transactions interface.

    '''
```
</details>

<details>
    <summary><b>session.transactions.transactions</b></summary>

```python
session.transactions.transactions : None | dict = None

    '''

    List of transaction pages that satify a time-based transaction query.
    The "pages" returned are URLs hosted on Oanda's website, presumable to
    prevent excessive network traffic (each page can old up to 1000
    transactions). `None` by default until populated by
    `session.transactions.update_transactions()`.

    '''
```
</details>

<details>
    <summary><b>session.transactions.specificTransaction</b></summary>

```python
session.transactions.specificTransaction : None | dict = None

    '''
    
    Details of a single account transaction. `None` by default until 
    populated by `session.transactions.update_specific()`.
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.inRange</b></summary>

```python
session.transactions.inRange : None | dict = None

    '''

    A range of transaction details for an account based on transaction IDs.
    `None` by default until populated by `session.transactions.update_range()`.

    '''
```
</details>

<details>
    <summary><b>session.transactions.sinceID</b></summary>

```python
session.transactions.sinceID : None | dict = None

    '''
    
    A range of transaction details for an account starting at (but not including) a
    provided transaction ID. `None` by default until populated by
    `session.transactions.update_since()`.

    '''
```
</details>

<details>
    <summary><b>session.transactions.transactionStream</b></summary>

```python
session.transactions.transactionStream : list | = None

    '''

    A continuously updated stream of account transactions starting from when
    `session.transactions.start_stream()` is called (`None` until 
    `session.transactions.start_stream()` is called). `list` if 
    `session.transactions.start_stream(record=True)`, otherwise
    will be a single entry `list` of the most recent stream entry.

    '''
```
</details>

<details>
    <summary><b>session.transactions.update_transactions()</b></summary>

```python
session.transactions.update_transactions(fromTime : datetime.datetime | str | None = None,
                                         toTime : datetime.datetime | str | None = None,
                                         pageSize : int | None = None,
                                         transactionTypes : list[str] | None = None) -> None

    ''' 
    
    Updates `session.transactions.transactions` attribute by filtering the given 
    account's transaction history by timerange and page size.
    

    Parameters
    ----------
    `fromTime` : datetime.datetime | str | None = None
        The starting time (inclusive) of the time range for the Transactions
        being queried. [default=Account Creation Time]. *Note* Ensure time
        it is properly formatted as RFC3339 if string.
    
    `toTime` : datetime.datetime | str | None = None
        The ending time (inclusive) of the time range for the Transactions 
        being queried. [default=Request Time]. *Note* Ensure time
        it is properly formatted as RFC3339 if string.

    `pageSize` : int
        The number of Transactions to include in each page of the results. 
        [default=100, maximum=1000]

    `transactionTypes` : list[str] | None = None
        The filter for restricting the types of transactions to retrieve.
        `None` defaults to zero type filtering.
    
        Example:
        ["ORDER", "TRANSFER_FUNDS"]
        
        Exhaustive List:
        "ORDER" :	Order-related Transactions. These are the Transactions that create, cancel, fill or trigger Orders\n
        "FUNDING"	Funding-related Transactions\n
        "ADMIN"	Administrative Transactions\n
        "CREATE"	Account Create Transaction\n
        "CLOSE"	Account Close Transaction\n
        "REOPEN"	Account Reopen Transaction\n
        "CLIENT_CONFIGURE"	Client Configuration Transaction\n
        "CLIENT_CONFIGURE_REJECT"	Client Configuration Reject Transaction\n
        "TRANSFER_FUNDS"	Transfer Funds Transaction\n
        "TRANSFER_FUNDS_REJECT"	Transfer Funds Reject Transaction\n
        "MARKET_ORDER"	Market Order Transaction\n
        "MARKET_ORDER_REJECT"	Market Order Reject Transaction\n
        "LIMIT_ORDER"	Limit Order Transaction\n
        "LIMIT_ORDER_REJECT"	Limit Order Reject Transaction\n
        "STOP_ORDER"	Stop Order Transaction\n
        "STOP_ORDER_REJECT"	Stop Order Reject Transaction\n
        "MARKET_IF_TOUCHED_ORDER"	Market if Touched Order Transaction\n
        "MARKET_IF_TOUCHED_ORDER_REJECT"	Market if Touched Order Reject Transaction\n
        "TAKE_PROFIT_ORDER"	Take Profit Order Transaction\n
        "TAKE_PROFIT_ORDER_REJECT"	Take Profit Order Reject Transaction\n
        "STOP_LOSS_ORDER"	Stop Loss Order Transaction\n
        "STOP_LOSS_ORDER_REJECT"	Stop Loss Order Reject Transaction\n
        "GUARANTEED_STOP_LOSS_ORDER"	Guaranteed Stop Loss Order Transaction\n
        "GUARANTEED_STOP_LOSS_ORDER_REJECT"	Guaranteed Stop Loss Order Reject Transaction\n
        "TRAILING_STOP_LOSS_ORDER"	Trailing Stop Loss Order Transaction\n
        "TRAILING_STOP_LOSS_ORDER_REJECT"	Trailing Stop Loss Order Reject Transaction\n
        "ONE_CANCELS_ALL_ORDER"	One Cancels All Order Transaction\n
        "ONE_CANCELS_ALL_ORDER_REJECT"	One Cancels All Order Reject Transaction\n
        "ONE_CANCELS_ALL_ORDER_TRIGGERED"	One Cancels All Order Trigger Transaction\n
        "ORDER_FILL"	Order Fill Transaction\n
        "ORDER_CANCEL"	Order Cancel Transaction\n
        "ORDER_CANCEL_REJECT"	Order Cancel Reject Transaction\n
        "ORDER_CLIENT_EXTENSIONS_MODIFY"	Order Client Extensions Modify Transaction\n
        "ORDER_CLIENT_EXTENSIONS_MODIFY_REJECT"	Order Client Extensions Modify Reject Transaction\n
        "TRADE_CLIENT_EXTENSIONS_MODIFY"	Trade Client Extensions Modify Transaction\n
        "TRADE_CLIENT_EXTENSIONS_MODIFY_REJECT"	Trade Client Extensions Modify Reject Transaction\n
        "MARGIN_CALL_ENTER"	Margin Call Enter Transaction\n
        "MARGIN_CALL_EXTEND"	Margin Call Extend Transaction\n
        "MARGIN_CALL_EXIT"	Margin Call Exit Transaction\n
        "DELAYED_TRADE_CLOSURE"	Delayed Trade Closure Transaction\n
        "DAILY_FINANCING"	Daily Financing Transaction\n
        "RESET_RESETTABLE_PL"	Reset Resettable PL Transaction

    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.update_specific()</b></summary>

```python
session.transactions.update_specific(transactionID : int | str) -> None

    ''' 
    
    Updates `session.transactions.specificTransaction` attribute by populating 
    full details of a single transaction.
    

    Parameters
    ----------
    `transactionID` : int | str
        Transaction ID to get details on.
        
    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.update_range()</b></summary>

```python
session.transactions.update_range(fromID : int | str,
                                  toID : int | str,
                                  transactionTypes : list[str] | None = None) -> None

    ''' 
    
    Updates `session.transactions.inRange` attribute by filtering the given 
    account's transaction history down to a specified range of transactions.
    

    Parameters
    ----------
    `fromID` : int | str
        The starting transaction ID (inclusive) to fetch.

    `toID` : int | str
        The ending transaction ID (inclusive) to fetch

    `transactionTypes` : list[str] | None = None
        The filter for restricting the types of transactions to retrieve.
        `None` defaults to zero type filtering.
        *Note* Exhaustive list found with `>help(Transactions.update_transactions)`
        or list found under "TransactionFilter": 
        https://developer.oanda.com/rest-live-v20/transaction-df/#TransactionFilter
    
        Example:
        ["ORDER", "TRANSFER_FUNDS"]
        
    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.update_since()</b></summary>

```python
session.transactions.update_since(sinceID : int | str,
                                  transactionTypes : list[str] | None = None) -> None

    ''' 
    
    Updates `session.transactions.sinceID` attribute by retrieving all 
    transactions that are newer than a given transaction ID (non-inclusive, 
    ie: returned values do not include the transaction ID provided).
    

    Parameters
    ----------
    `sinceID` : int | str
        The starting transaction ID (non-inclusive) to fetch.

    `transactionTypes` : list[str] | None = None
        The filter for restricting the types of transactions to retrieve.
        `None` defaults to zero type filtering.
        *Note* Exhaustive list found with `>help(Transactions.update_transactions)`
        or list found under "TransactionFilter": 
        https://developer.oanda.com/rest-live-v20/transaction-df/#TransactionFilter
    
        Example:
        ["ORDER", "TRANSFER_FUNDS"]
        
    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.start_stream()</b></summary>

```python
session.transactions.start_stream(record : bool = False) -> None

    '''
    
    Begins a stream to populate the `session.transactions.transaction_stream` 
    attribute. `session.transactions.transaction_stream` will be continuously 
    updated with any new transactions without user intervention (but may 
    remain empty when first run - this just means there haven't been any 
    new transactions since the stream began). Overwrites any previous content 
    stored in `session.transactions.transaction_stream`.
    

    Parameters
    ----------
    `record` : bool = False
        (Flag) When set to True, the `transactionStream` will be a `list` of every
        stream entry since the stream is started (ie: records previous entries).
        When set to False, `trasactionStream` will be a single-entry `list` 
        of the most recent dictionary received from the stream (ie: does not 
        record previous entries). [Default=False]

    
    Returns
    -------
    `None`
    
    '''
```
</details>

<details>
    <summary><b>session.transactions.stop_stream()</b></summary>

```python
session.transactions.stop_stream() -> None

    ''' 
    
    Stops `session.transactions.transaction_stream`'s managing thread 
    (`session.transactions._streamThread`). Prevents any new updates to 
    `session.transactions.transaction_stream` attribute. Ensure 
    `session.streamMonitor.doNotResusitate = 0` prior to running 
    `session.transactions.stop_stream()`, otherwise the monitor 
    will just immediately restart it.
    
    
    Parameters
    ----------
    `None`

    
    Returns
    -------
    `None`
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Price Quotes:</i>
> Stream live quotes, get bid-ask spreads, view currency conversion factors.
<details>
    <summary><b>session.pricing</b></summary>

```python
session.pricing : object

    '''

    Your OANDA pricing interface.

    '''
```
</details>

<details>
    <summary><b>session.pricing.latestCandle</b></summary>

```python
session.pricing.latestCandle : dict | None = None

    '''

    Current incomplete candle ("Dancing Bears") AND most recent complete 
    candle within an Account for a specified combination of instrument(s), 
    granularity(s), and price component(s). `None` until 
    `session.pricing.update_latest()` is called.
    
    '''
```
</details>

<details>
    <summary><b>session.pricing.candles</b></summary>

```python
session.pricing.candles : dict | None = None

    '''

    Historic candlestick data for an instrument. `None` until 
    `session.pricing.update_candles()` is called.

    '''
```
</details>

<details>
    <summary><b>session.pricing.pricing</b></summary>

```python
session.pricing.pricing : dict | None = None

    '''

    Pricing information for a specified list of instruments within an
    account. `None` until `session.pricing.update_pricing()` is called.

    '''
```
</details>

<details>
    <summary><b>session.pricing.pricingStream</b></summary>

```python
session.pricing.pricingStream : list | None = None

    '''

    A continuously updated stream of Account Prices starting from when
    `session.pricing.start_stream()` is called (`None` until 
    `session.pricing..start_stream()` is called). `list` if 
    `session.pricing.start_stream(record=True)`, otherwise
    single entry `list` of the most recent stream entry.

    This pricing stream does not include every single price created for the 
    Account, but instead will provide at most 4 prices per second (every 250
    milliseconds) for each instrument being requested. If more than one 
    price is created for an instrument during the 250 millisecond window, 
    only the price in effect at the end of the window is sent. This means 
    that during periods of rapid price movement, subscribers to this 
    stream will not be sent every price. Pricing windows for different 
    connections to the price stream are not all aligned in the same way 
    (i.e. they are not all aligned to the top of the second). This means 
    that during periods of rapid price movement, different subscribers may
    observe different prices depending on their alignment.

    '''
```
</details>

<details>
    <summary><b>session.pricing.update_latest()</b></summary>

```python
session.pricing.update_latest(candleSpecifications : list[str],
                              units : int | str = 1,
                              smooth : bool = False,
                              dailyAlignment : int | str = 17,
                              alignmentTimezone : str = "America/New_York",
                              weeklyAlignment: str = "Friday") -> None

    ''' 
    
    Updates `session.pricing.latestCandle` attribute using provided argument filters.


    Parameters
    ----------
    `candleSpecifications` : list[str]
        List of candle specifications to get pricing for, taking the string 
        argument format of: "<INSTRUMENT>:<GRANULARITY>:<COMPONENT>"

            *Note* Multiple <COMPONENTS> are supported:
            Just Mid (avg. Bid & Ask): ["EUR_USD:S5:M", "USD_JPY:M2:M"]
            Bid AND Ask: ["EUR_USD:S5:BA", "USD_JPY:M2:BA"]
            
            String Arguments:\n
            <INSTRUMENT>:
                    Check supported instrument strings (need `account` object from `Account()` first):\n
                        > `print([x["name"] if x["name"] else None for x in account.instruments["instruments"]])`\n

            <GRANULARITY>:
                    "S5"	: 5 second candlesticks, minute alignment\n
                    "S10"	: 10 second candlesticks, minute alignment\n
                    "S15"	: 15 second candlesticks, minute alignment\n
                    "S30"	: 30 second candlesticks, minute alignment\n
                    "M1"	: 1 minute candlesticks, minute alignment\n
                    "M2"	: 2 minute candlesticks, hour alignment\n
                    "M4"	: 4 minute candlesticks, hour alignment\n
                    "M5"	: 5 minute candlesticks, hour alignment\n
                    "M10"	: 10 minute candlesticks, hour alignment\n
                    "M15"	: 15 minute candlesticks, hour alignment\n
                    "M30"	: 30 minute candlesticks, hour alignment\n
                    "H1"	: 1 hour candlesticks, hour alignment\n
                    "H2"	: 2 hour candlesticks, day alignment\n
                    "H3"	: 3 hour candlesticks, day alignment\n
                    "H4"	: 4 hour candlesticks, day alignment\n
                    "H6"	: 6 hour candlesticks, day alignment\n
                    "H8"	: 8 hour candlesticks, day alignment\n
                    "H12"	: 12 hour candlesticks, day alignment\n
                    "D" 	: 1 day candlesticks, day alignment\n
                    "W"	    : 1 week candlesticks, aligned to start of week\n
                    "M" 	: 1 month candlesticks, aligned to first day of the month\n

            <COMPONENT>:
                    "M" : Midpoint candles
                    "B" : Bid candles
                    "A" : Ask candles
        
    `units` : int | str = 1
        The number of units used to calculate the volume-weighted average 
        bid and ask prices in the returned candles. [default=1]
    
    `smooth` : bool = False
        A flag that controls whether the candlestick is “smoothed” or not. 
        A smoothed candlestick uses the previous candles close price as its
        open price, while an unsmoothed candlestick uses the first price 
        from its time range as its open price. [default=False]

    `dailyAlignment` : int | str = 17
        The hour of the day (in the specified timezone) to use for 
        granularities that have daily alignments. This will be the
        time the daily "Close" will be calculated from. 
        [default=17, minimum=0, maximum=23]

    `alignmentTimezone` : str = "America/New_York"
        The timezone to use for the dailyAlignment parameter. Candlesticks 
        with daily alignment will be aligned to the dailyAlignment hour 
        within the alignmentTimezone. Note that the returned times will 
        still be represented in UTC. [default=America/New_York]
            
        List of "TZ Identifiers": https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        
    `weeklyAlignment` : str = "Friday"
        The day of the week used for granularities that have weekly 
        alignment. This will be the day of week that the "Close" will be 
        calculated from. [default=Friday]
            "Monday"	: Monday\n
            "Tuesday"	: Tuesday\n
            "Wednesday"	: Wednesday\n
            "Thursday"	: Thursday\n
            "Friday"	: Friday\n
            "Saturday"	: Saturday\n
            "Sunday"	: Sunday\n

    Returns
    -------
    `None`


    '''
```
</details>

<details>
    <summary><b>session.pricing.update_candles()</b></summary>

```python
session.pricing.update_candles(instrument : str,
                               price : str = "M",
                               granularity : str = "D",
                               count : int | str | None = None,
                               fromTime : datetime.datetime | str | None = None,
                               toTime : datetime.datetime | str | None = None,
                               smooth : bool = False,
                               includeFirst : bool | None = None,
                               dailyAlignment : int | str = 17,
                               alignmentTimezone : str = "America/New_York",
                               weeklyAlignment : str = "Friday",
                               units : int | str = 1
                               ) -> None

    ''' 
    
    Updates `session.pricing.candles` attribute using provided argument filters.
    
    
    Parameters
    ----------
        `instrument` : str
            Name of the Instrument to request candles for. *Note* if
            `Account()` object present, can check `account.instruments` for
            appropriate names.

        `price` : str = "M"
            The Price component(s) to get candlestick data for. [default=M]
                "M" : Midpoint candles
                "B" : Bid candles
                "A" : Ask candles
                "BA" : Bid and Ask candles
                "MBA" : Mid, Bid, and Ask candles
        
        `granularity` : str = "D"
            The granularity of the candlesticks to fetch [default=D]
                "S5"	: 5 second candlesticks, minute alignment\n
                "S10"	: 10 second candlesticks, minute alignment\n
                "S15"	: 15 second candlesticks, minute alignment\n
                "S30"	: 30 second candlesticks, minute alignment\n
                "M1"	: 1 minute candlesticks, minute alignment\n
                "M2"	: 2 minute candlesticks, hour alignment\n
                "M4"	: 4 minute candlesticks, hour alignment\n
                "M5"	: 5 minute candlesticks, hour alignment\n
                "M10"	: 10 minute candlesticks, hour alignment\n
                "M15"	: 15 minute candlesticks, hour alignment\n
                "M30"	: 30 minute candlesticks, hour alignment\n
                "H1"	: 1 hour candlesticks, hour alignment\n
                "H2"	: 2 hour candlesticks, day alignment\n
                "H3"	: 3 hour candlesticks, day alignment\n
                "H4"	: 4 hour candlesticks, day alignment\n
                "H6"	: 6 hour candlesticks, day alignment\n
                "H8"	: 8 hour candlesticks, day alignment\n
                "H12"	: 12 hour candlesticks, day alignment\n
                "D" 	: 1 day candlesticks, day alignment\n
                "W"	    : 1 week candlesticks, aligned to start of week\n
                "M" 	: 1 month candlesticks, aligned to first day of the month\n

        `count` : int | str | None = None
            The number of candlesticks to return in the response. `count` 
            should not be specified if both the `fromTime` and `toTime` 
            parameters are provided, as the time range combined with the 
            granularity will determine the number of candlesticks to return.
            `count` may be specified if only one `(from or to)Time` is provided. 
            [Default=500 if `None`, or only one of `fromTime` or `toTime`
            is set]. (Max 5000)
        
        `fromTime` : datetime.datetime | str | None = None
            The start of the time range to fetch candlesticks for. 
            *Note* Must be RFC3339 format if string.
        
        `toTime` : datetime.datetime | str | None = None
            The end of the time range to fetch candlesticks for.
            *Note* Must be RFC3339 format if string
        
        `smooth` : bool = False
            A flag that controls whether the candlestick is “smoothed” or 
            not. A smoothed candlestick uses the previous candles close 
            price as its open price, while an un-smoothed candlestick uses 
            the first price from its time range as its open price. 
            [default=False]
        
        `includeFirst` : bool | None = None
            A flag that controls whether the candlestick that is covered by 
            the from time should be included in the results. This flag 
            enables clients to use the timestamp of the last completed 
            candlestick received to poll for future candlesticks but avoid 
            receiving the previous candlestick repeatedly. [default=True, 
            when using 'fromTime' argument (even if left as `None`)]
        
        `dailyAlignment` : int | str = 17
            The hour of the day (in the specified timezone) to use for 
            granularities that have daily alignments. This will be the
            time the daily "Close" will be calculated from. 
            [default=17, minimum=0, maximum=23]

        `alignmentTimezone` : str = "America/New_York"
            The timezone to use for the dailyAlignment parameter. Candlesticks 
            with daily alignment will be aligned to the dailyAlignment hour 
            within the alignmentTimezone. Note that the returned times will 
            still be represented in UTC. [default=America/New_York]
                
            List of "TZ Identifiers": https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
            
        `weeklyAlignment` : str = "Friday"
            The day of the week used for granularities that have weekly 
            alignment. This will be the day of week that the "Close" will be 
            calculated from. [default=Friday]
                "Monday"	: Monday\n
                "Tuesday"	: Tuesday\n
                "Wednesday"	: Wednesday\n
                "Thursday"	: Thursday\n
                "Friday"	: Friday\n
                "Saturday"	: Saturday\n
                "Sunday"	: Sunday\n

        `units` : int | str = 1
            The number of units used to calculate the volume-weighted 
            average bid and ask prices in the returned candles. [default=1]
            
    Returns
    -------
    `None`
    
    
    '''
```
</details>

<details>
    <summary><b>session.pricing.update_pricing()</b></summary>

```python
session.pricing.update_pricing(instruments : list[str],
                               since : datetime.datetime | str | None = None,
                               includeHomeConversions : bool = True) -> None

    ''' 
    
    Updates `session.pricing.pricing` attribute using provided argument filters.
    

    Parameters
    ----------
    `instruments` : list[str]
        List of Instruments to get pricing for. [required]
        Example: ["EUR_USD", "JPY_USD"]

    `since` : datetime.datetime | str | None = None
        Date/Time filter to apply to the response. Only prices and home 
        conversions (if requested) that have changed since this time
        will be provided, and are filtered independently. `None` provides
        current prices and home conversions. [Default=None]
        *Note* Ensure RCF3339 formatted.
    
    `includeHomeConversions` : bool = True
        Flag that enables the inclusion of the homeConversions field in the 
        returned response. An entry will be returned for each currency in 
        the set of all base and quote currencies present in the requested 
        instruments list. [default=True]

    
    Returns
    -------
    `None`


    '''
```
</details>

<details>
    <summary><b>session.pricing.pretty_candles()</b></summary>

```python
session.pricing.pretty_candles(spread : bool = False) -> pandas.DataFrame

    '''
    
    Returns copy of candles in `session.pricing.candles` as a 
    `pandas.DataFrame`. No error checking is done prior to conversion - 
    ensure `session.pricing.candles` have  been successfully retrieved first 
    by confirming `session.pricing.rcode` == 200. *Note*: "o", "h", "l", and
    "c" will be appended with a suffix to indicate quote type:

        "<no suffix>"      : the average ("mid") of the bid-ask quotes (standard quote)
        "_bid"             : the bid
        "_ask"             : the ask
        "_spread"          : the bid-ask spread (if requested)


    Parameters
    ----------
    `spread` : bool = False
        If set to `True` and both the bid and ask were requested in your 
        `update_candles()` command, the spread will be appended to the
        returned DataFrame on your behalf. [default=False]

    Returns
    -------
    `pandas.DataFrame`
        Candles in `pandas.DataFrame` format.
    
    '''
```
</details>

<details>
    <summary><b>session.pricing.start_stream()</b></summary>

```python
session.pricing.start_stream(instruments : list[str],
                             snapshot : bool = True,
                             includeHomeConversions : bool = False,
                             record : bool = False) -> None

    ''' 
    
    Begins a stream to populate the `session.pricing.pricingStream` attribute.
    `session.pricing.pricingStream` will be continuously updated with any new
    prices without user intervention (but may remain empty when
    first run - this just means there haven't been any new pricing updates
    since the stream began). Overwrites any previous content stored in
    `session.pricing.pricingStream`.


    Parameters
    ----------
    `instruments` = list[str]
        List of Instruments to stream Prices for.
        Example: ["EUR_USD", "JPY_USD"]

    `snapshot` : bool = True
        Flag that enables/disables the sending of a pricing snapshot when 
        initially connecting to the stream. Will provide most recent quote 
        available, whether market is open or closed - if `False`, pricingStream
        will remain empty until Oanda server sends new quotes (this won't be
        until the next open if the stream is started while the market is closed).
        [default=True]
    
    `includeHomeConversions` : bool = False
        Flag that enables the inclusion of the homeConversions field in the 
        returned response. An entry will be returned for each currency in 
        the set of all base and quote currencies present in the requested 
        instruments list. [default=False]
    
    `record` : bool = False
        (Flag) When set to True, the `pricingStream` will be a `list` of every
        stream entry since the stream is started (ie: records previous entries).
        When set to False, `pricingStream` will be a single entry `list`
        of the most recent dictionary received from the stream (ie: does not
        record previous entries). [Default=False]

    Returns
    -------
    `None`

    '''
```
</details>

<details>
    <summary><b>session.pricing.stop_stream()</b></summary>

```python
session.pricing.stop_stream() -> None

    ''' 
    
    Stops `session.pricing.pricingStream`'s managing thread 
    (`session.pricing._streamThread`). Prevents any new updates to 
    `pricingStream` attribute. Ensure `session.streamMontior.doNotResusitate = 0`
    prior to running `self.stop_stream()`, otherwise the monitor
    will just immediately restart it.
    
    Parameters
    ----------
    None

    
    Returns
    -------
    `None`
    
    '''
```
</details>

<p>&nbsp;</p>

### <i>Session Monitors:</i>
> View a order logs, view a error logs, configure streaming preferences.
<details>
    <summary><b>session.errorMonitor</b></summary>

```python
session.errorMonitor : object

    '''

    Monitors all of the above OANDA interface objects for client-server errors.

    '''

```
</details>

<details>
    <summary><b>session.errorMonitor.logs</b></summary>

```python
session.errorMonitor.logs : list[dict]

    '''

    A continuously updated list of client-server errors made since the 
    session was started. *Note* If `logPath` is specified in 
    `easyoanda.start_session()`, any pre-existing logs within the specified log 
    file will  be loaded into this variable prior to appending additional logs to it.

    Single Log Entry Format:
    {
        "entryID" : the log's serialized entry number (beginning at 0)
        "datetime" : the date/time the error was logged (UTC)
        "originClass" : the "endpoint interface" type (a class within `session` module)
            that received the error

        "errorDetails" : the error message details, with contents:
            {
                "url" : full url that the request was sent to
                "headers" : headers included in the request (Authorization token is 
                    stripped for security, check independently if this is the 
                    suspected issue)
                "parameters" : parameters included in the request
                "payload" : the request's json payload (`None` if "GET" request)
                "code" : the error status code - will be HTTP code or "other" (999)
                "message" : the error message received
            }
    }
    
    '''
```
</details>

<details>
    <summary><b>session.orderMonitor</b></summary>

```python
session.orderMonitor : object

    '''

    Monitors `session.orders`, `session.trades`, and `session.positions` 
    interface objects for successful financial transactions.

    '''

```
</details>

<details>
    <summary><b>session.orderMonitor.logs</b></summary>

```python
session.orderMonitor.logs : list[dict]

    '''

    A continuously updated list of order confirmations made since the 
    session was started. *Note* If `logPath` is specified on 
    initialization, any pre-existing logs within the specified log file will 
    be loaded into this variable prior to appending additional logs to it.

    Single Log Entry Format:
    {
        "entryID" : the log's serialized entry number (beginning at 0)
        "datetime" : the date/time the order was confirmed (UTC)
        "originClass" : the "endpoint interface" type (a class within `session` module)
            that sent the order
        "confirmationDetails" : Oanda's reponse to successfully receiving the order
    }
    
    '''
```
</details>

<details>
    <summary><b>session.streamMonitor</b></summary>

```python
session.streamMonitor : object

    '''

    Monitors `session.pricing.pricingStream` and `session.transitions.transitionStream`
    (if active) for their respective heartbeats, setting "dead stream" error 
    messages and restarting streams as needed.

    '''
```
</details>

<details>
    <summary><b>session.streamMonitor.deadOnArrival</b></summary>

```python
session.streamMonitor.deadOnArrival : datetime.timedelta

    '''

    "Dead On Arrival" - number of seconds between heartbeats before a stream
    is considered dead. Oanda heartbeats are ~5s. Stream re-starts take ~2s.
    Allow at least ~7s (preferably more) if modifying this attribute. [Default=10]

    '''
```
</details>

<details>
    <summary><b>session.streamMonitor.doNotResusitate</b></summary>

```python
session.streamMonitor.doNotResusitate : int

    '''

    "Do Not Resuscitate" - number of times to attempt to restart a stream. 
    Read `session.streamMonitor.resetTime` details prior to changing this
    variable in production-ready code. [Default=3]

    '''
```
</details>

<details>
    <summary><b>session.streamMonitor.resetTime</b></summary>

```python
session.streamMonitor.resetTime : datetime.timedelta

    '''

    Number of minutes before resetting `session.streamMonitor.doNotResusitate` 
    counters back to zero for each  endpoint. *Note* `doNotResusitate` is 
    meant to give time for minor issues to resolve themselves (brief drops in 
    WiFi service, ISP routing issues, etc.) -  `resetTime` gives time for 
    higher-level issues to be resolved (Example: the Oanda streaming server 
    crashes, but is brought back up by their IT department within the 
    hour). [Default=60]

    '''
```
</details>

<p>&nbsp;</p>











