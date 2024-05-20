import os
import threading
import datetime
import time
import json
import copy

def _serialize_datetime(obj): 
    ''' Used as an argument for json.dumps() serial conversions within 
    ErrorMonitor and OrderMonitor for human-readable logging: 
    json.dumps(<data>, default=_format_values). Attempts to convert eligible 
    python datetime.datetime datatypes to RCF3339 formatted strings (does NOT 
    throw errors on any failed datetime conversions, json.dumps() will default 
    to making a "best-guess").
    
    Supported conversions:
            datetime.datetime

    Parameters
    ----------
    obj : unk
        Potential datetime value to encode.
    
    Returns
    -------
    None 
        
    '''
    # if datetime object, format as RCF3339 time
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat().replace("+00:00", "Z")
    
    else:
        # json docs requests a type error in place of original value (just
        # continues on with conversions)
        raise TypeError("Type not serializable") 

''' SESSION MONITORS '''
class ErrorMonitor(threading.Thread):
    ''' Monitors a list of Oanda "endpoint interface" objects for client-server
        errors.

    Attributes
    ----------
    `logs` : list[dict]
        A continuously updated list of client-server errors made since the 
        ErrorMonitor() object was started. *Note* If `logPath` is specified on 
        initialization, any pre-existing logs within the specified log file will 
        be loaded into this variable prior to appending additional logs to it.

        Single Log Entry Format:\n
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


    `_endpoints` : list
        The list of client "endpoint interface" objects that are currently
        being monitored.

    `_flags` : list[dict]
        A list of flags and recent error messages aligned with each endpoint
        being monitored. Each endpoint's flags and recent message are used to 
        prevent repeatedly recording the same error multiple times.

    `_logPath` : str | None
        Full path to log file, if specified. The log's on-disk format
        will be a json for each log entry (appended with a trailing comma). The
        final trailing comma is stripped prior to re-loading the log into memory.
        [Default=None]

    `_printErrors` : bool
        Whether printing errors to stdout. [Default=False]

    `_stop_signal` : threading.Event
        When set, stops the given thread.

    Methods
    --------------
    `stop()` : func
        Sets `self._stop_signal`, stopping the given thread.

    `start()` : func
        Starts the thread (using `run()` function details).

    `run()` : func
        Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects, checking to see if any errors have occured between
        the client (trader) and server (Oanda). Logs any errors that occur (no 
        error handling is done). Use `start()` to begin thread, not this function.

    '''

    def __init__(self, 
                 endpoints : list,
                 printErrors : bool = False, 
                 logPath : str | None = None) -> None:
        ''' Initializes ErrorMonitor object.
        
        Parameters
        ----------
        `endpoints` : list
            The list of client "endpoint interface" objects to monitor:

            Supported Object Types:\n
                `session.Account()`\n
                `session.Instruments()`\n
                `session.Orders()`\n
                `session.Trades()`\n
                `session.Positions()`\n
                `session.Transactions()`\n
                `session.Pricing()`

        `printErrors` : bool = False
            Whether to print errors to stdout. [Default=False]

        `logPath` : str | None = None
            (Optional) Full path to log file on disk for recording errors. If
            provided, will attempt to load any pre-existing logs to memory
            before error logging begins. [Default=None]

        Returns
        -------
        `None`

        '''

        # inherit Parent class Thread
        threading.Thread.__init__(self)

        # create a way to stop the thread if need be. 
        self._stop_signal = threading.Event()

        # set endpoints
        self._endpoints = [endpoint for endpoint in endpoints]
        
        # set corresponding endpoint flags
        self._flags = [{"flag" : 0, "message" : {}} for i in range(0, len(self._endpoints))]

        # set parameters
        self._logPath = logPath
        self._printErrors = printErrors

        # load prior logs (if available)
        if logPath:
            
            # (will be created once logging begins if file doesn't exist)
            if os.path.exists(logPath):

                with open(logPath, "r") as oldLogs:
                    # read in all but last "," (logs entries are recorded as "{},")
                    tempLogs = "[" + oldLogs.read()[:-1] + "]"
                    self.logs = json.loads(tempLogs)
        
        # otherwise prep container
        else:
            self.logs = []

        return None

    def stop(self):
        ''' Stops the given monitor thread (prevents continued error logging).
        Parameters
        ----------------
        None

        Returns
        -----------
        None
        '''

        self._stop_signal.set()
        
        return None

    def run(self):
        ''' Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects, checking to see if any errors have occured between
        the client (trader) and server (Oanda). Logs any errors that occur (no 
        error handling is done). Use `start()` to begin thread, not this.
        
        Parameters
        ----------------
        None

        Returns
        -----------
        `None`

        '''

        # continue until thread is stopped with `self.stop()`
        while not self._stop_signal.is_set():

            # iterate over provided endpoints
            for i in range(0, len(self._endpoints)):

                # aquire error lock to ensure both return code and message are aligned
                self._endpoints[i]._errorLock.acquire()

                # if no error code present, ensure corresponding endpoint flag is properly set
                if (self._endpoints[i].rcode == 200) or \
                   (self._endpoints[i].rcode == 201) or \
                   (self._endpoints[i].rcode == 888):
                    
                    if self._flags[i]["flag"] != 0:
                        self._flags[i]["flag"] = 0
                
                # otherwise, check to see if error needs to be recorded
                else:

                    # if corresponding flag and message already set, don't record error again
                    if (self._flags[i]["flag"] == 1) and \
                       (self._flags[i]["message"] == self._endpoints[i].errorMessage):
                        pass

                    # otherwise, record the new error
                    else:
                        errorEntry = {
                                        "entryID" : len(self.logs),
                                        "datetime" : datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                                        "originClass" : self._endpoints[i].__class__.__name__,
                                        "errorDetails" : copy.deepcopy(self._endpoints[i].errorMessage)
                                     }

                        # append new entry in memory
                        self.logs.append(errorEntry)

                        # print error to stdout (if applicable)
                        if self._printErrors:
                            print(json.dumps(errorEntry, default=_serialize_datetime, indent=4))

                        # record new entry to log file (if applicable)
                        if self._logPath:
                            # creates file if path doesn't exist
                            with open(self._logPath, "a+") as logFile:
                                logFile.write(json.dumps(errorEntry, default=_serialize_datetime, indent=4) + ",")

                        # set corresponding error flag & message
                        self._flags[i]["flag"] = 1
                        self._flags[i]["message"] = errorEntry["errorDetails"]

                # release error lock
                self._endpoints[i]._errorLock.release()

        return None

