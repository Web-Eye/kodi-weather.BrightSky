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
#

LOCATION_INPUT = 'LOCATION_INPUT'
LOCATION_SELECT = 'LOCATION_SELECT'
ERROR = 'ERROR'
ERROR_NOMINATIM = 'ERROR_NOMINATIM'
ERROR_NO_LOCATION_FOUND = 'ERROR_NO_LOCATION_FOUND'
ERROR_BRIGHTSKY = 'ERROR_BRIGHTSKY'

MONDAY = 'MONDAY'
TUESDAY = 'TUESDAY'
WEDNESDAY = 'WEDNESDAY'
THURSDAY = 'THURSDAY'
FRIDAY = 'FRIDAY'
SATURDAY = 'SATURDAY'
SUNDAY = 'SUNDAY'

MONDAY_SHORT = 'MONDAY_SHORT'
TUESDAY_SHORT = 'TUESDAY_SHORT'
WEDNESDAY_SHORT = 'WEDNESDAY_SHORT'
THURSDAY_SHORT = 'THURSDAY_SHORT'
FRIDAY_SHORT = 'FRIDAY_SHORT'
SATURDAY_SHORT = 'SATURDAY_SHORT'
SUNDAY_SHORT = 'SUNDAY_SHORT'

TODAY = 'TODAY'
TOMORROW = 'TOMORROW'

CLEAR = 'CLEAR'
CLEAR_DAY = 'CLEAR_DAY'
CLEAR_NIGHT = 'CLEAR_NIGHT'
PARTLY_COUDY_DAY = 'PARTLY_COUDY_DAY'
PARTLY_COUDY_NIGHT = 'PARTLY_COUDY_NIGHT'
CLOUDY = 'CLOUDY'
FOG = 'FOG'
WIND = 'WIND'
RAIN = 'RAIN'
SLEET = 'SLEET'
SNOW = 'SNOW'
HAIL = 'HAIL'
THUNDERSTORM = 'THUNDERSTORM'




class Translations:

    def __init__(self, addon):
        self._language = addon.getLocalizedString

    def getString(self, name):

        return {
            LOCATION_INPUT:             self._language(30100),
            LOCATION_SELECT:            self._language(30101),
            ERROR:                      self._language(30600),
            ERROR_NOMINATIM:            self._language(30601),
            ERROR_NO_LOCATION_FOUND:    self._language(30602),
            ERROR_BRIGHTSKY:            self._language(30603),
            MONDAY:                     self._language(30700),
            TUESDAY:                    self._language(30701),
            WEDNESDAY:                  self._language(30702),
            THURSDAY:                   self._language(30703),
            FRIDAY:                     self._language(30704),
            SATURDAY:                   self._language(30705),
            SUNDAY:                     self._language(30706),
            MONDAY_SHORT:               self._language(30707),
            TUESDAY_SHORT:              self._language(30708),
            WEDNESDAY_SHORT:            self._language(30709),
            THURSDAY_SHORT:             self._language(30710),
            FRIDAY_SHORT:               self._language(30711),
            SATURDAY_SHORT:             self._language(30712),
            SUNDAY_SHORT:               self._language(30713),
            TODAY:                      self._language(30714),
            TOMORROW:                   self._language(30715),
            CLEAR_DAY:                  self._language(30800),
            CLEAR_NIGHT:                self._language(30801),
            PARTLY_COUDY_DAY:           self._language(30802),
            PARTLY_COUDY_NIGHT:         self._language(30803),
            CLOUDY:                     self._language(30804),
            FOG:                        self._language(30805),
            WIND:                       self._language(30806),
            RAIN:                       self._language(30807),
            SLEET:                      self._language(30808),
            SNOW:                       self._language(30809),
            HAIL:                       self._language(30810),
            THUNDERSTORM:               self._language(30811),
            CLEAR:                      self._language(30812)

        }[name]
