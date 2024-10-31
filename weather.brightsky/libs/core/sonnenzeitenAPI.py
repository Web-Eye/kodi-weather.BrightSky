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

import json
import requests
import tzlocal

class sonnenzeitenAPI:

    def __init__(self):
        self._baseURL = 'https://api.sunrise-sunset.org/'
        self._request_timeout = 3
        self._request_headers =  {
                    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }

        self._tzid = tzlocal.get_localzone_name()

    def solarTimes(self, lat, lon, date=None):
        if lat is not None and lon is not None:
            url = self._baseURL + f'json?lat={lat}&lng={lon}&formatted=0&tzid={self._tzid}'

            if date is not None:
                url = f'{url}&date={date}'

            response = requests.get(url, timeout=self._request_timeout, headers=self._request_headers)
            return response.status_code, json.loads(response.content)