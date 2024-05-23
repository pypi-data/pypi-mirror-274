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
Handle Node Status

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#nodes) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

from typing import Union

from . import element


class Node( element.ConfigElement ):
    """
    CRUD and connection management REST API for Airlock Gateway cluster nodes
    """
    ELEMENT_PATH = "node"
    RELATIONSHIPS = ["ssl-certificate"]
    
    def read( self, id: int=None ) -> Union[dict, list[dict], None]:
        """
        Fetch definition of one or all nodes of loaded configuration from Airlock Gateway.
        Will also mark the current node in the list.
        
        Parameters:
        
        * `id`: identifier of node to retrieve, if not set, all nodes are returned
        """
        resp = super().read( id )
        nodeinfo = self._gw.get( "/configuration/nodes/current", expect=[200] ).json()['data']
        for entry in resp:
            if entry['id'] == nodeinfo['id']:
                entry['_me'] = True
            else:
                entry['_me'] = False
        return resp
    
    def getNodename( self ) -> str:
        """ Return current nodename """
        nodeinfo = self._gw.get( "/configuration/nodes/current", expect=[200] )
        return nodeinfo['attributes']['hostName']
    
    def setNodename( self, name: str ) -> str:
        """
        Set new nodename and return previous
        
        Parameter:
        * `name`: new nodename
        """
        nodeinfo = self._gw.get( "/configuration/nodes/current", expect=[200] )
        previous_name = nodeinfo['attributes']['hostName']
        self._gw.patch( "/configuration/nodes/current", data={'data': {'attributes': name}}, expect=[200] )
        return previous_name
    
