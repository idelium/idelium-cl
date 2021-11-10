"""
Idelium ws library
Author: idel fuschini
"""

from urllib.parse import urlencode
import requests,json,collections,sys,datetime,time,os
from pathlib import Path
from PIL import Image
import base64


class typeDir():
    PROJECT_MAIN_DIR=0
    PROJECT_DIR=1
    IDCYCLE_DIR=2
    STEP_DIR=3
    CONFIGURATIONSTEP_DIR=4
    PLUGIN_DIR=5
    ENVIRONMENTS_DIR=6
class connection():
    def start(method,url,payload=None,apiKey=None,debug=False):
        r = None
        headers = {'Content-Type': 'application/json','Idelium-Key' : apiKey }
        if method=="POST":
            r = requests.post(url,headers=headers,data=json.dumps(payload),verify=False)
        elif method=="PUT":
            r = requests.put(url,headers=headers,data=json.dumps(payload),verify=False)
        elif method=="GET":
            r = requests.get(url,headers=headers,verify=False)
        if debug == True:
                print("Response: " + r.text)
                print("Headers: " + json.dumps(headers))
                print("Payload: " + json.dumps(payload))
                print(str(r.status_code) + " " + method + " " + url)
        return json.loads(r.text,object_pairs_hook=collections.OrderedDict)   

