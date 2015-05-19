import ssl
import threading
import OpenSSL
import Certificate
import logging

logger = logging.getLogger('probe_module.sslCertificate')
logging.basicConfig(level=logging.DEBUG)


class SSLCertificate(threading.Thread):

    def __init__(self, input_module, output_module):
        threading.Thread.__init__(self)
        self.input_module = input_module
        self.output_module = output_module

    def run(self):
        ip = self.input_module.read()
        while ip is not None:
            try:
                logger.debug('Try to obtain certificate from %s ', ip)
                raw_certificate = ssl.get_server_certificate((ip, 443), ssl_version=ssl.PROTOCOL_TLSv1)
                certificate = Certificate.Certificate(ip, raw_certificate, OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, raw_certificate))
                self.output_module.write_dict(certificate.data_dict())
            except ssl.SSLError:
                logger.info('Error to obtain ssl certificate from %s', ip)
            except Exception, e:
                #print e
                logger.warning('Error %s from %s', e, ip)

            ip = self.input_module.read()
        logger.debug('Finish thread %s', self.getName())