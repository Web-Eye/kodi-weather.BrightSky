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

class nominatimAPI:

    def __init__(self):
        self._baseURL = 'https://nominatim.openstreetmap.org/'
        self._request_timeout = 3
        self._request_headers =  {
                    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }

    def search(self, fmt='json', quickSearch=None, detailSearch=None):
        if fmt and (quickSearch is not None or detailSearch is not None):
            url = self._baseURL + f'search?format={fmt}'
            if quickSearch:
                url = f'{url}&q={quickSearch}'
            elif detailSearch is not None:
                if 'amenity' in quickSearch:
                    amenity = detailSearch['amenity']
                    url = f'{url}&amenity={amenity}'
                if 'street' in quickSearch:
                    street = detailSearch['street']
                    url = f'{url}&street={street}'
                if 'city' in quickSearch:
                    city = detailSearch['city']
                    url = f'{url}&city={city}'
                if 'county' in quickSearch:
                    county = detailSearch['county']
                    url = f'{url}&county={county}'
                if 'state' in quickSearch:
                    state = detailSearch['state']
                    url = f'{url}&state={state}'
                if 'postalcode' in quickSearch:
                    postalcode = detailSearch['postalcode']
                    url = f'{url}&postalcode={postalcode}'

            response = requests.get(url, timeout=self._request_timeout, headers=self._request_headers )
            return response.status_code, json.loads(response.content)



