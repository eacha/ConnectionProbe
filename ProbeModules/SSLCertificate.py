import threading
import logging
from OpenSSL import SSL
from ProbeModules.SSLConnection import SSLConnection

logger = logging.getLogger('probe_module.sslCertificate')
logging.basicConfig(level=logging.DEBUG)


class SSLCertificate(threading.Thread):

    def __init__(self, input_module, output_module):
        threading.Thread.__init__(self)
        self.input_module = input_module
        self.output_module = output_module

    def get_certificate(self, ip, verify):
        logger.debug('Try to obtain certificate from %s ', ip)
        ssl_connection = SSLConnection(ip, 443, verify)
        certificate = ssl_connection.get_formatted_certificate().data_dict()
        self.output_module.write_dict(certificate)
        ssl_connection.close()

    def run(self):
        ip = self.input_module.read()
        while ip is not None:
            try:
                self.get_certificate(ip, True)
            except SSL.Error, e:
                logger.error('Error %s to obtain ssl certificate from %s', e, ip)
                try:
                    self.get_certificate(ip, False)
                except Exception, e:
                    logger.error('Error %s from %s', e, ip)
            except Exception, e:
                logger.error('Error %s from %s', e, ip)

            ip = self.input_module.read()

        logger.debug('Finish thread %s', self.getName())