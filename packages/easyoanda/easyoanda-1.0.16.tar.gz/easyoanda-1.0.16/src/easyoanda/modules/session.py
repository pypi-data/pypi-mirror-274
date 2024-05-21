from . import comms
from .prebuild import MarketOrder, LimitOrder, StopOrder, \
                     MarketIfTouchedOrder, TakeProfitOrder, \
                     StopLossOrder, GuaranteedStopLossOrder, \
                     TrailingStopLossOrder
import copy
import datetime
import threading
import pandas

''' SESSION SETTINGS '''
class BaseClient():
    ''' Initial configuration for communicating with Oanda server.

    Attributes
    ----------------
    `rest_URL` : str
        Server to send RESTFUL v20 comms to.

    `stream_URL` : str
        Server to request data streams from.

    `accountID` : str
        Unique Account ID for the account to trade with (identify
            within Oanda portal).

    `token` : str
        The given account's authentication header (created from token
        generated in Oanda portal for API access).
    
    `headers` : str
        Standard headers requested by Oanda API docs for most communications.

    Methods
    --------------
    `new()` : func
        Simple wrapper for `copy.deepcopy()`. Returns deepcopy of current
        BaseClient object. Useful for working with multiple accounts / 
        endpoints.
    
    '''

    def __init__(self, sessionType : str,
                 accountID : str,
                 token : str) -> None:
        ''' Initialize BaseClient object.

        Parameters
        ----------------
        `sessionType` : str
            Determines which oanda servers to send all subsequent communication
            to:

                "paper" = Paper account
                "live" = Live account\n
        
        `accountID` : str
            Unique Account ID for the account to trade with (identify
            within Oanda portal).

        `token` : str
            Unique token generated for Oanda account. *Note* All "live" accounts
            share the same token, but "paper" accounts have their own unique
            token - make sure you're providing the correct one for the 
            `sessionType` started.


        Returns
        -----------
        `None`

        '''


        # set server URLs
        if sessionType == "paper":
            self.rest_URL = "https://api-fxpractice.oanda.com"
            self.stream_URL = "https://stream-fxpractice.oanda.com"

        elif sessionType == "live":
            self.rest_URL = "https://api-fxtrade.oanda.com"
            self.stream_URL = "https://stream-fxtrade.oanda.com"

        # set account ID
        self.accountID = accountID

        # set bearer token
        self.token = "Bearer {}".format(token)

        # set standard headers
        self.headers = {"Authorization" : self.token, 
                        "Content-Type" : "application/json",
                        "AcceptDatetimeFormat" : "RFC3339"}

        return None

    def new(self):
        ''' Simple wrapper for `copy.deepcopy()`. Returns deepcopy of current
        BaseClient object. Useful for working with multiple accounts / 
        endpoints.

        Parameters
        ----------------
        `None`


        Returns
        -----------
        `BaseClient`
            Deepcopy of current BaseClient object.

        '''
        return copy.deepcopy(self)

''' ENDPOINT APIs '''
class Account():
    ''' Oanda account interface. Only class that explicitately starts
    a connection with "Keep-Alive" (ie: should create an object with this class
    prior to all other instantiations).

    Attributes
    ----------------  
    `fullDetails` : dict
        Full details for a single Account that a client has access to. Full
        pending Order, open Trade and open Position represenataion are
        provided.

    `summary` : dict
        Summary for a single Account that a client has access to.

    `instruments` : dict
        List of tradeable instruments for the given Account. The list of
        tradeable instruments is dependent on the regulatory division that the 
        Account is located in, thus should be the same for all Accounts owned by
        a single user.

    `changes` : dict
        Current state and changes in an account since a specified
        point in time (by TransactionID).

    `rcode` : int
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` module exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made subqsequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received

    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.
            
    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory

    `_firstTransactionID` : str
        Transaction ID of the first account summary of the session (used to
        identify changes to the given account from the beginning of the session
        onward).


    Methods
    --------------
    `update_fullDetails()` : func
        Updates `self.fullDetails` attribute.

    `update_summary()` : func
        Updates `self.summary` attribute.
    
    `update_changes()` : func
        Updates `self.changes` attributes using provided argument filters.

    `set_margin()` : func
        Sets the margin rate for an account. *Note* Know your account's
        maximum allowable margin rate - typically 50:1 (.02).
        
    '''
    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Account object.

        Parameters
        ----------------
        `base` : BaseClient
            Base configurations for current session.


        Returns
        -----------
        `None`

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()

        # set "Account" object range
        self._range = "/v3/accounts/{}".format(self._base.accountID)

        # setting first contact (full details) to "Keep-Alive"
        temp_header = dict(self._base.headers)
        temp_header["Connection"] = "Keep-Alive"

        # get full details
        target = ""
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=temp_header)
        if (self.rcode == 200) or (self.rcode == 201):
            self.fullDetails = response
        else:
            self.errorMessage = response

        # get account summary
        target = "/summary"        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)
        if (self.rcode == 200) or (self.rcode == 201):
            self.summary = response
        else:
            print(self.errorMessage)
            self.errorMessage = response
        
        # get tradable instruments
        target = "/instruments"        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers)
        if (self.rcode == 200) or (self.rcode == 201):
            self.instruments = response
        else:
            self.errorMessage = response

        # set transaction IDs
        if self.summary:
            self._firstTransactionID = self.summary["lastTransactionID"]
        else:
            self._firstTransactionID = None

        # get account changes baseline
        target = "/changes"
        params = {"sinceTransactionID" : self._firstTransactionID}        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target,
                                                headers=self._base.headers,
                                                parameters=params)
        if (self.rcode == 200) or (self.rcode == 201):
            self.changes = response
        else:
            self.errorMessage = response

        return None
    
    def update_fullDetails(self) -> None:
        ''' Updates `self.fullDetails` attribute.

        Parameters
        ----------------
        `None`

        Returns
        -----------
        `None`

        '''

        # get new full account details
        target = ""        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)
        if (self.rcode == 200) or (self.rcode == 201):
            self.fullDetails = response
        else:
            self.errorMessage = response
        
        # allow error logging as necessary
        self._errorLock.release()


        return None

    def update_summary(self) -> None:
        ''' Updates `self.summary` attribute.

        Parameters
        ----------------
        `None`

        Returns
        -----------
        `None`

        '''

        # get new account summary
        target = "/summary"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)
        if (self.rcode == 200) or (self.rcode == 201):
            self.summary = response
        else:
            self.errorMessage = response        

        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_changes(self, transactionID : int | str | None = None) -> None:
        ''' Updates `self.changes` attributes using provided argument filters.

        Parameters
        ----------------
        `transactionID` : int | str | None = None
            ID of the Transaction to get Account changes since - if
            `None`, will update from the beginning of the session.

        Returns
        -----------
        `None`

        '''

        # set transactionID
        if not transactionID:
            transactionID = self._firstTransactionID

        # get new account changes
        target = "/changes"
        params = {"sinceTransactionID" : transactionID}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target,
                                                headers=self._base.headers,
                                                parameters=params)
        if (self.rcode == 200) or (self.rcode == 201):
            self.changes = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def set_margin(self, marginRate : float | str) -> None:
        ''' Sets the margin rate for an account. *Note* Know your account's
        maximum allowable margin rate - typically 50:1 (.02) - to avoid failed
        requests.

        Parameters
        ----------
        `marginRate` : float | str
            New margin rate to set for account.

        Returns
        -------
        `None`
        
        '''

        # set new account margin rate
        target = "/configuration"
        data = {"marginRate" : marginRate}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.patch_request(self._base.rest_URL \
                                                + self._range \
                                                + target,
                                                headers=self._base.headers,
                                                data=data)
        if (self.rcode == 200) or (self.rcode == 201):
            pass
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

