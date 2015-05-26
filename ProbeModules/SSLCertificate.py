import ssl
import threading
import logging

import OpenSSL

from ProbeModules import Certificate


logger = logging.getLogger('probe_module.sslCertificate')
logging.basicConfig(level=logging.DEBUG)


class SSLCertificate(threading.Thread):

    def __init__(self, input_module, output_module):
        threading.Thread.__init__(self)
        self.input_module = input_module
        self.output_module = output_module

    def get_certificate(self, ip, validate=True):
        if validate:
            ca_cert = '/etc/ssl/certs/ca-certificates.crt'
        else:
            ca_cert = None
        raw_certificate = ssl.get_server_certificate((ip, 443), ssl_version=ssl.PROTOCOL_SSLv23,
                                          ca_certs=ca_cert)
        certificate = Certificate.Certificate(ip, validate, raw_certificate, OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, raw_certificate))
        self.output_module.write_dict(certificate.data_dict())

    def run(self):
        ip = self.input_module.read()
        while ip is not None:
            try:
                logger.debug('Try to obtain certificate from %s ', ip)
                self.get_certificate(ip)
            except ssl.SSLError, e:
                logger.error('Error %s to obtain ssl certificate from %s', e, ip)
                try:
                    self.get_certificate(ip, validate=False)
                except Exception, e:
                    logger.error('Error %s from %s', e, ip)
            except Exception, e:
                logger.error('Error %s from %s', e, ip)

            ip = self.input_module.read()

        logger.debug('Finish thread %s', self.getName())