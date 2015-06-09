import socket
from OpenSSL import SSL
from ProbeModules.Certificate import Certificate

__author__ = 'eduardo'

CA_CERTS = '/etc/ssl/certs/ca-certificates.crt'


class SSLConnection:

    def __init__(self, host, port, version=SSL.SSLv23_METHOD, verify=True):
        self.host = host
        self.port = port
        self.verify = verify
        self.sock = self.__connection_socket()
        self.context = self.__connection_context(version, verify)
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

    def __connection_context(self, version, verify):
        context = SSL.Context(version)
        if verify:
            context.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, self.certificate_callback)
            context.load_verify_locations(CA_CERTS)
        return context

    @staticmethod
    def certificate_callback(connection, x509, errnum, errdepth, ok):
        if not ok:
            return False
        return ok

    def get_certificate(self):
        return self.ssl_sock.get_peer_certificate()

    def get_certificate_chain(self):
        return self.ssl_sock.get_peer_cert_chain()

    def get_formatted_certificate(self):
        certificate = self.get_certificate()
        return Certificate(certificate, self.host)

    def get_formatted_cert_chain(self):
        chain = self. get_certificate_chain()
        formatted_chain = []
        for certificate in chain:
            formatted_chain.append(Certificate(certificate))
        return formatted_chain

    def close(self):
        self.ssl_sock.shutdown()
        self.sock.close()

## MAIN ##

ucursos = '200.9.100.67'
host = '77.236.230.12'
port = 443

try:
    sslconnection = SSLConnection(ucursos, port)
    print sslconnection.get_formatted_certificate().data_dict()
    for cert in sslconnection.get_formatted_cert_chain():
        print cert.data_dict()
    sslconnection.close()
except SSL.Error, e:
    print e
except socket.error, e:
    print e



