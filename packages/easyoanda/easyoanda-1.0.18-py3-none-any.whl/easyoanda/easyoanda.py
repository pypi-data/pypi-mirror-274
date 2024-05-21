from .modules import session
from .modules import monitor
from .modules.prebuild import MarketOrder, LimitOrder, StopOrder, \
                             MarketIfTouchedOrder, TakeProfitOrder, \
                             StopLossOrder, GuaranteedStopLossOrder, \
                             TrailingStopLossOrder


class OandaSession():
    ''' Wrapper class for all sub-session and monitor classes - used to create a 
    single object ("session") with access to all Oanda endpoints / sub-API calls.
    
    Attributes
    ----------
    `account` : modules.session.Account()
        Oanda account API:
        https://developer.oanda.com/rest-live-v20/account-ep/

    `instruments` : modules.session.Instruments()
        Oanda instrument API:
        https://developer.oanda.com/rest-live-v20/instrument-ep/
    
    `orders` : modules.session.Orders()
        Oanda orders API:
        https://developer.oanda.com/rest-live-v20/order-ep/
    
    `trades` : modules.session.Trades()
        Oanda trades API:
        https://developer.oanda.com/rest-live-v20/trade-ep/
    
    `positions` : modules.session.Positions()
        Oanda positions API:
        https://developer.oanda.com/rest-live-v20/position-ep/
    
    `transactions` : modules.session.Transactions()
        Oanda transactions API:
        https://developer.oanda.com/rest-live-v20/transaction-ep/
    
    `pricing` : modules.session.Pricing()
        Oanda pricing API:
        https://developer.oanda.com/rest-live-v20/pricing-ep/
    
    `errorMonitor` : modules.monitor.ErrorMonitor()
        Monitors Oanda interfaces for client-server errors.
    
    `streamMonitor` : modules.monitor.StreamMonitor()
        Monitors Oanda interface streams for connection interuptions, setting 
        stream alert error messages and restarting streams as needed.
    
    `orderMonitor` : modules.monitor.OrderMonitor()
        Monitors Oanda interfaces for successful order confirmations.
    

    Methods
    -------
    None
    
    '''

    def __init__(self,
                 sessionType : str,
                 accountID : str,
                 token : str,
                 errorLog : str,
                 errorPrint : bool,
                 orderLog : str,
                 orderPrint : bool,
                 streamBeats : int,
                 streamRetries : int,
                 streamReset : int
                 ) -> None:
        ''' Initializes OandaSession object. 
        
        Parameters
        ----------
        `sessionType` : str
            Determines which oanda servers to send all subsequent communication
            to:
                "paper" = Paper account\n
                "live" = Live account

        `accountID` : str
            Unique Account ID for the account to trade with (identify
            within Oanda portal).
        
        `token` : str
            Unique token generated for Oanda account. *Note* All "live" accounts
            share the same token, but "paper" accounts have their own unique
            token - make sure you're providing the correct one for the 
            `sessionType` started.
        
        `errorLog` : str | None
            (Optional) Full path to log file on disk for recording errors. If
            provided, will attempt to load any pre-existing logs to memory
            before error logging begins.
        
        `errorPrint` : bool
            Whether to print errors to stdout.
        
        `orderLog` : str | None
            (Optional) Full path to log file on disk for recording confirmations. 
            If provided, will attempt to load any pre-existing logs to memory
            before confirmation logging begins.
        
        `orderPrint` : bool
            Whether to print order confirmations to stdout.
        
        `streamBeats` : int
            Number of seconds between heartbeats before a stream is considered dead.
        
        `streamRetries` : int
            Number of times to attempt to restart a dead stream.
        
        `streamReset` : int
            Number of minutes before resetting `streamRetries` counters back to zero for each endpoint.

        Returns
        -------
        `None`

        '''

        # initialize base configuration class
        self._base = session.BaseClient(sessionType=sessionType,
                                               accountID=accountID,
                                               token=token)

        # initialize all session classes
        self.account = session.Account(self._base)
        self.instruments = session.Instruments(self._base)
        self.orders = session.Orders(self._base)
        self.trades = session.Trades(self._base)
        self.positions = session.Positions(self._base)
        self.transactions = session.Transactions(self._base)
        self.pricing = session.Pricing(self._base)

        # initialize error monitoring
        self.errorMonitor = monitor.ErrorMonitor(endpoints=
                                                        [self.account, 
                                                         self.instruments, 
                                                         self.orders,                                                     
                                                         self.trades, 
                                                         self.positions, 
                                                         self.transactions,
                                                         self.pricing],
                                                         printErrors=errorPrint,
                                                         logPath=errorLog)
        self.errorMonitor.start()

        # initialize stream monitoring
        self.streamMonitor = monitor.StreamMonitor(endpoints=
                                                          [self.pricing, 
                                                           self.transactions],
                                                           deadOnArrival=streamBeats,
                                                           doNotResusitate=streamRetries,
                                                           resetTime=streamReset)
        self.streamMonitor.start()

        # initialize order monitoring
        self.orderMonitor = monitor.OrderMonitor(endpoints=
                                                        [self.orders,                                                     
                                                         self.trades, 
                                                         self.positions],
                                                         printConfirmations=orderPrint,
                                                         logPath=orderLog)
        self.orderMonitor.start()


        return None

    def quit(self) -> None:
        '''
        
        Gracefully stops the given session's sub-threads (monitors and streams),
        allowing the parent program to cleanly exit.
        

        Parameters
        ----------
        None

        Returns
        -------
        `None`

        '''

        # prevent streams from re-starting
        self.streamMonitor.doNotResusitate = 0

        # stop streams if started and still running
        if self.pricing._streamThread:
            if self.pricing._streamThread.is_alive():
                self.pricing.stop_stream()
        
        if self.transactions._streamThread:
            if self.transactions._streamThread.is_alive():
                self.transactions.stop_stream()
        
        # stop monitors
        self.streamMonitor.stop()
        self.errorMonitor.stop()
        self.orderMonitor.stop()

        return None

