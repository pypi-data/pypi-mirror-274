from mixfitfunctions.mixfitfunction import MixfitFunction, MixfitFunctionFactory

import numpy as np

class MixfitFunctionDifferentialCauchyFactory(MixfitFunctionFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "DIFFERENTIALCAUCHY",
            "Differential Cauchy",
            "Differential Cauchy distribution",
            [
                { "name" : "x0", "desc" : "Most probable value", "vary" : True, "min" : None, "max" : None },
                { "name" : "gamma", "desc" : "Width", "vary" : True, "min" : None, "max" : None },
                { "name" : "amp", "desc" : "Amplitude", "vary" : True, "min" : None, "max" : None },
                { "name" : "offset", "desc" : "Constant offset", "vary" : True, "min" : None, "max" : None }
            ]
        )
        if "limits" in kwargs:
            self._limits = kwargs["limits"]
        else:
            self._limits = None

    def __call__(self, *args, **kwargs):
        return MixfitFunctionDifferentialCauchy(*args, limits = self._limits, **kwargs)

class MixfitFunctionDifferentialCauchy(MixfitFunction):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "DIFFERENTIALCAUCHY",
            "Differential Cauchy",
            "Differential Cauchy distribution",
            [
                { "name" : "x0", "desc" : "Most probable value", "vary" : True, "min" : None, "max" : None },
                { "name" : "gamma", "desc" : "Width", "vary" : True, "min" : None, "max" : None },
                { "name" : "amp", "desc" : "Amplitude", "vary" : True, "min" : None, "max" : None },
                { "name" : "offset", "desc" : "Constant offset", "vary" : True, "min" : None, "max" : None }
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
            amp = 1
            x0 = 0
            gamma = 1
            offs = 0
        else:
            if self._prefix is not None:
                pfx = f"{self._prefix}_"
            else:
                pfx = ""
            amp = ppars[f"{pfx}amp"]
            x0 = ppars[f"{pfx}x0"]
            gamma = ppars[f"{pfx}gamma"]
            offs = ppars[f"{pfx}offset"]

        return amp, x0, gamma, offs

    def __call__(self, pars, x, *, data = None):
        amp, x0, gamma, offs = self._parse_pparms(pars)
        val = -1.0 * amp * gamma / np.pi * 2 * (x - x0) / ((x - x0) ** 2 + gamma ** 2)**2 + offs
        if data is None:
            return val
        else:
            return data - val

    def guess(self, x, data):
        pfx = ""
        if self._prefix is not None:
            pfx = f"{self._prefix}_"
        if (np.max(data) - np.mean(data)) > (np.mean(data) - np.min(data)):
            return {
                    f"{pfx}amp" : np.max(data) - np.min(data),
                    f"{pfx}gamma" : 1,
                    f"{pfx}x0" : x[np.argmax(data)],
                    f"{pfx}offset" : np.min(data)
            }
        else:
            return {
                    f"{pfx}amp" : -1.0 * (np.max(data) - np.min(data)),
                    f"{pfx}gamma" : 1,
                    f"{pfx}x0" : x[np.argmin(data)],
                    f"{pfx}offset" : np.max(data)
            }

    def _p_repr(self, params):
        amp, x0, gamma, offs = self._parse_pparms(params)
        return f"DiffCauchy(amp={amp.value}+-{amp.stderr}, x0={x0.value}+-{x0.stderr}, gamma={gamma.value}+-{gamma.stderr}, offset={offs.value}+-{offs.stderr})"

