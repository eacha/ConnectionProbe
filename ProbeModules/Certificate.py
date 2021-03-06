from collections import OrderedDict
import OpenSSL
from datetime import datetime

__author__ = 'eduardo'


class Certificate:

    def __init__(self, x509, validation, ip=None):
        self.ip = ip
        self.x509 = x509
        self.raw_certificate = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
        self.validation = validation
        self.certificate_authority = x509.get_issuer()
        self.public_key = x509.get_pubkey()
        self.signature_algorithm = x509.get_signature_algorithm()
        self.subject = x509.get_subject()
        self.expired_time = datetime.strptime(x509.get_notAfter(), "%Y%m%d%H%M%SZ")

    def get_name_authority(self):
        return self.certificate_authority.commonName

    def get_signature_algorithm(self):
        try:
            return self.signature_algorithm
        except ValueError:
            return None

    def get_raw_certificate(self):
        return self.raw_certificate

    def get_key_bits(self):
        return self.public_key.bits()

    def get_organization_name(self):
        organization_name = self.subject.organizationName
        if organization_name is None:
            return self.subject.organizationalUnitName
        return organization_name

    def get_organization_url(self):
        return self.subject.commonName

    def get_x509(self):
        return self.x509

    def data_dict(self):
        return OrderedDict([('ip', self.ip),
                            ('Expired Time', self.expired_time),
                            ('validation', self.validation),
                            ('Organization Name', self.get_organization_name()),
                            ('Organization URL', self.get_organization_url()),
                            ('Certificate Authority', self.get_name_authority()),
                            ('Key Bits', self.get_key_bits()),
                            ('Signature Algorithm', self.get_signature_algorithm()),
                            ('Raw Certificate', self.raw_certificate.replace('\n', ''))])
