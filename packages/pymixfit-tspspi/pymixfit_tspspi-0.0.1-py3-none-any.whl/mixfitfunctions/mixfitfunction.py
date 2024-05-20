from lmfit import Parameters

class MixfitFunctionFactory:
    """A simple base class for function factories. Those generate function instances"""

    def __init__(
        self,
        fid,
        title,
        description,
        params
    ):
        """Initialize function base information

        Parameters
        ----------

        fid: str
            The function ID. This will be used to identify the function
            internally
        title: str
            A human readable title of the function
        description: str
            A human readable description of the function
        params: dict
            A dictionary containing descriptions of the parameters. Each
            parameter contains:

            {
                "name" : "...",
                "desc" : "...",
                "vary" : bool,
            }
        """
        if not isinstance(params, list):
            raise ValueError("Parameter descriptors have to be a list of dictionaries")
        if not isinstance(title, str):
            raise ValueError("Title has to be a string")
        if not isinstance(fid, str):
            raise ValueError("Function Id has to be a unique string")
        if not isinstance(description, str):
            raise ValueError("Function description has to be a string")

        for p in params:
            if not isinstance(p, dict):
                raise ValueError("Each parameter has to be described by a dictionary")
            if ("name" not in p) or ("desc" not in p):
                raise ValueError("Name and description are required for each parameter")

        self._fid = fid
        self._title = title
        self._description = description
        self._params = params

    def __call__(self):
        raise NotImplementedError()



class MixfitFunction:
    """Wrapper for all mixture fit candidate methods. This is an abstract base class"""
    def __init__(
        self,
        fid,
        title,
        description,
        params,
        prefix = None,
        limits = None
    ):
        """Initialize function base information

        Parameters
        ----------

        fid: str
            The function ID. This will be used to identify the function
            internally.
        title: str
            A human readable title of the function
        description: str
            A human readable description of the function
        params: dict
            A dictionary containing descriptions of the parameters. Each
            parameter contains:

            {
                "name" : "...",
                "desc" : "...",
                "vary" : bool,
            }
        prefix: str, optional
            An optional prefix to be used in front of parameter names
        limits: dict, optional
            An optional dictionary that includes min and max values for
            different parameters. The parameter names have to match the
            name field in parameter
        """

        if not isinstance(params, list):
            raise ValueError("Parameter descriptors have to be a list of dictionaries")
        if limits is not None:
            if not isinstance(limits, dict):
                raise ValueError("Limits field has to be a dictionary or none")
        if not isinstance(title, str):
            raise ValueError("Title has to be a string")
        if not isinstance(fid, str):
            raise ValueError("Function Id has to be a unique string")
        if not isinstance(description, str):
            raise ValueError("Function description has to be a string")

        for p in params:
            if not isinstance(p, dict):
                raise ValueError("Each parameter has to be described by a dictionary")
            if ("name" not in p) or ("desc" not in p):
                raise ValueError("Name and description are required for each parameter")
        if prefix is not None:
            if not isinstance(prefix, str):
                raise ValueError("Parameter name prefix has to be a string")

        self._fid = fid
        self._title = title
        self._description = description
        self._params = params
        self._prefix = prefix

        self._paramsd = {}
        for p in params:
            vary, mn, mx = True, None, None
            if "vary" in p:
                vary = p["vary"]
            if "min" in p:
                mn = p["min"]
            if "max" in p:
                mx = p["max"]
            
            self._paramsd[p["name"]] = {
                "desc" : p["desc"],
                "vary" : vary,
                "min" : mn,
                "max" : mx
            }

        if limits is not None:
            for l in limits:
                if l not in self._paramsd:
                    raise ValueError(f"Limit specified for parameter {l} that's not specified in parameter list")
    
                if len(limits[l]) != 2:
                    raise ValueError(f"Limit for parameter {l} is not a 2-list or 2-tuple!")
                if limits[l][0] == limits[l][1]:
                    self._paramsd[l]["vary"] = False
                else:
                    if limits[l][0] > limits[l][1]:
                        raise ValueError(f"Limit for parameter {l} is not valid, minimum larger than maximum")
                    self._paramsd[l]["min"] = limits[l][0]
                    self._paramsd[l]["max"] = limits[l][1]

    def __call__(self, pars, x, *, data = None):
        raise NotImplementedError()

    def guess(self, x, data):
        raise NotImplementedError()

    def lmparams(self, params, *, lmp = None):
        if lmp is None:
            lmp = Parameters()

        addp = []
        for p in params:
            if self._prefix is None:
                pname = p
            else:
                pname = p[len(self._prefix)+1:]
            lmp.add(p, value = params[p], min = self._paramsd[pname]["min"], max = self._paramsd[pname]["max"], vary = self._paramsd[pname]["vary"])

        return lmp
