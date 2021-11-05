"""
Integration Library for selenium
Author: idel fuschini

"""

class proxy(object): 
    def setProxy(self,url):
        http_proxy  = "<proxy>"
        proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy 
        }  
        return_value=None
        if url == "<proxy>":
            return_value=proxyDict
        elif url == "<proxy>":
            return_value=proxyDict
        return return_value