class Instruments():
    ''' Oanda instrument interface.
    
    Attributes
    ----------------
    `candles` : None | dict = None
        Candle stick data for an instrument. `None` until populated by
        `self.update_candles()`.
    
    `orderBook` : None | dict = None
        Snapshot of an instrument's order book at a given point in time.
        `None` until populated by `self.update_orderBook()`.
    
    `positionBook` : None | dict = None
        Snapshot of an instrument's position book at a given point in time.
        `None` until populated by `self.update_positionBook()`.

    `rcode` : int | None
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received
        
    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory
    
    Methods
    -----------------

    `update_candles()` : func
        Updates `self.candles` attribute using provided argument filters.
    
    `update_orderBook()` : func
        Updates `self.orderBook` attribute using provided argument filters.
    
    `update_positionBook()` : func
        Updates `self.positionBook` attribute using provided argument filters.
    
    `copy_candles()` : func
        Returns copy of candles in `self.candles` as a `pandas.DataFrame`. No
        error checking is done prior to the copy / formatting - ensure 
        `self.candles` have  been successfully retrieved first by confirming 
        `self.rcode` == 200.

    '''

    def __init__(self, base) -> None:
        ''' Initializes Instruments object.
        
        Parameters
        ----------------
        `base` : BaseClient
            Base configurations for current session.
            

        Returns
        -----------
        `None`

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()

        # set "Instruments" object range
        self._range = "/v3/instruments"

        # placeholder for candles / orderBook / positionBook
        self.candles = None
        self.orderBook = None
        self.positionBook = None
        self.rcode = 200        # error monitor will ignore until actual comms start

        return None

    def update_candles(self,
                       instrument : str,
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
                       ) -> None:
        ''' Updates `self.candles` attribute using provided argument filters.
        
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

        # get candles
        target = "/{}/candles".format(instrument)
        params = {"price" : price,
                  "granularity" : granularity,
                  "count" : count,
                  "from" :  fromTime,
                  "to" :  toTime,
                  "smooth" : smooth,
                  "includeFirst" : includeFirst,
                  "dailyAlignment" : dailyAlignment,
                  "alignmentTimezone" : alignmentTimezone,
                  "weeklyAlignment" : weeklyAlignment}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.candles = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_orderBook(self, 
                         instrument : str, 
                         time : datetime.datetime | str | None = None) -> None:
        ''' Updates `self.orderBook` attribute using provided argument filters.
        
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
        # get order book
        target = "/{}/orderBook".format(instrument)
        params = {"time" : time}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.orderBook = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_positionBook(self, 
                         instrument : str, 
                         time : datetime.datetime |  str | None = None) -> None:
        ''' Updates `self.positionBook` attribute using provided argument filters.
        
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
        # get position book
        target = "/{}/positionBook".format(instrument)
        params = {"time" : time}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.positionBook = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

            
        return None

    def copy_candles(self, spread : bool = False) -> pandas.DataFrame:
        '''
        
        Returns copy of candles in `self.candles` as a `pandas.DataFrame`. No
        error checking is done prior to the copy / formatting - ensure 
        `self.candles` have  been successfully retrieved first by confirming 
        `self.rcode` == 200. *Note*: "o", "h", "l", and  "c" will be appended 
        with a suffix to indicate quote type:

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

        # will contain mid / bid / ask / spread(s)
        mids = []
        bids = []
        asks = []
        spreads = []
        volumes = []

        # iterate over all retrieved candles
        for item in self.candles["candles"]:

            # temp candle - will be adding datetimes to various keys
            temp = copy.deepcopy(item)

            # attach datetime key to mid
            if "mid" in temp.keys():
                mid = temp["mid"]
                mid["datetime"] = temp["time"]
                mids.append(mid)

            # attach datetime key to bid
            if "bid" in temp.keys():
                bid = temp["bid"]
                bid["datetime"] = temp["time"]
                bids.append(bid)


            # attach datetime key to ask
            if "ask" in temp.keys():
                ask = temp["ask"]
                ask["datetime"] = temp["time"]
                asks.append(ask)


            # calculate spread + attach datetime key to spread
            if (spread) and ("bid" in temp.keys()) and ("ask" in temp.keys()):
                tempSpread =  {"o" :temp["bid"]["o"] - temp["ask"]["o"],
                               "h": temp["bid"]["h"] - temp["ask"]["h"],
                               "l": temp["bid"]["l"] - temp["ask"]["l"],
                               "c": temp["bid"]["c"] - temp["ask"]["c"],
                               "datetime" : temp["time"]}
                spreads.append(tempSpread)

            # build volume dictionary
            volume = {"volume" : temp["volume"], "datetime" : temp["time"]}
            volumes.append(volume)

        # will contain individual quotes
        quotes = []

        # build quote dataframes
        if mids:
            quotes.append(pandas.DataFrame(mids).set_index("datetime"))
        if bids:
            quotes.append(pandas.DataFrame(bids).set_index("datetime").add_suffix("_bid"))
        if asks:
            quotes.append(pandas.DataFrame(asks).set_index("datetime").add_suffix("_ask"))
        if spreads:
            quotes.append(pandas.DataFrame(spreads).set_index("datetime").add_suffix("_spread"))

        # build volumen dataframe
        quotes.append(pandas.DataFrame(volumes).set_index("datetime"))

        # join to one
        quotes = quotes[0].join(quotes[1:])

        return quotes

class Orders():
    ''' Oanda orders interface.

    Attributes
    ----------------
    `orders` : None | dict = None
        Filtered orders of an account. `None` until populated by
        `self.update_orders()`.

    `pendingOrders` : dict
        All pending orders in an account.

    `specificOrder` : None | dict = None
        Details of a single order in a given account. `None` until
        populated by `self.update_specific()`.

    `rcode` : int
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received

    `orderMessage` : dict = None
        Oanda's confirmation message if an order has been successfully created, 
        cancelled, or replaced. 

    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_orderLock` : threading.Lock
        Successful order codes are set prior to order confirmation messages - 
        this lock exists to ensure both are properly updated before 
        order monitoring thread records them.

    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory

    Methods
    --------------
    `update_orders()` : func
        Updates `self.orders` attribute using provided argument filters.

    `update_pending()` : func
        Updates `self.pendingOrders` (no filtering required).

    `update_specific()` : func
        Updates `self.specificOrder` attribute by populating full details of a 
        single order via a given order id ("orderSpecifier").

    `replace_order()` : func
        Replaces an order in an account by simultaneously cancelling it
        and creating a new order.
    
    `cancel_order()` : func
        Cancels a pending order in an account.

    `place_order()` : func
        Places an order for an account.

    '''

    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Orders object.

        Parameters
        ----------------
        `base` : BaseClient
            Base configurations for current session.
            

        Returns
        -----------
        `None`

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()
        self._orderLock = threading.Lock()

        # set "Orders" object range
        self._range = "/v3/accounts/{}".format(self._base.accountID)

        # get pending orders
        target = "/pendingOrders"        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.pendingOrders = response
        else:
            self.errorMessage = response        

        # placeholder for orders / specificOrder  / order confirmations
        self.orders = None
        self.specificOrder = None
        self.orderMessage = None

        return None

    def update_orders(self, 
                      instrument : str | None = None,
                      state : str = "PENDING",
                      ids : list[str | int] | None = None,
                      beforeID : str | int | None = None,
                      count : int = 50) -> None:
        ''' Updates `self.orders` attribute by filtering the given account's 
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
        
        # get filtered orders
        target = "/orders"
        params = {"ids" : ids,
                  "state": state,
                  "instrument" : instrument,
                  "count" : count,
                  "beforeID" : beforeID}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target,
                                                headers=self._base.headers,
                                                parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.orders = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_pending(self) -> None:
        ''' Updates `self.pendingOrders` (no filtering required).

        Parameters
        ----------------
        `None`

        Returns
        -----------
        `None`

        '''

        # get pending orders
        target = "/pendingOrders"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.pendingOrders = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()
            
        return None

    def update_specific(self, orderID : int | str) -> None:
        ''' Updates `self.specificOrder` attribute by populating full details of
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

        # get single order
        target = "/orders/{}".format(orderID)        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.specificOrder = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def replace_order(self, 
                      orderID: int | str,
                      newOrder : dict | MarketOrder | LimitOrder | StopOrder
                      | MarketIfTouchedOrder | TakeProfitOrder | StopLossOrder |
                      GuaranteedStopLossOrder | TrailingStopLossOrder) -> None:
        ''' Replaces an order in an account by simultaneously cancelling it
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
    
        # set target
        target = "/orders/{}".format(orderID)

        # create body
        data = {}

        # set payload
        if isinstance(newOrder, dict):
            data["order"] = newOrder
        else:
            data["order"] = newOrder.get_payload()        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        # Replace an active order
        response, self.rcode = comms.put_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers,
                                            data=data)
        
        if (self.rcode == 200) or (self.rcode == 201):

            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

             # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response

            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def cancel_order(self, 
                     orderID: int | str) -> None:
        ''' Cancels a pending order in an account.

        Parameters
        ----------
        `orderID`: int | str
            Specific order to cancel. `orderID` may be index (int)
            or "Client ID" (string) (Example: 6372 or "@my_order_100")

        Returns
        -------
        `None`

        '''

        # set target
        target = "/orders/{}/cancel".format(orderID)        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        # Replace an active order
        response, self.rcode = comms.put_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers)
        
        if (self.rcode == 200) or (self.rcode == 201):

            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

            # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response

            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()
        
        return None

    def place_order(self, 
                     newOrder : dict | MarketOrder | LimitOrder | StopOrder
                     | MarketIfTouchedOrder | TakeProfitOrder | StopLossOrder |
                     GuaranteedStopLossOrder | TrailingStopLossOrder) -> None:
        ''' Places an order for an account.

        Parameters
        ----------
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
    
        # set target
        target = "/orders"

        # create body
        data = {}

        # set payload
        if isinstance(newOrder, dict):
            data["order"] = newOrder
        else:
            data["order"] = newOrder.get_payload()        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        # Place the order
        response, self.rcode = comms.post_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers,
                                            data=data)

        if (self.rcode == 200) or (self.rcode == 201):
            
            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

            # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response
        
            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

class Trades():
    ''' Oanda trades interface.

    Attributes
    ----------------
    `trades` : None | dict = None
        Filtered trades of a given account. `None` until populated by
        `self.update_trades()`.

    `openTrades` : dict
        All open trades in an account.

    `specificTrade` : None | dict = None
        Details of a single trade in a given account. `None` until
        populated by `self.update_specific()`.

    `rcode` : int
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received

    `orderMessage` : dict = None
        Oanda's confirmation message if a trade has been successfully cancelled
        or modified.
            
    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_orderLock` : threading.Lock
        Successful order codes are set prior to order confirmation messages - 
        this lock exists to ensure both are properly updated before 
        order monitoring thread records them.

    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory

    Methods
    --------------
    `update_trades()` : func
        Updates `self.trades` attribute using provided argument filters.

    `update_open()` : func
        Updates `self.openTrades` (no filtering required).

    `update_specific()` : func
        Updates `self.specificTrade` attribute by populating full details of a 
        single trade via a given trade id ("tradeSpecifier").

    `close_trade()` : func
        Close (partially or fully) a specified open trade in an account.

    `modify_trade()` : func
        Create, replace, or cancel a trade's dependent orders (Take Profit, Stop 
        Loss, Trailing Stop Loss, and/or Guaranteed Stop Loss). 
        All dependent orders are set to Market Order fill types with the exception
        of Guaranteed Stop Losses (this is a server-side configuration). `distance`
        settings are evaluated off of their respective position types - ie: if a
        position is short, a stop/take profit using distance is calcualted off of
        the current ASK price (and filled once BID hits it); if a position is long, a
        stop / take profit is calculated off of the current BID price (and filled
        once the ASK hits it). If more specific exit requirements are needed,
        considered using `Orders` class to create / overwrite dependent orders with
        a completely new order instead of modifying dependent orders 
        directly with this implementation - this function is meant to be an 
        intuitive and quick way to modify dependent orders without going through 
        the trouble of creating an entire new order, there are just limits to 
        it's granularity (all are set to Market Orders with default price 
        evaluations). *Note* Can change multiple of the listed  dependents at once.

    '''

    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Trades object.

        Parameters
        ----------------
        `base` : BaseClient
            Base configurations for current session.
            

        Returns
        -----------
        `None`

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()
        self._orderLock = threading.Lock()

        # set "Trades" object range
        self._range = "/v3/accounts/{}".format(self._base.accountID)

        # get open trades
        target = "/openTrades"        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.openTrades = response
        else:
            self.errorMessage = response        

        # placeholder for trades / specificTrade  / order confirmations
        self.trades = None
        self.specificTrade = None
        self.orderMessage = None

        return None

    def update_trades(self, instrument : str | None = None,
                      state : str = "OPEN",
                      ids : list[str, int] | None = None,
                      beforeID : str | int | None = None,
                      count : int = 50) -> None:
        ''' Updates `self.trades` attribute using provided argument filters.

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
        
        # get filtered trades
        target = "/trades"
        params = {"ids" : ids,
                  "state": state,
                  "instrument" : instrument,
                  "count" : count,
                  "beforeID" : beforeID}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target,
                                                headers=self._base.headers,
                                                parameters=params)

        if (self.rcode == 200) or (self.rcode == 201):
            self.trades = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_open(self) -> None:
        ''' Updates `self.openTrades` (no filtering required).

        Parameters
        ----------------
        None

        Returns
        -----------
        `None`

        '''

        # get open trades
        target = "/openTrades"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.openTrades = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_specific(self, tradeID : int | str) -> None:
        ''' Updates `self.specificTrade` attribute by populating full details of
        a single trade via a given trade id ("tradeSpecifier").

        Parameters
        ----------------
        `tradeID` : int | str
            Specific trade to collect details on. `tradeID` may be index (int)
            or "Client ID" (string) (Example: 6395 or "@my_eur_usd_trade")

        Returns
        -----------
        `None`

        '''

        # get single trade
        target = "/trades/{}".format(tradeID)        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.specificTrade = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def close_trade(self, 
                    tradeID : int | str, 
                    units : int | str = "ALL") -> None:
        ''' Close (partially or fully) a specified open trade in an account.

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
        # set target
        target = "/trades/{}/close".format(tradeID)

        data = {"units" : units}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()
        
        # Fully / partially close a position
        response, self.rcode = comms.put_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers,
                                            data=data)

        if (self.rcode == 200) or (self.rcode == 201):
            
            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

            # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response

            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def modify_trade(self, tradeID : int | str,
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
                        gslGtdTime : datetime.datetime | str | None= None) -> None:
        ''' Create, replace, or cancel a trade's dependent orders (Take Profit,
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
        one instead of modifying dependents directly with this implementation - this 
        implementation is an intuitive, quick way to modify dependent 
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
        
        # set target
        target = "/trades/{}/orders".format(tradeID)
        
        # load payload
        if preBuilt:
            data = preBuilt

        else:
            data = {}

            # if cancelling Take Profit
            if cancelTP:
                data["takeProfit"] = None

            # if modifying Take Profit
            elif modifyTP:

                # prep payload sub-section
                data["takeProfit"] = {}

                # update take profit (only price or distance may be specified)
                if tpPrice:
                    data["takeProfit"]["price"] = tpPrice
                elif tpDistance:
                    data["takeProfit"]["distance"] = tpDistance

                # update time-in-force, if applicable
                if tpTimeInForce:
                    data["takeProfit"]["timeInForce"] = tpTimeInForce

                # update GTD date/time, if applicable
                if tpTimeInForce == "GTD":
                    data["takeProfit"]["gtdTime"] = tpGtdTime


            # if cancelling Stop Loss
            if cancelSL:
                data["stopLoss"] = None

            # if modifying Stop Loss
            elif modifySL:

                # prep payload sub-section
                data["stopLoss"] = {}
                
                # set stop (only price or distance may be specified)
                if slPrice:
                    data["stopLoss"]["price"] = slPrice
                elif slDistance:
                    data["stopLoss"]["distance"] = slDistance
                
                # update time-in-force, if applicable
                if slTimeInForce:
                    data["stopLoss"]["timeInForce"] = slTimeInForce
                
                # set GTD date/time, if applicable
                if slTimeInForce == "GTD":
                    data["stopLoss"]["gtdTime"] = slGtdTime


            # if cancelling Trailing Stop Loss
            if cancelTSL:
                data["trailingStopLoss"] = None

            # if modifying Trailing Stop Loss
            elif modifyTSL:

                # prep payload sub-section
                data["trailingStopLoss"] = {}

                # update stop
                data["trailingStopLoss"]["distance"] = tslDistance
                
                # update time-in-force, if applicable
                if tslTimeInForce:
                    data["trailingStopLoss"]["timeInForce"] = tslTimeInForce
                
                # update GTD date/time, if applicable
                if tslTimeInForce == "GTD":
                    data["trailingStopLoss"]["gtdTime"] = tslGtdTime
                

            # if cancelling Guaranteed Stop Loss
            if cancelGSL:
                data["guaranteedStopLoss"] = None

            # if modifying Guaranteed Stop Loss
            elif modifyGSL:

                # prep payload sub-section
                data["guaranteedStopLoss"] = {}

                # update stop (only price or distance may be specified)
                if gslPrice:
                    data["guaranteedStopLoss"]["price"] = gslPrice
                elif gslDistance:
                    data["guaranteedStopLoss"]["distance"] = gslDistance
                
                # update time-in-force, if applicable
                if gslTimeInForce:
                    data["guaranteedStopLoss"]["timeInForce"] = gslTimeInForce

                # update GTD date/time, if applicable
                if gslTimeInForce == "GTD":
                    data["guaranteedStopLoss"]["gtdTime"] = gslGtdTime

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        # Modify a trade's dependent orders
        response, self.rcode = comms.put_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers,
                                            data=data)

        if (self.rcode == 200) or (self.rcode == 201):        

            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

            # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response            
            
            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

