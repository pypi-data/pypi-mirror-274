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
Connect to and communicate with Gateway

Please refer to the [Airlock Gateway REST API](https://docs.airlock.com/gateway/latest/rest-api/config-rest-api.html#authentication) documentation to understand how
it works, e.g. the requirements for loading and activating a configuration.
"""

import atexit
import json
import os
import requests
import tempfile
import urllib3

from urllib3.exceptions import MaxRetryError
from requests.adapters import HTTPAdapter, Retry

from ...common import exception
from ...common import log, utils
from .api_policy import APIPolicy
from .backendgroup import BackendGroup
from .certificate import Certificate
from .configuration import Configuration
from .graphql import GraphQL
from .icap import ICAP
from .host import Host
from .iplist import IPList
from .jwks import LocalJWKS, RemoteJWKS
from .kerberos import Kerberos
from .mapping import Mapping
from .network_endpoint import NetworkEndpoint
from .node import Node
from .openapi import OpenAPI
from .vhost import VirtualHost


class GW( object ):
    """
    Representation of an Airlock Gateway

    * Allows configuration management over REST API.
    * Handles communication with Airlock Gateway, including session management
    * Provides access to REST APIs for individual configuration elements, such as mappings, virtual hosts etc.
    """

    def __init__( self, name: str, hostname: str, key: str, run_info=None ):
        """
        Parameters to connect to Airlock Gateway

        * `name` is a user-friendly (short) name
        * `hostname` is the FQDN or IP address of the management interface
        * `key` is the API key
        * `run_info` is provided by the Airscript shell and allows access to configuration and command line parameters
        """
        #: The http session established with the Airlock Gateway. Handles cookies, timeouts and retries on errors.
        self.session = None
        self._name = name
        self._hostname = hostname
        self._key = key
        self._run_info = run_info
        self._url = f"https://{hostname}/airlock/rest"
        self._version = None
        self._nodename = None
        self._certfile = None
        self._tlsVerify = True
        if self._run_info:
            self._timeout = self._run_info.config.get( "airscript.timeout" )
        else:
            self._timeout = 5
        self._log = log.Log( self.__module__, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.api_policy.APIPolicy` configuration element
        self.api_policy = APIPolicy( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.backendgroup.BackendGroup` configuration element
        self.backendgroup = BackendGroup( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.certificate.Certificate` configuration element
        self.certificate = Certificate( self._name, self, self._run_info )
        #: CRUD and management REST API for `pyAirlock.gateway.config_api.configuration.Configuration` 
        self.configuration = Configuration( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.graphql.GraphQL` configuration element
        self.graphql = GraphQL( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.host.Host` configuration element
        self.host = Host( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.icap.ICAP` configuration element
        self.icap = ICAP( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.iplist.IPList` configuration element
        self.iplist = IPList( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.jwks.LocalJWKS` configuration element
        self.jwks_local = LocalJWKS( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.jwks.RemoteJWKS` configuration element
        self.jwks_remote = RemoteJWKS( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.kerberos.Kerberos` configuration element
        self.kerberos = Kerberos( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.mapping.Mapping` configuration element
        self.mapping = Mapping( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.network_endpoint.NetworkEndpoint` configuration element
        self.network_endpoint = NetworkEndpoint( self._name, self, self._run_info )
        #: CRUD and connection management REST API for Airlock Gateway `pyAirlock.gateway.config_api.node.Node`
        self.node = Node( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.openapi.OpenAPI` configuration element
        self.openapi = OpenAPI( self._name, self, self._run_info )
        #: CRUD and connection management REST API for `pyAirlock.gateway.config_api.vhost.VirtualHost` configuration element
        self.vhost = VirtualHost( self._name, self, self._run_info )
    
    def getName( self ) -> str:
        """ Return short name. """
        return self._name
    
    def getHost( self ) -> str:
        """ Return FQDN or IP address. """
        return self._hostname
    
    def getKey( self ) -> str:
        """ Return API key. """
        return self._key
    
    def getVersion( self ) -> str:
        """
        Return connected Gateway's version.

        Airlock Gateways versions 7.x do not support this feature.
        pyAirlock will report their version number as fix "7.8".

        Please note that Airlock Gateway 7.8 was end-of-support in October 2023.
        """
        if self.session == None:
            raise( exception.AirlockNoSessionError )
        return self._version
    
    def getNodename( self ) -> str:
        """ Return connected Gateway's nodename. """
        if self.session == None:
            raise( exception.AirlockNoSessionError )
        return self._nodename
    
    def getAPI( self, type_name ):
        """
        Retrieve handler for CRUD and connection management REST API for the configuration element.
        
        Possible values for `type_name` are:
        * api-policy-service
        * back-end-group
        * ssl-certificate
        * graphql-document
        * host
        * icap-environment
        * ip-address-list
        * local-json-web-key-sets
        * remote-json-web-key-sets
        * kerberos
        * mapping
        * allowed-network-endpoint
        * node
        * openapi-document
        * virtual-host
        """
        if type_name == "api-policy-service":
            return self.api_policy
        elif type_name == "back-end-group":
            return self.backendgroup
        elif type_name == "ssl-certificate":
            return self.certificate
        elif type_name == "graphql-document":
            return self.graphql
        elif type_name == "host":
            return self.host
        elif type_name == "icap-environment":
            return self.i4
        elif type_name == "ip-address-list":
            return self.i4
        elif type_name == "local-json-web-key-sets":
            return self.jwks_local
        elif type_name == "remote-json-web-key-sets":
            return self.jwks_remote
        elif type_name == "kerberos":
            return self.kerberos
        elif type_name == "mapping":
            return self.mapping
        elif type_name == "allowed-network-endpoint":
            return self.network_endpoint
        elif type_name == "node":
            return self.node
        elif type_name == "openapi-document":
            return self.openapi
        elif type_name == "virtual-host":
            return self.vhost
        return None

    def setVerbosity( self, logLevel: int=None ) -> int:
        if logLevel != None:
            tmp_log = self._log( logLevel )
        return tmp_log

    def setCertificate( self, certfile=None, pem=None ):
        """
        Define CA certificate file to verify signature of Airlock Gateway's Config Center certificate.
        
        If Airlock Gateway Config Center uses a certificate not issued by any of the
        well-known certificate authorities (CAs) maintained in /etc/ssl/certs,
        the appropriate signing certificate must be specified here.

        Parameters:

        * `certfile`: path to CA certificate file, in PEM format
        * `pem`: CA certificate as string, in PEM format

        If you do not wish to verify the authenticity of the Airlock Gateway,
        you can use setTLSVerify() to turn verification off. This will also
        silence corresponding warnings.
        """
        if certfile == None and pem == None:
            self._certfile = None
        elif certfile:
            self._certfile = os.path.expanduser( certfile )
        else:
            try:
                fp, fname = tempfile.mkstemp( suffix=".pem", text=True )
                fp.write( pem )
                fp.close()
            except OSError as e:
                e.add_note( f"File: {fname}" )
                raise exception.AirlockFileWriteError()
            self._certfile = os.path.expanduser( fname )
            atexit.register( self._certificateCleanup, fname )
    
    def setTLSVerify( self, verify ) -> bool:
        """
        Suppress server certificate checking.
        
        Passing in `verify=False` completely disables server certificate checking.
        While this may be easy for self-signed Airlock Gateway Config Center
        certificates, it should not be used in production.
        
        Warning messages by the underlying libraries about unsecure connections
        will also be silenced.

        For an even stronger version, passing in `verify=None` also suppresses
        any warning messages related to the certificate.
        """
        if verify != True:
            urllib3.disable_warnings()
        if verify == None:
            self._tlsVerify = False
            return True
        if verify == True or verify == False:
            self._tlsVerify = verify
            return True
        return False
    
    def connect( self ):
        """
        Establish session with Airlock Gateway.
        """
        if self.session != None:
            return True
        self.session = requests.Session()
        self.session.headers.update( {"Authorization": f"Bearer {self._key}"} )
        # retries = Retry( total=5, backoff_factor=0, allowed_methods=None, status_forcelist=[ 500, 502, 503, 504 ] )
        # self.session.mount( self._url, HTTPAdapter( max_retries=retries ))
        try:
            resp = self.post( "/session/create", expect=[200] )
        except MaxRetryError:
            self.session = None
            raise exception.AirlockConnectionError()
        resp = self.get( "/system/status/node", expect=[200] )
        try:
            self._version = float( utils.getDictValue( resp.json(), "data.attributes.version" ))
        except TypeError:
            self._version = None
        try:
            self._nodename = utils.getDictValue( resp.json(), "data.attributes.hostName" )
        except TypeError:
            self._nodename = None
        self._log.info( f"Connected to '{self._name}' ({self._nodename})" )
        if not self._version:
            self._log.info( f"{self._name}: version indeterminable - assuming 7.8 but compatibility not guaranteed" )
            self._version = 7.8
            return True
        return True
    
    def disconnect( self ):
        """
        Disconnect from Airlock Gateway, closing administrator session.
        
        Subsequent calls to the Airlock Gateway REST API endpoint will result in an error.

        This session will no longer count as existing parallel session in Config Center nor cause a warning that another administrator is active.
        """
        self.post( "/session/terminate", expect=[200] )
        self.session = None
        self._log.info( "Disconnected from '%s'" % (self._name,) )

    def keepalive( self ):
        """
        A session to an Airlock Gateway times out after about 10 minutes of inactivity.
        To keep it active, REST API requests must be sent in regular intervals.
        This function fetches the node status and can be used as a side-effect free keep-alive.

        For standard scripts, this is not required.
        """
        self.get( "/configuration/license", expect=[200] )

    def get( self, path: str, accept=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API GET and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol), e.g. "/back-end-groups"
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `accept`: set if you expect something else than 'application/json' as response
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.get( f"{self._url}{path}",
                                 headers=self._headers( accept=accept ),
                                 timeout=self._timeout if timeout == None else timeout,
                                 verify=self._verify() )
        return self._validateResponse( resp, path, expect )
    
    def post( self, path: str, data=None, accept=None, content=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API POST and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:
        
        * `path`: REST API endpoint (without hostname or protocol), e.g. "/session/cxreate"
        * `data`: must be pre-formatted, e.g. ready to be converted to JSON if REST endpoint expects JSON
        * `content`: must be set if data is not JSON
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `accept`: set if you expect something else than 'application/json' as response
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.post( f"{self._url}{path}",
                                  headers=self._headers( accept=accept, content=content ),
                                  timeout=self._timeout if timeout == None else timeout,
                                  verify=self._verify(),
                                  data=json.dumps( data ))
        return self._validateResponse( resp, path, expect )
    
    def patch( self, path: str, data=None, accept=None, content=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API PATCH and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol), e.g. "/mappings/{id}/relationships/openapi-document"
        * `data`: must be pre-formatted, e.g. ready to be converted to JSON if REST endpoint expects JSON
        * `content`: must be set if data is not JSON
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `accept`: set if you expect something else than 'application/json' as response
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.patch( f"{self._url}{path}",
                                   headers=self._headers( accept=accept, content=content ),
                                   timeout=self._timeout if timeout == None else timeout,
                                   verify=self._verify(),
                                   data=json.dumps( data ) )
        return self._validateResponse( resp, path, expect )
    
    def put( self, path: str, data=None, accept=None, content=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API PUT and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol), e.g. "/mappings/import"
        * `data`: must be pre-formatted, e.g. ready to be converted to JSON if REST endpoint expects JSON
        * `content`: must be set if data is not JSON
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `accept`: set if you expect something else than 'application/json' as response
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.put( f"{self._url}{path}",
                                 headers=self._headers( accept=accept, content=content ),
                                 timeout=self._timeout if timeout == None else timeout,
                                 verify=self._verify(),
                                 data=json.dumps( data ) )
        return self._validateResponse( resp, path, expect )
    
    def delete( self, path: str, data=None, accept=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API DELETE and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol), e.g. "/virtual-hosts/{id}"
        * `data`: must be pre-formatted, e.g. ready to be converted to JSON if REST endpoint expects JSON
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `accept`: set if you expect something else than 'application/json' as response
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.delete( f"{self._url}{path}",
                                    headers=self._headers( accept=accept ),
                                    timeout=self._timeout if timeout == None else timeout,
                                    verify=self._verify(),
                                    data=json.dumps( data ) )
        return self._validateResponse( resp, path, expect )
    
    def upload( self, path: str, files=None, content=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API PUT to upload a file and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol)
        * `files`: must be a dict "{ 'file': <opened file handle> }"
        * `content`: must be set to the uploaded data's content type (which is probably not 'application/json')
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.put( f"{self._url}{path}",
                                 headers=self._headers( content=content ),
                                 timeout=self._timeout if timeout == None else timeout,
                                 verify=self._verify(),
                                 files=files )
        return self._validateResponse( resp, path, expect )
    
    def uploadCopy( self, path: str, files=None, content=None, timeout=None, expect: list[int]=None ):
        """
        Perform REST API POST to upload a file and return HTTP response.
        
        Session with Airlock Gateway must previously have been established.

        Parameters:

        * `path`: REST API endpoint (without hostname or protocol)
        * `files`: must be a dict "{ 'file': <opened file handle> }"
        * `content`: must be set to the uploaded data's content type (which is probably not 'application/json')
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `timeout`: override the default session timeout, specify number of seconds
        """
        resp = self.session.post( f"{self._url}{path}",
                                  headers=self._headers( content=content ),
                                  timeout=self._timeout if timeout == None else timeout,
                                  verify=self._verify(),
                                  files=files )
        return self._validateResponse( resp, path, expect )
    
    def _headers( self, accept=None, content=None ):
        """
        Return dict with HTTP headers to send to Airlock Gateway.

        Parameters:

        * `accept`: mime type of response, default is 'application/json'
        * `content`: mime type of sent data, default is 'application/json'
        """
        hdr = { "Accept": "application/json", "Content-Type": "application/json" }
        if accept != None:
            hdr['Accept'] = accept
        if content != None:
            hdr['Content-Type'] = content
        return hdr
    
    def _verify( self ):
        """ Return certificate verification setting for requests library. """
        verify=True
        if self._certfile != None:
            verify = self._certfile
        if self._tlsVerify == False:
            verify = False
        return verify
    
    def _validateResponse( self, response, path: str, expect: list[int] ):
        """
        Validate the response has one of the expect status codes

        Parameters:
        
        * `response`: the response to validate
        * `expect`: list of expected HTTP response codes, other values result in exceptions
        * `path`: original request path, for logging only
        """
        if expect:
            if response.status_code not in expect:
                if response.status_code >= 500:
                    self._log.critical( f"{self._name}: {path} returned {response.status_code}" )
                    raise exception.AirlockServerError( response.status_code, response.text )
                elif response.status_code >= 400:
                    self._log.error( f"{self._name}: {path} returned {response.status_code}" )
                    raise exception.AirlockAPIError( response.status_code, response.text )
                elif response.status_code >= 200:
                    self._log.warning( f"{self._name}: {path} returned {response.status_code}" )
        return response

    def _certificateCleanup( self, fname: str ) -> None:
        if fname != None:
            try:
                os.remove( fname )
            except OSError:
                pass
    
