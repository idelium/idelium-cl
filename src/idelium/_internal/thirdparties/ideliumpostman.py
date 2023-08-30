from __future__ import absolute_import
from requests_oauthlib import OAuth1
from argparse import HelpFormatter
import requests
import json
import sys
from re import A
from urllib.parse import urlencode
from idelium._internal.commons.ideliumprinter import InitPrinter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from idelium._internal.commons.postmantranslate import PostmanTranslate

printer = InitPrinter()


class PostmanCollection:
        
    def get_payload(self,request):
        return_data={}
        method=''
        if 'method' in request:
            method=request['method']
            if method == 'raw':
                return_data=request['value']
            elif method == 'formdata':
                return_data=self.get_parser(request['formdata'])
            else:
                print ("method not found: " + method)
                sys.exit()
        elif 'mode' in request:
            method = request['mode']
            if method=='raw':
                return_data = request['raw']
        else:
                print("method not found: " + method)
                sys.exit()
             
        return {
            'data':return_data,
            'method': method
        }
    
    def get_parser(self,string,type=None):
        object_return={}
        string_to_return=''
        for i in string:
            if 'disabled' in i and i['disabled'] == True:
                bypass = True
            else:
                if 'value' in i:
                    key=i['key']
                    if type == 'oauth1':
                        postman_translate = PostmanTranslate()
                        key=postman_translate.auth1(i['key'])
                        string_to_return = string_to_return + key + '="' + str(i['value']) + '",'
                    else:
                        object_return[key] = str(i['value'])
        if string_to_return != '':
            object_return=string_to_return
        return object_return
        
    ''' PostmanCollection '''

    def get_auth(self, auth):
        type_auth=auth['type']
        headers=None
        if type_auth == 'oauth1':
            headers={
                'Authorization': self.get_parser(auth['oauth1'], 'oauth1')
            }
        return headers
            

    def connection_test(self,request_test):
        ''' start '''
        method=request_test['method']
        url=request_test['url']['raw']
        headers = self.get_parser(request_test['header'])
        if 'auth' in request_test:
            headers = self.get_auth(request_test['auth'])
        if method == "POST" or method == "PUT" or method == "PATCH" or method == "DELETE":
            files={}
            payload = ''
            body = self.get_payload(request_test['body'])
        
            if body['method']=='formdata':
                files=body['data']
            elif body['method']=='raw':
                payload = body['data']
            if method== "POST":
                req = requests.post(url,
                                    headers=headers,
                                    data=json.dumps(payload),
                                    files=files,
                                    verify=False)
            elif method == "PUT":
                req = requests.put(url,
                                    headers=headers,
                                    data=json.dumps(payload),
                                    files=files,
                                    verify=False)
            elif method == "PATCH":
                req = requests.patch(url,
                                   headers=headers,
                                   data=json.dumps(payload),
                                   files=files,
                                   verify=False)
            elif method == "DELETE":
                req = requests.delete (url,
                                     headers=headers,
                                     data=json.dumps(payload),
                                     files=files,
                                     verify=False)
        elif method == "GET":
            files = {}
            payload = ''
            body = self.get_payload(request_test['body'])
            if body['method'] == 'formdata':
                files = body['data']
            elif body['method'] == 'raw':
                payload = body['data']
            req = requests.get(url, 
                               headers=headers, 
                               data=json.dumps(payload),
                               files=files,
                               verify=False)
        return {
            'response': req.text,
            'status': str(req.status_code),
            'method' : method,
            'url' : url
        }

    def get_item_folder(self,collection):
        change=False
        while 'item' in collection:
            collection = collection['item']
            change=True
        return {
            'collection' : collection,
            'change' : change
        }

    def parse_collection(self,collection,debug):
        collection_data=[]
        for item in collection['item']:
            if debug is True:
                printer.print_important_text(item['name'])
            item_folder=self.get_item_folder(item)
            if item_folder['change'] == True:
                for folder in item_folder['collection']:
                    if debug is True:
                        printer.success("-----> " + folder['name'])
                    collection_data.append(self.connection_test(folder['request']))
            else:      
                collection_data.append(self.connection_test(item['request']))
        return collection_data



    def start_postman_test(self,postman,debug):
        collection_response=self.parse_collection(postman['collection'],debug)

        return collection_response
        

