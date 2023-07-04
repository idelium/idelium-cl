"""System module."""
from __future__ import absolute_import

class Proxy():
    '''Proxy class'''
    @staticmethod
    def set_proxy(url):
        '''Set the proxy'''
        http_proxy  = "<proxy>"
        proxy_dict = {
              "http"  : http_proxy,
              "https" : http_proxy
        }
        return_value=None
        if url == "<proxy>":
            return_value = proxy_dict
        elif url == "<proxy>":
            return_value = proxy_dict
        return return_value
