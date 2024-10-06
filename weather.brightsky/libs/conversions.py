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
import math


def getWeatherCondition(condition):

    # TODO: translations

    return {
        'clear-day': 'clear-day',
        'clear-night': 'clear-night',
        'partly-cloudy-day': 'partly-cloudy-day',
        'partly-cloudy-night': 'partly-cloudy-night',
        'cloudy': 'cloudy',
        'fog': 'fog',
        'wind': 'wind',
        'rain': 'rain',
        'sleet': 'sleet',
        'snow': 'snow',
        'hail': 'hail',
        'thunderstorm': 'thunderstorm',
        'null': 'N/A',

        None: 'N/A'
    }[condition]


def getWindDirection(deg):
    if deg is None:
        return 10006
    if deg >= 349 or deg <= 11:
        return 71
    elif 12 <= deg <= 33:
        return 72
    elif 34 <= deg <= 56:
        return 73
    elif 57 <= deg <= 78:
        return 74
    elif 79 <= deg <= 101:
        return 75
    elif 102 <= deg <= 123:
        return 76
    elif 124 <= deg <= 146:
        return 77
    elif 147 <= deg <= 168:
        return 78
    elif 169 <= deg <= 191:
        return 79
    elif 192 <= deg <= 213:
        return 80
    elif 214 <= deg <= 236:
        return 81
    elif 237 <= deg <= 258:
        return 82
    elif 259 <= deg <= 281:
        return 83
    elif 282 <= deg <= 303:
        return 84
    elif 304 <= deg <= 326:
        return 85
    elif 327 <= deg <= 348:
        return 86

def getWindchill(temperature, wind_speed):
    if temperature is not None and wind_speed is not None:
        return 13.12 + 0.6215 * temperature + (0.3965 * temperature -11.37) * math.pow(wind_speed, 0.16)

    return 'N/A'

def getWeatherConditionIcon(condition):
    return {
        'clear-day': '32.png',
        'clear-night': '31.png',
        'partly-cloudy-day': '30.png',
        'partly-cloudy-night': '29.png',
        'cloudy': '26.png',
        'fog': '20.png',
        'wind': '24.png',
        'rain': '11.png',
        'sleet': '5.png',
        'snow': '16.png',
        'hail': '17.png',
        'thunderstorm': '3.png',
        'null': 'N/A',

        None: 'N/A'
    }[condition]

def getLongWeekDay(day):

    # TODO: translations

    return {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }[day]

def getShortWeekDay(day):

    # TODO: translations

    return {
        1: 'Mon',
        2: 'Tues',
        3: 'Wed',
        4: 'Thur',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'
    }[day]

# TODO: getShortLong Formats
# TODO: dateTime Conversions