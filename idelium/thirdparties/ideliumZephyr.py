"""
Integration Library for zaphy/jira
Author: idel fuschini
"""
from idelium.commons.ideliumPrinter import initPrinter
from urllib.parse import urlencode
import requests,json,collections,sys,datetime,time,os

class zephyrConnection():
    def get_date(self):
            today = datetime.date.today()
            return today.strftime('%Y-%m-%d')  

    def getTestCase(self,is_debug,is_test,api_url,zapi_url,issue,username,password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            printer=initPrinter()
            isOk=False
            """
                give all the step of testcase
            """
            urlIssue=api_url + 'issue/' + issue
            r = requests.get(urlIssue, auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " GET " + urlIssue)
                print(r.text)
            if r.status_code != 200:
                printer.danger("credential error o issue jira not exist")
                sys.exit(1)
            json_jira=json.loads(r.text,object_pairs_hook=collections.OrderedDict)
            if 'status' in json_jira['fields']:
                if 'name' in json_jira['fields']['status']:
                    if json_jira['fields']['status']['name']== 'Executable' or is_test==True:
                        isOk=True
                    else:
                        printer.danger("The issue " + issue + " is not 'Executable' but '" + json_jira['fields']['status']['name']  +"' so is skipped")
            urlzephyr=zapi_url + 'teststep/' + json_jira['id']
            r = requests.get(urlzephyr, auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " GET " + urlzephyr)
                print("Response: " + r.text)
            json_zephyr=json.loads(r.text,object_pairs_hook=collections.OrderedDict)
            return {"zapyhrObject" :json_zephyr, "jiraIssueId" : json_jira['id'],"isGoodIssueForTest" : isOk}
        
    def createCycle (self,is_debug,zapi_url,project_id,version_id,name,username,password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'cycle'
            if version_id == None:
                version_id = "-1"
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "name": name,
                    "startDate": self.get_date(),
                    "endDate": self.get_date(),
                    "projectId": project_id,
                    "versionId": version_id,
                    "sprintId": None
                    }
            r = requests.post(url,headers=headers,data=json.dumps(payload),auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " POST " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def createExecution (self,is_debug,zapi_url,cycle_id,folder_id,issue_id,project_id,username,password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'execution'
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "cycleId": cycle_id,
                    "issueId": issue_id,
                    "projectId": project_id,
                    }
            if folder_id != None:
                payload['folderId'] = folder_id
            r = requests.post(url,headers=headers,data=json.dumps(payload),auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " POST " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def createCycleFolder (self,is_debug,environment,zapi_url,cycle_id,version_id,project_id,username,password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'folder/create'
            headers = {'Content-Type': 'application/json'}
            nameFolder= "["  + environment + "] " +  datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 
            payload = {
                    "cycleId": cycle_id,
                    "name": nameFolder,
                    "description": "created test folder for this cycle",
                    "projectId": project_id,
                    "versionId": version_id    
                }
            r = requests.post(url,headers=headers,data=json.dumps(payload),auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " POST " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def getExecutions (self,is_debug,zapi_url,cycle_id,version_id,project_id,offset,username,password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'execution'
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "cycleId": cycle_id,
                    "versionId": version_id,
                    "action": "expand",
                    "projectId": project_id,
                    "offset" : offset,
                    "sorter" : "OrderId:ASC"
                    }
            query_string=urlencode(payload)
            url = url + "?" + query_string 
            r = requests.get(url,headers=headers, auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " GET " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def getStepId (self,is_debug,zapi_url,executionId,username,password):        
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'stepResult?executionId=' + str(executionId)
            r = requests.get(url, auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " GET " + url)
                print("Response: " + r.text)
            return json.loads(r.text)

    def updateTestStep(self, is_debug, zapi_url, stepId, status, stepFailed, username, password):
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'stepResult/' + str(stepId)
            headers = {'Content-Type': 'application/json'}
            comment = ''
            if stepFailed != None:
                if 'note' in stepFailed:
                    comment='Error:' + stepFailed['note']
            payload = {
                    "status": status,
                    "comment": comment
            }
            r = requests.put(url,headers=headers,data=json.dumps(payload),auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " PUT " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def updateExecution (self,is_debug,zapi_url,execution_id,status,username,password):        
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            url=zapi_url + 'execution/' + str(execution_id) + "/execute"
            headers = {'Content-Type': 'application/json'}
            payload = {
                    "status": status,
                    }
            r = requests.put(url,headers=headers,data=json.dumps(payload),auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " PUT " + url)
                print("Payload: " + json.dumps(payload))
                print("Response: " + r.text)
            return json.loads(r.text)
    def addAttachmentBuffered (self,is_debug,zapi_url,path,file_name,step_id,entity_type,username,password):        
            os.environ["NO_PROXY"]="jira.g2-networks.net"
            """
            Possible types: EXECUTION, STEPRESULT
            """
            url=zapi_url + 'attachment?entityId=' + str(step_id) + '&entityType=' + entity_type
            f=open(path  + file_name,'rb')
            files = {'file':(file_name, f, "multipart/form-data")}
            headers = {
                "X-Atlassian-Token": "nocheck",
                "Accept": "application/json",   
            }
            r = requests.post(url,headers=headers,files=files,auth=(username, password))
            if is_debug==True:
                print(str(r.status_code) + " POST " + url)
                print("Response: " + r.text)
            return json.loads(r.text)

#
#  Jira/Zaphyr interface
#


    def go_execution(self,idelium,config):
      printer=config['printer']
      zephyr=zephyrConnection()
      project_id=config['json_config']['projectId']
      for idCycle in config['idCycle'].split(","):
         printer.success("Start cycleId:" + str(idCycle))
         exit = False
         count=0
         offset=0
         folder_id=None

         if config['is_test']==False:
            jsonCreateFolder=self.createCycleFolder(config['is_debug'],
                                                      config['json_config']['environment'],
                                                      config['zapi_url'],
                                                      idCycle,
                                                      config['idVersion'],
                                                      config['project_id'],
                                                      config['username'],
                                                      config['password']
                                                      )
            if 'id' in jsonCreateFolder:
               folder_id=jsonCreateFolder['id']
            else:
               printer.danger('Jira Error:' + jsonCreateFolder['error'])
               sys.exit()
         while exit == False:
            returnExecution=self.getExecutions(config['is_debug'],config['zapi_url'],idCycle,config['idVersion'],project_id,offset,config['username'],config['password'])
            for execution in returnExecution['executions']:
               id_jira=execution['issueKey']
               original_execution_id=execution['id']
               execution_name=execution['cycleName']
               idCycle=execution['cycleId']
               printer.printImportantText(id_jira + ": " + execution['summary'])
               config['execution_name']=execution_name
               config['id_jira']=id_jira
               config['original_execution_id']=original_execution_id
               config['folder_id']=folder_id
               config['idCycle']=idCycle
               self.start_test_case(config)
               count=count + 1
            if count == returnExecution['totalExecutions']:
               exit=True
            else:
               offset=offset +  10

    def start_test_case(self,idelium,testConfigurations,config):
      printer=config['printer']
      wrapper=idelium.getWrapper(config)
      project_id=config['json_config']['projectId']
      zapyhrObject=self.getTestCase(config['is_debug'],
                                       config['is_test'],
                                       config['api_url'],
                                       config['zapi_url'],
                                       config['idJira'],
                                       config['username'],
                                       config['password'])
      if len(zapyhrObject['zapyhrObject']) and zapyhrObject['isGoodIssueForTest']==True:
         executionId=None
         returnExecution=None
         if config['is_test']==False:
            if config['idCycle']==None:
                     returnCycle=self.createCycle(config['is_debug'],
                                                      config['zapi_url'],
                                                      config['project_id'],
                                                      config['idVersion'],
                                                      config['execution_name'],
                                                      config['username'],
                                                      config['password'])
                     returnExecution=self.createExecution(config['is_debug'],
                                                            config['zapi_url'],
                                                            config['returnCycle']['id'],
                                                            config['folder_id'],
                                                            config['zapyhrObject']['jiraIssueId'],
                                                            config['project_id'],
                                                            config['username'],
                                                            config['password'])
            else:
                     returnExecution=self.createExecution(config['is_debug'],
                                                            config['zapi_url'],
                                                            config['idCycle'],
                                                            config['folder_id'],
                                                            config['zapyhrObject']['jiraIssueId'],
                                                            config['project_id'],
                                                            config['username'],
                                                            config['password'])
            allStepsExecution=None
            for execution in returnExecution:
               executionId=execution
               allStepsExecution=self.getStepId(config['is_debug'],
                                                  config['zapi_url'],
                                                  config['execution'],
                                                  config['username'],
                                                  config['password'])
         driver=None
         index=0
         executionStatus="1"
         stop_execute_steps=False
         for testCase in zapyhrObject['zapyhrObject']['stepBeanCollection']:
            #if is_test==True:
            #   input("Test Mode Press Enter to continue...")
            step=testCase['step'].lower()
            if step not in config['json_step_config']:
               printer.danger("Warning, the  step: '" + step + "' is not defined")
               sys.exit(1)            
            try:
               file_step=config['dir_step_files'] + "/" + config['json_step_config'][step] + '.json'
               with open(file_step) as json_data:
                  json_step = json.load(json_data)
            except Exception as e:
               print (e)
               printer.danger("Warning, the file step: " + file_step + " not exist or is not a json (err 1)")
               sys.exit(1)
            if stop_execute_steps == False:
               printer.underline(config['json_step']['name'] + " (" + str(testCase['id']) + ")")
               config['wrapper']=wrapper
               config['json_step']=json_step
               objectReturn=self.execute_step (driver,testConfigurations, config)
               status=objectReturn['status']
               driver=objectReturn['driver']
               stepFailed=objectReturn['stepFailed']
               if config['is_test']==False:
                  self.updateTestStep(config['is_debug'],config['zapi_url'],allStepsExecution[index]['id'],status,stepFailed,config['username'],config['password'])
               if status=="2" or status=="5":
                     executionStatus=status
                     path='screenshots/'
                     file_name=str(testCase['id']) + ".png"
                     if not os.path.exists(path):
                           os.makedirs(path)
                     if config['json_step']['attachScreenshot'] == True:
                        wrapper.screen_shot(driver,path + file_name)    
                        if config['is_test']==False:
                           self.addAttachmentBuffered(config['is_debug'],config['zapi_url'],path,file_name,allStepsExecution[index]['id'],'STEPRESULT',config['username'],config['password'])
                        os.unlink(path + file_name)
                     if config['json_step']['failedExit'] == True:
                        printer.danger( "La issue " + config['idJira'] + " e' forzamente interrotta causa fallimento bloccante dello step")
                        stop_execute_steps=True
               index=index + 1
         driver.quit()
         if config['is_test']==False:
            self.updateExecution(config['is_debug'],config['zapi_url'],executionId,executionStatus,config['username'],config['password'])
            if (config['original_execution_id'] != None):
               self.updateExecution(config['is_debug'],config['zapi_url'],config['original_execution_id'],executionStatus,config['username'],config['password'])
