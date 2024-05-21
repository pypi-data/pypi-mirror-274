#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Artificial Intelligence & Data Science Studio                                       #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /studioai/analysis/container.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/studioai                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 09:31:46 am                                               #
# Modified   : Thursday October 19th 2023 07:34:06 pm                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
from dependency_injector import containers, providers

from studioai.analysis.visualize.visualizer import SeabornCanvas, Visualizer


# ------------------------------------------------------------------------------------------------ #
#                                    VISUALIZER CONTAINER                                          #
# ------------------------------------------------------------------------------------------------ #
class AnalysisContainer(containers.DeclarativeContainer):
    canvas = providers.Factory(SeabornCanvas)
    visualizer = providers.Factory(Visualizer, canvas=canvas)
