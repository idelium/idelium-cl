from behave.__main__ import main as behave_main
class IdeliumAppium():
    @staticmethod
    def wait_for_elements(driver, config, object_step):
        behave_main("path/to/specified/folder")
