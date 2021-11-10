"""
idelium-cl
Author: idel fuschini

"""
import sys,json,os
from pathlib import Path
from idelium.ideliumManager import startManager
from idelium.ideliumWs import ideliumWs
from idelium.ideliumClLib import initIdelium
from idelium.thirdparties.ideliumZephyr import zephyrConnection
from idelium.commons.ideliumPrinter import initPrinter
import urllib.parse
import tempfile
ideliumVersion="1.0.5"
idelium=startManager()
printer=initPrinter()
ideliumws=ideliumWs()
ideliumClLib=initIdelium()
zephyr=zephyrConnection()

execution_name="automation test python"
base_url=None
zapi_url=None
api_url=None
dir_configuration_step='configurationStep'
dir_step_files='step'
dir_plugins="plugin"
dir_idelium_scripts='./configuration'
is_test=False
is_debug=False
device=None
width=1920
height=1080
username=None
password=None
environmentName=None
idJira=None
file_steps=None
idVersion=None
idCycle=None
user_agent=None
idProject=None
idChannel = None
url = None
isRealDevice = False
os = None
appiumServer = None
appiumDesiredCaps = None
count=0
ideliumws_baseurl="https://service.idelium.io"
ideliumKey=None
reportingService= 'idelium'
forcedownload=False
local=False

checkRequired=ideliumClLib.getReguiredParams()

print ("Idelium Command Line " + ideliumVersion)
for i in sys.argv:
   array_command=i.split("=")
   if array_command[0] == "--username":
      username=array_command[1]
      checkRequired['username']=1
   elif array_command[0] == "--password":
      password=array_command[1]
      checkRequired['password']=1
   elif array_command[0] == "--environment":
      environmentName=array_command[1]
      checkRequired['environment']=1
   elif array_command[0] == "--idJira":
      idJira=array_command[1]
      checkRequired['idJira']=1
   elif array_command[0] == "--idVersion":
      idVersion=array_command[1]
      checkRequired['idVersion']=1
   elif array_command[0] == "--idCycle":
      idCycle=array_command[1]
      checkRequired['idCycle']=1
   elif array_command[0] == "--idProject":
      idProject = array_command[1]
   elif array_command[0] == "--idChannel":
      idChannel = array_command[1]
   elif array_command[0] == "--useragent":
      user_agent=array_command[1]
   elif array_command[0] == "--jiraApiUrl":
      api_url=array_command[1]
   elif array_command[0] == "--zephyrApiUrl":
      zapi_url=array_command[1]
   elif array_command[0] == "--dirConfigurationStep":
      dir_configuration_step=array_command[1]
   elif array_command[0] == "--dirStepFiles":
      dir_step_files=array_command[1]
   elif array_command[0] == "--dirIdeliumScript":
      dir_idelium_scripts=array_command[1]
   elif array_command[0] == "--height":
      height=int(array_command[1])
   elif array_command[0] == "--width":
      width=int(array_command[1])
   elif array_command[0] == "--device":
      device=array_command[1]
   elif array_command[0] == "--test":
      is_test=True
   elif array_command[0] == "--verbose":
      is_debug=True  
   elif array_command[0] == "--fileSteps":
      file_steps=array_command[1]
   elif array_command[0] == "--url":
      url = array_command[1]
   elif array_command[0] == "--ideliumws_baseurl":
      ideliumws_baseurl = array_command[1]
   elif array_command[0] == "--reportingService":
      reportingService = array_command[1]
   elif array_command[0] == "--ideliumApi":
      ideliumApi = array_command[1]
   elif array_command[0] == "--ideliumKey":
      ideliumKey=''
      for i in array_command:
         if i != "--ideliumKey":
            if i == '':
               ideliumKey = ideliumKey + '='
            else:
               ideliumKey = ideliumKey + i
   elif array_command[0] == "--help":
      print(ideliumClLib.getSyntax())
      sys.exit(0)
   else:
      if (count > 0):
         print ("\n" + array_command[0] + ": is not a valid option")
         print (ideliumClLib.getSyntax())
         sys.exit(1)
   count=count=count + 1
