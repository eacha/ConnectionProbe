import pprint
import socket
from OpenSSL import SSL

HOST = '200.9.100.69'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, 443))

context = SSL.Context(SSL.SSLv23_METHOD)

ssl_sock = SSL.Connection(context, sock)
ssl_sock.set_connect_state()
ssl_sock.set_tlsext_host_name(HOST)
ssl_sock.do_handshake()
x509 = ssl_sock.get_peer_certificate()
pprint.pprint(ssl_sock.get_peer_cert_chain())
pprint.pprint(x509.get_subject())


