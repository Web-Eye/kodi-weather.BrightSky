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
import sys
import datetime

import requests

from libs.common.tools import get_query_args, base64Decode, base64Encode, datetimeToString, getDateTime
from libs.conversions import getWeatherCondition, getWindDirection, getWindchill, getWeatherConditionIcon, \
    getLongWeekDay, getShortWeekDay, getWeatherConditionShort
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

        self._tempunit = xbmc.getRegion('tempunit')
        self._speedunit = xbmc.getRegion('speedunit')
        self._datelong = xbmc.getRegion('datelong')
        self._dateShort = xbmc.getRegion('dateshort')
        self._time = xbmc.getRegion('time')
        self._meridiem = xbmc.getRegion('meridiem')

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

                                    if 'address' in content and 'city' in content['address'] and content['address']['city'] != '':
                                        city = content['address']['city']

                            location['short_name'] = city

                            self._addon.setSetting(f'location{locationId}', labels[result])
                            self._addon.setSetting(f'locationId{locationId}', base64Encode(json.dumps(location)))


                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NO_LOCATION_FOUND))
                else:
                    if 'error' in content and 'message' in content['error']:
                        self._guiManager.setToastNotification('error', content['error']['message'])
                    else:
                        self._guiManager.setToastNotification('error', self._t.getString(ERROR_NOMINATIM))

            except requests.exceptions.ConnectionError as e:
                self._guiManager.setToastNotification('error', e.response.text)

    def getMaxLocations(self):
        result = 0
        for i in range(1, 6):
            if self._addon.getSetting(f'location{i}') != '' and self._addon.getSetting(f'locationId{i}') != '':
                result += 1


        return result

    def clear_current(self):
        pass

    def getToday(self, location):
        pass

        # Today.IsFetched
        # Today.Sunrise
        # Today.Sunset

    def getWeatherCurrent(self, api, location):
        success = False

        self._window.setProperty('Current.IsFetched', 'false')

        try:

            responseCode, content = api.currentWeather(location)
            if responseCode == 200:

                if 'weather' in content:
                    success = True
                    weather = content['weather']

                    self._window.setProperty('Current.Location', location.get('short_name', location.get('display_name')))
                    self._window.setProperty('Current.Condition', self._t.getString(getWeatherCondition(weather.get('icon'))))
                    self._window.setProperty('Current.Temperature', str(weather.get('temperature', 'N/A')))
                    self._window.setProperty('Current.Wind', str(weather.get('wind_speed_30', 'N/A')))
                    self._window.setProperty('Current.WindDirection', xbmc.getLocalizedString(getWindDirection(weather.get('wind_direction_30'))))
                    self._window.setProperty('Current.Humidity', str(weather.get('relative_humidity', 'N/A')))
                    self._window.setProperty('Current.DewPoint', str(weather.get('dew_point', 'N/A')))
                    self._window.setProperty('Current.FeelsLike', str(getWindchill(weather.get('temperature'), weather.get('wind_speed_30'))))
                    self._window.setProperty('Current.OutlookIcon', getWeatherConditionIcon(weather.get('icon')))
                    self._window.setProperty('Current.Precipitation', str(weather.get('precipitation_60')) + 'mm')
                    self._window.setProperty('Current.Pressure', str(weather.get('pressure_msl')))
                    self._window.setProperty('Current.Cloudiness', str(weather.get('cloud_cover')))
                    self._window.setProperty('Current.WindGust', str(weather.get('wind_gust_speed_30')))
                    self._window.setProperty('Current.IsFetched', 'true')

                    success = True

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
    def getDailyOutlook(d):
        max_key = ''
        max_entity = 0
        for key in d:
            if d[key] > max_entity:
                max_key = key
                max_entity = d[key]

        return max_key

    def getWeatherForecast(self, api, location):
        success = False

        self._window.setProperty('Daily.IsFetched', 'false')
        self._window.setProperty('36Hour.IsFetched', 'false')
        self._window.setProperty('Weekend.IsFetched', 'false')
        self._window.setProperty('Hourly.IsFetched', 'false')

        try:

            startDate = datetime.date.today()
            endDate = startDate + datetime.timedelta(days=16)

            responseCode, content = api.forecast(location=location, startDate=startDate, endDate=endDate)
            if responseCode == 200:

                if 'weather' in content:
                    success = True
                    accumulated = { 'daily': {},
                                    'hourly': {}
                                    }

                    day_count = 0
                    hour_count = 0
                    now_datetime = datetime.datetime.today() - datetime.timedelta(hours=1)

                    for item in content['weather']:

                        item_datetime = getDateTime(item['timestamp'], '%Y-%m-%dT%H:%M:%S%z')
                        day_timestamp = datetimeToString(item_datetime, '%Y-%m-%d')
                        hour_timestamp = datetimeToString(item_datetime, '%Y-%m-%d %H:%M:%S')

                        doHour = item_datetime > now_datetime and item_datetime.hour % 3 == 0 and hour_count < 35

                        temperature = item.get('temperature')

                        if day_timestamp not in accumulated['daily']:
                            day_count += 1
                            if day_count < 17:
                                accumulated['daily'][day_timestamp] = {}
                                accumulated['daily'][day_timestamp]['LongDay'] = self._t.getString(getLongWeekDay(item_datetime.isoweekday()))
                                accumulated['daily'][day_timestamp]['ShortDay'] = self._t.getString(getShortWeekDay(item_datetime.isoweekday()))
                                accumulated['daily'][day_timestamp]['LongDate'] = datetimeToString(item_datetime, self._datelong)
                                accumulated['daily'][day_timestamp]['ShortDate'] = datetimeToString(item_datetime, self._dateShort)
                                accumulated['daily'][day_timestamp]['HighTemperature'] = temperature
                                accumulated['daily'][day_timestamp]['LowTemperature'] = temperature
                                accumulated['daily'][day_timestamp]['Outlook'] = {}
                                accumulated['daily'][day_timestamp]['Outlook'][str(item.get('icon'))] = 1

                                # TODO: Humidity, precipitation, WindSpeed, WindDirection, WindDegree, TempMorn,
                                #  TempDay, TempEve, TempNight, DewPoint, WindGust, Pressure, Cloudiness, Precipitation

                        else:
                            if temperature > accumulated['daily'][day_timestamp]['HighTemperature']:
                                accumulated['daily'][day_timestamp]['HighTemperature'] = temperature

                            if temperature < accumulated['daily'][day_timestamp]['LowTemperature']:
                                accumulated['daily'][day_timestamp]['LowTemperature'] = temperature

                            accumulated['daily'][day_timestamp]['Outlook'][str(item.get('icon'))] = accumulated['daily'][day_timestamp]['Outlook'].get(str(item.get('icon')), 0) + 1

                        if doHour and hour_timestamp not in accumulated['hourly']:
                            hour_count += 1
                            accumulated['hourly'][hour_timestamp] = {}
                            accumulated['hourly'][hour_timestamp]['Time'] = datetimeToString(item_datetime, '%H:%M')
                            accumulated['hourly'][hour_timestamp]['LongDate'] = day_timestamp
                            accumulated['hourly'][hour_timestamp]['ShortDate'] = day_timestamp
                            accumulated['hourly'][hour_timestamp]['Outlook'] = self._t.getString( getWeatherCondition(item.get('icon')))
                            accumulated['hourly'][hour_timestamp]['ShortOutlook'] = self._t.getString(getWeatherConditionShort(item.get('icon')))
                            accumulated['hourly'][hour_timestamp]['OutlookIcon'] = getWeatherConditionIcon(item.get('icon'))
                            accumulated['hourly'][hour_timestamp]['WindSpeed'] = str(item.get('wind_speed'))
                            accumulated['hourly'][hour_timestamp]['WindDirection'] = xbmc.getLocalizedString(getWindDirection(item.get('wind_direction')))
                            accumulated['hourly'][hour_timestamp]['WindDegree'] = str(item.get('wind_direction'))
                            accumulated['hourly'][hour_timestamp]['WindDegree'] = str(item.get('wind_gust_speed'))
                            accumulated['hourly'][hour_timestamp]['Humidity'] = str(item.get('relative_humidity'))
                            accumulated['hourly'][hour_timestamp]['Temperature'] = str(item.get('temperature')) + self._tempunit
                            accumulated['hourly'][hour_timestamp]['DewPoint'] = str(item.get('dew_point'))
                            accumulated['hourly'][hour_timestamp]['FeelsLike'] = str(getWindchill(item.get('temperature'), item.get('wind_speed')))
                            accumulated['hourly'][hour_timestamp]['Pressure'] = str(item.get('pressure_msl'))
                            accumulated['hourly'][hour_timestamp]['Cloudiness'] = str(item.get('cloud_cover'))
                            accumulated['hourly'][hour_timestamp]['Precipitation'] = str(item.get('precipitation')) + 'mm'

                        if day_count > 16 and hour_count > 34:
                            break

                    success = len(accumulated['daily']) > 0 or len(accumulated['hourly']) > 0

                    if len(accumulated['daily']) > 0:
                        self._window.setProperty('Daily.IsFetched', 'true')
                        i = 0
                        for item in accumulated['daily'].values():
                            i += 1
                            for key in item.keys():

                                if key == 'HighTemperature':
                                    self._window.setProperty(f'Daily.{i}.{key}', str(item[key]) + self._tempunit)
                                elif key == 'LowTemperature':
                                    self._window.setProperty(f'Daily.{i}.{key}', str(item[key]) + self._tempunit)
                                elif key == 'Outlook':
                                    outlook = self.getDailyOutlook(item[key])
                                    self._window.setProperty(f'Daily.{i}.{key}', self._t.getString(getWeatherCondition(outlook)))
                                    self._window.setProperty(f'Daily.{i}.ShortOutlook', self._t.getString(getWeatherConditionShort(outlook)))
                                    self._window.setProperty(f'Daily.{i}.OutlookIcon', getWeatherConditionIcon(outlook))

                                else:
                                    self._window.setProperty(f'Daily.{i}.{key}', str(item[key]))

                    if len(accumulated['hourly']) > 0:
                        self._window.setProperty('Hourly.IsFetched', 'true')
                        i = 0
                        for item in accumulated['hourly'].values():
                            i += 1
                            for key in item.keys():
                                self._window.setProperty(f'Hourly.{i}.{key}', str(item[key]))


        except requests.exceptions.ConnectionError as e:
            self._guiManager.setToastNotification('error', e.response.text)

        if not success:
            self.clear_current()


    def getWeather(self, param):

        self._window.setProperty('Weather.IsFetched', 'false')
        self._window.setProperty('WeatherProvider', 'Bright Sky API')
        # self._window.setProperty('WeatherProviderLogo', 'false')

        locationId = param
        location = json.loads(base64Decode(self._addon.getSetting(f'locationId{locationId}')))
        if location:

            self.getToday(location)

            api = brightskyAPI()
            self.getWeatherCurrent(api, location)
            self.getWeatherForecast(api, location)

            self._window.setProperty(f'Location{locationId}', location['display_name'])
            self._window.setProperty('Locations', str(self.getMaxLocations()))
            self._window.setProperty('Weather.IsFetched', 'true')


    def run(self):
        if sys.argv[1].isnumeric():
            method = 'weather_request'
            param = int(sys.argv[1])
        else:
            args = get_query_args(sys.argv[1])
            method = args.get('action')
            param = args.get('id')

        if method is not None:
            {
                'location': self.getLocation,
                'weather_request': self.getWeather

            }[method](param=param)


