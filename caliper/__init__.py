# -*- coding: utf-8 -*-
# Caliper-python package
#
# Copyright (c) 2015 IMS Global Learning Consortium, Inc. All Rights Reserved.
# Trademark Information- http://www.imsglobal.org/copyright.html

# IMS Global Caliper Analytics™ APIs are publicly licensed as Open Source
# Software via GNU General Public License version 3.0 GPL v3. This license
# contains terms incompatible with use in closed-source software including a
# copyleft provision.

# IMS Global also makes available an Alternative License based on the GNU Lesser
# General Public License. LGPL v3 Licensees (via the Alternative License) are
# required to be IMS Global members. Membership in IMS is a commitment by a
# supplier to the IMS community for ongoing support for achieving "plug and play"
# integration.  IMS Membership dues pay for ongoing maintenance for the
# Alternative License to be applicable to updates to the Caliper Analytics
# APIs. The rationale for this dual-license approach and membership component is
# to help assure a requisite level of ongoing development, project management,
# and support for the software.

# Licensees of IMS Global Caliper Analytics APIs are strongly encouraged to
# become active contributors to the Caliper Analytics project and other projects
# within IMS Global. Prospective licensees should understand that their initial
# base contribution and ongoing membership fees are insufficient to fully fund
# the ongoing development and maintenance of Caliper APIs and that voluntary
# contributions are the primary "fuel" ensuring any open source project's
# viability. Contributions can include development, bug fixing, bug reporting,
# performance analysis, and other aspects of the overall development process.

# Contributor status at the "github" level will be individual-based. Contributors
# will need to sign an IMS Global Contributor License Agreement (CLA) that grants
# IMS Global a license to contributions.

# If you are interested in licensing the IMS Global Caliper Analytics APIs please
# email licenses@imsglobal.org

"""
Caliper library
~~~~~~~~~~~~~~~

Caliper is a library, written in python, to help you implement an IMS
Caliper-compliant sensor or endpoint for you learning services.

:copyright: (c) 2015 IMS Global Learning Consortium, Inc. All Rights Reserved.
:license: GPLv3 or LPGLv3. See LICENSE for more details.
"""
from __future__ import absolute_import

__title__ = 'caliper_python'
__version__ = '0.9.0'
__build__ = 0x000900
__author__ = 'IMS Global Learning Consortium, Inc.'
__license__ = 'GPLv3; LGPLv3 for IMS Global Members'
__copyright__ = 'Copyright 2015 IMS Global Learning Consortium, Inc.'

from caliper.sensor import Sensor as Sensor
import caliper.base as base


def build_default_sensor():
    return Sensor.fashion_default_sensor_with_config(config_options=base.HttpOptions())

def build_sensor_from_config(config_options):
    return Sensor.fashion_default_sensor_with_config(config_options=config_options)

def build_sensor_for_client(client):
    return Sensor.fashion_default_sensor_with_client(client=client)

## set default logging handler to avoid "No handler found" warnings.
## Thanks to Kenneth Reitz' requests library for this pattern

import logging
try: # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logger = logging.getLogger(__name__).addHandler(NullHandler())

