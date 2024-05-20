from mixfitfunctions.mixfitfunction import MixfitFunction, MixfitFunctionFactory

import numpy as np

class MixfitFunctionLinearFactory(MixfitFunctionFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "LINEAR",
            "Linear",
            "Linear function",
            [
                { "name" : "slope", "desc" : "Slope of linear function", "vary" : True, "min" : None, "max" : None },
                { "name" : "intercept", "desc" : "Position where linear function intercepts the ordinate", "vary" : True, "min" : None, "max" : None }
            ]
        )
        if "limits" in kwargs:
            self._limits = kwargs["limits"]
        else:
            self._limits = None

    def __call__(self, *args, **kwargs):
        return MixfitFunctionLinear(*args, limits = self._limits, **kwargs)

class MixfitFunctionLinear(MixfitFunction):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "LINEAR",
            "Linear",
            "Linear function",
            [
                { "name" : "slope", "desc" : "Slope of linear function", "vary" : True, "min" : None, "max" : None },
                { "name" : "intercept", "desc" : "Position where linear function intercepts the ordinate", "vary" : True, "min" : None, "max" : None }
            ],
            *args,
            **kwargs
        )

    def _parse_pparms(self, ppars):
        if not isinstance(ppars, dict):
            pars = ppars.valuesdict()
        else:
            pars = ppars

        if pars is None:
            slope = 0
            intercept = 0
        else:
            if self._prefix is not None:
                pfx = f"{self._prefix}_"
            else:
                pfx = ""
            slope = ppars[f"{pfx}slope"]
            intercept = ppars[f"{pfx}intercept"]

        return slope, intercept

    def __call__(self, pars, x, *, data = None):
        slope, intercept = self._parse_pparms(pars)
        val = x * slope + intercept
        if data is None:
            return val
        else:
            return data - val

    def guess(self, x, data):
        pfx = ""
        if self._prefix is not None:
            pfx = f"{self._prefix}_"

        k = (data[-1] - data[0]) / (x[-1] - x[0])
        d = data[0] - k * x[0]

        return {
            f"{pfx}slope" : k,
            f"{pfx}intercept" : d
        }

    def _p_repr(self, params):
        slope, intercept = self._parse_pparms(params)
        return f"Linear(slope={slope.value}+-{slope.stderr}, intercept={intercept.value}+-{intercept.stderr})"
