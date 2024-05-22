#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/analysis/stats/inferential/correlation.py                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 08:15:08 pm                                                 #
# Modified   : Thursday October 19th 2023 08:01:24 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.analysis.visualize.visualizer import Visualizer
from studioai.analysis.container import AnalysisContainer
from studioai.analysis.stats.inferential.profile import StatTestProfile
from studioai.analysis.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)


# ================================================================================================ #
#                                  PEARSON'S CORRELATION                                           #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class PearsonCorrelationResult(StatTestResult):
    name: str = "Pearson Correlation Coefficient"
    data: pd.DataFrame = None
    a: str = None
    b: str = None
    dof: float = None
    strength: str = None
    low_ci: float = (None,)
    high_ci: float = (None,)

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[AnalysisContainer.visualizer]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(data=self.data, x=self.a, y=self.b, title=self.result)

    def report(self) -> str:
        return f"Pearson Correlation Test\nr({self.dof})={round(self.value,2)}, {self._report_pvalue(self.pvalue)}"


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class PearsonCorrelationTest(StatisticalTest):
    """Pearson correlation coefficient and p-value for testing non-correlation.

    The Pearson correlation coefficient [1] measures the linear relationship between two
    datasets. Like other correlation coefficients, this one varies between -1 and +1 with 0
    implying no correlation. Correlations of -1 or +1 imply an exact linear relationship.
    Positive correlations imply that as x increases, so does y. Negative correlations imply
    that as x increases, y decreases.

    This function also performs a test of the null hypothesis that the distributions underlying
    the samples are uncorrelated and normally distributed. (See Kowalski [3] for a discussion of
    the effects of non-normality of the input on the distribution of the correlation coefficient.)
    The p-value roughly indicates the probability of an uncorrelated system producing datasets
    that have a Pearson correlation at least as extreme as the one computed from these datasets.

    Args:
        data (pd.DataFrame): DataFrame containing at least two variables. Optional
        a (str): Keys in the DataFrame.
        b (str): Keys in the DataFrame.
        alpha (float): The test significance level. Default=0.05

    """

    __id = "pearson"

    def __init__(
        self,
        data: pd.DataFrame,
        a: str,
        b: str,
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._data = data
        self._a = a
        self._b = b
        self._alpha = alpha
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        try:
            pearson_result = stats.pearsonr(
                x=self._data[self._a].values, y=self._data[self._b].values, alternative="two-sided"
            )
        except Exception as e:  # pragma: no cover
            msg = f"Unable to calculate pearson correlation.\n{e}"
            self._logger.exception(msg)
            raise

        r = pearson_result.statistic
        pvalue = pearson_result.pvalue
        confidence_interval = pearson_result.confidence_interval(0.05)
        self._logger.debug(pearson_result)
        self._logger.debug(confidence_interval)

        dof = len(self._data) - 2

        # Create the result object.
        self._result = PearsonCorrelationResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            strength=self._interpret_r(r=r).capitalize(),
            low_ci=confidence_interval.low,
            high_ci=confidence_interval.high,
            value=r,
            dof=dof,
            pvalue=pvalue,
            data=self._data,
            a=self._a,
            b=self._b,
            alpha=self._alpha,
        )

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation."
        elif r >= 0.70:
            return f"high {direction} correlation."
        elif r >= 0.5:
            return f"moderate {direction} correlation."
        elif r >= 0.3:
            return f"low {direction} correlation."
        else:
            return "negligible correlation."


# ================================================================================================ #
#                                SPEARMAN'S CORRELATION                                            #
# ================================================================================================ #
# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class SpearmanCorrelationResult(StatTestResult):
    name: str = "Spearman Rank Correlation Coefficient"
    strength: str = None
    data: pd.DataFrame = None
    a: str = None
    b: str = None
    dof: float = None
    n: int = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[AnalysisContainer.visualizer]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(data=self.data, x=self.a, y=self.b, title=self.result)

    def report(self) -> str:
        return f"Spearman Correlation Test\nr({self.dof})={round(self.value,3)}, {self._report_pvalue(self.pvalue)}"


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class SpearmanCorrelationTest(StatisticalTest):
    __id = "spearman"

    def __init__(self, data: pd.DataFrame, a=str, b=str, alpha: float = 0.05) -> None:
        super().__init__()
        self._data = data
        self._a = a
        self._b = b
        self._alpha = alpha
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        r, pvalue = stats.spearmanr(
            a=self._data[self._a].values,
            b=self._data[self._b].values,
            alternative="two-sided",
            nan_policy="omit",
        )

        dof = len(self._data) - 2

        # Create the result object.
        self._result = SpearmanCorrelationResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            strength=self._interpret_r(r).capitalize(),
            value=r,
            pvalue=pvalue,
            dof=dof,
            data=self._data,
            a=self._a,
            b=self._b,
            alpha=self._alpha,
            n=len(self._data),
        )

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation"
        elif r >= 0.70:
            return f"high {direction} correlation"
        elif r >= 0.5:
            return f"moderate {direction} correlation"
        elif r >= 0.3:
            return f"low {direction} correlation"
        else:
            return "negligible correlation"
