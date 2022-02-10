"""System module."""
import os
import json
from http.server import BaseHTTPRequestHandler
from threading import Thread

class IdeliumServer(BaseHTTPRequestHandler):
    ''' IdeliumServer '''

    def init(idelium_get,params,ws,cllLib,prn):
        global idelium
        global cl_params
        global ideliumws
        global idelium_cl_lib
        global printer
        idelium = idelium_get
        cl_params = params
        ideliumws=ws
        idelium_cl_lib = cllLib
        printer = prn
    def do_GET(self):
        global idelium
        global cl_params
        global ideliumws
        global idelium_cl_lib
        global printer
        '''
            path= /idCycle/idProject/environment/<optional>
        '''
        data = self.path.split("/")
        if data[1] == 'reset':
            os.remove(cl_params['dir_idelium_scripts'] + 'server')
            self.wfile.write(
                bytes('{"message": "reset done"}', "utf-8"))
        else:
            print('ko')
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(
                    bytes('{"message": "invalid request"}', "utf-8"))

    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        if self.path == '/launchtest':
            json_post=json.loads(post_data.decode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            params = cl_params
            params['idCycle'] = json_post['idTestCycle']
            params['idProject'] = json_post['idProject']
            params['environment'] = json_post['environment']
            params['ideliumKey'] = json_post['key']
            params['browser'] = json_post['browser']
            self.close_connection
            if not os.path.exists(cl_params['dir_idelium_scripts'] + 'server'):
                define_parameters = idelium_cl_lib.load_parameters(
                    params, ideliumws, printer)
                if define_parameters is False:
                    self.wfile.write(
                        bytes('{"message": "bad parameters"}', "utf-8"))
                else:
                    params = define_parameters['cl_params']
                    params['json_config']['browser'] == params['browser']
                    test_config = define_parameters['test_config']
                    if cl_params['reportingService'] == 'idelium':
                        Thread(target=ideliumws.start_test, args=[
                            idelium, test_config, params]).start()
                        self.wfile.write(
                            bytes('{"message": "test started"}', "utf-8"))
            else:
                self.wfile.write(
                    bytes('{"message": "another test is running, please retry"}', "utf-8"))




