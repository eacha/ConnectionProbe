import pprint
import socket
from OpenSSL import SSL

__author__ = 'eduardo'


class SSLConnection:

    def __init__(self, host, port, version=SSL.SSLv23_METHOD):
        self.host = host
        self.port = port
        self.sock = self.__connection_socket()
        self.context = SSL.Context(version)
        self.ssl_sock = self.__connection_ssl_socket()

    def __connection_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock

    def __connection_ssl_socket(self):
        ssl_sock = SSL.Connection(self.context, self.sock)
        ssl_sock.set_connect_state()
        ssl_sock.set_tlsext_host_name(self.host)
        ssl_sock.do_handshake()
        return ssl_sock

    def get_certificate(self):
        return self.ssl_sock.get_peer_certificate()

    def get_certificate_chain(self):
        return self.ssl_sock.get_peer_cert_chain()


## MAIN ##

# host = '200.9.100.69'
# port = 443
#
# sslconnection = SSLConnection(host, port)
# pprint.pprint(sslconnection.get_certificate().get_subject())
# for cert in sslconnection.get_certificate_chain():
#     pprint.pprint(cert.get_subject())



