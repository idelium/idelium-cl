"""System module."""
from __future__ import absolute_import
import sys
from idelium.ideliummanager import StartManager
from idelium.ideliumws import IdeliumWs
from idelium.ideliumclib import InitIdelium
from idelium.thirdparties.ideliumzephyr import ZephyrConnection
from idelium.commons.ideliumprinter import InitPrinter
IDELIUM_VERSION="2.0.0"
idelium=StartManager()
printer=InitPrinter()
ideliumws=IdeliumWs()
ideliumClLib=InitIdelium()
printer.print_important_text ("Idelium Command Line " + IDELIUM_VERSION)
printer.print_important_text ("Selenium version:" + ideliumClLib.get_selenium_version())
defineParameters= ideliumClLib.define_parameters(sys.argv,ideliumws,printer)
cl_params=defineParameters['cl_params']
test_config=defineParameters['test_config']

if cl_params['ideliumServer'] is False:
    if cl_params['fileSteps'] is not None:
        idelium.execute_single_step (test_config,cl_params)
    elif cl_params['reportingService'] == 'idelium':
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
