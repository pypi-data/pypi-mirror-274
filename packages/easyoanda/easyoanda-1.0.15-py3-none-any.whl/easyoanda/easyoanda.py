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

def calc_units(currentQuotes : dict,
               homeTradeSize : float) -> int:
    '''
    
    Convert a trade size quoted in your account's home currency to an 
    equivalent trade size in a target instrument's units. *Note* OANDA 
    orders are placed using the target instrument's units - these units must 
    be INTEGERS! If the equivalent trade size units contain decimals, the units
    will be "floored" to the nearest integer (decimals will be dropped). Your
    resulting positions will always be SLIGHTLY smaller than your requested size
    to comply with OANDA specifications - the true size of your position can be 
    verified with `easyoanda.calc_home()`.


    Parameters
    ----------
    `currentQuotes` : dict
        The current pricing details of the trade's target instrument - this 
        will be `currentQuotes=session.pricing.pricing`. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.
    
    `homeTradeSize` : float
        Your preferred trade size, quoted in your account's home currency. 
        Positive units indicate long position, negative units indicate short
        position.

    Returns
    -------
    int
        The equivalent trade size in the target instrument's units.
    
    
    '''
    
    # pull conversion factor
    baseConversion = currentQuotes["homeConversions"][0]["positionValue"]
    
    # units to buy / sell
    if homeTradeSize > 0:
        
        # floor if positive
        units = homeTradeSize // baseConversion

    else:

        # ceiling if negative
        units = -(-homeTradeSize // baseConversion)

    return int(units)

def calc_home(currentQuotes : dict,
              targetTradeSize : int) -> int:
    '''
    
    Convert a trade size quoted in a target instrument's units to the 
    equivalent trade size in your home currency. *Note* When entering
    trades, OANDA requires position units to be integers - when sizing
    positions with `easyoanda.calc_size()`, returned sizes are "floored" to
    truncate decimals and will be SLIGHTLY smaller than your requested position 
    size - this is done to comply with OANDA's specifications. Use this function 
    to view any slight differences.


    Parameters
    ----------
    `currentQuotes` : dict
        The current pricing details of the trade's target instrument - this 
        will be `currentQuotes=session.pricing.pricing`. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.
    
    `targetTradeSize` : float
        The trade size, quoted in the target instrument's units. 
        Positive units indicate a long position, negative units indicate 
        a short position.

    Returns
    -------
    float
        The equivalent size of the trade in your home currency.
    
    
    '''

    # pull base conversion
    baseConversion = currentQuotes["homeConversions"][0]["positionValue"]

    # convert trade size
    homeTradeSieze = targetTradeSize * baseConversion

    return homeTradeSieze

def calc_stop_level(currentQuotes : dict,
                    targetTradeSize : int,
                    maxLoss : float | None = None,
                    entryPrice : float | None = None) -> None:
    '''
    
    Calculates the optimal stop-loss price of a target instrument, given
    a trade's size, quoted in the target instrumet's units, and maximum loss 
    threshold, quoted in your account's home currency.

    
    Parameters
    ----------
    `currentQuotes` : dict
        This will be: `currentQuotes = session.pricing.pricing` for 
        the trade's target instrument pricing data. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.

    `targetTradeSize` : int
        The position size of the trade, quoted in the target instrument's units.
        Positive units indicate a long position, negative units indicate a
        short position. *Note* Reminder: OANDA trade units must be INTEGERS.

    `maxLoss` : float | None = None
        The maximum allowable loss a trader is willing to take on the position,
        quoted in your account's home currency.
    
    `entryPrice` : float | None = None
        The trade's projected entry price. If `None`, will assume trade is 
        a market order and will use most recently quoted bid / ask provided
        within `currentQuotes` (depending on sign of tradeUnits). [default=None]

    Returns
    -------
    float
        The optimal stop-loss price, quoted in the target instrument's units.

    '''

    # pull quote conversion factor
    quoteConversion = currentQuotes["homeConversions"][1]["positionValue"]

    # per unit impact
    perUnitImpact = abs(targetTradeSize) * quoteConversion

    # distance = maxLoss / perUnitImpact
    distance = maxLoss / perUnitImpact

    # projected price already present
    if entryPrice:
        pass

    # or using current quotes
    else:
        # going long - setting price to most recent ask
        if targetTradeSize > 0:
            entryPrice = currentQuotes["prices"][0]["closeoutAsk"]

        # or going short - setting price to most recent bid
        else:
            entryPrice = currentQuotes["prices"][0]["closeoutBid"]


    # calculate stop for long
    if targetTradeSize > 0:
        stopLossAt = entryPrice - distance

        # round up to .0000X
        tempStopAt = stopLossAt * 100000
        stopLossAt = -(-tempStopAt // 1)
        stopLossAt = tempStopAt / 100000
    
    # calculate stop for short
    else:
        stopLossAt = entryPrice + distance

        # round down to .0000X
        tempStopAt = stopLossAt * 100000
        tempStopAt = tempStopAt // 1
        stopLossAt = tempStopAt / 100000


    return stopLossAt

def calc_trade_size(currentQuotes : dict,
                    exitPrice : float,
                    maxLoss : float,
                    entryPrice : float | None = None) -> None:

    '''

    Calculate the optimal trade size in a target instrument's units, given
    a target maximum loss price (stop loss price), quoted in the target 
    instrument's units, and a maximum loss threshold, quoted in the account's 
    home currency.*Note* OANDA orders are placed using the target instrument's 
    units - these units must be INTEGERS! If the equivalent trade size units 
    contain decimals, the units will be "floored" to the nearest integer 
    (decimals will be dropped). Your resulting positions will always be SLIGHTLY 
    smaller than your requested size to comply with OANDA specifications - the 
    true size of your position can be verified with `easyoanda.calc_home()`.


    Parameters
    ----------
    `currentQuotes` : dict
        This will be: `currentQuotes = session.pricing.pricing` for 
        the trade's target instrument pricing data. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.

    `exitPrice` : float
        The trade's target stop loss level.

    `maxLoss` : float | None = None
        The maximum allowable loss a trader is willing to take on the position,
        quoted in their home currency.
    
    `entryPrice` : float | None = None
        The trade's projected entry price. If `None`, will assume the trade is 
        a market order and will use the most recently quoted bid / ask provided
        within `currentQuotes`. The average of the bid-ask is used as a 
        benchmark to evaluate the `exitPrice` against to determine if the
        position is long  or short, but the specific bid or ask will be used 
        for sizing calculations afterwards. If your market order stops are 
        extremely close to the bid/ask (anything less than half the spread), 
        it may be worthwhile to enter this parameter manually. [default=None]

    
    Returns
    -------
    int
        The optimal trade size in the target instrument's units.

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
    lossPerUnitImpact = maxLoss / distance

    # if long
    if lossPerUnitImpact > 0:
        
        # floor if positive
        targetTradeUnits = lossPerUnitImpact // quoteConversion

    else:

        # short - ceiling negative
        targetTradeUnits = -(-lossPerUnitImpact // quoteConversion)

    return targetTradeUnits

def calc_pip_impact(currentQuotes : dict,
                    targetTradeSize : float) -> None:
    '''
    
    Calculate the impact a single pip change has your position, quoted in your
    account's home currency - keep in mind a single pip for instruments quoted 
    in "JPY" or "HUF" is .01, whereas a pip in all other quotes are .0001.

    
    Parameters
    ----------
    `currentQuotes` : dict
        The current pricing details of the trade's target instrument - this 
        will be `currentQuotes=session.pricing.pricing`. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.
    
    `targetTradeSize` : float
        Your trade size, quoted in the target instrument's units.

    Returns
    -------
    float
        The the impact a single pip change has on your position, quoted in
        your account's home currency.
    
    '''

    # pull quote conversion factor
    quoteConversion = currentQuotes["homeConversions"][1]["positionValue"]

    # calculating pip impact
    quotedUnits = targetTradeSize * quoteConversion

    # special pip adjustment if quoted in "JPY" or "HUF"
    if (currentQuotes["homeConversions"][1]["currency"] == "JPY") \
        or (currentQuotes["homeConversions"][1]["currency"] == "HUF"):
        perPipImpact = quotedUnits / 100

    # otherwise, standard pip adjustment
    else:
        perPipImpact = quotedUnits / 10000

    return abs(perPipImpact)

def calc_price_impact(currentQuotes : dict,
                      targetTradeSize : dict,
                      exitPrice : float,
                      entryPrice : float) -> None:

    '''
    
    Calculate the impact that movements between a target instrument's prices
    have on a trade's positional value, quoted in the account's home currency.
    
    
    Parameters
    ----------
    `currentQuotes` : dict
        This will be: `currentQuotes = session.pricing.pricing` for 
        the trade's target instrument pricing data. Pricing data
        must include home conversion factors - see 
        help(session.pricing.update_pricing) for details, if necessary.

    `targetTradeSize` : int
        The position size of the trade, quoted in the target instrument's units.
        Positive units indicate a long position, negative units indicate a
        short position. *Note* Reminder: OANDA trade units must be INTEGERS.

    `exitPrice` : float
        The trade's target exit level.

    `entryPrice` : float | None = None
        The trade's projected entry price. If `None`, will assume trade is 
        a market order and will use most recently quoted bid / ask provided
        within `currentQuotes` (depending on sign of tradeUnits). [default=None]


    Returns
    -------
    float
        The potential positional change of a trade's value, quoted in the
        account's home currency.

    '''


    # calculate pip impact
    pipImpact = calc_pip_impact(currentQuotes, targetTradeSize)

    # went long - entered at the ask
    if targetTradeSize > 0:

        # set entry price as needed
        if entryPrice:
            pass
        else:
            entryPrice = currentQuotes["prices"][0]["closeoutAsk"]

        # calculate long distance
        distance = exitPrice - entryPrice
        
    # went short - entered at the bid
    else:

        # set entry price as needed
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















