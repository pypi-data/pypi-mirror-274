#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/preprocessing/encode.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday September 27th 2023 03:35:41 am                                           #
# Modified   : Thursday October 19th 2023 07:44:29 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pandas as pd
import numpy as np

from studioai.preprocessing.base import Encoder


# ------------------------------------------------------------------------------------------------ #
class RankFrequencyEncoder(Encoder):
    """Encodes and optionally standardizes data.

    This method uses both the value counts as well as the reverse rank of the value
    based upon its count. The encoded value is the sum of its reverse rank and the
    count. This prevents collisions that would normally happen with frequency based encoding.

    Booleans are encoded as 0 (False) or 1 (True)

    """

    def __init__(self) -> None:
        super().__init__()
        self._encodings = {}  # Nested dictionary of column > keys (orig) > values (encodings)
        self._decodings = {}  # Nested dictionary of column > keys (encodings) > values (orig)

    def fit(self, df: pd.DataFrame) -> Encoder:
        """Fits the data to the encoder

        Creates the mapping between the original and encoded values by column name.

        Args:
            df (pd.DataFrame): DataFrame to be fit to the encoder.
        """
        self._columns = df.columns
        self._dtypes = df.dtypes.astype(str).replace("0", "object").to_dict()
        for col in df.columns:
            self._fit_feature(df[col])
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the Data

        Args:
            df (pd.DataFrame): DataFrame to be encoded.
        """
        return df.replace(to_replace=self._encodings)

    def inverse_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert data back to the original representation.

        Args:
            df (pd.DataFrame): The encoded data.
        """
        df = df.round(0)
        df_out = df.replace(to_replace=self._decodings)
        df_out = df_out.astype(self._dtypes)
        return df_out

    def _fit_feature(self, feature: pd.Series) -> None:
        """Fits a single feature to the encoder."""
        if feature.dtype in ["object", "category"]:
            counts = (
                feature.value_counts(sort=True, ascending=True, normalize=False)
                .to_frame()
                .reset_index()
            )
            keys = counts[feature.name].values
            values = (counts["count"].astype("int64") + counts.index).values.astype("int64")
            self._set_map(col=feature.name, keys=keys, values=values)

        elif feature.dtype == "bool":
            keys = [True, False]
            values = [1, 0]
            self._set_map(col=feature.name, keys=keys, values=values)

    def _set_map(self, col: str, keys: np.ndarray, values: np.ndarray) -> None:
        """Updates the encodings/decodings map"""

        self._encodings[col] = {k: v for k, v in zip(keys, values)}
        self._decodings[col] = {k: v for k, v in zip(values, keys)}
