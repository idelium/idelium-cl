from __future__ import absolute_import


class PostmanTranslate():
    '''Event Key'''
    @staticmethod
    def auth1(string):
        ''' auth1 '''
        return_value=string
        oauth1 = {
                    "consumerKey": "OAuth oauth_consumer_key",
                    "signatureMethod": "oauth_signature_method",
                    "timestamp": "oauth_timestamp",
                    "nonce": "oauth_nonce",
                    "version": "oauth_version"    
                }
        if string in oauth1:
            return_value=oauth1[string]
        return return_value
