# -*- coding: utf-8 -*-
# Copyright 2024 WebEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import base64
import urllib
import time

from urllib.parse import urlparse
from datetime import datetime


def base64Encode(s):
    b = s.encode("ascii")

    encoded = base64.b64encode(b)
    return encoded.decode("ascii")

def base64Decode(s):
    b = s.encode("ascii")
    decoded = base64.b64decode(b)
    return decoded.decode("ascii")

def get_query_args(s_args):
    args = urllib.parse.parse_qs(s_args)

    for key in args:
        args[key] = args[key][0]
    return args

def datetimeToString(dt, dstFormat):
    return dt.strftime(dstFormat)

def getDateTime(strDateTime, strFormat):
    if strDateTime is not None:
        return datetime(*(time.strptime(strDateTime, strFormat)[0:6]))
    return None