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

from libs.translations import *

def getWeatherCondition(condition):

    return {
        'clear-day': CLEAR_DAY,
        'clear-night': CLEAR_NIGHT,
        'partly-cloudy-day': PARTLY_COUDY_DAY,
        'partly-cloudy-night': PARTLY_COUDY_NIGHT,
        'cloudy': CLOUDY,
        'fog': FOG,
        'wind': WIND,
        'rain': RAIN,
        'sleet': SLEET,
        'snow': SNOW,
        'hail': HAIL,
        'thunderstorm': THUNDERSTORM,
        'null': 'N/A',

        None: 'N/A'
    }[condition]

def getWeatherConditionShort(condition):

    return {
        'clear-day': CLEAR,
        'clear-night': CLEAR,
        'partly-cloudy-day': CLOUDY,
        'partly-cloudy-night': CLOUDY,
        'cloudy': CLOUDY,
        'fog': FOG,
        'wind': WIND,
        'rain': RAIN,
        'sleet': SLEET,
        'snow': SNOW,
        'hail': HAIL,
        'thunderstorm': THUNDERSTORM,
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

    return {
        1: MONDAY,
        2: TUESDAY,
        3: WEDNESDAY,
        4: THURSDAY,
        5: FRIDAY,
        6: SATURDAY,
        7: SUNDAY
    }[day]

def getShortWeekDay(day):

    return {
        1: MONDAY_SHORT,
        2: TUESDAY_SHORT,
        3: WEDNESDAY_SHORT,
        4: THURSDAY_SHORT,
        5: FRIDAY_SHORT,
        6: SATURDAY_SHORT,
        7: SUNDAY_SHORT
    }[day]

# TODO: getShortLong Formats
# TODO: dateTime Conversions