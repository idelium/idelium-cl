from __future__ import absolute_import

import time  # To generate the OAuth timestamp
import urllib.parse  # To URLencode the parameter string
import hmac  # To implement HMAC algorithm
import hashlib  # To generate SHA256 digest
from base64 import b64encode  # To encode binary data into Base64
import binascii  # To convert data into ASCII
import requests  # To make HTTP requests
class OuthSignature:
    @staticmethod
    def create_parameter_string(oauth_consumer_key, oauth_nonce, oauth_signature_method, oauth_timestamp, oauth_token, oauth_version):
        parameter_string = ''
        parameter_string = parameter_string + 'oauth_consumer_key=' + oauth_consumer_key
        parameter_string = parameter_string + '&oauth_nonce=' + oauth_nonce
        parameter_string = parameter_string + '&oauth_signature_method=' + oauth_signature_method
        parameter_string = parameter_string + \
            '&oauth_timestamp=' + oauth_timestamp
        parameter_string = parameter_string + \
            '&oauth_token=' + oauth_token
        parameter_string = parameter_string + '&oauth_version=' + oauth_version
        return parameter_string


    @staticmethod
    def create_signature(secret_key, signature_base_string, oauth_signature_method):
        signature = None
        if oauth_signature_method == 'HMAC-SHA1':
            signature = hashlib.sha1
        elif oauth_signature_method == 'HMAC-SHA256':
            signature = hashlib.sha256
        elif oauth_signature_method == 'HMAC-512':
            signature = hashlib.sha512
        print ('signathur method: '  + oauth_signature_method)
        encoded_string = signature_base_string.encode()
        encoded_key = secret_key.encode()
        temp = hmac.new(encoded_key, encoded_string, signature).hexdigest()
        byte_array = b64encode(binascii.unhexlify(temp))
        return byte_array.decode()
