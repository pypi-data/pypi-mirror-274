import requests
import threading
import json
import datetime
import copy

''' CLIENT-SERVER COMMUNICATIONS '''
def _to_objects(dictionary) -> dict:
    ''' Converts eligible string values to python datatypes (does NOT throw 
    errors on any failed conversions, value will just remain a string). Used as 
    an argument for json.loads() object hook conversions: 
    json.loads(<data>, object_hook=_to_objects). Supported conversion:
            int\n
            float\n
            datetime.datetime
    
    Parameters
    ----------
    dictionary: dict
        The json to iterate over.

    Returns
    -------
    dict
    
    '''
    for key in dictionary:
        if type(dictionary[key]) == str:
            
            # likely a float or RCF3339 time if string contains "."
            if "." in dictionary[key]:
                # more often than not, it's a float
                try: 
                    dictionary[key] = float(dictionary[key])
                except:
                    # otherwise typically RCF3339 time
                    try:
                        dictionary[key] = datetime.datetime.fromisoformat(dictionary[key])
                    # if neither, should likely remain a string
                    except:
                        pass
            
            # try converting integers, as well
            else:
                try: 
                    dictionary[key] = int(dictionary[key])
                except:
                    pass

    return dictionary

def _to_strings(obj : dict) -> dict:
    ''' Designed for pre-formatting server requests, recursively replaces objects
    with their  string equivalents (datetime.datetime objects are formatted as 
    RCF3339 in UTC). *Note* Times will be converted to UTC prior to conversion -
    ensure timezones are properly assigned within datetime objects if operating 
    in a different timezone.
    
    Parameters
    ----------
    obj : dict
        The dictionary to recurse over.

    Returns
    -------
    dict
        A dictionary with all eligible values (recursively) formatted as 
        strings (or None).

    '''

    # recurse down list
    if isinstance(obj, list):
        for entry in range(0, len(obj)):
            obj[entry] = _to_strings(obj[entry])

    # recurse down dictionary
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = _to_strings(obj[key])

    # check if object is a datetime (and convert / format if it is)
    elif isinstance(obj, datetime.datetime):
        obj = obj.astimezone(datetime.UTC).isoformat().replace("+00:00", "Z")
        if obj[-1] != "Z":
            obj = obj + "Z"
    
    # pass over None(s)
    elif obj is None:
        pass

    # otherwise, check if object is a string (and convert if not)
    elif not isinstance(obj, str):
        obj = str(obj)

    return obj

def get_request(endpoint : str,
                headers : None | dict = None,
                parameters : None | dict = None) -> tuple[dict, int]:
    ''' `requests.get()` wrapper with custom error handling.

    Parameters
    ----------------
    `endpoint` : str = ""
        Target URL.
        
    `header` : None | dict = None
        Headers to pass. 

    `parameters` : None | dict = None
        Parameters to pass.


    Returns
    -----------
    dict
        Dictionary of response.

    int
        Request response return code.

    '''

    # _to_strings() converts object's items in place
    cparameters = copy.deepcopy(parameters)

    # send request and validate response
    try:
        response = requests.get(endpoint, 
                            headers=headers, 
                            params=_to_strings(cparameters))
        status_code = response.status_code

    # catches all errors EXCEPT HTTPErrors
    except Exception as err:
        error = str(err)
        
        # arbitrary "non-HTTP error" status code
        status_code = 999

    # if success
    if (status_code == 200) or (status_code == 201):
        rdata = response.json(object_hook=_to_objects)

    # otherwise error occured
    else:
        # if non-HTTP error, error message already set
        if status_code == 999:
            pass
        # otherwise set HTTP error message
        else:
            error = response.json(object_hook=_to_objects)
        
        # build error message payload
        rdata = {"url" : endpoint,
                "headers" : copy.copy(headers),
                "parameters" : cparameters,
                "payload" : None,
                "code" : status_code,
                "message" : error}
        
        # remove Oanda token
        rdata["headers"]["Authorization"] = "<REDACTED>"


    return rdata, status_code

