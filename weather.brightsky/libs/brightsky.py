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
import json
import sys

import requests

from libs.conversions import getWeatherCondition, getWindDirection, getWindchill, getWeatherConditionIcon
from libs.core.brightskyAPI import brightskyAPI
from libs.core.nominatimAPI import nominatimAPI
from libs.kodion.gui_manager import *
from libs.kodion.addon import Addon
from libs.translations import *



class brightsky:

    def __init__(self):
        # -- Constants ----------------------------------------------
        self._ADDON_ID = 'weather.brightsky'

        width = getScreenWidth()
        self._addon = Addon(self._ADDON_ID)

        self._window = getWindow(12600)

        self._NAME = self._addon.getAddonInfo('name')
        self._FANART = self._addon.getAddonInfo('fanart')
        self._ICON = self._addon.getAddonInfo('icon')
        self._POSTERWIDTH = int(width / 3)
        self._DEFAULT_IMAGE_URL = ''
        self._t = Translations(self._addon)

        self._guiManager = GuiManager(0, self._ADDON_ID, self._DEFAULT_IMAGE_URL, self._FANART)

    def getLocation(self, param):
        locationId = param
        keyword = getKeyboardText(heading=self._t.getString(LOCATION_INPUT))
        if keyword is not None and keyword:

            try:
                api = nominatimAPI()
                responseCode, content = api.search(quickSearch=keyword)

                if responseCode == 200:
                    if len(content) > 0:

                        labels = []
                        locations_info = []
                        locations = []
                        for location in content:
                            labels.append(location['display_name'])
                            locations_info.append({ 'addresstype': location['addresstype'],
                                                    'name': location['name']
                                                    })

                            locations.append({ 'display_name': location['display_name'],
                                               'short_name': '',
                                               'lat': location['lat'],
                                               'lon': location['lon']
                                               })

                        result = self._guiManager.MsgBoxSelect(self._t.getString(LOCATION_SELECT), labels)
                        if result != -1:
                            city = labels[result]
                            location_info = locations_info[result]
                            location = locations[result]
                            if location_info['addresstype'] == 'city' and location_info['name'] != '':
                                city = location_info['name']
                            else:

                                responsecode, content = api.reverse(lat=location['lat'], lon= location['lon'], addressdetails=1)
                                if responseCode == 200:

                                    xbmc.log(json.dumps(content))

                                    if 'address' in content and 'city' in content['address'] and content['address']['city'] != '':
                                        city = content['address']['city']

                            location['short_name'] = city

                            self._addon.setSetting(f'location{locationId}', labels[result])
                            self._addon.setSetting(f'locationId{locationId}', self._base64Encode(json.dumps(location)))


                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NO_LOCATION_FOUND))
                else:
                    if 'error' in content and 'message' in content['error']:
                        self._guiManager.setToastNotification('error', content['error']['message'])
                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NOMINATIM))

            except requests.exceptions.ConnectionError as e:
                self._guiManager.setToastNotification('error', e.response.text)

    def clear_current(self):
        pass

    def getWeather(self, param):
        success = False
        locationId = param
        location = json.loads(self._base64Decode(self._addon.getSetting(f'locationId{locationId}')))
        if location:

            try:

                api = brightskyAPI()
                responseCode, content = api.currentWeather(location)

                xbmc.log(json.dumps(content))

                if responseCode == 200:


                    # Current.FeelsLike

                    # Current.ConditionIcon(eg.resource: // resource.images.weathericons.default / 28.png)
                    # Current.FanartCode

                    if 'weather' in content:
                        success = True
                        weather = content['weather']

                        self._window.setProperty('Current.Location', location.get('short_name', location.get('display_name')))
                        self._window.setProperty('Current.Condition', getWeatherCondition(weather.get('icon')))
                        self._window.setProperty('Current.Temperature', str(weather.get('temperature', 'N/A')))
                        self._window.setProperty('Current.Wind', str(weather.get('wind_speed_30', 'N/A')))
                        self._window.setProperty('Current.WindDirection', xbmc.getLocalizedString(getWindDirection(weather.get('wind_direction_30'))))
                        self._window.setProperty('Current.Humidity', str(weather.get('relative_humidity', 'N/A')))
                        self._window.setProperty('Current.DewPoint', str(weather.get('dew_point', 'N/A')))
                        self._window.setProperty('Current.FeelsLike', str(getWindchill(weather.get('temperature'), weather.get('wind_speed_30'))))
                        self._window.setProperty('Current.ConditionIcon', getWeatherConditionIcon(weather.get('icon')))

                        # self._window.setProperty(f'Location{locationId}', self._addon.getSetting(f'location{locationId}'))
                        # self._window.setProperty('Locations', '1')

                else:
                    if 'error' in content and 'message' in content['error']:
                        self._guiManager.setToastNotification('error', content['error']['message'])
                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_BRIGHTSKY))

            except requests.exceptions.ConnectionError as e:
                self._guiManager.setToastNotification('error', e.response.text)


        if not success:
           self.clear_current()

    @staticmethod
    def _base64Encode(s):
        b = s.encode("ascii")

        encoded = base64.b64encode(b)
        return encoded.decode("ascii")

    @staticmethod
    def _base64Decode(s):
        b = s.encode("ascii")
        decoded = base64.b64decode(b)
        return decoded.decode("ascii")


    @staticmethod
    def _get_query_args(s_args):
        args = urllib.parse.parse_qs(s_args)

        for key in args:
            args[key] = args[key][0]
        return args


    def run(self):
        if sys.argv[1].isnumeric():
            method = 'weather_request'
            param = int(sys.argv[1])
        else:
            args = self._get_query_args(sys.argv[1])
            method = args.get('action')
            param = args.get('id')

        if method is not None:
            {
                'location': self.getLocation,
                'weather_request': self.getWeather

            }[method](param=param)