class Positions():
    ''' Oanda positions interface.

    Attributes
    ----------------
    `positions` : dict
        All positions for an account. Positions listed are for every 
        instrument that has had a position during the lifetime of an account.

    `openPositions` : dict
        All open positions for an account. An open position is a position in an
        account that currently has a trade opened for it. *Note* If a trade has
        a state of "CLOSE_WHEN_TRADEABLE", it MAY NOT be included here
        (testing to come).

    `specificPosition` : None | dict = None
        Details of a single instrument's position in an account. The position
        may or may not be open.
        `None` until populated by `self.update_specific()`.

    `rcode` : int
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received

    `orderMessage` : dict = None
        Oanda's confirmation message if a position has been successfully partially
        or fully closed.

    `_orderLock` : threading.Lock
        Successful order codes are set prior to order confirmation messages - 
        this lock exists to ensure both are properly updated before 
        order monitoring thread records them.
        
    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory

    Methods
    --------------
    `update_positions()` : func
        Updates `self.positions` attribute (no arguments required).

    `update_open()` : func
        Updates `self.openPositions` attribute (no arguments required).

    `update_specific()` : func
        Updates `self.specificPosition` attribute by populating full details of
        a  single position (open or closed) via a given instrument.

    `close_position()` : func
        Fully or partially closes out an open position for a specific 
        instrument in an account using a non-optional "market order" (this is a
        server-side configuration).

    '''

    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Positions object.

        Parameters
        ----------------
        `base` : BaseClient
            Base configurations for current session.
            

        Returns
        -----------
        None

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()
        self._orderLock = threading.Lock()

        # set "Positions" object range
        self._range = "/v3/accounts/{}".format(self._base.accountID)

        # get all positions
        target = "/positions"        
        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.positions = response
        else:
            self.errorMessage = response        
            
        # get open positions
        target = "/openPositions"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.openPositions = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        # placeholder for specific position / order confirmations
        self.specificPosition = None
        self.orderMessage = None

        return None

    def update_positions(self) -> None:
        ''' Updates `self.positions` attribute (no arguments required).

        Parameters
        ----------------
        `None`

        Returns
        -----------
        `None`

        '''
        
        # update all positions
        target = "/positions"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.positions = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None
       
    def update_open(self) -> None:
        ''' Updates `self.openPositions` attribute (no arguments required).

        Parameters
        ----------------
        `None`

        Returns
        -----------
        `None`

        '''
        
        # update open positions
        target = "/openPositions"        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                + self._range \
                                                + target, 
                                                headers=self._base.headers)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.openPositions = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()
            
        return None

    def update_specific(self, instrument : str) -> None:
        ''' Updates `self.specificPosition` attribute by populating full details
        of a single position (open or closed) via a given instrument.

        Parameters
        ----------------
        `instrument` : str
            Instrument name to get position details on.


        Returns
        -----------
        `None`

        '''

        # get single position
        target = "/positions/{}".format(instrument)        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target, 
                                                    headers=self._base.headers)
        if (self.rcode == 200) or (self.rcode == 201):
            self.specificPosition = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def close_position(self,
                       instrument : str,
                       longUnits : str | int = "NONE",
                       shortUnits : str | int = "NONE") -> None:
        ''' Fully or partially closes out an open position for a specific 
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
            on the account, may send `shortUnits` argument as well
            ("ALL" or integer), otherwise `shortUnits` must remain "NONE" if passing
            "ALL" or integer `longUnits` parameter.

        `shortUnits` : str | int = "NONE"
            Indication of how much of the short Position to closeout. Either the
            string “ALL”, the string “NONE”, or a integer representing how many
            units of the short position to close using a PositionCloseout
            MarketOrder. The units specified must always be positive. If hedging 
            is permitted on the account, may send `longUnits` argument as well
            ("ALL" or integer), otherwise `longUnits` must remain "NONE" if passing
            "ALL" or integer `shortUnits` parameter.
        
            
        Returns
        -------
        `None`
        
        '''

        # set target
        target = "/positions/{}/close".format(instrument)
        
        # load payload
        data = {"longUnits" : longUnits,
                "shortUnits" : shortUnits}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()
        
        # Fully / partially close a position
        response, self.rcode = comms.put_request(self._base.rest_URL \
                                            + self._range \
                                            + target, 
                                            headers=self._base.headers,
                                            data=data)
        
        if (self.rcode == 200) or (self.rcode == 201):        

            # acquire lock to prevent order confirmation logging until messsage recorded
            self._orderLock.acquire()

            # set custom order confirmation code
            self.rcode = 888
            self.orderMessage = response            
            
            # allow confirmation message to be recorded
            self._orderLock.release()

        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

