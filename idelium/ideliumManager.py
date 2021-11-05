"""
Integration Library for selenium
Author: idel fuschini

"""
import sys
from idelium.commons.resultEnum import result
from idelium.wrappers.ideliumSelenium import ideliumSelenium
from idelium.wrappers.ideliumAppium import ideliumAppium
import importlib.util
import sys
from pathlib import Path

class startManager():
   def load_module(self,name):
      print (name)
      name = name + ".plugin"
      print (name)
      mod = __import__(name,fromlist=['plugin'])
      return mod

   def getWrapper(self,config):
      wrapper=None
      if config['isRealDevice']==False:
         if config['is_debug']==True:
            print ('Using wrapper Selenium')
         wrapper=ideliumSelenium()
      else:
         if config['is_debug']==True:
            print ('Using wrapper Appium')
         wrapper=ideliumAppium()
      return wrapper
   

   def execute_step (self,driver,testConfigurations,config):
               status="1"
               stepFailed=""
               wrapper=config['wrapper']
               printer=config['printer']
               for objectStep in config['json_step']['steps']:
                  if status=="1":
                     returnObjectStep=wrapper.command(objectStep['stepType'],driver,config,objectStep)
                     if returnObjectStep != None: 
                        if 'config' in returnObjectStep.keys():
                           config = returnObjectStep['config']
                        if 'driver' in returnObjectStep.keys():
                           driver =  returnObjectStep ['driver']
                        if returnObjectStep['returnCode'] == result.ko:
                           status="2"
                     else:
                        try:
                           module =importlib.import_module("plugin." + objectStep['stepType'],package=__package__)
                           params=None
                           if 'params' in objectStep:
                              params=objectStep['params']
                           pluginResponse=module.init(driver,config['json_config'],params)
                           if pluginResponse == result.ko:
                              status="2"
                              print("Plugin response: " + objectStep['note'], end="->", flush=True)
                              printer.danger('FAILED')
                           if pluginResponse == result.na:
                              status="5"
                              print("Plugin response: " + objectStep['note'], end="->", flush=True)
                              printer.warning('NA')
                        except Exception as e:
                           printer.danger('----------')
                           print (e)
                           printer.danger('----------')
                           printer.danger("Warning stepType: " + objectStep['stepType'] + " not exist or there is an error in your extra module")
                           sys.exit(1)
                     if status == "2":
                        stepFailed = objectStep
                  else:
                     printer.danger(objectStep['stepType'] + ": skipped")
               return { "driver" : driver, "status" : status,"stepFailed" : stepFailed}

   def execute_single_step (self,testConfigurations,config):
            printer=config['printer']
            driver=None

            if config['isRealDevice']==False:
               if config['is_debug']==True:
                  print ('Using wrapper Selenium')
               wrapper=ideliumSelenium()
            else:
               if config['is_debug']==True:
                  print ('Using wrapper Appium')
               wrapper=ideliumAppium()
            for file_step_name in config['file_steps'].split(","):
               try:
                  json_step=testConfigurations['steps'][file_step_name]
                  printer.underline(json_step['name'])
                  config['wrapper']=wrapper
                  config['printer']=printer
                  config['json_step']=json_step
                  objectReturn=self.execute_step (driver,testConfigurations,config)
                  driver=objectReturn['driver']
                  stringToShow=file_step_name + " the return value " + objectReturn['status']
                  if objectReturn['status']=="1":
                     printer.success(stringToShow)
                  elif objectReturn['status']=="5":
                     printer.warning(stringToShow)                  
                  else:
                     printer.danger(stringToShow)

               except Exception as e:
                  printer.danger('---------- Execute step ------')
                  print (e)
                  printer.danger('----------')
                  printer.danger("Warning, the file step: " + file_step + " not exist or is not a json (err 2)")
                  sys.exit(1)  






