import socket
from OpenSSL import SSL
from ProbeModules.Certificate import Certificate

__author__ = 'eduardo'

CA_CERTS = '/etc/ssl/certs/ca-certificates.crt'


class SSLConnection:

    def __init__(self, host, port, verify, version=SSL.SSLv23_METHOD):
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
        return Certificate(certificate, self.verify, ip=self.host)

    def get_formatted_cert_chain(self):
        chain = self. get_certificate_chain()
        formatted_chain = []
        for certificate in chain:
            formatted_chain.append(Certificate(certificate, False))
        return formatted_chain

    def close(self):
        self.ssl_sock.shutdown()
        self.sock.close()


def is_timeout(error):
    return 'ETIMEDOUT' in error


def is_connection_reset(error):
    return 'ECONNRESET' in error


def is_tlsv1(error):
    if isinstance(error.message, list):
        return 'tlsv1 alert protocol version' in error.message[0]
    return False


def get_certificate(ip, verify, version=SSL.SSLv23_METHOD):
    ssl_connection = SSLConnection(ip, 443, verify, version=version)
    certificate = ssl_connection.get_formatted_certificate().data_dict()
    ssl_connection.close()
    return certificate

# if __name__ == '__main__':
#
#     ip = '186.67.248.4'
#
#     try:
#         get_certificate(ip, True, version=SSL.SSLv23_METHOD)
#     except SSL.Error, e:
#         if ('ECONNRESET' not in e) and ('ETIMEDOUT' not in e):
#             if tlsv1(e):
#                 try:
#                     get_certificate(ip, False, version=SSL.TLSv1_METHOD)
#                 except Exception, e:
#                     print e
#     except Exception, e:
#         print e


