![Idelium](https://idelium.io/assets/images/idelium.png)

# Idelium-CLI

This is Idelium Command Line is the tool for test automation integrated with Idelium Web.

Idelium-CLI can be used through a continues integration software, such as Jenkins, GitLabs, Bamboo etc.

For more info: https://idelium.io

[![Introducing Idelium](https://img.youtube.com/vi/nGe3c_CU0NQ/0.jpg)](https://youtu.be/nGe3c_CU0NQ)

## Requirement

Python 3.8.X

## Install Libraries


```
pip install selenium
pip install Appium-Python-Client
pip install webdriver-manager
pip install Pillow

```
On windows:
```
pip install Pillow
```


## Download idelium-cli

```
git clone https://github.com/idelium/idelium-cli.git
cd idelium-cli
```

## Run the script

idelium-cli can be used in two ways:

1. to directly launch a test cycle, useful for those who want to integrate integration tests with jenkins, bamboo or similar:

```
python ideliumcl.py --ideliumKey=1234 --idCycle=2 --idProject=8 --environment=prod
```

2. for idelium-cli in server mode useful for those who want to buy idelium enterprise, and then configure different platforms and launch tests remotely:

```
python ideliumcl.py --ideliumServer
```

## Test Libraries used

### Selenium

For configure idelium-cli for test web application with chrome,firefox, windows, safari:

https://www.selenium.dev/documentation/webdriver/

### Appium

For configure idelium-cli for test native, hybrid and mobile web apps with iOS, Android and Windows:

https://appium.io/

## Webdriver

The webdriver is the interface to write instructions that work interchangeably across browsers, each browser has its own driver:

#### ChromeDriver

https://chromedriver.chromium.org/downloads

#### Geckodriver for Firefox

https://github.com/mozilla/geckodriver/releases

#### EDGE

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

#### Internet Explorer 11

https://support.microsoft.com/en-us/topic/webdriver-support-for-internet-explorer-11-9e1331c5-3198-c835-f622-ada80fe8c1fa

#### Safari

https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari

## Thanks

Special thanks to Marco Vernarecci, who supports me to make the product better
