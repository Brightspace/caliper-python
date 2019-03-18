# -*- coding: utf-8 -*-
# Caliper-python package
#
# This file is part of the IMS Caliper Analytics(tm) and is licensed to IMS
# Global Learning Consortium, Inc. (http://www.imsglobal.org) under one or more
# contributor license agreements. See the NOTICE file distributed with this
# work for additional information.
#
# IMS Caliper is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# IMS Caliper is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#
"""
Caliper library
~~~~~~~~~~~~~~~

Caliper is a library, written in python, to help you implement an IMS
Caliper-compliant sensor or endpoint for you learning services.

:license: See NOTICE for license details.
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
from future.standard_library import install_aliases
install_aliases()
from builtins import *

__title__ = 'imsglobal_caliper'
__version__ = '1.1.10.2'
__build__ = 0x01011002
__author__ = 'IMS Global Learning Consortium, Inc.'
__license__ = 'LGPLv3'

import logging, os

from caliper.base import HttpOptions as HttpOptions
from caliper.constants import CALIPER_VERSION as CALIPER_VERSION
from caliper.sensor import Sensor as Sensor, SimpleSensor as SimpleSensor
__all__ = ['Sensor', 'SimpleSensor', 'HttpOptions', CALIPER_VERSION]


def build_default_sensor(sensor_id=None):
    return Sensor.fashion_sensor_with_config(
        config_options=HttpOptions(optimize_serialization=True), sensor_id=sensor_id)


def build_default_sensor_for_client(client=None, sensor_id=None):
    return Sensor.fashion_default_sensor_with_client(client=client, sensor_id=sensor_id)


def build_sensor_from_config(config_options=None, sensor_id=None):
    return Sensor.fashion_sensor_with_config(
        config_options=config_options or HttpOptions(optimize_serialization=True),
        sensor_id=sensor_id)

def build_simple_sensor(config_options=None, sensor_id=None):
    return SimpleSensor.fashion_simple_sensor(config_options=config_options, sensor_id=sensor_id)


## set default logging handler to avoid "No handler found" warnings.
## Thanks to Kenneth Reitz' requests library for this pattern
logger = logging.getLogger(__name__).addHandler(logging.NullHandler())
