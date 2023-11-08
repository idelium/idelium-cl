from __future__ import absolute_import
import requests
import json
import sys
import base64
from requests_hawk import HawkAuth
from hashlib import sha256
from idelium._internal.commons.postmantranslate import PostmanTranslate
from datetime import datetime
from requests_oauthlib import OAuth1
from argparse import HelpFormatter
from re import A
from urllib.parse import urlencode
from idelium._internal.commons.ideliumprinter import InitPrinter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



printer = InitPrinter()


class PostmanCollection:
    
    def find_element_in_array(self, array, key, value):
        for i in array:
            if key in i:
                if i[key]==value:
                    return i
        return ''        
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
            elif method == 'formdata':
                return_data = self.get_parser(request['formdata'])
            elif method == 'urlencoded':
                return_data = self.get_parser(request['urlencoded'])
            else:
                print("mode not found: " + method)
                sys.exit()

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
        authReturn = None
        if type_auth == 'oauth1':
            consumer_key = self.find_element_in_array(
                auth['oauth1'], 'key', 'consumerKey')['value']
            consumer_secret = self.find_element_in_array(
                auth['oauth1'], 'key', 'consumerSecret')['value']
            signature_method = self.find_element_in_array(
                auth['oauth1'], 'key', 'signatureMethod')['value']
            nonce = self.find_element_in_array(
                auth['oauth1'], 'key', 'nonce')['value']
            token = self.find_element_in_array(
                auth['oauth1'], 'key', 'token')['value']
            token_secret = self.find_element_in_array(
                auth['oauth1'], 'key', 'tokenSecret')['value']
            auth = OAuth1(consumer_key, consumer_secret, token, token_secret, signature_type='auth_header', signature_method=signature_method)
            authReturn = {
                'type': 'oauth1',
                'content': auth
            }
        elif type_auth == 'basic':
            username = self.find_element_in_array(
                auth['basic'], 'key', 'username')['value']
            password = self.find_element_in_array(auth['basic'],'key','password')['value']
            string_authentication=username + ':' + password
            message_bytes =string_authentication.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            authReturn = {
                'type': 'headers',
                'content': {
                    'Authorization': 'Basic ' + base64_message
                }
            }
        elif type_auth == 'digest':
            authReturn = {
                'type': 'getheaders',
                'content': None
            }
        elif type_auth == 'hawk':
            authid=self.find_element_in_array(
                auth['hawk'], 'key', 'authId')['value']
            authkey = self.find_element_in_array(
                auth['hawk'], 'key', 'authKey')['value']
            hawk_auth = HawkAuth(id=authid, key=authkey, algorithm='sha256')
            authReturn = {
                'type': 'hawk',
                'content': hawk_auth
            }
        return authReturn
            

    def connection_test(self,request_test,name_test,debug):
        ''' start '''
        method=request_test['method']
        url=request_test['url']['raw']
        headers = self.get_parser(request_test['header'])
        start_time = datetime.now()
        payload = {}
        auth=None
        redirect_allow=False
        auth_headers=None
        if 'auth' in request_test:
            auth_headers=self.get_auth(request_test['auth'])
            print (auth_headers)
            if auth_headers['type'] == 'headers':
                headers = auth_headers['content']
            elif auth_headers['type'] == 'hawk':
                auth = auth_headers['content']
            elif auth_headers['type'] == 'oauth1':
                auth = auth_headers['content']
                redirect_allow = True

        if method == "POST" or method == "PUT" or method == "PATCH" or method == "DELETE":
            files={}
            body = self.get_payload(request_test['body'])
        
            if body['method']=='formdata':
                files=body['data']
            elif body['method']=='raw':
                payload = body['data']
            if method== "POST":
                req = requests.post(url,
                                    headers=headers,
                                    auth=auth,
                                    data=json.dumps(payload),
                                    files=files,
                                    allow_redirects=redirect_allow,
                                    verify=False)
                
            elif method == "PUT":
                req = requests.put(url,
                                    headers=headers,
                                    auth=auth,
                                    data=json.dumps(payload),
                                    files=files,
                                    allow_redirects=redirect_allow,
                                    verify=False)
            elif method == "PATCH":
                req = requests.patch(url,
                                     headers=headers,
                                     auth=auth,
                                     data=json.dumps(payload),
                                     files=files,
                                    allow_redirects=redirect_allow,
                                     verify=False)
            elif method == "DELETE":
                req = requests.delete (url,
                                       headers=headers,
                                       auth=auth,
                                       data=json.dumps(payload),
                                       files=files,
                                    allow_redirects=redirect_allow,
                                       verify=False)
        elif method == "GET":
            files = {}      
            if auth_headers != None and auth_headers['type'] == 'oauth1':
                payload = {}
                req = requests.get(url,auth=auth)
            else:
                body = self.get_payload(request_test['body'])
                if body['method'] == 'formdata':
                    payload = body['data']
                elif body['method'] == 'raw':
                    payload = body['data']
                req = requests.get(url,
                                    headers=headers,
                                    auth=auth,
                                    data=payload,
                                    files=files,
                                    allow_redirects=redirect_allow,
                                    verify=False)
        finish_time = datetime.now()
        if debug == True:
            print("Headers: " + json.dumps(headers))
            print("Payload: " + json.dumps(payload))
            print("Response: " + req.text)
        delta = (finish_time - start_time)
        return {
            'name' : name_test,
            'response': req.text,
            'status': str(req.status_code),
            'method' : method,
            'url' : url,
            'time' : delta.total_seconds()
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
                    #if folder['name'] == 'OAuth1.0 Verify Signature':
                    collection_data.append(self.connection_test(folder['request'],folder['name'], debug))
                        #sys.exit()

            else:      
                collection_data.append(self.connection_test(item['request'],debug))
        return collection_data

    def start_postman_test(self,postman,debug):
        collection_response=self.parse_collection(postman['collection'],debug)

        return collection_response
        

