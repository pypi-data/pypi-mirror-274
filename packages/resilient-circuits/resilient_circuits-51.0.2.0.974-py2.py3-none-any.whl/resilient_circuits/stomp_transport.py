# (c) Copyright IBM Corp. 2010, 2018. All Rights Reserved.
""" stompest StompFrameTransport allowing for ssl.wrap_socket """

import logging
import ssl
import socket
from stompest.sync.transport import StompFrameTransport
from stompest.error import StompConnectionError
import socks
from resilient import constants, helpers

LOG = logging.getLogger(__name__)


class EnhancedStompFrameTransport(StompFrameTransport):
    """ add support for older ssl module and http proxy """

    proxy_host = None
    proxy_port = None
    proxy_user = None
    proxy_password = None

    @staticmethod
    def match_hostname(cert, hostname):
        """ Check that hostname matches cert """
        names = []
        # Python 3 has an ssl.match_hostname method, which does hostname validation.
        try:
            ssl.match_hostname(cert, hostname)
            return
        except AttributeError as err:
            # We don't have the backported python 3 ssl module, do a simplified check
            for sub in cert.get('subject', ()):
                for key, value in sub:
                    if key == 'commonName':
                        names.append(value)
                        if value == hostname:
                            return
        raise Exception("{0} does not match the expected value in the certificate {1}".format(hostname, str(names)))

    def connect(self, timeout=None):
        """ Allow older versions of ssl module, allow http proxy connections """
        LOG.debug("stomp_transport.connect()")
        ssl_params = None
        if isinstance(self.sslContext, dict):
            # This is actually a dictionary of ssl parameters for wrapping the socket
            ssl_params = self.sslContext
            self.sslContext = None

        proxy_details = helpers.get_and_parse_proxy_env_var(constants.ENV_HTTPS_PROXY)
        proxy_type = socks.HTTP

        if helpers.is_env_proxies_set() and proxy_details:

            if helpers.is_in_no_proxy(self.host):
                self.proxy_host = None
                self.proxy_port = None
                self.proxy_user = None
                self.proxy_password = None

            else:
                self.proxy_host = proxy_details.get("hostname", "")
                self.proxy_port = proxy_details.get("port")
                self.proxy_user = proxy_details.get("username", "")
                self.proxy_password = proxy_details.get("password", "")

        try:
            if self.proxy_host:
                LOG.info("Connecting through proxy %s", self.proxy_host)
                self._socket = socks.socksocket()
                self._socket.set_proxy(proxy_type, self.proxy_host, self.proxy_port, True,
                                       username=self.proxy_user, password=self.proxy_password)
            else:
                self._socket = socket.socket()

            self._socket.settimeout(timeout)
            self._socket.connect((self.host, self.port))

            if ssl_params:
                # For cases where we don't have a modern SSLContext (so no SNI)
                cert_required = ssl.CERT_REQUIRED if ssl_params["ca_certs"] else ssl.CERT_NONE
                self._socket = ssl.wrap_socket(
                    self._socket,
                    keyfile=ssl_params['key_file'],
                    certfile=ssl_params['cert_file'],
                    cert_reqs=cert_required,
                    ca_certs=ssl_params['ca_certs'],
                    ssl_version=ssl_params['ssl_version'])
                if cert_required:
                    LOG.info("Performing manual hostname check")
                    cert = self._socket.getpeercert()
                    self.match_hostname(cert, self.host)

            if self.sslContext:
                self._socket = self.sslContext.wrap_socket(self._socket, server_hostname=self.host)

        except IOError as e:
            raise StompConnectionError('Could not establish connection [%s]' % e)
        self._parser.reset()