class StreamMonitor(threading.Thread):
    ''' Monitors "endpoint interface" streams for their respective heartbeats,
    setting "dead stream" error messages and restarting streams as needed.
    
    Attributes
    ----------
    `deadOnArrival` : datetime.timedelta
        "Dead On Arrival" - number of seconds between heartbeats before a stream
        is considered dead. Oanda heartbeats are ~5s. Stream re-starts take ~2s.
        Allow at least ~7s (preferably more) if modifying this attribute. [Default=10]

    `doNotResusitate` : int
        "Do Not Resuscitate" - number of times to attempt to restart a stream.
        [Default=3]

    `resetTime` : datetime.timedelta
        Number of minutes before resetting `doNotResusitate` counters back to zero for each 
        endpoint. *Note* `doNotResusitate` is meant to give time for minor issues to resolve 
        themselves (brief drops in WiFi service, ISP routing issues, etc.) - 
        `resetTime` gives time for higher-level issues to be resolved (Example: 
        the Oanda streaming server crashes, but is brought back up by their 
        IT department within the hour). [Default=60]

    `_endpoints` : list
        The list of client "endpoint interface" objects with potential streams.

    `_dnrCount` : list
        A list with the number of times each endpoint has had its stream restarted
        since StreamMonitor() began, aligned with `self._endpoints`.

    `_lastReset` : datetime.datetime
        The last time all stream-reset attempts (`_dnrCount`) were set back to zero.

    Methods
    -------
    `stop()` : func
        Sets `self._stop_signal`, stopping the given thread.

    `start()` : func
        Starts the thread (using `run()` function details).

    `run()` : func
        Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects with streams, checking to see if any of the streams'
        heartbeats are timestamped later than `self.deadOnArrival` minimum number of
        seconds (restarts them if they are). Use `start()` to begin thread, not 
        this function.
    
    '''

    def __init__(self,
                 endpoints : list,
                 deadOnArrival : int = 10,
                 doNotResusitate : int = 3,
                 resetTime : int = 60) -> None:
        ''' Initializes StreamMonitor object.

        Parameters
        ----------
        `endpoints` : list
            The list of client "endpoint interface" objects with potential streams
            to monitor.

            Supported Endpoint Classes:\n
            `sessions.Transactions()`\n
            `sessions.Pricing()`
        
        `deadOnArrival` : int = 10
            "Dead On Arrival" - number of seconds between heartbeats before 
            a stream is considered dead. [Default=10]

        `doNotResusitate` : int = 3
            "Do Not Resuscitate" - number of times to attempt to restart 
            a dead stream. [Default=3]

        `resetTime` : int = 60
            Number of minutes before resetting `doNotResusitate` counters back to zero for each 
            endpoint. [Default=60]

        Returns
        -------
        `None`
        
        '''

        # inherit Parent attributes
        threading.Thread.__init__(self)
        
        # enable way to stop the thread
        self._stop_signal = threading.Event()

        # load attributes
        self.deadOnArrival = datetime.timedelta(seconds=deadOnArrival)
        self.doNotResusitate = doNotResusitate
        self.resetTime = datetime.timedelta(minutes=resetTime)
        self._endpoints = [endpoint for endpoint in endpoints]
        self._dnrCount = [0 for i in range(0, len(self._endpoints))]
        self._lastReset = datetime.datetime.now(datetime.UTC)

        return None

    def stop(self):
        ''' Stops the given monitor thread (prevents continued stream management).
        Parameters
        ----------------
        None

        Returns
        -----------
        None
        '''

        self._stop_signal.set()
        
        return None

    def run(self):
        ''' Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects with streams, checking to see if any of the streams'
        heartbeats are timestamped later than `self.deadOnArrival` minimum number of
        seconds (restarts them if they are). Use `start()` to begin thread, not 
        this function.

        Parameters
        ----------
        None

        Returns
        -------
        `None`

        '''
        
        # continue until stop flag set
        while not self._stop_signal.is_set():

            # reset stream re-start attempts if enough time (self.resetTime) has passed
            if self._lastReset < datetime.datetime.now(datetime.UTC) - self.resetTime:
                self._dnrCount = [0] * len(self._endpoints)
                self._lastReset = datetime.datetime.now(datetime.UTC)

            # iterate over endpoints
            for i in range(0, len(self._endpoints)):
                
                # if a stream has been started
                if self._endpoints[i].streamHeartbeat:

                    streamIsDead = False
                    
                    # make sure the stream wasn't JUST started
                    if len(self._endpoints[i].streamHeartbeat) != 0:

                        # set deadOnArrival benchmark
                        benchmark = datetime.datetime.now(datetime.UTC) - self.deadOnArrival

                        # if stream is older than deadOnArrival time, stream is considered dead
                        if self._endpoints[i].streamHeartbeat[-1]["time"] < benchmark:
                            streamIsDead = True
                        
                        # otherwise, it's considered fine
                        else:
                            pass

                    # decide what to do with dead stream
                    if streamIsDead:

                        restartStream = False

                        # set message for stream restart attempts
                        if self._dnrCount[i] >= self.doNotResusitate:
                            status_message = "Max stream restarts attempted, leaving stream dead."
                        else:
                            status_message = "Attempting to restart stream..."
                            restartStream = True

                        # acquire lock to prevent logging until message complete
                        self._endpoints[i]._errorLock.acquire()

                        # set error code errorMessage attributes
                        self._endpoints[i].rcode = 999
                        self._endpoints[i].errorMessage = \
                        {
                            "url" : None,
                            "headers" : None,
                            "parameters" : None,
                            "payload" : None, 
                            "code" : 999,
                            "message" : "Dead stream. Prior restart attempts: {}. Restart attempts permitted: {}. {}".format(self._dnrCount[i],
                                                                                                                             self.doNotResusitate,
                                                                                                                             status_message)
                        }

                        # allow error logging
                        self._endpoints[i]._errorLock.release()

                        # restart the stream
                        if restartStream:
                            # ensure old stream stopped
                            self._endpoints[i].stop_stream()
                            time.sleep(2)

                            # start new strem
                            self._endpoints[i].start_stream(*self._endpoints[i]._streamArgs)
                            
                            # give time for stream to start & avoid Oanda request throttling
                            time.sleep(2)
                            
                            self._dnrCount[i] = self._dnrCount[i] + 1

        return None

