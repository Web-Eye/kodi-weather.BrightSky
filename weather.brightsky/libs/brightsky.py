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
import xbmc
import requests

from libs.core.nominatimAPI import nominatimAPI
from libs.kodion.gui_manager import *
from libs.kodion.addon import Addon
from libs.translations import *
from xbmc import LOGINFO, LOGDEBUG


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
                        locations = []
                        for location in content:
                            labels.append(location['display_name'])
                            locations.append({ 'lat': location['lat'],
                                               'lon': location['lon']
                                               })

                        result = self._guiManager.MsgBoxSelect(self._t.getString(LOCATION_SELECT), labels)
                        if result != -1:
                            self._addon.setSetting(f'location{locationId}', labels[result])
                            self._addon.setSetting(f'locationId{locationId}', self._base64Encode(json.dumps(locations[result])))


                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NO_LOCATION_FOUND))
                else:
                    if 'error' in content and 'message' in content['error']:
                        self._guiManager.setToastNotification('error', content['error']['message'])
                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NOMINATIM))

            except requests.exceptions.ConnectionError as e:
                self._guiManager.setToastNotification('error', e.response.text)

    def getWeather(self, param):
        locationId = param
        location = json.loads(self._base64Decode(self._addon.getSetting(f'locationId{locationId}')))
        if location:
            pass

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


