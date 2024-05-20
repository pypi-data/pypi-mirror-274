import datetime

''' ENTRY ORDERS'''
class _BaseEntry():
    ''' Base entry order specifications. All entry orders extend this class.
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given entry order.

    Methods
    -------
    `set_takeProfit()` : func
        Creates and sets entry order's TakeProfit dependent order.
    
    `set_stopLoss()` : func
        Creates and sets entry order's StopLoss dependent order.
    
    `set_trailingStop()` : func
        Creates and sets entry order's TrailingStopLoss dependent order.
    
    `set_guaranteedStop()` : func
        Creates and sets entry order's GuarnateedStopLoss dependent order.
    
    `get_payload()` : func
        Returns entry order's payload.

    '''

    def __init__(self) -> None:
        ''' Initializes BaseOrder object. 

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''

        # shared order specifications
        self.payload = {"type" : None,
                        "instrument" : None,
                        "units" : None,
                        "timeInForce" : None,
                        "positionFill" : None}

        return None
    
    def set_takeProfit(self,
                       price : float | None = None,
                       distance : float | None = None,
                       timeInForce : str = "GTC",
                       gtdTime : datetime.datetime | str | None = None) -> None:
        ''' Creates and sets entry order's TakeProfit dependent order.

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
        
        # create dependent field
        self.payload["takeProfitOnFill"] = {}

        # set required specifications
        if price:
            self.payload["takeProfitOnFill"]["price"] = price
        else:
            self.payload["takeProfitOnFill"]["distance"] = distance
        
        self.payload["takeProfitOnFill"]["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["takeProfitOnFill"]["gtdTime"] = gtdTime

        return None
    
    def set_stopLoss(self,
                     price : float | None = None,
                     distance : float | None = None,
                     timeInForce : str = "GTC",
                     gtdTime : datetime.datetime | str | None = None) -> None:
        ''' Creates and sets entry order's StopLoss dependent order.

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
        
        # create dependent field
        self.payload["stopLossOnFill"] = {}

        # set required specifications
        if price:
            self.payload["stopLossOnFill"]["price"] = price
        else:
            self.payload["stopLossOnFill"]["distance"] = distance
        
        self.payload["stopLossOnFill"]["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["stopLossOnFill"]["gtdTime"] = gtdTime

        return None
    
    def set_trailingStop(self,
                         distance : float,
                         timeInForce : str = "GTC",
                         gtdTime : datetime.datetime | str | None = None) -> None:
        ''' Creates and sets entry order's TrailingStopLoss dependent order.

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

        # create dependent field
        self.payload["trailingStopLossOnFill"] = {}

        # set required specifications
        self.payload["trailingStopLossOnFill"]["distance"] = distance

        self.payload["trailingStopLossOnFill"]["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["trailingStopLossOnFill"]["gtdTime"] = gtdTime

        return None
    
    def set_guaranteedStop(self,
                           price : float | None = None,
                           distance : float | None = None,
                           timeInForce : str = "GTC",
                           gtdTime : datetime.datetime | str | None = None) -> None:
        ''' Creates and sets entry order's GuarnateedStopLoss dependent order.

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
        
        # create dependent field
        self.payload["guaranteedStopLossOnFill"] = {}

        # set required specifications
        if price:
            self.payload["guaranteedStopLossOnFill"]["price"] = price
        else:
            self.payload["guaranteedStopLossOnFill"]["distance"] = distance
        
        self.payload["guaranteedStopLossOnFill"]["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["guaranteedStopLossOnFill"]["gtdTime"] = gtdTime

        return None

    def get_payload(self):
        ''' Returns entry order's payload.
        
        Parameters
        ----------
        None

        Returns
        -------
        dict
            The Oanda formatted entry order's specifications.
        
        '''

        return self.payload

class MarketOrder(_BaseEntry):
    ''' Market order specifications.
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given market order.

    Methods
    -------
    `set()` : func
        Sets required Market Order specifications. 

    '''

    def __init__(self) -> None:
        ''' Initializes MarketOrder object. 

        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''

        _BaseEntry.__init__(self)

        # set Market Order type
        self.payload["type"] = "MARKET"

        return None

    def set(self,
                  instrument : str,
                  units : int,
                  priceBounds : float | None = None,
                  timeInForce : str = "FOK",
                  positionFill : str = "DEFAULT") -> None:
        ''' Sets required Market Order specifications. 
        
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

        
        # set required specifications
        self.payload["instrument"] = instrument
        self.payload["units"] = units
        self.payload["timeInForce"] = timeInForce
        self.payload["positionFill"] = positionFill
        
        # set optional specifications
        if priceBounds:
            self.payload["priceBounds"] = priceBounds

        return None
    
class LimitOrder(_BaseEntry):
    ''' Limit order specifications. *Note* A general note on LimitOrders:

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
        
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given limit order.

    Methods
    -------
    `set()` : func
        Sets required Limit Order specifications. 

    '''

    def __init__(self) -> None:
        ''' Initializes LimitOrder object. 

        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''

        _BaseEntry.__init__(self)

        # set Market Order type
        self.payload["type"] = "LIMIT"

        return None

    def set(self,
                  instrument : str,
                  units : int,
                  price : float,
                  timeInForce : str = "GTC",
                  gtdTime : datetime.datetime | str | None = None,
                  positionFill : str = "DEFAULT",
                  triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required Limit Order specifications. 

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

        
        # set required specifications
        self.payload["instrument"] = instrument
        self.payload["units"] = units
        self.payload["price"] = price
        self.payload["timeInForce"] = timeInForce
        
        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["positionFill"] = positionFill
        self.payload["triggerCondition"] = triggerCondition

        return None

class StopOrder(_BaseEntry):
    ''' Stop order specifications. *Note* A general note on StopOrders:

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
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given stop order.

    Methods
    -------
    `set()` : func
        Sets required Stop Order specifications. 

    '''

    def __init__(self) -> None:
        ''' Initializes StopOrder object. 

        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''

        _BaseEntry.__init__(self)

        # set Market Order type
        self.payload["type"] = "STOP"

        return None

    def set(self,
                  instrument : str,
                  units : int,
                  price : float,
                  priceBound : float | None = None,
                  timeInForce : str = "GTC",
                  gtdTime : datetime.datetime | str | None = None,
                  positionFill : str = "DEFAULT",
                  triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required Stop Order specifications. 
        
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

        
        # set required specifications
        self.payload["instrument"] = instrument
        self.payload["units"] = units
        self.payload["price"] = price
        self.payload["timeInForce"] = timeInForce
        
        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["positionFill"] = positionFill
        self.payload["triggerCondition"] = triggerCondition

        # set optional specifications
        if priceBound:
            self.payload["priceBound"] = priceBound

        return None

class MarketIfTouchedOrder(_BaseEntry):
    ''' MarketIfTouched order specifications. *Note* A general note on 
    MarketIfTouchedOrders:

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
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given market-if-touched order.

    Methods
    -------
    `set()` : func
        Sets required MarketIfTouched Order specifications. 

    '''

    def __init__(self) -> None:
        ''' Initializes MarketIfTouchedOrder object. 

        Parameters
        ----------
        None
        
        Returns
        -------
        `None`
        
        '''

        _BaseEntry.__init__(self)

        # set Market Order type
        self.payload["type"] = "MARKET_IF_TOUCHED"

        return None

    def set(self,
                  instrument : str,
                  units : int,
                  price : float,
                  priceBound : float | None = None,
                  timeInForce : str = "GTC",
                  gtdTime : datetime.datetime | str | None = None,
                  positionFill : str = "DEFAULT",
                  triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required MarketIfTouched Order specifications. 
        
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

        
        # set required specifications
        self.payload["instrument"] = instrument
        self.payload["units"] = units
        self.payload["price"] = price
        self.payload["timeInForce"] = timeInForce
        
        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["positionFill"] = positionFill
        self.payload["triggerCondition"] = triggerCondition

        # set optional specifications
        if priceBound:
            self.payload["priceBound"] = priceBound

        return None

''' DEPENDENT ORDERS '''
class _BaseDependent():
    ''' Base dependent order specifications. All dependent orders extend this 
    class.
    
    Attributes
    ----------
    `payload` : dict
        Specifications of the given dependent order.

    Methods
    -------
    `get_payload()` : func
        Returns dependent order's payload.

    '''

    def __init__(self) -> None:
        ''' Initializes BaseDependent object. 

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''

        # shared dependent specifications
        self.payload = {"type" : None,
                        "tradeID" : None,
                        "timeInForce" : None,
                        "triggerCondition": None}

        return None

    def get_payload(self):
        ''' Returns dependent order's payload.
        
        Parameters
        ----------
        None

        Returns
        -------
        dict
            The Oanda formatted dependent order's specifications.
        
        '''

        return self.payload

class TakeProfitOrder(_BaseDependent):
    ''' TakeProfit Order specifications.

    Attributes
    ----------
    `payload` : dict
        Specifications of the given TakeProfit order.

    Methods
    -------
    `set()` : func
        Sets required TakeProfit order specifications. 

    '''

    def __init__(self) -> None:
        ''' Instantiates TakeProfitOrder object.

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''

        # inherit base class
        _BaseDependent.__init__(self)

        # set payload type
        self.payload["type"] = "TAKE_PROFIT"

        return None

    def set(self,
                   tradeID : int,
                   price : float | None = None,
                   distance : float | None = None,
                   timeInForce : str = "GTC",
                   gtdTime : datetime.datetime | str | None = None,
                   triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required TakeProfit Order requirements.
        
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

        # set required specifications
        self.payload["tradeID"] = tradeID
        
        if price:
            self.payload["price"] = price
        else:
            self.payload["distance"] = distance
        
        self.payload["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["triggerCondition"] = triggerCondition

        return None

class StopLossOrder(_BaseDependent):
    ''' StopLoss Order specifications.

    Attributes
    ----------
    `payload` : dict
        Specifications of the given StopLoss order.

    Methods
    -------
    `set()` : func
        Sets required StopLoss order specifications. 

    '''

    def __init__(self) -> None:
        ''' Instantiates StopLossOrder object.

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''
        # inherit base class
        _BaseDependent.__init__(self)

        # set payload type
        self.payload["type"] = "STOP_LOSS"

        return None

    def set(self,
                   tradeID : int,
                   price : float | None = None,
                   distance : float | None = None,
                   timeInForce : str = "GTC",
                   gtdTime : datetime.datetime | str | None = None,
                   triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required StopLoss Order requirements.
        
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

        # set required specifications
        self.payload["tradeID"] = tradeID
        
        if price:
            self.payload["price"] = price
        else:
            self.payload["distance"] = distance
        
        self.payload["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["triggerCondition"] = triggerCondition

        return None

class GuaranteedStopLossOrder(_BaseDependent):
    ''' GuaranteedStopLoss Order specifications.

    Attributes
    ----------
    `payload` : dict
        Specifications of the given GuaranteedStopLoss order.

    Methods
    -------
    `set()` : func
        Sets required GuaranteedStopLoss order specifications. 

    '''

    def __init__(self) -> None:
        ''' Instantiates GuaranteedStopLossOrder object.

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''

        # inherit base class
        _BaseDependent.__init__(self)

        # set payload type
        self.payload["type"] = "GUARANTEED_STOP_LOSS"

        return None

    def set(self,
                   tradeID : int,
                   price : float | None = None,
                   distance : float | None = None,
                   timeInForce : str = "GTC",
                   gtdTime : datetime.datetime | str | None = None,
                   triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required GuaranteedStopLoss Order requirements.
        
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

        # set required specifications
        self.payload["tradeID"] = tradeID
        
        if price:
            self.payload["price"] = price
        else:
            self.payload["distance"] = distance
        
        self.payload["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["triggerCondition"] = triggerCondition

        return None

class TrailingStopLossOrder(_BaseDependent):
    ''' TrailingStopLoss Order specifications.

    Attributes
    ----------
    `payload` : dict
        Specifications of the given TrailingStopLoss order.

    Methods
    -------
    `set()` : func
        Sets required TrailingStopLoss order specifications. 

    '''

    def __init__(self) -> None:
        ''' Instantiates TrailingStopLossOrder object.

        Parameters
        ----------
        None

        Returns
        -------
        `None`
        
        '''
        
        # inherit base class
        _BaseDependent.__init__(self)

        # set payload type
        self.payload["type"] = "TRAILING_STOP_LOSS"

        return None

    def set(self,
                   tradeID : int,
                   distance : float,
                   timeInForce : str = "GTC",
                   gtdTime : datetime.datetime | str | None = None,
                   triggerCondition : str = "DEFAULT") -> None:
        ''' Sets required TrailingStopLoss Order requirements.
        
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

        # set required specifications
        self.payload["tradeID"] = tradeID
        
        self.payload["distance"] = distance
        
        self.payload["timeInForce"] = timeInForce

        if (timeInForce == "GTD") and (gtdTime):
            self.payload["gtdTime"] = gtdTime

        self.payload["triggerCondition"] = triggerCondition

        return None

