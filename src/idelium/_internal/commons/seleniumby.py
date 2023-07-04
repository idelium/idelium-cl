"""System module."""
from __future__ import absolute_import
from selenium.webdriver.common.by import By

class SelBy() :
    ''' SelBy '''
    @staticmethod
    def get_by (key):
        ''' get_by'''
        keys_array= {
            'ID': By.ID,
            'XPATH': By.XPATH,
            'LINKTEXT': By.LINK_TEXT,
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
        if key.upper() in keys_array.keys():
            return keys_array[key.upper()]
        return None
