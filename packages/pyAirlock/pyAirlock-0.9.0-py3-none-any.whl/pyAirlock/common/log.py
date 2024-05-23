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

import logging
import logging.config
import os
import platform

from enum import IntEnum
from colorama import Fore, Style


class logLevels( IntEnum ):
    """
    Log levels for pyAirlock are not hierarchical but a bitmap.
    This allows to select specific log messages without including unrequired ones.
    Simply add the values for the requested log levels, e.g. FATAL + CRITICAL + ERROR = 7
    """
    NONE = 0
    FATAL = 1
    CRITICAL = 2
    ERROR = 4
    WARNING = 8
    INFO = 16
    VERBOSE = 32
    TRACE = 64
    DEBUG = 128

COLORS = { "DEBUG": Fore.LIGHTWHITE_EX, "INFO": Fore.GREEN, "WARNING": Fore.LIGHTGREEN_EX, "ERROR": Fore.RED, "CRITICAL": Fore.LIGHTRED_EX }

config_loaded = False
default_level = None
if platform.system() == "Windows":
    default_logfile = os.path.expanduser( "~/log/pyAirlock.log" )
    if not os.path.exists( os.path.dirname( default_logfile )):
        os.mkdir( os.path.dirname( default_logfile ))
else:
    default_logfile = "/var/log/pyAirlock/pyAirlock.log"

def set_level( level: int ):
    """
    Set the default log level

    Parameter:
    * `level`: see `logLevels`
    """
    global default_level

    tmp = default_level
    if isinstance( level, int ):
        default_level = level
    return tmp