class ideliumWs():
    def createFolder(self,config):
            url=config['url'] + 'testcycle' 
            payload = {
                    "testCycleId": config['idCycle'],
                    }
            return connection.start('POST',url,payload,config['ideliumKey'],config['is_debug'])
    def createTest(self,config,idTest,name):
            url=config['url'] + 'test' 
            payload = {
                    "testCycleId": config['idCycle'],
                    "testId" : idTest,
                    "name" : name,
                    }
            return connection.start('POST',url,payload,config['ideliumKey'],config['is_debug'])
    def updateTest(self,config,testId,status):
            url=config['url'] + 'test' 
            payload = {
                    "testId" : testId,
                    "status" : status,
                    }
            return connection.start('PUT',url,payload,config['ideliumKey'],config['is_debug'])
    def createStep(self,config,idTest,idStep,name,status):
            url=config['url'] + 'step' 
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "testCycleId": config['idCycle'],
                    "testId" : idTest,
                    "stepId" : idStep,
                    "name" : name,
                    "status" : int(status),
                    "screenshots" : "[]",
                    }
            return connection.start('POST',url,payload,config['ideliumKey'],config['is_debug'])
    def updateStep(self,config,idStep,screenshots):
            url=config['url'] + 'step' 
            payload = {
                    "stepId" : idStep,
                    "screenshots" : json.dumps(screenshots),
                    }
            return connection.start('PUT',url,payload,config['ideliumKey'],config['is_debug'])

    def getEnvironments(self,config):
        url=config['url'] + 'environments/' + str(config['idProject'])
        return connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])

    def getCycles(self,config):
        url=config['url'] + 'testcycle/' + config['idCycle']
        jsonCycle=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])
        if 'config' in jsonCycle:
            return json.loads(jsonCycle['config'])
        else:
            return -1

    def getTests(self,config,id):
        url=config['url'] + 'test/' + str(id)
        jsonTest=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])
        return json.loads(jsonTest['config'])
    
    def getStep(self,config,id):
        url=config['url'] + 'step/' + str(id)
        jsonStep=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])
        return {
            "objectStep" : json.loads(jsonStep['config']),
            "step_json_name" : jsonStep['name'] + '_' + str(id),
            "step_json_description" : jsonStep['name'],
        }


    def createDirectories(self,config):
        configurationDirectories=[
            config['dir_idelium_scripts'],
            config['dir_idelium_scripts'] + "/" + config['idProject'],
            config['dir_idelium_scripts'] + "/" + config['idProject'] + "/" + config['idCycle'],
            config['dir_idelium_scripts'] + "/" + config['idProject'] + "/" + config['idCycle'] + "/step",
            config['dir_idelium_scripts'] + "/" + config['idProject'] + "/" + config['idCycle'] + "/configurationStep",
            config['dir_idelium_scripts'] + "/" + config['idProject'] + "/" + config['idCycle'] + "/plugin",
            config['dir_idelium_scripts'] + "/" + config['idProject'] + "/" + config['idCycle'] + "/environments",
        ]
        if config['local'] == True:
            for dir in configurationDirectories:
                p = Path(dir)
                if p.exists() == False:
                    if config['is_test']==True:
                        print ('create ' + dir)
                    os.mkdir(dir)
        else:
            print ('start download configuration')
        return configurationDirectories


    def downloadConfigurationFiles(self, config):
        printer=config['printer']
        configurationStep={}
        configurationDirectories=self.createDirectories(config)
        objectCycle=self.getCycles(config)
        if objectCycle == -1:
            printer.danger('The idCycle ' + str(config['idCycle']) + ' not exist')
            sys.exit(1)
        arraySteps={}
        arrayEnvironments={}
        arrayPlugins={}
        configStep=None
        """
        search cycle for this cycle
        """
        for cycle in objectCycle:
            """
            search test for this cycle
            """
            objectTest=self.getTests(config,cycle['id'])
            for test in objectTest:
                step=self.getStep(config,test['id'])
                """
                write step
                """
                arraySteps[step['step_json_name']]=step['objectStep']
                print (step['step_json_name'])
                jsonFilePath=configurationDirectories[typeDir.STEP_DIR] + "/" + step['step_json_name'] + '.json'
                if config['local']==True and (Path(jsonFilePath).exists()==False or config['forcedownload']==True):
                    with open(jsonFilePath, 'w') as f:
                        json.dump(step['objectStep'], f,indent=4, sort_keys=False)
        """
        write_configuration_step
        """
        configStep=None
        jsonFilePath=configurationDirectories[typeDir.CONFIGURATIONSTEP_DIR] + '/config_step.json'
        if config['local']==True and (Path(jsonFilePath).exists()==False or config['forcedownload']==True):
            with open(jsonFilePath, 'w') as f:
                json.dump(configurationStep, f,indent=4, sort_keys=False)
               
        """
        search  plugins for projectId
        """
        url=config['url'] + 'plugins/' + str(config['idProject'])
        jsonPlugins=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])
        for pluginDet in jsonPlugins:
            url=config['url'] + 'plugin/' + str(pluginDet['id'])
            jsonPlugin=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])      
            """
            save  plugin for projectId
            """
            arrayPlugins[jsonPlugin['name']]=jsonPlugin['code']
            pyFilePath=configurationDirectories[typeDir.PLUGIN_DIR] + "/" + jsonPlugin['name'] + '.py'   
            if config['local']==False:
                    pluginsDir=config['dir_idelium_scripts'] + "/plugin"
                    p = Path(pluginsDir)
                    if p.exists() == False:
                        os.mkdir(pluginsDir)
                        if config['is_debug']==True:
                            print('created temporary directory', pluginsDir)         
                    pyFilePath=pluginsDir + "/" + jsonPlugin['name'] + '.py' 

            if Path(pyFilePath).exists()==False or config['forcedownload']==True:
                py_file = open(pyFilePath, "wt")
                n = py_file.write(jsonPlugin['code'])
                py_file.close()
        """
        download environments
        """
        jsonEnvironments=self.getEnvironments(config)
        printer.success('finish download file')
        for env in jsonEnvironments:
            url=config['url'] + 'environment/' + str(env['id'])        
            jsonEnvironment=connection.start('GET',url,None,config['ideliumKey'],config['is_debug'])
            fileNameEnvironment=jsonEnvironment['code']
            codeEnvironment=json.loads(jsonEnvironment['config'],object_pairs_hook=collections.OrderedDict)
            arrayEnvironments[fileNameEnvironment]=codeEnvironment
            jsonFilePath=configurationDirectories[typeDir.ENVIRONMENTS_DIR] + '/' + fileNameEnvironment +".json"
            if config['local']==True and (Path(jsonFilePath).exists()==False or config['forcedownload']==True):
                with open(jsonFilePath, 'w') as f:
                    json.dump(codeEnvironment, f,indent=4, sort_keys=False)
        return { 
            "steps": arraySteps,
            "environments" : arrayEnvironments,
            "plugins" : arrayPlugins,
            "configStep" : configStep,
            "environmentDir" : configurationDirectories[typeDir.ENVIRONMENTS_DIR],
            "stepDir" : configurationDirectories[typeDir.STEP_DIR],
            "configStepDir" : configurationDirectories[typeDir.CONFIGURATIONSTEP_DIR],
            "idCycleDir" : configurationDirectories[typeDir.IDCYCLE_DIR],
        }

    def startTest(self,idelium,testConfigurations,config):
        wrapper=idelium.getWrapper(config)
        objectCycle=self.getCycles(config)
        driver=None
        
        idCycle=self.createFolder(config)['idCycle']
        for cycle in objectCycle:
            """
            search test for this cycle
            """
            printer=config['printer']
            objectTest=self.getTests(config,cycle['id'])
            printer.success('Test: ' + cycle['description'])
            idTest=self.createTest(config,idCycle,cycle['name'])['idTest']
            testFailed=False
            for test in objectTest:
                if testFailed==False:
                    json_step=testConfigurations['steps'][test['name'] + '_' + str(test['id'])]
                    print (json.dumps(json_step))
                    printer.underline(json_step['name'] + '(' + str(test['id']) + ')')
                    config['wrapper']=wrapper
                    config['printer']=printer
                    config['json_step']=json_step
                    objectReturn=idelium.execute_step (driver,testConfigurations,config)
                    status=objectReturn['status']
                    driver=objectReturn['driver']
                    stepFailed=objectReturn['stepFailed']
                    config['status']=status
                    config['stepFailed']=stepFailed
                    idStep=None
                    if config['is_test']==False:
                        idStep=self.createStep(config,idTest,test['id'],test['name'],status)['idStep']                   
                    if status=="2" or status=="5":
                        path='screenshots/'
                        file_name=str(idTest) + ".png"
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if config['json_step']['attachScreenshot'] == True:
                            wrapper.screen_shot(driver,path + file_name)    
                        if config['is_test']==False:
                            file_name_jpg=path + str(idTest) + ".jpg"
                            with Image.open(path + file_name) as im:
                                rgb_im = im.convert('RGB')
                                rgb_im.save(file_name_jpg)
                                with open(file_name_jpg, "rb") as img_file:
                                    screenshotBase64 = base64.b64encode(img_file.read())
                                    self.updateStep(config,idStep,['data:image/jpg;base64,' + str(screenshotBase64)[2:-1]])

                            os.unlink(path + file_name)
                            os.unlink(file_name_jpg)
                        if config['json_step']['failedExit'] == True:
                            printer.danger( "The test '" + cycle['name'] + "' it is forcibly interrupted due to the blocking failure of the step")
                            idTest=self.updateTest(config,idTest,2)
                            testFailed=True
                    else:
                        self.updateTest(config,idTest,1)
            
            driver.quit()