class Transactions():
    ''' Oanda transactions interface.

    Attributes
    ----------------
    `transactions` : None | dict = None
        List of transaction pages that satify a time-based transaction query.
        The "pages" returned are URLs hosted on Oanda's website, presumable to
        prevent excessive network traffic (each page can old up to 1000
        transactions). `None` by default until populated by
        `self.update_transactions()`.

    `specificTransaction` : None | dict = None
        Details of a single account transaction. `None` by default until 
        populated by `self.update_specific()`.

    `inRange` : None | dict = None
        Range of transactions for an account based on the transaction IDs.
        `None` by default until populated by `self.update_range()`.

    `sinceID` : None | dict = None
        Range of transactions for an account starting at (but not including) a
        provided transaction ID. `None` by default until populated by
        `self.update_since()`.

    `transactionStream` : list | = None
        A continuously updated stream of account transactions starting from when
        `self.start_stream()` is called (`None` until `self.start_stream()`
        is called). `list` if `self.start_stream(record=True)`, otherwise
        will be a single entry `list` of the most recent stream entry.

    `streamHeartbeat` : list | None = None
        Most recent stream heartbeat (if stream is running).

    `rcode` : int | None = None
        Most recent HTTPS request return code.

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received

            *Note* Dead stream errors will only contain "code" and "message"
            
    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_streamThread` : _StreamingThread | None = None
        Custom class object; Thread running streaming connection in background.

    `_streamArgs` : list
        The list of arguements used to start the stream (these will be used to
        restart the stream if it ever dies).
        
    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory

    Methods
    --------------
    `update_transactions()` : func
        Updates `self.transactions` attribute by filtering the given account's
        transaction history by timerange and page size.

    `update_specific()` : func
        Updates `self.specificTransaction` attribute by populating full
         details of a single transaction.

    `update_range()` : func
        Updates `idRange` attribute by filtering the given account's transaction
        history down to a specified range of transactions.

    `update_since()` : func
        Updates `self.sinceID` attribute by retrieving all transactions that
        are newer than a given transaction ID (non-inclusive, ie: returned
        values do not include the transaction ID provided).

    `start_stream()` : func
        Begins a stream to populate the `self.transaction_stream` attribute.
        `self.transaction_stream` will be continuously updated with any new
        transactions without user intervention (but may remain empty when first
        run - this just means there haven't been any new transactions since the
        stream began). Overwrites any previous content stored in
        `self.transaction_stream`.

    `stop_stream()` : func
        Stops `self.transaction_stream`'s managing thread (`self._streamThread`).
        Prevents any new updates to `self.transaction_stream`. Ensure any
        StreamMonitor() objects that are monitoring this stream are stopped
        prior to running `self.stop_stream()`, otherwise the monitor object
        will just immediately restart it.

    '''

    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Transactions object.

        Parameters
        ----------------
        `base` : BaseClient
            Custom class object; base configurations for current session.
            

        Returns
        -----------
        None

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()

        # set "Transactions" object range
        self._range = "/v3/accounts/{}/transactions".format(self._base.accountID)

        # placeholder for all attributes
        self.transactions = None
        self.specificTransaction = None
        self.inRange = None
        self.sinceID = None
        self.rcode = 200        # error monitor will ignore until actual comms start
        self.transactionStream = None
        self.streamHeartbeat = None
        self._streamThread = None
        self._streamArgs = None

        return None

    def update_transactions(self,
                            fromTime : datetime.datetime | str | None = None,
                            toTime : datetime.datetime | str | None = None,
                            pageSize : int | None = None,
                            transactionTypes : list[str] | None = None) -> None:
        ''' Updates `self.transactions` attribute by filtering the given account's
        transaction history by timerange and page size.
        
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
        # get filtered transactions
        target = ""
        params = {"from" : fromTime,
                  "to": toTime,
                  "pageSize" : pageSize,
                  "type" : transactionTypes}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)

        if (self.rcode == 200) or (self.rcode == 201):
            self.transactions = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_specific(self, transactionID : int | str) -> None:
        ''' Updates `self.specificTransaction` attribute by populating full
         details of a single transaction.
        
        Parameters
        ----------
        `transactionID` : int | str
            Transaction ID to get details on.
            
        Returns
        -------
        `None`
        
        '''

        # get specific transaction
        target = "/{}".format(transactionID)        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers)

        if (self.rcode == 200) or (self.rcode == 201):
            self.specificTransaction = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_range(self,
                     fromID : int | str,
                     toID : int | str,
                     transactionTypes : list[str] | None = None) -> None:
        ''' Updates `self.inRange` attribute by filtering the given account's
        transaction history down to a specified range of transactions.
        
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
        # get filtered transaction range
        target = "/idrange"
        params = {"from" : fromID,
                  "to": toID,
                  "type" : transactionTypes}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)

        if (self.rcode == 200) or (self.rcode == 201):
            self.inRange = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_since(self,
                     sinceID : int | str,
                     transactionTypes : list[str] | None = None) -> None:
        ''' Updates `self.sinceID` attribute by retrieving all transactions that
        are newer than a given transaction ID (non-inclusive, ie: returned
        values do not include the transaction ID provided).
        
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
        # get new transactions since the specific transaction
        target = "/sinceid"
        params = {"id" : sinceID,
                  "type" : transactionTypes}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)

        if (self.rcode == 200) or (self.rcode == 201):
            self.sinceID = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def start_stream(self, record : bool = False) -> None:
        ''' Begins a stream to populate the `self.transaction_stream` attribute.
        `self.transaction_stream` will be continuously updated with any new
        transactions without user intervention (but may remain empty when first
        run - this just means there haven't been any new transactions since the
        stream began). Overwrites any previous content stored in
        `self.transaction_stream`.
        
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

        # begin stream thread
        target = "/stream"
        newStreamNeeded = True

        # if no streams, start one
        if not self._streamThread:
            pass

        # if current stream running, don't allow new stream until stopped.
        # `if` statement above catches running this on potential `None` object
        elif self._streamThread.is_alive():
            
            # set arbitrary error code
            self.rcode = 999
            self.errorMessage = "A transactionStream is already active for this object. \
            Please stop the current stream with `self.stop_stream()` before \
            requesting a new stream."
            
            newStreamNeeded = False
            
        # start a new stream
        if newStreamNeeded:

            # store stream arguments
            self._streamArgs = [record]        
            
            # *note* pointing at stream_URL (most point at rest_URL)
            self._streamThread = comms.get_streamThread(self._base.stream_URL + \
                                                        self._range + target,
                                                        headers=self._base.headers,
                                                        record=record)

            # acquire lock to prevent logging until evaluation is complete
            self._errorLock.acquire()

            self.rcode = self._streamThread.status_code

            if (self.rcode == 200) or (self.rcode == 201):
                self._streamThread.start()
                
                # set heartbeat and transaction stream
                self.streamHeartbeat = self._streamThread.lastHeartbeat
                self.transactionStream = self._streamThread.content
            
            else:
                self.errorMessage = self._streamThread.errorMessage        
            
            # allow error logging as necessary
            self._errorLock.release()

        return None

    def stop_stream(self) -> None:
        ''' Stops `self.transaction_stream`'s managing thread 
        (`self._streamThread`). Prevents any new updates to 
        `self.transaction_stream` attribute. Ensure any
        StreamMonitor() objects that are monitoring this stream are stopped
        prior to running `self.stop_stream()`, otherwise the monitor object
        will just immediately restart it.
        
        Parameters
        ----------
        `None`

        
        Returns
        -------
        `None`
        
        '''

        # stop stream
        self._streamThread.stop()

        return None