countRequired=0

if ideliumKey==None:
   fileIdeliumKey=str(Path.home()) + '/.idelium'
   if Path(fileIdeliumKey).is_file()==True:
      f = open(fileIdeliumKey, "r")
      ideliumKey=f.read()
   else:
      print (ideliumClLib.getSyntax())
      printer.danger('ideliumKey is not setted !')
      sys.exit(1)

for i in checkRequired:
   countRequired=countRequired + checkRequired[i] 

if file_steps == None:
   if reportingService == 'idelium':
      if (idProject == None or idCycle == None ):
         print (ideliumClLib.getSyntax())
         printer.danger("\nidProject and idCycle are mandatory")
         sys.exit(1)

   if reportingService=='zephyr':
      if countRequired <4:
         print (ideliumClLib.getSyntax())
         printer.danger ("\nMissed required options")
         sys.exit(1)

      if (idVersion == None and idCycle != None) or (idVersion != None and idCycle == None):
         printer.danger ("\nversionId and cycleId must be setted together")
         print (ideliumClLib.getSyntax())
         sys.exit(1)
      if len (sys.argv) < 5:
         print (ideliumClLib.getSyntax())
         sys.exit(1)

api_idelium=ideliumws_baseurl + '/api/ideliumcl/'
'''
   configure default path for chromedriver
'''
sys.path.insert(0,'./chromedriver/last')

if environmentName == None:
      print ("\nenvironment must be set")
      print (ideliumClLib.getSyntax())
      sys.exit(1)

if local==False:   
   dir_idelium_scripts=tempfile.gettempdir()
   sys.path.append(dir_idelium_scripts)
#else:
#   if reportingService=='idelium':
#      dir_idelium_scripts=dir_idelium_scripts + "/" + idProject + "/" + idCycle
#   elif reportingService=='zephyr':
#      if idProject != None:
#         if idChannel == None:
#            print("\nwith idProject setted usually idChannel must be set")
#         else:
#            dir_idelium_scripts=dir_idelium_scripts + "/" + idProject + "/" + idChannel
testConfigurations=None
testConfigurations=ideliumws.downloadConfigurationFiles({
      "printer" : printer,
      "url" : api_idelium,
      "idCycle" : idCycle,
      "ideliumKey" : ideliumKey,
      "is_debug" : is_debug,
      "dir_idelium_scripts" : dir_idelium_scripts,
      "idProject" : idProject,
      "forcedownload" : forcedownload,
      "is_test" : is_test,
      "local" : local,
   })
environment=testConfigurations['environmentDir'] + "/" + environmentName
file_configuration_step=testConfigurations['configStepDir'] + '/config_step.json'
if local==True:   
   sys.path.append(testConfigurations['idCycleDir'])



json_config=None
json_step_config=None

if local==False:
   print ('Environment:' + environmentName)
   if environmentName in testConfigurations['environments']: 
      json_config=testConfigurations['environments'][environmentName]
   else:
      printer.danger('Environment "' + environmentName + '" or idProject ' + idProject + ' not exist')
      sys.exit(1)
else:
   try:
      with open(environment + ".json") as json_data:
            json_config = json.load(json_data)

   except:
      printer.danger("The environment: " + environment + " not exist or i not a json")
      sys.exit(1)
if 'userAgent' in json_config:
   user_agent=json_config['userAgent']
if 'isRealDevice' in json_config:
   isRealDevice=json_config['isRealDevice']
if 'appiumServer' in json_config:
   appiumServer=json_config['appiumServer']
if 'isRealDevice' in json_config:
   appiumDesiredCaps=json_config['appiumDesiredCaps']
if idProject != None:
   json_config['projectId'] = idProject


