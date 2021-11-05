"""
Printerformatter
Author: idel fuschini

"""

class bcolors:
    HEADER = '\033[95m'
    NABLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class initPrinter():
    def underline(self,testName):
      """
         bold & underline
      """
      print (bcolors.BOLD + bcolors.UNDERLINE + "Step: " + testName + bcolors.ENDC )
    def success(self,okString):
      print (bcolors.OKGREEN + okString + bcolors.ENDC)
    def danger(self,koString):
      print (bcolors.FAIL + koString + bcolors.ENDC)
    def warning(self,naString):
      print (bcolors.NABLUE + naString + bcolors.ENDC)
    def printImportantText(self,testName):
      print (bcolors.BOLD + testName + bcolors.ENDC)