class Pricing():
    ''' Oanda pricing interface.
    
    Attributes
    ----------
    `latestCandle` : dict | None = None
        Current incomplete candle ("Dancing Bears") AND most recent complete 
        candle within an Account for a specified combination of instrument(s), 
        granularity(s), and price component(s). `None` until `update_latest()` 
        is called.

    `candles` : dict | None = None
        Historic candlestick data for an instrument. `None` until 
        `update_candles()` is called.
        
    `pricing` : dict | None = None
        Pricing information for a specified list of instruments within an
        account. `None` until `self.update_pricing()` is called.
    
    `pricingStream` : list | None = None
        A continuously updated stream of Account Prices starting from when
        `self.start_stream()` is called (`None` until `self.start_stream()`
        is called). `list` if `self.start_stream(record=True)`, otherwise
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
    
    `rcode` : int | None = None
        Most recent HTTPS request return code. 

    `errorMessage` : dict | None
        Most recent client-server error (`None` until error occurs); may be 
        Oanda HTTPError messages OR  `requests` modeul exceptions (the API used 
        in all client-server communications throughout this module). Will NOT
        be overwritten if a succesful request is made susequently (ie. check
        self.rcode when troubleshooting)
            Keys:
            "url" : full url that the request was sent to
            "headers" : headers included in the request (Authorization token is 
                stripped for security, check independently if this is the 
                suspected issue)
            "parameters" : parameters included in the request
            "payload" : the request's json payload (`None` if "GET" request)
            "code" : status code (HTTP code or `999`)
            "message" : the error message received
        
            *Note* Dead stream errors will only contain "code" and "message"
            
    `streamHeartbeat` : list | None = None
        Most recent stream heartbeat (if stream is running).

    `_errorLock` : threading.Lock
        Return codes are set prior to error messages - this lock exists to 
        ensure both are properly updated before error monitoring thread
        evaluates them.

    `_streamTread` : _StreamingThread | None = None
        Custom class object; Thread running streaming connection in background.

    `_streamArgs` : list
        The list of arguements used to start the stream (these will be used to
        restart the stream if it ever dies).

    `_base` : BaseClient
        Base configurations shared throughout the session for communicating
        with Oanda server.
    
    `_range` : str
        Main file path on the server to send requests to. *Note* The final
        file/directory of a request is specified in a different local variable,
        `target`. Example:
            rest_URL = https://api-fxpractice.oanda.com\n
            range = /v3/accounts/123-123-12345678-123\n
            target = /someSubdirectory
    
    Methods
    -------
    `update_latest()` : func
        Updates `self.latest` attribute using provided argument filters.
    
    `update_candles()` : func
        Updates `self.candles` attribute using provided argument filters.
    
    `update_pricing()` : func
        Updates `self.pricing` attribute using provided argument filters.

    `copy_candles()` : func
        Returns copy of candles in `self.candles` as a `pandas.DataFrame`. No
        error checking is done prior to the copy / formatting - ensure 
        `self.candles` have  been successfully retrieved first by confirming 
        `self.rcode` == 200.
        
    `start_stream()` : func
        Begins a stream to populate the `self.pricingStream` attribute.
        `self.pricingStream` will be continuously updated with any new
        prices without user intervention (but may remain empty when
        first run - this just means there haven't been any new pricing updates
        since the stream began). Overwrites any previous content stored in
        `self.pricingStream`.
    
    `stop_stream()` : func
        Stops `self.pricingStream`'s managing thread (`self._streamThread`). 
        Prevents any new updates to `pricingStream` attribute. Ensure any
        StreamMonitor() objects that are monitoring this stream are stopped
        prior to running `self.stop_stream()`, otherwise the monitor object
        will just immediately restart it.
    
    '''

    def __init__(self, base : BaseClient) -> None:
        ''' Initializes Pricing object.

        Parameters
        ----------------
        `base` : BaseClient
            Custom class object; base configurations for current session.
            

        Returns
        -----------
        None

        '''

        # set base configs
        self._base = base.new()
        self.errorMessage = None
        self._errorLock = threading.Lock()

        # set "Pricing" object range
        self._range = "/v3/accounts/{}".format(self._base.accountID)

        # placeholder for all attributes
        self.latestCandle = None
        self.pricing = None
        self.latestCandle = None
        self.candles = None
        self.rcode = 200        # error monitor will ignore until actual comms start
        self.pricingStream = None
        self.streamHeartbeat = None
        self._streamThread = None
        self._streamArgs = None

        return None

    def update_latest(self, 
                      candleSpecifications : list[str],
                      units : int | str = 1,
                      smooth : bool = False,
                      dailyAlignment : int | str = 17,
                      alignmentTimezone : str = "America/New_York",
                      weeklyAlignment: str = "Friday") -> None:
        ''' Updates `self.latestCandle` attribute using provided argument filters.

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

        # get latest
        target = "/candles/latest"
        params = {"candleSpecifications" : candleSpecifications,
                  "units" : units,
                  "smooth" : smooth,
                  "dailyAlignment" : dailyAlignment,
                  "alignmentTimezone" : alignmentTimezone,
                  "weeklyAlignment" : weeklyAlignment}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.latestCandle = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def update_candles(self,
                       instrument : str,
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
                       ) -> None:
        ''' Updates `self.candles` attribute using provided argument filters.
        
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

        # get candles
        target = "/instruments/{}/candles".format(instrument)
        params = {"price" : price,
                  "granularity" : granularity,
                  "count" : count,
                  "from" :  fromTime,
                  "to" :  toTime,
                  "smooth" : smooth,
                  "includeFirst" : includeFirst,
                  "dailyAlignment" : dailyAlignment,
                  "alignmentTimezone" : alignmentTimezone,
                  "weeklyAlignment" : weeklyAlignment,
                  "units" : units}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)
        
        if (self.rcode == 200) or (self.rcode == 201):
            self.candles = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()
        
        return None

    def update_pricing(self,
                       instruments : list[str],
                       since : datetime.datetime | str | None = None,
                       includeHomeConversions : bool = True) -> None:
        ''' Updates `self.pricing` attribute using provided argument filters.
        
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

        # get pricing
        target = "/pricing"
        params = {"instruments" : instruments,
                  "since" : since,
                  "includeHomeConversions" : includeHomeConversions}        

        # acquire lock to prevent logging until evaluation is complete
        self._errorLock.acquire()

        response, self.rcode = comms.get_request(self._base.rest_URL \
                                                    + self._range \
                                                    + target,
                                                    headers=self._base.headers,
                                                    parameters=params)

        if (self.rcode == 200) or (self.rcode == 201):
            self.pricing = response
        else:
            self.errorMessage = response        
            
        # allow error logging as necessary
        self._errorLock.release()

        return None

    def copy_candles(self, spread : bool = False) -> pandas.DataFrame:
        '''
        
        Returns copy of candles in `self.candles` as a `pandas.DataFrame`. No
        error checking is done prior to the copy / formatting - ensure 
        `self.candles` have  been successfully retrieved first by confirming 
        `self.rcode` == 200. *Note*: "o", "h", "l", and  "c" will be appended 
        with a suffix to indicate quote type:

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

        # will contain mid / bid / ask / spread(s)
        mids = []
        bids = []
        asks = []
        spreads = []
        volumes = []

        # iterate over all retrieved candles
        for item in self.candles["candles"]:

            # temp candle - will be adding datetimes to various keys
            temp = copy.deepcopy(item)

            # attach datetime key to mid
            if "mid" in temp.keys():
                mid = temp["mid"]
                mid["datetime"] = temp["time"]
                mids.append(mid)

            # attach datetime key to bid
            if "bid" in temp.keys():
                bid = temp["bid"]
                bid["datetime"] = temp["time"]
                bids.append(bid)


            # attach datetime key to ask
            if "ask" in temp.keys():
                ask = temp["ask"]
                ask["datetime"] = temp["time"]
                asks.append(ask)


            # calculate spread + attach datetime key to spread
            if (spread) and ("bid" in temp.keys()) and ("ask" in temp.keys()):
                tempSpread =  {"o" :temp["bid"]["o"] - temp["ask"]["o"],
                               "h": temp["bid"]["h"] - temp["ask"]["h"],
                               "l": temp["bid"]["l"] - temp["ask"]["l"],
                               "c": temp["bid"]["c"] - temp["ask"]["c"],
                               "datetime" : temp["time"]}
                spreads.append(tempSpread)

            # build volume dictionary
            volume = {"volume" : temp["volume"], "datetime" : temp["time"]}
            volumes.append(volume)

        # will contain individual quotes
        quotes = []

        # build quote dataframes
        if mids:
            quotes.append(pandas.DataFrame(mids).set_index("datetime"))
        if bids:
            quotes.append(pandas.DataFrame(bids).set_index("datetime").add_suffix("_bid"))
        if asks:
            quotes.append(pandas.DataFrame(asks).set_index("datetime").add_suffix("_ask"))
        if spreads:
            quotes.append(pandas.DataFrame(spreads).set_index("datetime").add_suffix("_spread"))

        # build volumen dataframe
        quotes.append(pandas.DataFrame(volumes).set_index("datetime"))

        # join to one
        quotes = quotes[0].join(quotes[1:])

        return quotes

    def start_stream(self,
                     instruments : list[str],
                     snapshot : bool = True,
                     includeHomeConversions : bool = False,
                     record : bool = False) -> None:
        ''' Begins a stream to populate the `self.pricingStream` attribute.
        `self.pricingStream` will be continuously updated with any new
        prices without user intervention (but may remain empty when
        first run - this just means there haven't been any new pricing updates
        since the stream began). Overwrites any previous content stored in
        `self.pricingStream`.

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

        # set target
        target = "/pricing/stream"
        newStreamNeeded = True

        # if no threads, start one
        if not self._streamThread:
            pass

        # if current thread running, don't allow new thread until original stopped.
        # `if` statement above catches running this on potential `None` object
        elif self._streamThread.is_alive():
            
            # set arbitrary error code
            self.rcode = 999
            self.errorMessage = "A pricingStream thread is already running for \
            this object. Please stop the current thread with `self.stop_stream()`\
            before requesting a new streaming thread."
            
            newStreamNeeded = False
            
        # start a new stream
        if newStreamNeeded:

            # store stream args
            self._streamArgs = [instruments, snapshot, includeHomeConversions, record]
            
            # set parameters
            params = {"instruments" : instruments,
                    "snapshot" : snapshot,
                    "includeHomeConversions" : includeHomeConversions}
            
            # build stream thread
            # *note* pointing at stream_URL (most point at rest_URL)
            self._streamThread = comms.get_streamThread(self._base.stream_URL + \
                                                        self._range + target,
                                                        headers=self._base.headers,
                                                        parameters=params,
                                                        record=record)
                    

            # acquire lock to prevent logging until evaluation is complete
            self._errorLock.acquire()

            self.rcode = self._streamThread.status_code

            if (self.rcode == 200) or (self.rcode == 201):
                self._streamThread.start()
                
                # set heartbeat and transaction stream
                self.streamHeartbeat = self._streamThread.lastHeartbeat
                self.pricingStream = self._streamThread.content
            
            else:
                self.errorMessage = self._streamThread.errorMessage        
            
            # allow error logging as necessary
            self._errorLock.release()

        return None

    def stop_stream(self) -> None:
        ''' Stops `self.pricingStream`'s managing thread (`self._streamThread`). 
        Prevents any new updates to `pricingStream` attribute. Ensure any
        StreamMonitor() objects that are monitoring this stream are stopped
        prior to running `self.stop_stream()`, otherwise the monitor object
        will just immediately restart it.
        
        Parameters
        ----------
        `None`

        
        Returns
        -------
        `None`
        
        '''

        # stop stream
        self._streamThread.stop()

        return None

    