def post_request(endpoint : str,
                headers : None | dict = None,
                parameters : None | dict = None,
                data : None | dict = None) -> tuple[dict, int]:
    ''' `requests.post()` wrapper with custom error handling.

    Parameters
    ----------------
    `endpoint` : str = ""
        Target URL.
        
    `header` : None | dict = None
        Headers to pass. 

    `parameters` : None | dict = None
        Parameters to pass.

    `data` : None | dict = None
        Data to pass.

    Returns
    -----------
    dict
        Dictionary of response.

    int
        Request response return code.

    '''

    # _to_strings() converts object's items in place
    cparameters = copy.deepcopy(parameters)
    cdata = copy.deepcopy(data)
    
    # send request and validate response
    try:       
        response = requests.post(url=endpoint,
                        headers=headers, 
                        params=_to_strings(cparameters), 
                        json=_to_strings(cdata))
        status_code = response.status_code

    # catches all errors EXCEPT HTTPErrors
    except Exception as err:
        error = str(err)
        
        # arbitrary "non-HTTP error" status code
        status_code = 999

    # if success
    if (status_code == 200) or (status_code == 201):
        rdata = response.json(object_hook=_to_objects)

    # otherwise error occured
    else:
        # if non-HTTP error, error message already set
        if status_code == 999:
            pass
        # otherwise set HTTP error message
        else:
            error = response.json(object_hook=_to_objects)
        
        # build error message payload
        rdata = {"url" : endpoint,
                "headers" : copy.copy(headers),
                "parameters" : cparameters,
                "payload" : cdata,
                "code" : status_code,
                "message" : error}
        
        # remove Oanda token
        rdata["headers"]["Authorization"] = "<REDACTED>"

    return rdata, status_code

def put_request(endpoint : str,
                headers : None | dict = None,
                parameters : None | dict = None,
                data : None | dict = None) -> tuple[dict, int]:
    ''' Simple wrapper for requests.put()

    Parameters
    ----------------
    `endpoint` : str = ""
        Target URL.
        
    `header` : None | dict = None
        Headers to pass. 

    `parameters` : None | dict = None
        Parameters to pass.

    `data` : None | dict = None
        Data to pass.

    Returns
    -----------
    dict
        Dictionary of response.

    int
        Request response return code.

    '''

    # _to_strings() converts object's items in place
    cparameters = copy.deepcopy(parameters)
    cdata = copy.deepcopy(data)

    # send request and validate response
    try:
        response = requests.put(url=endpoint,
                            headers=headers, 
                            params=_to_strings(cparameters), 
                            json=_to_strings(cdata))
        status_code = response.status_code

    # catches all errors EXCEPT HTTPErrors
    except Exception as err:
        error = str(err)
        
        # arbitrary "non-HTTP error" status code
        status_code = 999

    # if success
    if (status_code == 200) or (status_code == 201):
        rdata = response.json(object_hook=_to_objects)

    # otherwise error occured
    else:
        # if non-HTTP error, error message already set
        if status_code == 999:
            pass
        # otherwise set HTTP error message
        else:
            error = response.json(object_hook=_to_objects)
        
        # build error message payload
        rdata = {"url" : endpoint,
                "headers" : copy.copy(headers),
                "parameters" : cparameters,
                "payload" : cdata,
                "code" : status_code,
                "message" : error}
        
        # remove Oanda token
        rdata["headers"]["Authorization"] = "<REDACTED>"

    return rdata, status_code

def patch_request(endpoint : str,
                headers : None | dict = None,
                parameters : None | dict = None,
                data : None | dict = None) -> tuple[dict, int]:
    ''' Simple wrapper for requests.patch()

    Parameters
    ----------------
    `endpoint` : str = ""
        Target URL.
        
    `header` : None | dict = None
        Headers to pass. 

    `parameters` : None | dict = None
        Parameters to pass.

    `data` : None | dict = None
        Data to pass.

    Returns
    -----------
    dict
        Dictionary of response.

    int
        Request response return code.

    '''

    # _to_strings() converts object's items in place
    cparameters = copy.deepcopy(parameters)
    cdata = copy.deepcopy(data)

    # send request and validate response
    try:        
        response = requests.patch(url=endpoint,
                              headers=headers, 
                              params=_to_strings(cparameters), 
                              json=_to_strings(cdata))
        status_code = response.status_code

    # catches all errors EXCEPT HTTPErrors
    except Exception as err:
        error = str(err)
        
        # arbitrary "non-HTTP error" status code
        status_code = 999

    # if success
    if (status_code == 200) or (status_code == 201):
        rdata = response.json(object_hook=_to_objects)

    # otherwise error occured
    else:
        # if non-HTTP error, error message already set
        if status_code == 999:
            pass
        # otherwise set HTTP error message
        else:
            error = response.json(object_hook=_to_objects)
        
        # build error message payload
        rdata = {"url" : endpoint,
                "headers" : copy.copy(headers),
                "parameters" : cparameters,
                "payload" : cdata,
                "code" : status_code,
                "message" : error}
        
        # remove Oanda token
        rdata["headers"]["Authorization"] = "<REDACTED>"

    return rdata, status_code

