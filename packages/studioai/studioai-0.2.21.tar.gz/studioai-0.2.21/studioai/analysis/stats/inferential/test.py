#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/analysis/stats/inferential/test.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday September 29th 2023 10:45:53 am                                              #
# Modified   : Thursday October 19th 2023 07:56:31 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd
import numpy as np
from typing import Union

from studioai.analysis.stats.inferential.independence import (
    ChiSquareIndependenceTest,
    ChiSquareIndependenceResult,
)
from studioai.analysis.stats.inferential.association import CramersVAnalysis, CramersV
from studioai.analysis.stats.inferential.association import KendallsTauAnalysis, KendallsTau
from studioai.analysis.stats.inferential.gof import KSTest, KSTestResult
from studioai.analysis.stats.inferential.correlation import (
    PearsonCorrelationTest,
    PearsonCorrelationResult,
)
from studioai.analysis.stats.inferential.correlation import (
    SpearmanCorrelationTest,
    SpearmanCorrelationResult,
)
from studioai.analysis.stats.inferential.centrality import TTest, TTestResult


# ------------------------------------------------------------------------------------------------ #
class Inference:
    """Bundles hypothesis testing into a single class."""

    def __init__(self) -> None:
        self._data = None

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        self._data = data

    def chisquare(
        self, a: str, b: str, data: pd.DataFrame = None, alpha: float = 0.05
    ) -> ChiSquareIndependenceResult:
        data = data if data is not None else self._data
        test = ChiSquareIndependenceTest(data=data, a=a, b=b, alpha=alpha)
        test.run()
        return test.result

    def cramersv(self, a: str, b: str, data: pd.DataFrame = None, alpha: float = 0.05) -> CramersV:
        data = data if data is not None else self._data
        test = CramersVAnalysis(data=data, a=a, b=b, alpha=alpha)
        test.run()
        return test.result

    def kendallstau(
        self,
        a: str,
        b: str,
        data: pd.DataFrame = None,
        variant: str = "c",
        alternative: str = "two-sided",
    ) -> KendallsTau:
        data = data if data is not None else self._data
        test = KendallsTauAnalysis(data=data, a=a, b=b, variant=variant, alternative=alternative)
        test.run()
        return test.result

    def kstest(self, a: np.ndarray, b: Union[str, np.ndarray], alpha: float = 0.05) -> KSTestResult:
        test = KSTest(a=a, b=b, alpha=alpha)
        test.run()
        return test.result

    def pearson(
        self,
        a: str,
        b: str,
        data: pd.DataFrame = None,
        alpha: float = 0.05,
    ) -> PearsonCorrelationResult:
        data = data if data is not None else self._data
        test = PearsonCorrelationTest(data=data, a=a, b=b, alpha=alpha)
        test.run()
        return test.result

    def spearman(
        self,
        a: str,
        b: str,
        data: pd.DataFrame = None,
        alpha: float = 0.05,
    ) -> SpearmanCorrelationResult:
        data = data if data is not None else self._data
        test = SpearmanCorrelationTest(data=data, a=a, b=b, alpha=alpha)
        test.run()
        return test.result

    def ttest(
        self,
        a: np.ndarray,
        b: np.ndarray,
        varname: str = None,
        alpha: float = 0.05,
        homoscedastic: bool = True,
    ) -> TTestResult:
        test = TTest(
            a=a,
            b=b,
            varname=varname,
            alpha=alpha,
            homoscedastic=homoscedastic,
        )
        test.run()
        return test.result
