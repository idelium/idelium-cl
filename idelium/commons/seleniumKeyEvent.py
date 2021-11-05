from selenium.webdriver.common.keys import Keys

class eventKey() :
    def getKey (self,key):
        keysArray= {
            "KEY_ADD": Keys.ADD,
            "KEY_ALT": Keys.ALT,
            "KEY_ARROW_DOWN": Keys.ARROW_DOWN,
            "KEY_ARROW_LEFT": Keys.ARROW_LEFT,
            "KEY_ARROW_RIGHT": Keys.ARROW_RIGHT,
            "KEY_ARROW_UP": Keys.ARROW_UP,
            "KEY_BACKSPACE": Keys.BACKSPACE,
            "KEY_BACK_SPACE": Keys.BACK_SPACE,
            "KEY_CANCEL": Keys.CANCEL,
            "KEY_CLEAR": Keys.CLEAR,
            "KEY_COMMAND": Keys.COMMAND,
            "KEY_CONTROL": Keys.CONTROL,
            "KEY_DECIMAL": Keys.DECIMAL,
            "KEY_DELETE": Keys.DELETE,
            "KEY_DIVIDE": Keys.DIVIDE,
            "KEY_DOWN": Keys.DOWN,
            "KEY_END": Keys.END,
            "KEY_ENTER": Keys.ENTER,
            "KEY_EQUALS": Keys.EQUALS,
            "KEY_ESCAPE": Keys.ESCAPE,
            "KEY_F1": Keys.F1,
            "KEY_F10": Keys.F10,
            "KEY_F11": Keys.F11,
            "KEY_F12": Keys.F12,
            "KEY_F2": Keys.F2,
            "KEY_F3": Keys.F3,
            "KEY_F4": Keys.F4,
            "KEY_F5": Keys.F5,
            "KEY_F6": Keys.F6,
            "KEY_F7": Keys.F7,
            "KEY_F8": Keys.F8,
            "KEY_F9": Keys.F9,
            "KEY_HELP": Keys.HELP,
            "KEY_HOME": Keys.HOME,
            "KEY_INSERT": Keys.INSERT,
            "KEY_LEFT": Keys.LEFT,
            "KEY_LEFT_ALT": Keys.LEFT_ALT,
            "KEY_LEFT_CONTROL": Keys.LEFT_CONTROL,
            "KEY_LEFT_SHIFT": Keys.LEFT_SHIFT,
            "KEY_META": Keys.META,
            "KEY_MULTIPLY": Keys.MULTIPLY,
            "KEY_NULL": Keys.NULL,
            "KEY_NUMPAD0": Keys.NUMPAD0,
            "KEY_NUMPAD1": Keys.NUMPAD1,
            "KEY_NUMPAD2": Keys.NUMPAD2,
            "KEY_NUMPAD3": Keys.NUMPAD3,
            "KEY_NUMPAD4": Keys.NUMPAD4,
            "KEY_NUMPAD5": Keys.NUMPAD5,
            "KEY_NUMPAD6": Keys.NUMPAD6,
            "KEY_NUMPAD7": Keys.NUMPAD7,
            "KEY_NUMPAD8": Keys.NUMPAD8,
            "KEY_NUMPAD9": Keys.NUMPAD9,
            "KEY_PAGE_DOWN": Keys.PAGE_DOWN,
            "KEY_PAGE_UP": Keys.PAGE_UP,
            "KEY_PAUSE": Keys.PAUSE,
            "KEY_RETURN": Keys.RETURN,
            "KEY_RIGHT": Keys.RIGHT,
            "KEY_SEMICOLON": Keys.SEMICOLON,
            "KEY_SEPARATOR": Keys.SEPARATOR,
            "KEY_SHIFT": Keys.SHIFT,
            "KEY_SPACE": Keys.SPACE,
            "KEY_SUBTRACT": Keys.SUBTRACT,
            "KEY_TAB": Keys.TAB,
            "KEY_UP": Keys.UP,            
        }
        if key in keysArray.keys():
            return keysArray[key]
        else:
            return None
