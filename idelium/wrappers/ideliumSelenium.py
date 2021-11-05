"""
ideliumSelenium Library for selenium
Versione 0.0.1

Author: idel fuschini

"""
import time,sys
from idelium.commons.ideliumPrinter import initPrinter
from idelium.commons.resultEnum import result
from idelium.commons.seleniumKeyEvent import eventKey
from idelium.commons.seleniumBy import selBy
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class ideliumSelenium(): 
   def sleep (self, driver,config,objectStep):
       time.sleep(objectStep['seconds'])
       return {"returnCode" : result.ok}

   def wait_and_click(self,driver,xpath_condition,note):
      if self.wait_for_next_step_real(driver,xpath_condition,note) == result.ok:
         if self.click_xpath(driver,xpath_condition,note) == result.ko:
            return {"returnCode" : result.ko}
         else:
            return {"returnCode" : result.ok}
      else:
         return {"returnCode" : result.ok}

   def find_element_by_xpath(self,driver,xpath_condition,note=None):
      return driver.find_element_by_xpath(xpath_condition)
   def find_elements_by_xpath(self,driver,xpath_condition,note=None):   
      return driver.find_elements_by_xpath(xpath_condition)
   def find_element(self,driver,by,target,note=None):
      return driver.find_element(by,target)
   def find_elements(self,driver,by,target,note=None):   
      return driver.find_elements(by,target)
   def page_source(self,driver,note=None):
      return driver.page_source
   def switch_to_frame(self,driver,objectDriver,note=None):
      driver.switch_to_frame(objectDriver)
      return result.ok
   def switch_to_default_content(self,driver,object,note=None):
      driver.switch_to_default_content()
      return result.ok
   def find_object_element(self, seleniumObject, xpath_condition, note=None):
        return seleniumObject.find_element_by_xpath(xpath_condition)
   def click_object(self,seleniumObject,note):   
      printer=initPrinter()
      try:
         print (note,end="->", flush=True)
         time.sleep(1)
         seleniumObject.click()
         printer.success('ok')
         return result.ok
      except Exception as e:
         print (e) 
         printer.danger('FAILED')
         #sys.exit(1)
         return result.ko

   def drag_and_drop(driver,config,objectStep):
      printer=initPrinter()
      try:
         dragElement=driver.find_element_by_xpath(objectStep['xpathDrag'])
         dropElement=driver.find_element_by_xpath(objectStep['xpathDrop'])
         action=ActionChain(driver)
         action.drag_and_drop(dragElement,dropElement).perform()
         return {"returnCode" : result.ok}
      except:
         printer.danger('FAILED')
         #sys.exit(1)
         return {"returnCode" : result.ko}



   def open_browser(self,driver,config,objectStep):
      driver = None
      if (config['json_config']['browser']=='chrome'):
         if config['device'] != None:
            mobile_emulation = { "deviceName": config['device'] }
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = webdriver.Chrome(chrome_options=chrome_options)
         else:
            if config['user_agent'] != None:
               opts = Options()
               opts.add_argument("user-agent=" + config['user_agent'])
               driver = webdriver.Chrome(chrome_options=opts)
            else:
               driver = webdriver.Chrome()
            driver.set_window_size(config['width'], config['height'])

      elif (config['json_config']['browser']=='firefox'):
         if config['user_agent'] != None:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", config['user_agent'])
            driver = webdriver.Firefox(profile)
         else:
            driver = webdriver.Firefox()
         driver.set_window_size(config['width'], config['height'])
      else:
         if config['device'] != None:
            mobile_emulation = { "deviceName": config['device'] }
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = webdriver.Chrome(chrome_options=chrome_options)
         else:
            if config['user_agent'] != None:
               opts = Options()
               opts.add_argument("user-agent=" + config['user_agent'])
               driver = webdriver.Chrome(chrome_options=opts)
            else:
               driver = webdriver.Chrome()
            driver.set_window_size(config['width'], config['height'])
      print (objectStep)
      if 'url' in objectStep:
         driver.get(objectStep['url'])
      else:      
         driver.get(config['json_config']['url'])
      returnCode=result.ok   
      objectStep['xpath']=config['json_config']['xpath_check_url']
      if self.wait_for_next_step(driver,config,objectStep)['returnCode']==result.ko:
         returnCode=result.ko   
         config['json_step']['attachScreenshot'] = True
         config['json_step']['failedExit'] = True
      return {"driver" : driver, "returnCode" : returnCode, "config": config}


   def write_localstorage(self,driver,config,objectStep):
      printer=initPrinter()
      try:
         print (objectStep['note'],end="->", flush=True)
         scriptJS=""
         for objectData in objectStep['dataLocalStorage']:
               for key in objectData:
                  scriptJS=scriptJS + "localStorage.setItem(\"" + key  + "\", '" +  objectData[key] + "')\n"
         scriptJS=scriptJS +"return Array.apply(0, new Array(localStorage.length)).map(function (o, i) { return localStorage.getItem(localStorage.key(i)); })"
         driver.execute_script(scriptJS)
         printer.success('ok')
         return {"returnCode" : result.ok}
      except:
         printer.danger('FAILED')
         #sys.exit(1)
         return {"returnCode" : result.ko}

   def screen_shot(self,driver,file_name):
      """
         screenshot
      """
      printer=initPrinter()
      try:
         driver.get_screenshot_as_file(file_name)
         return result.ok
      except:
         printer.danger('FAILED')
         sys.exit(1)
         return result.ko

   '''
      generic no xpath 
   '''
   def click(self,driver,config,objectStep):
      printer=initPrinter()
      by=selBy()
      try:
         print (objectStep['note'],end="->", flush=True)
         time.sleep(1)
         'for retrocompat'
         if 'xpath' in objectStep: 
            objectStep['findBy']='XPATH'
            objectStep['target']=objectStep['xpath']
         driver.find_element(by.getBy(objectStep['findBy']),objectStep['target']).click()
         printer.success('ok')
         return {"returnCode" : result.ok}
      except:
         printer.danger('FAILED')
         return {"returnCode" : result.ko}
   def clear(self,driver,config,objectStep):
      printer=initPrinter()
      by=selBy()
      try:
         print (objectStep['note'],end="->", flush=True)
         time.sleep(1)
         if 'xpath' in objectStep: 
            objectStep['findBy']='XPATH'
            objectStep['target']=objectStep['xpath']
         driver.find_element(by.getBy(objectStep['findBy']),objectStep['target']).clear()
         printer.success('ok')
         return {"returnCode" : result.ok}
      except:
         printer.danger('FAILED')
         return {"returnCode" : result.ko}
   def send_keys(self,driver,config,objectStep):
      printer=initPrinter()
      seleniumKey=eventKey()
      by=selBy()
      try:
         string_to_input=objectStep['text']
         key=seleniumKey.getKey(string_to_input)
         if key == None:
            if objectStep['text'][:1] == '%':
               string_to_input=config['json_config'][objectStep['text'][1:]]
         else:
            string_to_input=key
         print (objectStep['note'],end="->", flush=True)
         time.sleep(1)
         if 'xpath' in objectStep: 
            objectStep['findBy']='XPATH'
            objectStep['target']=objectStep['xpath']
         driver.find_element(by.getBy(objectStep['findBy']),objectStep['target']).send_keys(string_to_input)
         printer.success('ok')
         return {"returnCode" : result.ok}
      except:
         printer.danger('FAILED')
         #sys.exit(1)
         return {"returnCode" : result.ko}




   def wait_for_next_step(self,driver,config,objectStep):
      by=selBy()
      if 'xpath' in objectStep: 
         objectStep['findBy']='XPATH'
         objectStep['target']=objectStep['xpath']
      if self.wait_for_next_step_real(driver,by.getBy(objectStep['findBy']),objectStep['target'],objectStep['note']) == result.ko:
         return {"returnCode" : result.ko}
      else:
         return {"returnCode" : result.ok}
   
   def wait_for_next_step_real(self,driver,by,target,note,waitSeconds=20):
      failed=False
      printer=initPrinter()
      try:
         print (note,end="->", flush=True)
         WebDriverWait(driver, waitSeconds).until(
              EC.presence_of_element_located((by, target))
         )
      except:
         printer.danger('FAILED')
         failed=True
         return result.ko
      finally:
         if failed==False:
            printer.success('ok')
            return result.ok   
         return result.ko






   def  command (self,command,driver,objConfig,objectStep):
      printer=initPrinter()
      commands= {
            "wait_and_click":self.wait_and_click,
            "wait_for_next_step":self.wait_for_next_step,
            "wait_for_next_step_real":self.wait_for_next_step_real,
            "find_element_by_xpath":self.find_element_by_xpath,
            "find_elements_by_xpath":self.find_elements_by_xpath,
            "find_element":self.find_element_by_xpath,
            "find_elements":self.find_elements_by_xpath,
            "page_source":self.page_source,
            "switch_to_frame":self.switch_to_frame,
            "switch_to_default_content":self.switch_to_default_content,
            "find_object_element":self.find_object_element,
            "click_object":self.click_object,
            "click":self.click,
            "clear":self.clear,
            "write":self.send_keys,
            "open_browser":self.open_browser,
            "write_localstorage":self.write_localstorage,
            "screen_shot": self.screen_shot,       
            "sleep": self.sleep,
      }
      if command in commands.keys():
         return commands[command](driver,objConfig,objectStep)
      else:
         printer.danger ('Idelium Selenium | action non trovata:' + command)
         return None