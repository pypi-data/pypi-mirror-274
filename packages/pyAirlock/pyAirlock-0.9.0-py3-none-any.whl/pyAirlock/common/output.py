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

from colorama import Fore, Style


class Info( object ):
    def __init__( self, theme: str="dark" ):
        self._theme = theme

    def label( self, msg: str ):
        print( Fore.WHITE + msg + Style.RESET_ALL )

    def msg( self, msg: str ):
        print( Fore.CYAN + msg + Style.RESET_ALL )
    
    def nocolor( self, msg: str ):
        print( msg )
    
    def yellow( self, msg: str ):
        print( Fore.YELLOW + msg + Style.RESET_ALL )
    
    def green( self, msg: str ):
        print( Fore.GREEN + msg + Style.RESET_ALL )
    
    def blue( self, msg: str ):
        print( Fore.BLUE + msg + Style.RESET_ALL )
    
    def red( self, msg: str ):
        print( Fore.RED + msg + Style.RESET_ALL )
    
    def cyan( self, msg: str ):
        print( Fore.CYAN + msg + Style.RESET_ALL )
    
    def black( self, msg: str ):
        print( Fore.BLACK + msg + Style.RESET_ALL )
    
    def white( self, msg: str ):
        print( Fore.WHITE + msg + Style.RESET_ALL )
    
    def magenta( self, msg: str ):
        print( Fore.MAGENTA + msg + Style.RESET_ALL )
    
