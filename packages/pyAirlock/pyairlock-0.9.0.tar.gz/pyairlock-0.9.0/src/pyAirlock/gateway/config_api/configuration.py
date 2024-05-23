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
Handle Configuration

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#configurations) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

import json

from typing import Union

from ...common import exception
from . import element
from ...common import log, utils


class Configuration( element.ConfigElement ):
    """
    CRUD and management REST API for Airlock Gateway configurations

    For all configuration work, a configuration must first be loaded into the workspace:
    * `create`: initialise an empty configuration
    * `load_active`: load the currently active configuration
    * `load`: load a specific configuration by id
    """
    
    ELEMENT_PATH = "configuration"

    def __init__( self, name, gw, run_info ):
        """
        Parameters:

        * `name` is a user-friendly (short) name
        * `gw` references a `gateway.GW` object to communicate with the Airlock Gateway
        * `run_info` is provided by the Airscript shell and allows access to configuration and command line parameters
        """
        super().__init__( name, gw, run_info )
        self._activation_options = None
        self._log = log.Log( self.__module__, self._run_info )
    
    def create( self ) -> dict:
        """
        Use REST API to create an emtpy configuration in workspace
        """
        return self._post( "load-empty-config", expect=[204] )

    def update( self, activation: dict ) -> Union[dict, None]:
        """
        Activate a configuration

        Parameter:
        * `activation`: parameters for activation, dict with the following keys:
          * `comment`
          * `options`
          * `group`
          See `activate` for details.
        """
        comment = utils.getDictValue( activation, 'comment' )
        options = utils.getDictValue( activation, 'options' )
        group = utils.getDictValue( activation, 'group' )
        return self.activate( comment=comment, options=options, group=group )

    def delete( self, id: int ):
        """
        Delete a specified configuration
        
        Parameter:
        * `id`: Identifier of configuration
        """
        resp = self._gw.delete( f"/configuration/configurations/{id}", expect=[204,400,404] )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such config: {id}" )
            return False
        elif resp.status_code == 400:
            self._log.error( f"{self._name}: Config deletion failed: {resp.status_code} ({resp.text})" )
            return False
        return True
    
    def access_all( self ) -> Union[list[dict], None]:
        """ Get list of all configurations """
        return self.read()
    
    def load( self, id: int ) -> bool:
        """
        Load specific configuration into workspace
        
        Parameter:
        * `id`: Identifier of configuration
        """
        return self._post( "load", id, expect=[204,404] )
    
    def load_active( self ) -> bool:
        """ Load currently active configuration into workspace """
        return self._post( "load-active", expect=[204] )
    
    def activate( self, comment=None, options: dict=None, group: list=None ) -> bool:
        """
        Activate this configuration.
        
        Parameters:

        * `comment`: required, if you absolutely don't want to specify one, you may pass comment=\"\".
        * `options`: allow to control merging and cluster-wide activation.
            { 'merge': merge concurrent activation attempts, default true
              'cluster': activate on both nodes of cluster, default true
              'ignoreChanged': do not merge but overwrite other changes, required after upload, default false
            }
        * `group` allows to automatically mirror a successfully activated configuration to sibling nodes (not yet implemented).
        """
        if self._activation_options:
            params['options'] = self._activation_options
        else:
            params = {'options': {}}
        params['options']['autoMerge'] = utils.getDictValue( options, 'merge', True )
        params['options']['failoverAction'] = utils.getDictValue( options, 'cluster', True )
        params['options']['ignoreOutdatedConfiguration'] = utils.getDictValue( options, 'ignoreChanged', False )
        if comment == None:
            self._log.warn( "No comment specified! If you don't want to specify one, please use '<obj>.activate( comment=\"\" )'" )
            return False
        elif comment != "":
            params['comment'] = comment
        if self.validate() != []:
            self._log.warning( f"{self._name}: Config not valid" )
            return False
        params = json.dumps( {'comment': comment })
        resp = self._gw.post( "/configuration/configurations/activate", data=params, expect=[200,400,409] )
        if resp.status_code != 200:
            self._log.error( f"{self._name}: Config activation failed: {resp.status_code} ({resp.text})" )
            return False
        if group == None:
            return True
        raise exception.AirlockNotImplementedError( "group activation" )
    
    def save( self, comment=None ) -> bool:
        """
        Save this configuration.
        
        A `comment` is required. If you absolutely don't want to specify one, you may pass comment=\"\".
        """ 
        if comment == None:
            self._log.warn( "No comment specified! If you don't want to specify one, please use '<obj>.activate( comment=\"\" )'" )
            return False
        elif comment != "":
            params = json.dumps( {'comment': comment })
        else:
            params = None
        resp = self._gw.post( "/configuration/configurations/save", data=params, expect=[204,400] )
        if resp.status_code != 200:
            self._log.error( f"{self._name}: Config save failed: {resp.status_code} ({resp.text})" )
            return False
        return True
    
    def export( self, id: int=None, zip_file: str=None ):
        """
        Download configuration from Airlock Gateway as a zip file.

        If `id` is not specified, download currently active configuration.
        If `zip_file` is specified, configuration is saved to it. Otherwise, it is contained in the return value.
        """
        if id:
            resp = self._gw.get( f"/configuration/configurations/{id}/export", accept="application/zip", expect=[200,400,404] )
        else:
            resp = self._gw.get( f"/configuration/configurations/export", accept="application/zip", expect=[200,400] )
        if resp.status_code == 404:
            self._log.verbose( f"{self._name}: No such config: {id}" )
            return resp
        elif resp.status_code != 200:
            self._log.error( f"{self._name}: Config download failed: {resp.status_code} ({resp.text})" )
            return resp
        if zip_file:
            try:
                with open( zip_file, "wb" ) as fp:
                    fp.write( resp.content )
            except OSError as e:
                e.add_note( f"File: {zip_file}" )
                raise exception.AirlockFileWriteError()
            return None
        return resp
    
    def upload( self, zip_file: str, verify: bool=True ) -> bool:
        """
        Upload configuration to Airlock Gateway from zip file.

        Parameters:
        
        * `zip_file`: path to ZIP file with Airlock Gateway configuration
        * `verify`: if true, upload will fail if configuration has errors (workspace will contain empty config)
        """
        try:
            files = { 'file': open( zip_file, 'rb' ) }
        except OSError as e:
            e.add_note( f"File: {zip_file}" )
            raise exception.AirlockFileNotFoundError()
        self._gw.get( f"/configuration/configurations/import", content="application/zip", files=files, expect=[200] )
        if verify:
            if self.validate() != []:
                self._log.warning( f"{self._name}: Uploaded config not valid - replaced with empty config" )
                self.create()
                return False
        try:
            self._activation_options['ignoreOutdatedConfiguration'] = True
        except KeyError:
            self._activation_options = {'ignoreOutdatedConfiguration': True}
        return True
    
    def validate( self ) -> list[str]:
        """ Retrieve validation messages for this configuration """
        messages = []
        resp = self._gw.get( "/configuration/validator-messages", expect=[200] )
        if resp.text != "":
            for entry in resp.json()['data']:
                messages.append( entry )
        return messages
    