class _StreamingThread(threading.Thread):
    ''' Creates a thread to keep streamed content updated.

    Attributes
    ----------------
    `response` : requests.models.Response | None
        If the endpoint is succesfully reached (even if HTTPError), this will 
        contain the response generated from `requests.get(..., stream=True)`.

    `status_code` : int
        Either (1) the return code from the `requests.get(..., stream=True)` if
        the endpoint was reached (may or may not be an HTTPError code), or (2)
        an arbitrary `999` status code indicating some other error (network,
        programattic, etc).

    `errorMessage` : dict
        Error message details if `response.get(..., stream=True)` failed in
        any way (whether endpoint was reached or not):
            Keys:
            "url" : endpoint that received the request
            "headers" : headers sent to the endpoint (auth token is removed for 
                security purposes, check your token independently if you suspect 
                this is the issue)
            "parameters" : parameters sent to the endpoint
            "payload" : `None` for "GET" requests
            "code" : status code (HTTP code or `999`)
            "message" : error message

    `lastHeartbeat` : list
        If the stream is succesfully started, contains the most recent heartbeat 
        received from the stream (used to monitor stream's status).

    `content` : list
        If the stream is succesfully started and thread is recording content 
        (set by initialization parameter `record=True`),
        contains all received content since beginning of the stream, stored
        as a `list` (does not included stream "heartbeats") - this has the potential 
        to get very large if the stream runs for a while (be mindful of
        memory usage). If not recording content (set by initialization parameter
        `record=False`) contains each new single stream entry, stored as a `list`
        with a single entry - each new entry overwrites whatever previous single 
        entry was previously received (memory friendly).

    `_feed` : generator
        The stream's `self.iter_lines()` iterator object - `self.run()` iterates
        of this for updating content if the stream is succesfully started.

    `_recording` : bool
        (Flag) when True, appends new stream entries. When False, overwrites
        prior stream entry.

    `_stop_signal` : threading.Event
        When set, stops the given thread.

    Methods
    --------------
    `stop()` : func
        Sets `self._stop_signal`, stopping the given thread.


    `start()` : func
        Starts the thread (using `run()` function definition).

    `run()` : func
        Overrides threading.Thread.run(). Loops over `_feed` iterator object,
        appending/replacing new entries to `content`. Checks to see if 
        `self._stop_signal` is set before each new loop. Use `start()` to
        begin thread, not this function.
    
    Inheritance
    ----------------
    threading.Thread : class
        https://docs.python.org/3/library/threading.html#threading.Thread
    
    '''

    def __init__(self,
                 endpoint : str = "",
                 headers : None | dict = None,
                 parameters : None | dict = None,
                 record : bool = False) -> None:
        ''' Initializes StreamingThread object, begins connection stream.

        Parameters
        ----------------
        `endpoint` : str = ""
            Target URL.
            
        `header` : None | dict = None
            Headers to pass. 

        `parameters` : None | dict = None
            Parameters to pass.

        `record` : bool = False
            When set to True, the streamThread will record every new entry 
            it receives, appending the entry to the streamThread's `self.content` 
            attribute (as a list). If set to False, the streamThread will 
            overwrite it's `self.content` attribute with each new entry it 
            receives (as a dict). [Default=False]

        Returns
        -----------
        None

        '''

        # inherit Thread attributes
        threading.Thread.__init__(self)
        
        # create a way to stop the thread if need be. 
        self._stop_signal = threading.Event()
        
        # _to_strings() converts object's items in place
        cparameters = copy.deepcopy(parameters)

        # send request and validate response
        try:
            # start the stream
            self.response = requests.get(endpoint,
                            headers=headers,
                            params=_to_strings(cparameters),
                            stream=True)

            # set encoding type (how to translate octet-stream)
            if self.response.encoding is None:
                self.response.encoding = 'utf-8'

            # read in feed (decoding octet stream with above encoding type)
            self._feed = self.response.iter_lines(decode_unicode=True)
            
            # set status code
            self.status_code = self.response.status_code

            # set content container to record stream feed
            self.content = []
            self.lastHeartbeat = []
            self._recording = record

        # catches all errors EXCEPT HTTPErrors
        except Exception as err:
            
            # set error message to exception received
            error = str(err)
            
            # arbitrary "non-HTTP error" status code
            self.status_code = 999

        # if success, let thread run
        if (self.status_code == 200) or (self.status_code == 201):
            pass

        # otherwise error occured
        else:
            # if non-HTTP error, set null attributes (error message already set)
            if self.status_code == 999:
                self.response = None

            # otherwise set HTTP error message
            else:
                error = self.response.json(object_hook=_to_objects)
            
            # set additional null attributes
            self.lastHeartbeat = None
            self.content = None
            self._feed = None
            self._recording = None

            # kill thread even if accidentally started
            self._stop_signal.set()

            # build error message payload
            self.errorMessage = {"url" : endpoint,
                                 "headers" : copy.copy(headers),
                                 "parameters" : cparameters,
                                 "payload" : None,
                                 "code" : self.status_code,
                                 "message" : error}
            
            # remove Oanda token
            self.errorMessage["headers"]["Authorization"] = "<REDACTED>"

        return None

    def stop(self) -> None:
        ''' Stops the given streaming thread.

        Parameters
        ----------------
        None


        Returns
        -----------
        None

        '''
        self._stop_signal.set()

        return None

    def run(self) -> None:
        ''' Overrides threading.Thread.run(). Loops over `_feed` iterator object
        (the streamed content), and appends new entries to `content` if
        `recording=True`. Will continue to iterate until `self.stop()` is called.

        Parameters
        ----------------
        None


        Returns
        -----------
        None

        '''

        # read in feed line by line
        for line in self._feed:

            # keep doing this as long as thread is alive
            if not self._stop_signal.is_set():

                # if there's data to read
                if line:
                    # if it's a "HEARTBEAT", update the stream status:
                    if "HEARTBEAT" in line:
                        # convert strings to a dictionaries with proper objects
                        new_entry = json.loads(line, object_hook=_to_objects)

                        # if first heartbeat
                        if len(self.lastHeartbeat) == 0:
                            self.lastHeartbeat.append(new_entry)
                        # otherwise overwrite the last heartbeat
                        else:
                            self.lastHeartbeat[-1] = new_entry

                    # if it's not a "HEARTBEAT":
                    else:
                        # convert strings to a dictionaries with proper objects
                        new_entry = json.loads(line, object_hook=_to_objects)

                        # record entry if recording
                        if self._recording:
                            self.content.append(new_entry)
                        
                        # otherwise overwrite previous entry
                        else:
                            if len(self.content) == 0:
                                self.content.append(new_entry)
                            else:
                                self.content[-1] = new_entry
            
            # stop thread if `self._stop_signal` gets set via self.stop()
            else:
                break

def get_streamThread(endpoint : str,
                headers : None | dict = None,
                parameters : None | dict = None,
                record : bool = False) -> _StreamingThread:
    ''' Create a thread that collects and stores streamed content. 
    Thread must be started with self.start() once object is returned.

    Parameters
    ----------------
    `endpoint` : str = ""
        Target URL.
        
    `header` : None | dict = None
        Headers to pass. 

    `parameters` : None | dict = None
        Parameters to pass.

    `record` : bool = False
        When set to True, the streamThread will record every new entry it receives,
        appending the entry to the streamThread's `self.content` attribute (as a `list`).
        If set to False, the streamThread will overwrite it's `self.content` attribute
        with each new entry it receives (as a single-entry `list`). [Default=False]


    Returns
    -----------
    _StreamingThread
        Thread of the program managing the stream.

    '''
    streamThread = _StreamingThread(endpoint, 
                                   headers=headers, 
                                   parameters=parameters,
                                   record=record)

    return streamThread

