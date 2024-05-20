from mixfitfunctions.mixfitfunction import MixfitFunction, MixfitFunctionFactory

import numpy as np

class MixfitFunctionConstantFactory(MixfitFunctionFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "CONSTANT",
            "Constant",
            "Constant offset",
            [
                { "name" : "offset", "desc" : "Constant shift", "vary" : True, "min" : None, "max" : None }
            ]
        )
        if "limits" in kwargs:
            self._limits = kwargs["limits"]
        else:
            self._limits = None

    def __call__(self, *args, **kwargs):
        return MixfitFunctionConstant(*args, limits = self._limits, **kwargs)

class MixfitFunctionConstant(MixfitFunction):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "CONSTANT",
            "Constant",
            "Constant offset",
            [
                { "name" : "offset", "desc" : "Constant shift", "vary" : True, "min" : None, "max" : None }
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
            offs = 0
        else:
            if self._prefix is not None:
                pfx = f"{self._prefix}_"
            else:
                pfx = ""
            offs = ppars[f"{pfx}offset"]

        return offs

    def __call__(self, pars, x, *, data = None):
        offs = self._parse_pparms(pars)
        val = np.full((len(x),), offs)
        if data is None:
            return val
        else:
            return data - val

    def guess(self, x, data):
        pfx = ""
        if self._prefix is not None:
            pfx = f"{self._prefix}_"
        return {
            f"{pfx}offset" : np.mean(data)
        }

    def _p_repr(self, params):
        offs = self._parse_pparms(params)
        return f"Constant(offset={offs.value}+-{offs.stderr})"
