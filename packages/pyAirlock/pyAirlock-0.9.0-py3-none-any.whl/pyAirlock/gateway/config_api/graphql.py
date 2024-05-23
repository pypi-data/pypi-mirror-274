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
Handle GraphQL Document

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#graphql) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from . import element


class GraphQL( element.ConfigElement ):
    """
    CRUD and connection management REST API for GraphQL API specifications
    """
    ELEMENT_PATH = "api-security/graphql-document"
    RELATIONSHIPS = ["mapping"]
    
    def download( self, id: int ) -> str:
        """
        Download content of GraphQL document.

        Parameter:
        * `id`: identifier of GraphQL document
        """
        resp = self._gw.get( f"/configuration/{self.ELEMENT_PATH}s/{id}/content", expect=[200], accept="application/octet-stream" )
        return resp.content()
    
    def upload( self, id: int, data ) -> bool:
        """
        Upload content of GraphQL document.

        Parameter:
        * `id`: identifier of GraphQL document
        """
        resp = self._gw.put( f"/configuration/{self.ELEMENT_PATH}s/{id}/content", data=data, expect=[204], content="application/octet-stream" )
        return True
    
