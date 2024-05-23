# pyAirlock: Python library for Airlock products
# 
# Copyright (c) 2019-2024 Urs Zurbuchen <info@airlock.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
Handle IP List

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#ip-address-list) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class IPList( element.ConfigElement ):
    """
    CRUD and connection management REST API for IP address lists
    """
    ELEMENT_PATH = "ip-address-list"
    RELATIONSHIPS = ["mappings-whitelist", "mappings-backlist", "mappings-backlist-exception",
                     "mappings-request-frequency-filter-whitelist"]
    
