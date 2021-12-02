''' Bcolors '''
HEADER = "\033[95m"
NABLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
class InitPrinter:
    ''' InitPrinter '''
    @staticmethod
    def underline(test_name):
        '''underline'''
        print(BOLD + UNDERLINE + "Step: " + test_name +
              ENDC)
    @staticmethod
    def success(ok_string):
        '''success'''
        print(OKGREEN + ok_string + ENDC)
    @staticmethod
    def danger(ko_string):
        '''danger'''
        print(FAIL + ko_string + ENDC)
    @staticmethod
    def warning(na_string):
        '''warning'''
        print(NABLUE + na_string + ENDC)
    @staticmethod
    def print_important_text(txt_string):
        '''print_important_text'''
        print(BOLD + txt_string + ENDC)
