from mixfitfunctions.mixfitfunction import MixfitFunction, MixfitFunctionFactory

import numpy as np

class MixfitFunctionGaussianFactory(MixfitFunctionFactory):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "GAUSSIAN",
            "Gaussian",
            "Gaussian distribution",
            [
                { "name" : "mu", "desc" : "Most probable value", "vary" : True, "min" : None, "max" : None },
                { "name" : "sigma", "desc" : "Standard deviation", "vary" : True, "min" : None, "max" : None },
                { "name" : "amp", "desc" : "Amplitude", "vary" : True, "min" : None, "max" : None },
                { "name" : "offset", "desc" : "Constant offset", "vary" : True, "min" : None, "max" : None }
            ]
        )
        if "limits" in kwargs:
            self._limits = kwargs["limits"]
        else:
            self._limits = None

    def __call__(self, *args, **kwargs):
        return MixfitFunctionGaussian(*args, limits = self._limits, **kwargs)

class MixfitFunctionGaussian(MixfitFunction):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "GAUSSIAN",
            "Gaussian",
            "Gaussian distribution",
            [
                { "name" : "mu", "desc" : "Most probable value", "vary" : True, "min" : None, "max" : None },
                { "name" : "sigma", "desc" : "Standard deviation", "vary" : True, "min" : None, "max" : None },
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
            mu = 0
            sig = 1
            offs = 0
        else:
            if self._prefix is not None:
                pfx = f"{self._prefix}_"
            else:
                pfx = ""
            amp = ppars[f"{pfx}amp"]
            mu = ppars[f"{pfx}mu"]
            sig = ppars[f"{pfx}sigma"]
            offs = ppars[f"{pfx}offset"]

        return amp, mu, sig, offs

    def __call__(self, pars, x, *, data = None):
        amp, mu, sig, offs = self._parse_pparms(pars)
        val = amp * np.exp(-np.power(x - mu, 2.0) / (2 * np.power(sig, 2.0))) + offs
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
                    f"{pfx}sigma" : 1,
                    f"{pfx}mu" : x[np.argmax(data)],
                    f"{pfx}offset" : np.min(data)
            }
        else:
            return {
                    f"{pfx}amp" : -1.0 * (np.max(data) - np.min(data)),
                    f"{pfx}sigma" : 1,
                    f"{pfx}mu" : x[np.argmin(data)],
                    f"{pfx}offset" : np.max(data)
            }

    def _p_repr(self, params):
        amp, mu, sig, offs = self._parse_pparms(params)
        return f"Gaussian(amp={amp.value}+-{amp.stderr}, mu={mu.value}+-{mu.stderr}, sigma={sig.value}+-{sig.stderr}, offset={offs.value}+-{offs.stderr})"

