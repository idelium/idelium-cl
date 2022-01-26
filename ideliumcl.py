"""System module."""
from __future__ import absolute_import
import sys
import ssl
import os
from http.server import HTTPServer

from idelium.ideliummanager import StartManager
from idelium.ideliumserver import IdeliumServer
from idelium.ideliumws import IdeliumWs
from idelium.ideliumclib import InitIdelium
from idelium.thirdparties.ideliumzephyr import ZephyrConnection
from idelium.commons.ideliumprinter import InitPrinter
idelium=StartManager()
printer=InitPrinter()
ideliumws=IdeliumWs()
idelium_cl_lib=InitIdelium()
IDELIUM_VERSION = '2.0.1'
printer.print_important_text("Idelium Command Line " + IDELIUM_VERSION)
printer.print_important_text ("Selenium version:" + idelium_cl_lib.get_selenium_version())
define_parameters= idelium_cl_lib.define_parameters(sys.argv,ideliumws,printer)
cl_params=define_parameters['cl_params']

if cl_params['ideliumServer'] is False:
    define_parameters = idelium_cl_lib.load_parameters(cl_params, ideliumws, printer)
    cl_params = define_parameters['cl_params']
    test_config = define_parameters['test_config']
    if cl_params['reportingService'] == 'idelium':
        ideliumws.start_test(idelium,test_config,cl_params)
    elif cl_params['reportingService'] == 'zephyr':
        zephyr=ZephyrConnection()
        if cl_params['idJira'] is not None:
            zephyr.start_test_case(idelium,test_config,cl_params)
        else:
            zephyr.go_execution(idelium,cl_params)
    else:
        printer.danger('Error: ' + cl_params['reportingService'] + ' has a wrong value')
    printer.success('Finish test')
else:
    if os.path.exists(cl_params['dir_idelium_scripts'] + 'server'):
        os.remove(cl_params['dir_idelium_scripts'] + 'server')
    server_address = ('0.0.0.0', cl_params['ideliumServerPort'])
    IdeliumServer.init(idelium, cl_params, ideliumws, idelium_cl_lib,printer)
    sslctx = ssl.SSLContext()
    sslctx.check_hostname = False
    sslctx.load_cert_chain(certfile='cert/cert.pem', keyfile="cert/key.pem")
    httpd = HTTPServer(server_address, IdeliumServer)
    httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
    printer.success('Server start on port:' +
          str(cl_params['ideliumServerPort']))
    httpd.serve_forever()
