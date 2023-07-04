from __future__ import absolute_import
from argparse import HelpFormatter

import json
import collections
from re import A
import sys
import datetime
import time
import os
from urllib.parse import urlencode
import requests
from idelium._internal.commons.ideliumprinter import InitPrinter
'''from postpy2.core import PostPython'''
from idelium._internal.thirdparties.postpy2.core import PostPython


class PostmanCollection:
    ''' PostmanCollection '''
    @staticmethod
    def start_postman_test(collection):
        print ('postman')
        printer = InitPrinter()
        runner = PostPython(collection['collection'])
        if collection['environment'] != None:
            runner.environments.load(collection['environment'])
        #response = runner.AuthDigest.digestauth_request()
        folders= runner.getmethods()
        print ("---------")
        response_test={}
        for methods in  folders:
            for method in methods:
                array_name=method.split(".")
                call=array_name[1] + "."  + array_name[2]
                object = getattr(runner, array_name[1])
                response = getattr(object, array_name[2])
                #try: 
                test=response()
                attributes = [
                            'apparent_encoding',
                            'content',
                            'cookies',
                            'elapsed',
                            'encoding',
                            'headers',
                            'history',
                            'is_permanent_redirect',
                            'is_redirect',
                            'links',
                            'next',
                            'ok',
                            'raw',                 
                            'reason',
                            'request',
                            'status_code',
                            'text',
                            'url'                        
                    ]
                results={}
                for attribute in attributes:
                    results[attribute]=str(getattr(test,attribute))
                response_test[call] = results
                #except:
                #    printer.danger ("Error call: " + call  +  "()")
                #print ("------------------------------------------------")
                
        #print(json.dumps(response_test,indent=4))
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(response_test,f, indent=4)
        return response_test
        
