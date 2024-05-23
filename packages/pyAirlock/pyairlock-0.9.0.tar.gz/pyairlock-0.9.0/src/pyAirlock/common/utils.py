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

def getDictValue( d: dict=None, path: str=None, default=None ):
    """
    Retrieve a value from dict, identified by key path.

    Parameters:
    
    * `d`: dict to search in
    * `path`: concatenated, dot-separated keys specifying path in dict to requested element, e.g. airscript.init.scripts
    * `default`: value to return if `path` is not found
    """
    if d == None or not isinstance( d, dict ):
        return default
    for key in path.split( '.' ):
        try:
            d = d[key]
        except KeyError:
            return default
    return d
