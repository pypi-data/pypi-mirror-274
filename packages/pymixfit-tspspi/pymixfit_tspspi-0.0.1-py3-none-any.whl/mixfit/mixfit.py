import numpy as np

from lmfit import Parameters, minimize

from mixfitfunctions.mixfitfunction import MixfitFunctionFactory
from mixfitfunctions.gaussian import MixfitFunctionGaussianFactory
from mixfitfunctions.constant import MixfitFunctionConstantFactory
from mixfitfunctions.linear import MixfitFunctionLinearFactory
from mixfitfunctions.differentialgaussian import MixfitFunctionDifferentialGaussianFactory
from mixfitfunctions.cauchy import MixfitFunctionCauchyFactory
from mixfitfunctions.differentialcauchy import MixfitFunctionDifferentialCauchyFactory

class Mixture:
    def __init__(self):
        self._functions = []
        self._params = []
        self._chis = []

    def __call__(self, x, *, data = None):
        # Evaluate the mixture at the specified points
        res = np.zeros((len(x),))
        for i_f, f in enumerate(self._functions):
            res = res + f(self._params[i_f], x)
        if data is None:
            return res
        else:
            return data - res

    def _call2(self, params, x, data = None):
        res = np.zeros((len(x),))
        for i_f, f in enumerate(self._functions):
            res = res + f(params, x)
        if data is None:
            return res
        else:
            return data - res

    def _refine(self, x, data):
        # Perform refinment using all functions ...

        # Build global Parameters object ...
        inParams = Parameters()
        for p1 in self._params:
            for p2 in p1:
                inParams.add(p1[p2])

        # Run minimizer ...
        globalRes = minimize(
            self._call2,
            inParams,
            args = (x,),
            kws = { 'data' : data }
        )
 
        # Create local parameters objects again ...
        newParams = []
        self._chis.append(globalRes.chisqr)

        for p1 in self._params:
            newParams.append(Parameters())
            for p2 in p1:
                newParams[-1].add(globalRes.params[p2])
        self._params = newParams

    def __repr__(self):
        res = ""
        for ifun, fun in enumerate(self._functions):
            res = res + "\n" + fun._p_repr(self._params[ifun])
        return res


