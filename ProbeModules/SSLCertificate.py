import ssl
import threading
import OpenSSL
import Certificate


class SSLCertificate(threading.Thread):

    def __init__(self, input_module, output_module):
        threading.Thread.__init__(self)
        self.input_module = input_module
        self.output_module = output_module

    def run(self):
        ip = self.input_module.read()
        while ip is not None:
            try:
                print 'try to obtain certificate from ' + ip
                raw_certificate = ssl.get_server_certificate((ip, 443), ssl_version=ssl.PROTOCOL_TLSv1)
                certificate = Certificate.Certificate(ip, raw_certificate, OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, raw_certificate))
                self.output_module.write_dict(certificate.data_dict())
            except ssl.SSLError:
                print 'Error to obtain ssl certificate from ' + ip
            except Exception, e:
                print e

            ip = self.input_module.read()