if local==False:
   json_step_config=testConfigurations['configStep']
else:
   try:
      print ("Loading Steps")
      with open(file_configuration_step) as json_data:
            json_step_config = json.load(json_data)
   except:
      printer.danger("The file configuration: " + file_configuration_step + " not exist or is not a json")
      sys.exit(1)
   if idProject != None:
      json_step_config['idProject']=idProject
   if 'device' in json_config:
      device = json_config['device']
   if url != None:
      json_config['url']=url


if file_steps != None:
   idelium.execute_single_step (testConfigurations,{
      "printer" : printer,
      "dir_step_files" : dir_step_files,
      "dir_plugins" : dir_plugins,
      "file_steps" : file_steps,
      "json_config" : json_config,
      "user_agent" : user_agent,
      "device" : device,
      "width" : width,
      "height" : height,
      "is_debug" : is_debug,
      "isRealDevice" : isRealDevice,
      "os" : os,
      "appiumServer" : appiumServer,
      "appiumDesiredCaps" : appiumDesiredCaps,
      "local" : local,
   })
elif reportingService=='idelium':
      ideliumws.startTest(idelium,testConfigurations,{
         "printer" : printer,
         "url" : api_idelium,
         "idCycle" : idCycle,
         "ideliumKey" : ideliumKey,
         "dir_idelium_scripts" : dir_idelium_scripts,
         "idProject" : idProject,
         "dir_step_files" : dir_step_files,
         "dir_plugins" : dir_plugins,
         "file_steps" : file_steps,
         "json_config" : json_config,
         "user_agent" : user_agent,
         "device" : device,
         "width" : width,
         "height" : height,
         "is_debug" : is_debug,
         "is_test" : is_test,
         "isRealDevice" : isRealDevice,
         "os" : os,
         "appiumServer" : appiumServer,
         "appiumDesiredCaps" : appiumDesiredCaps,
         "local" : local,
      })
elif reportingService=='zephyr':
      if idJira !=None:
         zephyr.start_test_case(idelium,testConfigurations,{
                           "device":device,
                           "printer" : printer,
                           "width" :width,
                           "height" :height,
                           "dir_step_files" :dir_step_files,
                           "dir_plugins": dir_plugins,
                           "execution_name" :execution_name,
                           "is_test" :is_test,
                           "is_debug" :is_debug,
                           "idJira" :idJira,
                           "original_execution_id" : None,
                           "folder_id" : None,
                           "idCycle" : idCycle,
                           "idVersion" : idVersion,
                           "json_config" : json_config,
                           "json_step_config" : json_step_config,
                           "zapi_url" : zapi_url,
                           "api_url" : api_url,
                           "user_agent" :user_agent,
                           "username" :username,
                           "password" :password,
                           "isRealDevice" :isRealDevice,
                           "os": os,
                           "appiumServer" : appiumServer,
                           "appiumDesiredCaps" :appiumDesiredCaps,
                           "local" : local,
         })
      else:
         zephyr.go_execution(idelium,testConfigurations,{
                        "device" : device,
                        "printer" : printer,
                        "width" : width,
                        "height" : height,
                        "dir_step_files" : dir_step_files,                       
                        "dir_plugins" : dir_plugins,
                        "execution_name" : execution_name,
                        "is_test" : is_test,
                        "is_debug" : is_debug,
                        "idCycle" : idCycle,
                        "idVersion" : idVersion,
                        "json_config" : json_config,
                        "json_step_config" : json_step_config,
                        "zapi_url" : zapi_url,
                        "api_url": api_url,
                        "user_agent": user_agent,
                        "username": username,
                        "password": password,
                        "isRealDevice":isRealDevice,
                        "os": os,
                        "appiumServer": appiumServer,
                        "appiumDesiredCaps" : appiumDesiredCaps,
                        "local" : local,
         })
else:
   printer.danger('Error: "reportingService" has a wrong value')

print ('Finish test')
