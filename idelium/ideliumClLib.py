class initIdelium():
    def getSyntax(self):
        return """
\033[1mUsage\033[0m: idelium-cl.py [options]

Options:

   --help                  show this help
   --idCycle               cycle id to associate to the execution "idCycle1,idCycle2,...."
   --idProject             force idProject
   --environment           environment json config file (required)
   --useragent             set useragent for the test
   --test                  for testing without store the results
   --verbose               for debugging 
   --dirChromedriver       default path of chromedriver path ("./chromedriver/last")
   --dirConfigurationStep  default path ("./configurationStep") for configuration steps 
   --dirStepFiles          default path ("./step") of directory for step files 
   --dirIdeliumScript      default path (".") of directory for step files
   --width                 default width of screen 1024
   --height                default height of screen 768
   --device                if is set useragent,height and width are ignored
   --fileSteps             for test single step json "name1,name2,...."
   --url                   url for test 
   --ideliumws_baseurl     idelium server url ex: http://localhost
   --reportingService      where the data will be save: idelium | zephyr
   --ideliumKey            is the key for access to the idelium api
   --forcedownload         force to ovewrite the configuration files
   --idChannel             idChannel

   Zephir 
   --jiraApiUrl            for change the default jira url (https://<host jira>/rest/api/latest/)
   --idJira                jira id (required if idVersion and idCycle not setted)
   --idVersion             version id to associate the execution 
   --username              jira username (required)
   --password              jira password (required)



For Example: 

default reporting service: idelium-cl --ideliumKey=1234 --idCycle=2 --idProject=8 --environment=prod

working with jira/zephyr: idelium-cl --reportingService=zephyr --idJira=prj-1234 --username=user --password=secret --environment=prod.json --useragent='apple 1134'

"""
    def getReguiredParams(self):
        return {
   "idProject" : 0,
   "idCycle" : 0,
   "environment" : 0,
   "ideliumKey": 0,
}
