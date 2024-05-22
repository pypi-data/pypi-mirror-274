#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/analysis/stats/inferential/base.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 22nd 2023 07:44:59 pm                                                #
# Modified   : Thursday October 19th 2023 08:01:04 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base classes used throughout the inferential package."""
from __future__ import annotations
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass

from studioai.analysis.stats.inferential.profile import StatTestProfile
from studioai import DataClass
from studioai.util.io import IOService

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
ANALYSIS_TYPES = {
    "univariate": "Univariate",
    "bivariate": "Bivariate",
    "multivariate": "Multivariate",
}


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestResult(DataClass):
    name: str = None
    hypothesis: str = None
    H0: str = None
    statistic: str = None
    value: float = 0
    pvalue: float = 0
    alpha: float = 0.05

    @abstractmethod
    def report(self) -> str:
        """Reports results in APA Style"""

    def _report_alpha(self) -> str:
        a = int(self.alpha * 100)
        return f"significant at {a}%."

    def _report_pvalue(self, pvalue: float) -> str:  # pragma: no cover
        """Rounds the pvalue in accordance with the APA Style Guide 7th Edition"""
        if pvalue < 0.001:
            return "p<.001"
        else:
            return "p=" + str(round(pvalue, 4))


# ------------------------------------------------------------------------------------------------ #
class StatisticalTest(ABC):
    """Base class for Statistical Tests"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""


# ------------------------------------------------------------------------------------------------ #
class StatAnalysis(ABC):
    """Base class for Statistical Measurer classes"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""
