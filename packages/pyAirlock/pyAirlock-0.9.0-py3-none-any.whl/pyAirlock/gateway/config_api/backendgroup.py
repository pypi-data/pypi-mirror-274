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
Handle Back-end Group

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#back-end-group) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class BackendGroup( element.ConfigElement ):
    """
    CRUD and connection management REST API for backend groups
    """

    ELEMENT_PATH = "back-end-group"
    RELATIONSHIPS = ["mapping", "kerberos-environment", "client-certificate"]

    def mode( self, id: int, data: dict ) -> bool:
        """
        Use REST API to set mode of backend host
        
        Parameters:
        
        * `id`: identifier of configuration element to retrieve
        * `data`: dict with backend host settings. Please refer to Airlock Gateway REST API documentation (https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#change-mode-of-a-back-end-host) for details.
        """
        return self.post( "host-mode", id=id, data=data, expect=[200,404] )
    
