"""
wrapperSelenium Library for selenium
Versione 0.0.1

Author: idel fuschini

"""
import  sys,time
import base64
from idelium.commons.ideliumPrinter import initPrinter
from idelium.commons.androidEventKey import eventkey
from idelium.commons.resultEnum import result
from appium import webdriver





class ideliumAppium():    
    def wait_for_elements(self,driver,config, objectStep):
        wait_time=5
        if 'waitTime' in config['json_config']: 
            wait_time=config['json_config']['waitTime']
        print ("Waiting for Login dialog to open, max wait =" + str(wait_time) + " seconds")
        timeout = time.time() + wait_time   # Timer based on wait_time to prevent infinite loops
        el=None
        while True:
            time.sleep(1)   # Prevent CPU slamming with short timeout between loops
            if time.time() > timeout:
                print ('timeout exception')
                break
            try:
                if 'xpath' in objectStep:
                    el = driver.find_element_by_xpath(objectStep['xpath'])
                elif 'native_interface_element' in objectStep:
                    native_interface_element=config['appiumDesiredCaps']['appPackage'] + ":id/" + objectStep['native_interface_element']
                    el = driver.find_element_by_id(native_interface_element) 
                break
            except Exception as e:
                print ('still waiting')
        return el



    def connect_appium(self,driver,config,objectStep):
        # os,appiumServer,appiumDesiredCaps,note=None

        returnCode=result.ok
        driver=None
        printer=initPrinter()
        if config['is_debug']==True:
            print ('try to connect:' + config['appiumServer'])
        print (objectStep['note'],end="->", flush=True)
        try:
            driver = webdriver.Remote(config['appiumServer'], config['appiumDesiredCaps'],keep_alive=False)
            printer.success('ok')
            contexts=driver.contexts
            printer.warning ('Context name:')
            index=0
            for i in contexts:
                index =index + 1
                printer.warning (str(index) + ")" + i)
        except Exception as e:
            printer.danger('ko')
            print (e)
            config['json_step']['attachScreenshot'] = False
            config['json_step']['failedExit'] = False
            printer.danger('Verify if Appium server is running')
            printer.danger('The test is stopped')
            sys.exit(1)
        return {"driver" : driver,"config" : config, "returnCode" : returnCode}

    def appium_send_keys(self,driver,config,objectStep):
        returnCode=result.ok
        printer=initPrinter()
        print (objectStep['note'],end="->", flush=True)
        el=self.wait_for_elements(driver,config,objectStep)
        if el==None:
            returnCode=result.ko
        else:
            if config['json_config']['appiumDesiredCaps']['platformName'] == 'android':
                el.click()
                time.sleep(1)
                eventKey=eventkey()
                for string in objectStep['keys']:
                    for keyCommand in eventKey.getArrayOfChar(string):
                        arrayCommand=keyCommand.split(',')
                        if len(arrayCommand) == 1:
                            driver.press_keycode(keyCommand)
                        else:
                            driver.press_keycode(arrayCommand[0],arrayCommand[1])
            else:
                for string in objectStep['keys']:
                    el.send_keys(string)
        return {"returnCode" : returnCode}
    def appium_click(self,driver,config,objectStep):
        returnCode=result.ok
        printer=initPrinter()
        print (objectStep['note'],end="->", flush=True)
        el=self.wait_for_elements(driver,config,objectStep)
        if el==None:
            returnCode=result.ko
        else:
            el.click()

        return {"returnCode" : returnCode}




    def appium_switch_context(self,driver,config,objectStep):
        returnCode=result.ok
        printer=initPrinter()
        print (objectStep['note'],end="->", flush=True)
        try:
            el = driver.switch_to.context(objectStep['contextName'])
            driver.wait_activity
            printer.success('ok')
        except Exception as e:
            print (e)
            returnCode=result.ko
            printer.danger('ko')
        return {"returnCode" : returnCode}

    def appium_execute_script(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/mobile-command/
        """
        returnCode=result.ok
        el=driver.execute_script(objectStep['script'])
        return returnCode
    def appium_desired_capabilities(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/get/
        """
        return driver.desired_capabilities()
    def appium_back(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/back/
        """
        returnCode=result.ok
        driver.back()
        return returnCode
    def appium_page_source(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/source/
        """
        print (driver.page_source)
        return driver.page_source
    def appium_set_page_load_timeout(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/timeouts/timeouts/
        """
        returnCode=result.ok
        driver.set_page_load_timeout(objectStep['milliseconds'])
        return returnCode
    def appium_implicitly_wait(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/timeouts/implicit-wait/
        """
        returnCode=result.ok
        driver.implicitly_wait(objectStep['milliseconds'])
        return returnCode
    def appium_set_script_timeout(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/timeouts/async-script/
        """
        returnCode=result.ok
        driver.set_script_timeout(objectStep['milliseconds'])
        return returnCode
    def appium_orientation(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/orientation/get-orientation/
        """
        return driver.orientation
    def appium_orientation(self,driver,config,objectStep):
        """
            orientation: LANDSCAPE,PORTRAIT
            for more info:
            https://appium.io/docs/en/commands/session/orientation/set-orientation/
        """
        returnCode=result.ok
        driver.orientation(objectStep['orientation'])
        return returnCode
    def appium_location(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/geolocation/get-geolocation/
        """
        return driver.location()
    def appium_orientation(self,driver,config,objectStep):
        """
            orientation: LANDSCAPE,PORTRAIT
            for more info:
            https://appium.io/docs/en/commands/session/geolocation/set-geolocation/
        """
        returnCode=result.ok
        driver.set_location(objectStep['latitude'],objectStep['ongitude'],objectStep['altitude'])
        return returnCode
    def appium_log_types(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/logs/get-log-types/
        """
        return driver.log_types()
    def appium_get_log(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/logs/get-log/
        """
        return driver.get_log(objectStep['typeString'])
    def appium_update_settings(self,driver,config,objectStep):
        """
            orientation: LANDSCAPE,PORTRAIT
            for more info:
            https://appium.io/docs/en/commands/session/settings/update-settings/
        """
        returnCode=result.ok
        driver.update_settings(objectStep['jsonSettings'])
        return returnCode
    def appium_get_settings(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/session/settings/get-settings/
        """
        return driver.get_settings
    def start_start_activity(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/activity/start-activity/
        """
        return driver.start_activity(objectStep['jsonActivityParameters'])
    def appium_current_activity(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/activity/current-activity/
        """
        return driver.current_activity
    def appium_current_package(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/activity/current-package/
        """
        return driver.current_package
    def appium_current_package(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/install-app/
        """
        printer=initPrinter()
        try:
            driver.install_app(objectStep['appPath'])
            return result.ok
        except Exception as e:
            print(e)
            printer.danger('FAILED')
            sys.exit(1)
            return result.ko
    def appium_is_app_installed(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/is-app-installed/
        """
        return driver.is_app_installed(objectStep['appPackage'])
    def appium_launch_app(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/launch-app/
        """
        returnCode=result.ok
        driver.launch_app()
        return returnCode
    def appium_background_app(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/background-app/
        """
        returnCode=result.ok
        driver.background_app(objectStep['seconds'])
        return returnCode
    def appium_close_app(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/close-app/
        """
        returnCode=result.ok
        driver.close_app()
        return returnCode
    def appium_reset_app(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/reset-app/
        """
        returnCode=result.ok
        driver.reset()
        return returnCode
    def appium_remove_app(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/remove-app/
        """
        returnCode=result.ok
        driver.remove_app()
        return returnCode
    def appium_activate_app(self,driver,config,objectStep):
        """
            examples:
            driver.appium_activate_app('com.apple.Preferences')
            driver.appium_activate_app('io.appium.android.apis')
            for more info:
            https://appium.io/docs/en/commands/device/app/activate-app/
        """
        returnCode=result.ok
        driver.activate_app(objectStep['bundleId'])
        return returnCode
    def appium_terminate_app(self,driver,config,objectStep):
        """
            examples:
            driver.appium_terminate_app('com.apple.Preferences')
            driver.appium_terminate_app('io.appium.android.apis')
            for more info:
            https://appium.io/docs/en/commands/device/app/terminate-app/
        """
        returnCode=result.ok
        driver.terminate_app(objectStep['bundleId'])
        return returnCode
    def appium_query_app_state(self,driver,config,objectStep):
        """
            examples:
            driver.appium_query_app_state('com.apple.Preferences')
            driver.appium_query_app_state('io.appium.android.apis')
            for more info:
            https://appium.io/docs/en/commands/device/app/app-state/
        """
        returnCode=result.ok
        driver.query_app_state(bundleId)
        return returnCode
    def appium_app_strings(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/get-app-strings/
        """
        returnCode=result.ok
        driver.app_strings(objectStep['language'],objectStep['pathFile'])
        return returnCode
    def appium_end_test_coverage(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/app/end-test-coverage/
        """
        returnCode=result.ok
        driver.end_test_coverage(objectStep['intent'],objectStep['path'])
        return returnCode
    def appium_set_clipboard(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/clipboard/set-clipboard/
        """
        returnCode=result.ok
        driver.set_clipboard(objectStep['string'])
        return returnCode
    def appium_set_power_ac(self,driver,config,objectStep):
        """
            Examples:
            self.driver.set_power_ac(Power.AC_OFF)
            for more info:
            https://appium.io/docs/en/commands/device/emulator/power_ac/
        """
        returnCode=result.ok
        driver.set_power_ac(objectStep['powerOnOff'])
        return returnCode
    def appium_set_power_capacity(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/emulator/power_capacity/
        """
        returnCode=result.ok
        driver.set_power_capacity(objectStep['percent'])
        return returnCode
    def appium_push_file(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/files/push-file/
        """
        returnCode=result.ok
        driver.push_file(objectStep['path'],objectStep['data'])
        return returnCode
    def appium_pull_file(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/files/pull-file/
        """
        return driver.pull_file(objectStep['path'])
    def appium_pull_folder(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/files/pull-folder/
        """
        return driver.pull_folder(objectStep['path'])
    def appium_shake(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/interactions/shake/
        """
        returnCode=result.ok
        driver.shake()
        return returnCode
    def appium_lock(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/interactions/lock/
        """
        returnCode=result.ok
        driver.lock()
        return returnCode
    def appium_unlock(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/interactions/unlock/
        """
        returnCode=result.ok
        driver.unlock()
        return returnCode
    def appium_is_locked(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/interactions/is-locked/
        """
        returnCode=result.ok
        driver.is_locked()
        return returnCode
    def appium_press_keycode(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/keys/press-keycode/
        """
        returnCode=result.ok
        driver.press_keycode(objectStep['keyCode'])
        return returnCode
    def appium_long_press_keycode(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/keys/long_press-keycode/
        """
        returnCode=result.ok
        driver.long_press_keycode(objectStep['keyCode'])
        return returnCode
    def appium_hide_keyboard(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/keys/hide-keyboard/
        """
        returnCode=result.ok
        driver.hide_keyboard()
        return returnCode
    def appium_is_keyboard_shown(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/keys/is-keyboard-shown/
        """
        return driver.is_keyboard_shown()
    def appium_toggle_wifi(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/toggle-wifi/
        """
        returnCode=result.ok
        driver.toggle_wifi()
        return returnCode
    def appium_toggle_location_services(self,driver,config,objectStep): 
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/toggle-location-services/
        """
        returnCode=result.ok
        driver.toggle_location_services()
        return returnCode
    def appium_send_sms(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/send-sms/
        """
        returnCode=result.ok
        driver.send_sms(objectStep['phoneNumber'],objectStep['message'])
        return returnCode
    def appium_make_gsm_call(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/gsm-call/
        """
        returnCode=result.ok
        driver.make_gsm_call(objectStep['phoneNumber'],objectStep['gsmAction'])
        return returnCode
    def appium_set_gsm_signal(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/gsm-signal/
        """
        returnCode=result.ok
        driver.set_gsm_signal(gsmSignalStrength)
        return returnCode
    def appium_set_gsm_voice(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/gsm-voice/
        """
        returnCode=result.ok
        driver.set_gsm_voice(objectStep['gsmVoiceState'])
        return returnCode
    def appium_set_network_speed(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/network/network-speed/
        """
        returnCode=result.ok
        driver.set_network_speed(objectStep['netSpeed'])
        return returnCode
    def appium_get_performance_data(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/performance-data/get-performance-data/
        """
        returnCode=result.ok
        driver.get_performance_data(objectStep['packageName'],objectStep['dataType'],objectStep['dataReatTimeOut'])
        return returnCode
    def appium_get_performance_data_types(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/performance-data/performance-data-types/
        """
        return driver.get_performance_data_types()
    def appium_start_recording_screen(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/recording-screen/start-recording-screen/
        """
        returnCode=result.ok
        if objectStep['options']==None:
            driver.start_recording_screen()
        else:
            driver.start_recording_screen(objectStep['options'])
        return returnCode
    def appium_stop_recording_screen(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/recording-screen/stop-recording-screen/
        """
        returnCode=result.ok
        driver.stop_recording_screen()
        return returnCode
    def appium_touch_id(self,driver,config,objectStep):
        """
            self.driver.touch_id(false); # Simulates a failed touch
            self.driver.touch_id(true); # Simulates a passing touch        
            for more info:
            https://appium.io/docs/en/commands/device/simulator/touch-id/
        """
        returnCode=result.ok
        driver.touch_id(objectStep['touch'])
        return returnCode
    def appium_toggle_touch_id_enrollment(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/simulator/toggle-touch-id-enrollment/
        """
        returnCode=result.ok
        driver.toggle_touch_id_enrollment()
        return returnCode
    def appium_open_notifications(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/system/open-notifications/
        """
        returnCode=result.ok
        driver.open_notifications()
        return returnCode
    def appium_get_system_bars(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/system/system-bars/
        """
        returnCode=result.ok
        driver.get_system_bars()
        return returnCode
    def appium_get_system_time(self,driver,config ,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/system/system-time/
        """
        returnString=None
        if (objectStep['date']==None):
            returnString=driver.get_device_time()
        else:
            returnString=driver.get_device_time(objectStep['date'])
        return returnString
    def appium_get_device_density(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/system/display-density/
        """
        returnCode=result.ok
        driver.get_device_density()
        return returnCode
    def appium_finger_print(self,driver,config,objectStep):
        """
            for more info:
            https://appium.io/docs/en/commands/device/authentication/finger-print/
        """
        returnCode=result.ok
        driver.finger_print(objectStep['number'])
        return returnCode
    def appium_find_element_by_accessibility_id(self,driver,config,objectStep):
        """
            for more info:
           https://appium.io/docs/en/commands/element/find-element/
        """
        return driver.find_element_by_accessibility_id(objectStep['accessibilityId'])
    def appium_switch_to(self,driver,config,objectStep):
        """
        """
        return driver.switch_to()
    
    def screen_shot(self,driver,fileName):
        """
                screenshot appium
        """
        printer=initPrinter()
        try:
            currentContext=driver.current_context
            fakeObjectStep={}
            fakeObjectStep['contextName']='NATIVE_APP'
            fakeObjectStep['note']='take screenshot'
            self.appium_switch_context(driver,None,fakeObjectStep)
            screenshot=driver.get_screenshot_as_base64()
            fakeObjectStep['contextName']=currentContext
            self.appium_switch_context(driver,None,fakeObjectStep)
            screenshot_data = base64.b64decode(screenshot)
            newFile = open(fileName, "wb")
            newFile.write(screenshot_data)
            newFile.close()
            return result.ok
        except Exception as e:
            print(e)
            printer.danger('FAILED APP SCREENSHOT')
            return result.ko

    def  command (self,command,driver,objConfig,objectStep):
        printer=initPrinter()
        commands= {
                "connect_appium" : self.connect_appium,
                "appium_send_keys" : self.appium_send_keys,
                "appium_send_keys_xpath": self.appium_send_keys,
                "appium_click" : self.appium_click,
                "appium_click_xpath" : self.appium_click,
                "appium_switch_context" : self.appium_switch_context,
                "appium_execute_script" : self.appium_execute_script,
                "appium_desired_capabilities" : self.appium_desired_capabilities,
                "appium_back" : self.appium_back,
                "appium_page_source" : self.appium_page_source,
                "appium_set_page_load_timeout" : self.appium_set_page_load_timeout,
                "appium_implicitly_wait" : self.appium_implicitly_wait,
                "appium_set_script_timeout" : self.appium_set_script_timeout,
                "appium_orientation" : self.appium_orientation,
                "appium_orientation" : self.appium_orientation,
                "appium_location" : self.appium_location,
                "appium_orientation" : self.appium_orientation,
                "appium_log_types" : self.appium_log_types,
                "appium_get_log" : self.appium_get_log,
                "appium_update_settings" : self.appium_update_settings,
                "appium_get_settings" : self.appium_get_settings,
                "appium_start_start_activity" : self.start_start_activity,
                "appium_current_activity" : self.appium_current_activity,
                "appium_current_package" : self.appium_current_package,
                "appium_current_package" : self.appium_current_package,
                "appium_is_app_installed" : self.appium_is_app_installed,
                "appium_launch_app" : self.appium_launch_app,
                "appium_background_app" : self.appium_background_app,
                "appium_close_app" : self.appium_close_app,
                "appium_reset_app" : self.appium_reset_app,
                "appium_remove_app" : self.appium_remove_app,
                "appium_activate_app" : self.appium_activate_app,
                "appium_terminate_app" : self.appium_terminate_app,
                "appium_query_app_state" : self.appium_query_app_state,
                "appium_app_strings" : self.appium_app_strings,
                "appium_end_test_coverage" : self.appium_end_test_coverage,
                "appium_set_clipboard" : self.appium_set_clipboard,
                "appium_set_power_ac" : self.appium_set_power_ac,
                "appium_set_power_capacity" : self.appium_set_power_capacity,
                "appium_push_file" : self.appium_push_file,
                "appium_pull_file" : self.appium_pull_file,
                "appium_pull_folder" : self.appium_pull_folder,
                "appium_shake" : self.appium_shake,
                "appium_lock" : self.appium_lock,
                "appium_unlock" : self.appium_unlock,
                "appium_is_locked" : self.appium_is_locked,
                "appium_press_keycode" : self.appium_press_keycode,
                "appium_long_press_keycode" : self.appium_long_press_keycode,
                "appium_hide_keyboard" : self.appium_hide_keyboard,
                "appium_is_keyboard_shown" : self.appium_is_keyboard_shown,
                "appium_toggle_wifi" : self.appium_toggle_wifi,
                "appium_toggle_location_services" : self.appium_toggle_location_services,
                "appium_send_sms" : self.appium_send_sms,
                "appium_make_gsm_call" : self.appium_make_gsm_call,
                "appium_set_gsm_signal" : self.appium_set_gsm_signal,
                "appium_set_gsm_voice" : self.appium_set_gsm_voice,
                "appium_set_network_speed" : self.appium_set_network_speed,
                "appium_get_performance_data" : self.appium_get_performance_data,
                "appium_get_performance_data_types" : self.appium_get_performance_data_types,
                "appium_start_recording_screen" : self.appium_start_recording_screen,
                "appium_stop_recording_screen" : self.appium_stop_recording_screen,
                "appium_touch_id" : self.appium_touch_id,
                "appium_toggle_touch_id_enrollment" : self.appium_toggle_touch_id_enrollment,
                "appium_open_notifications" : self.appium_open_notifications,
                "appium_get_system_bars" : self.appium_get_system_bars,
                "appium_get_system_time" : self.appium_get_system_time,
                "appium_get_device_density" : self.appium_get_device_density,
                "appium_finger_print" : self.appium_finger_print,
                "appium_find_element_by_accessibility_id" : self.appium_find_element_by_accessibility_id,
                "appium_switch_to" : self.appium_switch_to,

        }
        if command in commands.keys():
            return commands[command](driver,objConfig,objectStep)
        else:
            printer.danger ('Idelium Appium | action non trovata:' + command)
            return None