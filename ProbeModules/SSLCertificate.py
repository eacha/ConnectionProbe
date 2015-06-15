import threading
import logging
from OpenSSL import SSL
from ProbeModules.SSLConnection import SSLConnection

logger = logging.getLogger('probe_module.sslCertificate')
logging.basicConfig(filename='SSLCertificate.log', level=logging.DEBUG)


class SSLCertificate(threading.Thread):

    def __init__(self, input_module, output_module):
        threading.Thread.__init__(self)
        self.input_module = input_module
        self.output_module = output_module

    def get_certificate(self, ip, verify, version=SSL.SSLv23_METHOD):
        logger.debug('Try to obtain certificate from %s ', ip)
        ssl_connection = SSLConnection(ip, 443, verify, version)
        certificate = ssl_connection.get_formatted_certificate().data_dict()
        self.output_module.write_dict(certificate)
        ssl_connection.close()

    def get_certificate_exception(self, ip, verify):
        try:
            self.get_certificate(ip, verify)
        except Exception, error:
            logger.error('Error %s from %s', error, ip)

    def get_certificate_tlsv1(self, ip):
        try:
            self.get_certificate(ip, True, version=SSL.TLSv1_METHOD)
        except SSL.Error, error:
            logger.error('Error %s to obtain ssl certificate from %s', error, ip)
            if (not SSLConnection.is_connection_reset(error)) and (not SSLConnection.is_timeout(error)):
                try:
                    self.get_certificate(ip, False, version=SSL.TLSv1_METHOD)
                except Exception, error:
                    logger.error('Error %s from %s', error, ip)
        except Exception, error:
            logger.error('Error %s from %s', error, ip)

    def run(self):
        ip = self.input_module.read()
        while ip is not None:
            try:
                self.get_certificate(ip, True)
            except SSL.Error, error:
                logger.error('Error %s to obtain ssl certificate from %s', error, ip)
                if (not SSLConnection.is_connection_reset(error)) and (not SSLConnection.is_timeout(error)):
                    if SSLConnection.is_tslv1(error):
                        self.get_certificate_tlsv1(ip)
                    else:
                        self.get_certificate_exception(ip, False)
            except Exception, error:
                logger.error('Error %s from %s', error, ip)

            ip = self.input_module.read()

        logger.debug('Finish thread %s', self.getName())