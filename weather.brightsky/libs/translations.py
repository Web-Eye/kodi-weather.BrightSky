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

class Translations:

    def __init__(self, addon):
        self._language = addon.getLocalizedString

    def getString(self, name):

        return {
            LOCATION_INPUT:             self._language(30100),
            LOCATION_SELECT:            self._language(30101),
            ERROR:                      self._language(30600),
            ERROR_NOMINATIM:            self._language(30601),
            ERROR_NO_LOCATION_FOUND:    self._language(30602)

        }[name]