def start_session(sessionType : str,
                  accountID : str,
                  token : str,
                  errorLog : str | None = None,
                  errorPrint : bool = False,
                  orderLog : str | None = None,
                  orderPrint : bool = False,
                  streamBeats : int = 10,
                  streamRetries : int = 3,
                  streamReset : int = 60
                  ) -> None:
    '''  Instantiates an OandaSession object with API access to Oanda trading 
    endpoints.
    
    Parameters
    ----------
    `sessionType` : str
        Determines which oanda servers to send all subsequent communication
        to:
            sessionType="paper" : Paper account\n
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
    
    # start Oanda session
    session = OandaSession(sessionType,
                            accountID,
                            token,
                            errorLog,
                            errorPrint,
                            orderLog,
                            orderPrint,
                            streamBeats,
                            streamRetries,
                            streamReset)

    return session

def to_baseUnits(currentQuotes : dict,
                 homeUnits : float,
                 truncate : bool = False) -> float | int:
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
    
    # pull conversion factor
    baseConversion = currentQuotes["homeConversions"][0]["positionValue"]

    # converting for an order
    if truncate:

        # units to buy / sell
        if homeUnits > 0:
            
            # floor if positive
            baseUnits = homeUnits // baseConversion

        else:

            # ceiling if negative
            baseUnits = -(-homeUnits // baseConversion)

        baseUnits = int(baseUnits)

    # else general conversion
    else:
        baseUnits = homeUnits / baseConversion

    return baseUnits

def to_homeUnits(currentQuotes : dict,
                 baseUnits : float | int) -> float:
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

    # pull base conversion
    baseConversion = currentQuotes["homeConversions"][0]["positionValue"]

    # convert to home units
    homeUnits = baseUnits * baseConversion

    return homeUnits

def find_optimal_stop(currentQuotes : dict,
                      baseUnits : int,
                      maxLoss : float,
                      entryPrice : float | None = None) -> None:
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

    # pull quote conversion factor
    quoteConversion = currentQuotes["homeConversions"][1]["positionValue"]

    # per unit impact
    perUnitImpact = abs(baseUnits) * quoteConversion

    # distance = maxLoss / perUnitImpact
    distance = abs(maxLoss) / perUnitImpact

    # projected price already present
    if entryPrice:
        pass

    # or using current quotes
    else:
        # going long - setting price to most recent ask
        if baseUnits > 0:
            entryPrice = currentQuotes["prices"][0]["closeoutAsk"]

        # or going short - setting price to most recent bid
        else:
            entryPrice = currentQuotes["prices"][0]["closeoutBid"]


    # calculate stop for long
    if baseUnits > 0:
        stopLossAt = entryPrice - distance

        # round up to .0000X
        tempStopAt = stopLossAt * 100000
        tempStopAt = -(-tempStopAt // 1)
        stopLossAt = tempStopAt / 100000
    
    # calculate stop for short
    else:
        stopLossAt = entryPrice + distance

        # round down to .0000X
        tempStopAt = stopLossAt * 100000
        tempStopAt = tempStopAt // 1
        stopLossAt = tempStopAt / 100000


    return stopLossAt

def find_optimal_size(currentQuotes : dict,
                      maxLoss : float,
                      exitPrice : float,
                      entryPrice : float | None = None) -> None:

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

    # pull quote conversion factor
    quoteConversion = currentQuotes["homeConversions"][1]["positionValue"]

    # get entry price
    if entryPrice:
        pass
    else:
        
        # benchmark to determine if long or short
        benchmark = (currentQuotes["prices"][0]["closeoutAsk"]                 \
                   + currentQuotes["prices"][0]["closeoutBid"]) / 2


        # going short - setting price to most recent bid
        if exitPrice > benchmark:
            entryPrice = currentQuotes["prices"][0]["closeoutBid"]

        # or going long - setting price to most recent ask
        else:
            entryPrice = currentQuotes["prices"][0]["closeoutAsk"]


    # calculate distance betwen entry and exit loss
    distance = entryPrice - exitPrice

    # calculate target loss perUnitImpact
    lossPerUnitImpact = abs(maxLoss) / distance

    # if long
    if lossPerUnitImpact > 0:
        
        # floor if positive
        baseUnits = lossPerUnitImpact // quoteConversion

    else:

        # short - ceiling negative
        baseUnits = -(-lossPerUnitImpact // quoteConversion)

    return baseUnits

def get_pip_impact(currentQuotes : dict,
                   baseUnits : float) -> None:
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

    # pull quote conversion factor
    quoteConversion = currentQuotes["homeConversions"][1]["positionValue"]

    # calculating pip impact
    quotedUnits = baseUnits * quoteConversion

    # special pip adjustment if quoted in "JPY" or "HUF"
    if (currentQuotes["homeConversions"][1]["currency"] == "JPY") \
        or (currentQuotes["homeConversions"][1]["currency"] == "HUF"):
        perPipImpact = quotedUnits / 100

    # otherwise, standard pip adjustment
    else:
        perPipImpact = quotedUnits / 10000

    return abs(perPipImpact)

def get_price_impact(currentQuotes : dict,
                      baseUnits : float,
                      exitPrice : float,
                      entryPrice : float | None = None) -> None:

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
            
    `exitPrice` : float
        The instrument's ending price level.

    `entryPrice` : float | None = None
        The instrument's starting price level. If `None`, will assume entry
        price level is based on current bid/ask quotes (evaluated by sign of 
        `baseUnits`). [default=None]

    Returns
    -------
    float
        The price impact of changes between the two price levels (as measured
        in the account's home currency).

    '''


    # calculate pip impact
    pipImpact = get_pip_impact(currentQuotes, baseUnits)

    # went long - entered at the ask
    if baseUnits > 0:

        # set entry level as needed
        if entryPrice:
            pass
        else:
            entryPrice = currentQuotes["prices"][0]["closeoutAsk"]

        # calculate long distance
        distance = exitPrice - entryPrice
        
    # went short - entered at the bid
    else:

        # set entry level as needed
        if entryPrice:
            pass

        else:
            entryPrice = currentQuotes["prices"][0]["closeoutBid"]

        # calculate short distance
        distance = entryPrice - exitPrice

    # calculate pips in distance if "JPY" or "HUF"
    if (currentQuotes["homeConversions"][1]["currency"] == "JPY") \
        or (currentQuotes["homeConversions"][1]["currency"] == "HUF"):
        pips = distance * 100

    # otherwise, calculate standard pips
    else:
        pips = distance * 10000

    # calculate total position impact
    positionImpact = pipImpact * pips

    return positionImpact















