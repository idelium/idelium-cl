from selenium.webdriver.common.by import By

class selBy() :
    def getBy (self,key):
        keysArray= {
            'ID': By.ID,
            'XPATH': By.XPATH,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'NAME' : By.NAME,
            'TAG_NAME' : By.TAG_NAME,
            'TAG' : By.CLASS_NAME,
            'CLASS_NAME' : By.CLASS_NAME,
            'CLASS' : By.CLASS_NAME,
            'CSS_SELECTOR' : By.CSS_SELECTOR,
            'CSS' : By.CSS_SELECTOR,
        }
        if key.upper() in keysArray.keys():
            return keysArray[key.upper()]
        else:
            return None
