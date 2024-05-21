#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/data/prep/base.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday September 27th 2023 03:35:41 am                                           #
# Modified   : Thursday September 28th 2023 03:15:10 am                                            #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Encoder(ABC):
    @abstractmethod
    def fit(self, df: pd.DataFrame) -> Encoder:
        """Fits the data to the encoder

        Creates the mapping between the original and encoded values by column name.

        Args:
            df (pd.DataFrame): DataFrame to be fit to the encoder.
        """

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the Data

        Args:
            df (pd.DataFrame): DataFrame to be encoded.
        """

    @abstractmethod
    def inverse_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert data back to the original representation.

        Args:
            df (pd.DataFrame): The encoded data.
        """

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits the data to the encoder, then transforms the data

        Args:
            df (pd.DataFrame): The encoded data.
        """
        self.fit(df=df)
        return self.transform(df=df)
