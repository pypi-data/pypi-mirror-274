"""
pyAirlock: Python library for Airlock products

Copyright (c) 2019-2024 Urs Zurbuchen <info@airlock.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import yaml

from . import exception, utils

class Config( object ):
    """
    The configuration for pyAirlock specifying known Airlock Gateways and IAM servers
    and their relevant connection parameters, such as hostnames, API keys etc.
    """
    def __init__( self, fname: str=None ):
        """
        The load the configuration, call `load()`.

        Parameter:
        * `fname`: path to YAML config file
        """
        self._fname = fname
        self._config = {}
        self._valid = False

    def load( self, fname: str=None ):
        """
        Load the configuration from YAML file

        Parameter:
        * `fname`: path to YAML config file
        """
        if fname == None:
            fname = self._fname
        self._valid = False
        try:
            with open( self._fname, "r" ) as fp:
                self._config = yaml.safe_load( fp )
        except FileNotFoundError:
            raise exception.AirlockFileNotFoundError()
        except yaml.scanner.ScannerError:
            raise exception.AirlockConfigError()
        self._valid = True

    def get( self, path: str, default: str=None, base: dict=None ):
        """
        Retrieve a configuration value, identified by key path.

        Parameters:
        
        * `path`: concatenated, dot-separated keys specifying path in configuration dict to requested element, e.g. airscript.init.scripts
        * `default`: value to return if `path` is not found
        * `base`: dict to search in, use full config if not set
        """
        if not self._valid:
            return None
        if base == None or type( base ) != dict:
            d = self._config
        else:
            d = base
        return utils.getDictValue( d, path, default )
    
    def is_valid( self ) -> bool:
        """
        Return true if configuration has been loaded
        """
        return self._valid
    
