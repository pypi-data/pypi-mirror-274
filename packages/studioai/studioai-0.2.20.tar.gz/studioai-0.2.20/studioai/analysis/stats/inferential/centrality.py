#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /studioai/analysis/stats/inferential/centrality.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 11:41:00 pm                                                 #
# Modified   : Thursday October 19th 2023 07:34:06 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import numpy as np
from scipy import stats
from dependency_injector.wiring import inject, Provide

from studioai.analysis.container import AnalysisContainer
from studioai.analysis.visualize.visualizer import Visualizer
from studioai.analysis.stats.inferential.profile import StatTestProfile
from studioai.analysis.stats.inferential.base import (
    StatTestResult,
    StatisticalTest,
)

from studioai.analysis.stats.descriptive.continuous import ContinuousStats


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class TTestResult(StatTestResult):
    name: str = "Student's t-test"
    dof: int = None
    homoscedastic: bool = None
    a: np.ndarray = None
    a_name: str = None
    b: np.ndarray = None
    b_name: str = None
    varname: str = None
    a_stats: ContinuousStats = None
    b_stats: ContinuousStats = None

    @inject
    def __post_init__(self, visualizer: Visualizer = Provide[AnalysisContainer.visualizer]) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = self.result()
        self.visualizer.ttestplot(statistic=self.value, dof=self.dof, alpha=self.alpha, title=title)

    def report(self) -> str:
        return f"{self.name}\na: (N = {self.a_stats.count}, M = {round(self.a_stats.mean,2)}, SD = {round(self.a_stats.std,2)})\nb: (N = {self.b_stats.count}, M = {round(self.b_stats.mean,2)}, SD = {round(self.b_stats.std,2)})\nt({self.dof}) = {round(self.value,2)}, {self._report_pvalue(self.pvalue)} {self._report_alpha()}"


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class TTest(StatisticalTest):
    """Calculate the T-test for the means of two independent samples of scores.

    This is a test for the null hypothesis that 2 independent samples have identical average
    (expected) values. This test assumes that the populations have identical variances by default.

    Args:
        a: (np.ndarray): An array containing the first of two independent samples.
        b: (np.ndarray): An array containing the second of two independent samples.
        alpha (float): The level of statistical significance for inference.
        homoscedastic (bool): If True, perform a standard independent 2 sample test t
            hat assumes equal population variances. If False, perform Welch’s
            t-test, which does not assume equal population variance.

    """

    __id = "t2"

    def __init__(
        self,
        a: np.ndarray,
        b: np.ndarray,
        varname: str = None,
        alpha: float = 0.05,
        homoscedastic: bool = True,
    ) -> None:
        super().__init__()
        self._a = a
        self._b = b
        self._varname = varname
        self._alpha = alpha
        self._homoscedastic = homoscedastic
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
        """Executes the TTest."""

        statistic, pvalue = stats.ttest_ind(a=self._a, b=self._b, equal_var=self._homoscedastic)

        a_stats = ContinuousStats.describe(x=self._a)
        b_stats = ContinuousStats.describe(x=self._b)

        dof = len(self._a) + len(self._b) - 2

        # Create the result object.
        self._result = TTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            homoscedastic=self._homoscedastic,
            varname=self._varname,
            dof=dof,
            value=np.abs(statistic),
            alpha=self._alpha,
            pvalue=pvalue,
            a=self._a,
            b=self._b,
            a_stats=a_stats,
            b_stats=b_stats,
        )
