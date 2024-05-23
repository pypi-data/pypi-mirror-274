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

"""
Exceptions for pyAirlock

"""


class AirlockError( Exception ):
    """ All exceptions raised by pyAirlock """


# library
class AirlockLibraryError( AirlockError ):
    """ Library usgae/processing error """

class AirlockConfigError( AirlockLibraryError ):
    """ Configuration error """

class AirlockInternalError( AirlockLibraryError ):
    """ Library-internal error """

class AirlockNotImplementedError( AirlockLibraryError ):
    """ Access planned but not yet implemented feature """


# communication-related
class AirlockCommunicationError( AirlockError ):
    """ Generic communication error with server """

class AirlockConnectionError( AirlockCommunicationError ):
    """ Unable to connect to Airlock Gateway """

class AirlockNoSessionError( AirlockCommunicationError ):
    """ No session established """


# environment
class AirlockFileSystemError( AirlockError ):
    """ File read or write failures """

class AirlockFileNotFoundError( AirlockFileSystemError ):
    """ File not found """

class AirlockFileWriteError( AirlockFileSystemError ):
    """ Unable to create or write file """


# rest api requests
class AirlockRequestError( AirlockError ):
    """ Invalid request """

class AirlockDataTypeError( AirlockRequestError ):
    """ Invalid configuration element data type """

class AirlockDataConnectionError( AirlockRequestError ):
    """ Data must not contain relationships """

class AirlockInvalidDataFormatError( AirlockRequestError ):
    """ Invalid structure of request data """

class AirlockNotSupportedError( AirlockRequestError ):
    """ Operation not supported """


# rest api response
class AirlockResponseError( AirlockError ):
    """ Invalid response """

class AirlockDataError( AirlockResponseError ):
    """ Unexpected data format """

class AirlockAPIError( AirlockResponseError ):
    """ Unexpected REST API response """

    def __init__( self, status_code: int, reason: str ):
        self.status_code = status_code
        self.reason = "Status code " + str( status_code ) + ": " + reason
        super().__init__( self.reason )

class AirlockServerError( AirlockAPIError ):
    """ Server experienced an issue while performing REST API request """

    