class OrderMonitor(threading.Thread):
    ''' Monitors a list of Oanda "endpoint interface" objects for successful
    order confirmations.

    Attributes
    ----------
    `logs` : list[dict]
        A continuously updated list of order confirmations made since the 
        OrderMonitor() object was started. *Note* If `logPath` is specified on 
        initialization, any pre-existing logs within the specified log file will 
        be loaded into this variable prior to appending additional logs to it.

        Single Log Entry Format:\n
        {
            "entryID" : the log's serialized entry number (beginning at 0)
            "datetime" : the date/time the order was confirmed (UTC)
            "originClass" : the "endpoint interface" type (a class within `session` module)
                that sent the order
            "confirmationDetails" : Oanda's reponse to successfully receiving the order
        }


    `_endpoints` : list
        The list of client "endpoint interface" objects that are currently
        being monitored.

    `_flags` : list[dict]
        A list of flags and recent confirmation messages aligned with each endpoint
        being monitored. Each endpoint's flags and recent message are used to 
        prevent repeatedly recording the same message multiple times.

    `_logPath` : str | None
        Full path to log file, if specified. The log's on-disk format
        will be a json for each log entry (appended with a trailing comma). The
        final trailing comma is stripped prior to re-loading the log into memory.
        [Default=None]

    `_printConfirmation` : bool
        Whether printing order confirmations to stdout. [Default=False]

    `_stop_signal` : threading.Event
        When set, stops the given thread.

    Methods
    --------------
    `stop()` : func
        Sets `self._stop_signal`, stopping the given thread.

    `start()` : func
        Starts the thread (using `run()` function details).

    `run()` : func
        Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects, checking to see if any new order confirmation have
        been received, logging them as appropriate. Use `start()` to 
        begin thread, not this function.

    '''

    def __init__(self, 
                 endpoints : list,
                 printConfirmations : bool = False, 
                 logPath : str | None = None) -> None:
        ''' Initializes OrderMonitor object.
        
        Parameters
        ----------
        `endpoints` : list
            The list of client "endpoint interface" objects to monitor:

            Supported Object Types:\n
                `session.Orders()`\n
                `session.Trades()`\n
                `session.Positions()`\n

        `printConfirmations` : bool = False
            Whether to print order confirmations to stdout. [Default=False]

        `logPath` : str | None = None
            (Optional) Full path to log file on disk for recording confirmations. 
            If provided, will attempt to load any pre-existing logs to memory
            before confirmation logging begins. [Default=None]

        Returns
        -------
        `None`

        '''

        # inherit Parent class Thread
        threading.Thread.__init__(self)

        # create a way to stop the thread if need be. 
        self._stop_signal = threading.Event()

        # set endpoints
        self._endpoints = [endpoint for endpoint in endpoints]
        
        # set corresponding endpoint flags
        self._flags = [{"flag" : 0, "message" : {}} for i in range(0, len(self._endpoints))]

        # set parameters
        self._logPath = logPath
        self._printConfirmations = printConfirmations

        # load prior logs (if available)
        if logPath:
            
            # (will be created once logging begins if file doesn't exist)
            if os.path.exists(logPath):

                with open(logPath, "r") as oldLogs:
                    # read in all but last "," (logs entries are recorded as "{},")
                    tempLogs = "[" + oldLogs.read()[:-1] + "]"
                    self.logs = json.loads(tempLogs)
        
        # otherwise prep container
        else:
            self.logs = []

        return None

    def stop(self):
        ''' Stops the given monitor thread (prevents continued order confirmation 
        logging).
        
        Parameters
        ----------------
        None

        Returns
        -----------
        None
        '''

        self._stop_signal.set()
        
        return None

    def run(self):
        ''' Overrides threading.Thread.run(). Contiuously iterates over all "endpoint 
        interface" objects, checking to see if any new order confirmation have
        been received, logging them as appropriate. Use `start()` to 
        begin thread, not this function.
        
        Parameters
        ----------------
        None

        Returns
        -----------
        `None`

        '''

        # continue until thread is stopped with `self.stop()`
        while not self._stop_signal.is_set():

            # iterate over provided endpoints
            for i in range(0, len(self._endpoints)):

                # aquire order lock to ensure both return code and message are aligned
                self._endpoints[i]._orderLock.acquire()

                # if no confirmation code present, ensure flag is properly set
                if (self._endpoints[i].rcode != 888):
                    if self._flags[i]["flag"] != 0:
                        self._flags[i]["flag"] = 0
                
                # otherwise, check to see if confirmation needs to be recorded
                else:
                    
                    # if corresponding flag and message already set, don't record confirmation again
                    if (self._flags[i]["flag"] == 1) and \
                       (self._flags[i]["message"] == self._endpoints[i].orderMessage):
                        pass

                    # otherwise, record the new confirmation
                    else:
                        confirmationEntry = {
                                        "entryID" : len(self.logs),
                                        "datetime" : datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
                                        "originClass" : self._endpoints[i].__class__.__name__,
                                        "confirmationDetails" : copy.deepcopy(self._endpoints[i].orderMessage)
                                     }

                        # append new entry in memory
                        self.logs.append(confirmationEntry)

                        # print confirmation to stdout (if applicable)
                        if self._printConfirmations:
                            print(json.dumps(confirmationEntry, default=_serialize_datetime, indent=4))

                        # record new entry to log file (if applicable)
                        if self._logPath:
                            # creates file if path doesn't exist
                            with open(self._logPath, "a+") as logFile:
                                logFile.write(json.dumps(confirmationEntry, default=_serialize_datetime, indent=4) + ",")

                        # set corresponding confirmation flag & message
                        self._flags[i]["flag"] = 1
                        self._flags[i]["message"] = confirmationEntry["confirmationDetails"]

                # release order lock
                self._endpoints[i]._orderLock.release()

        return None