class Console( object ):
    """
    Send log messages to console
    """
    def __init__( self ):
        self._level = 15

    def setLevel( self, level: int ) -> int:
        """
        Set the console log level

        Parameter:
        * `level`: see `logLevels`
        """
        tmp = self._level
        if level != None:
            self._level = level
        return tmp
    
    def fatal( self, msg: str ):
        """
        Log message to console on level 'fatal'.
        Message is only printed if current log level is an odd number.

        Use in case your program cannot continue and needs to abort.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.FATAL:
            print( Fore.LIGHTRED_EX + f"Fatal: {msg}" + Style.RESET_ALL )
        
    def critical( self, msg: str ):
        """
        Log message to console on level 'critical'.

        Use if your program experienced serious problems and may no longer work correctly.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.CRITICAL:
            print( Fore.LIGHTRED_EX + f"Critical: {msg}" + Style.RESET_ALL )
        
    def error( self, msg: str ):
        """
        Log message to console on level 'error'.

        Use if your program experienced an issue which might be resolved by simply retrying the operation.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.ERROR:
            print( Fore.RED + f"Error: {msg}" + Style.RESET_ALL )

    def warn( self, msg: str ):
        """
        Log message to console on level 'warn'.

        Use to notify the user of your program about an unexpected situation which has no immediate impact.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.WARNING:
            print( Fore.LIGHTGREEN_EX + f"Warning: {msg}" + Style.RESET_ALL )

    def info( self, msg: str ):
        """
        Log message to console on level 'info'.

        Use to inform the user of your program about its process.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.INFO:
            print( Fore.GREEN + msg + Style.RESET_ALL )

    def verbose( self, msg: str ):
        """
        Log message to console on level 'verbose'.

        Use to provide detailed information about your programs operations.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.VERBOSE:
            print( Fore.WHITE + msg + Style.RESET_ALL )

    def trace( self, msg: str ):
        """
        Log message to console on level 'trace'.

        Use this for detailed information about the individual REST API calls.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.TRACE:
            print( Fore.LIGHTWHITE_EX + f"Trace: {msg}" + Style.RESET_ALL )

    def debug( self, msg: str ):
        """
        Log message to console on level 'debug'.

        Use to print program-internal state which may help the developer in case of an issue.

        Parameter:
        * `msg`: the message to print
        """
        if self._level & logLevels.DEBUG:
            print( Fore.LIGHTWHITE_EX + f"Debug: {msg}" + Style.RESET_ALL )

    def out( self, level: int, msg: str ):
        """
        Log message to console on specified level.

        Parameter:
        * `level`: log level
        * `msg`: the message to print
        """
        if level == logLevels.FATAL:
            self.critical( msg )
        elif level == logLevels.CRITICAL:
            self.critical( msg )
        elif level == logLevels.ERROR:
            self.error( msg )
        elif level == logLevels.WARNING:
            self.warn( msg )
        elif level == logLevels.INFO:
            self.info( msg )
        elif level == logLevels.VERBOSE:
            self.verbose( msg )
        elif level == logLevels.TRACE:
            self.trace( msg )
        elif level == logLevels.DEBUG:
            self.debug( msg )


class Log( object ):
    """
    The logging facility to send messages to a logfile
    """
    def __init__( self, module, run_info=None, handler_init: bool=False ):
        global config_loaded, default_logfile, default_level

        # setup logging
        self._color = False
        self._out = None
        self._level = None
        try:
            if default_level == None:
                default_level = run_info.log_level
            if default_level != run_info.log_level:
                self._level = run_info.log_level
            if run_info.console:
                self._out = Console()
        except AttributeError:
            pass
        self._myLogger = logging.getLogger( module )
        if handler_init and len( self._myLogger.handlers ) == 0:
            if run_info:
                if config_loaded == False and isinstance( run_info.config, dict ) and 'logging' in run_info.config:
                    logging.config.dictConfig( run_info.config.get( 'logging.config' ))
                    config_loaded = True
                else:
                    fname = default_logfile
                    if run_info.log_file:
                        fname = run_info.log_file
                    elif isinstance( run_info.config, dict ):
                        fname = run_info.config.get( 'logging.logfile' )
            else:
                fname = default_logfile
            self._myLogger.setLevel( logging.WARNING )
            handler = None
            if self._out or not fname or (run_info and run_info.log_file in ['/dev/stdout','/dev/stderr']):
                handler = logging.StreamHandler()
                handler.setFormatter( ColoredFormatter( "%(message)s", True ))
            else:
                handler = logging.FileHandler( fname )
                handler.setFormatter( logging.Formatter( "%(asctime)s - %(levelname)s - %(name)s - %(message)s" ))
            if handler:
                handler.setLevel( logging.DEBUG )
                self._myLogger.addHandler( handler )
        self.set_level( self._level )

    def log( self, level: int, message: str, *args, **kwargs ):
        global default_level
        if self._level != None:
            loglevel = level & self._level
        elif default_level:
            loglevel = level & default_level
        else:
            loglevel = 0
        if loglevel > 0:
            if self._out:
                self._out.out( level, message )
            else:
                loglevel = self._map_level( level )
                if loglevel > logLevels.NONE:
                    self._myLogger.log( loglevel, message, *args, **kwargs )

    def info( self, message: str, *args, **kwargs ):
        self.log( logLevels.INFO, message, *args, **kwargs )

    def verbose( self, message: str, *args, **kwargs ):
        self.log( logLevels.VERBOSE, message, *args, **kwargs )

    def warning( self, message: str, *args, **kwargs ):
        self.log( logLevels.WARNING, message, *args, **kwargs )

    def error( self, message: str, *args, **kwargs ):
        self.log( logLevels.ERROR, message, *args, **kwargs )

    def critical( self, message: str, *args, **kwargs ):
        self.log( logLevels.CRITICAL, message, *args, **kwargs )

    def fatal( self, message: str, *args, **kwargs ):
        self.log( logLevels.FATAL, message, *args, **kwargs )

    def debug( self, message: str, *args, **kwargs ):
        self.log( logLevels.DEBUG, message, *args, **kwargs )

    def trace( self, message: str, *args, **kwargs ):
        self.log( logLevels.TRACE, message, *args, **kwargs )

    def get_level( self ) -> int:
        global default_level
        if self._level:
            return self._level
        else:
            return default_level
    
    def set_level( self, level: int ):
        # map from application log levels, which are bitmasks selecting multiple levels concurrently, to
        # Python logging level, which are hierarchical
        self._level = level
        if self._level != None:
            python_level = self._map_level( level )
            if python_level == logLevels.NONE:
                python_level = logLevels.WARNING
        else:
            python_level = logLevels.WARNING
        self._myLogger.setLevel( python_level )

    def getLogger( self ):
        return self._myLogger

    def _map_level( self, level: int ) -> int:
        python_level = logLevels.NONE
        if level & logLevels.DEBUG:
            python_level = logging.DEBUG
        elif level & logLevels.TRACE:
            python_level = logging.INFO
        elif level & logLevels.VERBOSE:
            python_level = logging.INFO
        elif level & logLevels.INFO:
            python_level = logging.INFO
        elif level & logLevels.WARNING:
            python_level = logging.WARNING
        elif level & logLevels.ERROR:
            python_level = logging.ERROR
        elif level & logLevels.CRITICAL:
            python_level = logging.CRITICAL
        return python_level


class ColoredFormatter( logging.Formatter ):
    def __init__( self, msg_template: str, colored: bool=True ):
        super( ColoredFormatter, self ).__init__( msg_template )
        self._colored = colored

    def format( self, record ):
        string = super( ColoredFormatter, self ).format( record )
        if self._colored and record.levelname in COLORS:
            string = COLORS[record.levelname] + string + Fore.RESET
        return string
