# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

"""
The Q-CTRL QUA Adapter package allows you to integrate Boulder Opal with the QUA
quantum computing language.
"""

__author__ = "Q-CTRL <support@q-ctrl.com>"
__version__ = "0.5.0"

from .qua_config_gen import add_pulse_to_config

__all__ = ["add_pulse_to_config"]