class Mixfit:
    def __init__(
        self,
        allowed = [
            MixfitFunctionGaussianFactory(),
            MixfitFunctionConstantFactory(),
            MixfitFunctionLinearFactory(),
            MixfitFunctionDifferentialGaussianFactory(),
            MixfitFunctionCauchyFactory(),
            MixfitFunctionDifferentialCauchyFactory()
        ],
        maxIterations = None,
        minResiduumImprovement = None,
        stopError = None
    ):
        for a in allowed:
            if not isinstance(a, MixfitFunctionFactory):
                raise ValueError(f"{a} is not a MixfitFunctionFactory")

        if maxIterations is not None:
            if int(maxIterations) != maxIterations:
                raise ValueError("Maximum iterations have to a a positive integer")
            if maxIterations < 1:
                raise ValueError("At least one iteration is required")
        if minResiduumImprovement is not None:
            if float(minResiduumImprovement) <= 0:
                raise ValueError("Minimum residuum improvement has to be a positive value")
        if stopError is not None:
            if float(stopError) <= 0:
                raise ValueError("Stop error has to be a positive value")

        self._factories = allowed
        self._maxIterations = maxIterations
        self._minResiduumImprovement = minResiduumImprovement
        self._stopError = stopError

    def fit(
        self,
        x,
        inputData
    ):
        res = Mixture()

        while True:
            # First all of our stop conditions
            # ================================
            if self._maxIterations is not None:
                # Check if we have reached the maximum number of iterations
                if len(res._chis) >= self._maxIterations:
                    break
            if len(res._chis) > 1:
                if res._chis[-2] < res._chis[-1]:
                    # We did not improve on the last step - we always terminate then
                    # and drop the last step
                    res._chis.pop()
                    res._functions.pop()
                    res._params.pop()
                    break
                if res._chis[-1] == 0:
                    # We also break if we have a perfect fit of course ...
                    break
                if self._minResiduumImprovement is not None:
                    # Check if we have achived the minimum improvement
                    if (res._chis[-2] - res._chis[-1]) < self._minResiduumImprovement:
                        res._chis.pop()
                        res._functions.pop()
                        res._params.pop()
                        break
            if len(res._chis) > 0:
                if self._stopError is not None:
                    # Check if our error is smaller than our stop condition
                    if res._chis[-1] < self._stopError:
                        break

            # Subtract the previously fitted functions from our
            # input data as our "stage input"
            # =================================================
            stageInput = inputData - res(x)

            # Now iterate over all candidates that we're allowed to use
            # and check which one works best ...
            candidates = []
            candidates_params = []
            candidates_chi = []
            for fac in self._factories:
                # Create function from factory ...
                fun = fac(prefix=f"f{len(res._functions)}")

                # Get guess
                guess = fun.guess(x, stageInput)
                guessParams = fun.lmparams(guess)

                #fig, ax = plt.subplots()
                #ax.plot(x, stageInput, 'x')
                #ax.plot(x, fun(guessParams, x))
                #ax.grid()
                #plt.show()
                
                # Run minimizer on our candidate function
                singleRes = minimize(
                    fun,
                    guessParams,
                    args = (x,),
                    kws = { 'data' : stageInput }
                )

                candidates.append(fun)
                candidates_params.append(singleRes.params)
                candidates_chi.append(singleRes.chisqr)

            # Locate best fit for this stage input
            # ====================================
            candidates_chi = np.asarray(candidates_chi)
            minchi = np.argmin(candidates_chi)

            res._functions.append(candidates[minchi])
            res._params.append(candidates_params[minchi])

            # Now preform refinment on the whole function
            # and all parameters of the whole mixture
            # ===========================================

            res._refine(x, inputData)


            # Debug output
            # ============
            #fig, ax = plt.subplots(1,3,figsize=(6.4*2*3, 4.8*2))
            #ax[0].plot(x, testdta, 'x')
            #ax[0].plot(x, res(x))
            #ax[0].grid()
            #ax[1].plot(res._chis)
            #ax[1].grid()
            #ax[2].plot(x, stageInput)
            #ax[2].plot(x, res._functions[-1](res._params[-1], x))
            #ax[2].grid()
            #plt.show()
        return res

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import sys


    dc = MixfitFunctionCauchyFactory()
    ddc = MixfitFunctionDifferentialCauchyFactory()
    dc = dc()
    ddc = ddc()

    #fig, ax = plt.subplots()
    #x = np.linspace(-10, 10, 1000)
    #ax.plot(x, dc({"x0" : 3, "gamma" : 5, "offset" : 0, "amp" : 2}, x))
    #ax.plot(x, ddc({"x0" : 3, "gamma" : 5, "offset" : 0, "amp" : 10}, x))
    #ax.grid()
    #plt.show()
    #sys.exit(0)

    dgf = MixfitFunctionDifferentialGaussianFactory()
    dg = dgf()

    x = np.linspace(-10, 10, 100)
    testsigma = 3
    testmu = 1
    testoffset = 0.5

    testsigma2 = 0.7
    testmu2 = -3
    testamp2 = 0.3
    testoffset2 = 0

    testsigma3 = 0.1
    testmu3 = 6
    testamp3 = -0.1
    testoffset3 = 0

    testdta = np.exp(-0.5 * ((x - testmu)/(testsigma))**2.0) * 1.0 / np.sqrt(2 * np.pi * testsigma) - testoffset
    testdta = testdta + testamp2 * np.exp(-0.5 * ((x - testmu2)/(testsigma2))**2.0) * 1.0 / np.sqrt(2 * np.pi * testsigma2) + testoffset
    testdta = testdta + testamp3 * np.exp(-0.5 * ((x - testmu3)/(testsigma3))**2.0) * 1.0 / np.sqrt(2 * np.pi * testsigma3) + testoffset
    testdta = testdta + x * 0.001
    testdta = testdta + dg({ "mu" : 2, "sigma" : 0.22, "amp" : 0.05, "offset" : 0 }, x)
    testdta = testdta + np.random.normal(0, 0.015, testdta.shape)
    testdta = testdta + np.full((len(x),),5.5)

    mf = Mixfit(
        maxIterations = 10,
        stopError = 0.05,
        allowed = [
           MixfitFunctionGaussianFactory(limits = {"mu" : (-10, 10), "sigma" : (0.5, 3)}),
           MixfitFunctionDifferentialGaussianFactory(limits = { "sigma" : (0.01, 1) }),
           MixfitFunctionLinearFactory(),
           MixfitFunctionCauchyFactory()
        ]
    )
    res = mf.fit(x, testdta)

    fig, ax = plt.subplots(1,2,figsize=(6.4*4, 4.8*2))
    ax[0].plot(x, testdta, 'x')
    ax[0].plot(x, res(x))
    ax[0].grid()
    ax[1].plot(res._chis)
    ax[1].grid()
    plt.show()
