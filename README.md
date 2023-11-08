![Idelium](https://idelium.io/assets/images/idelium.png)

# Idelium-CLI

This is Idelium Command Line is the tool for test automation integrated with [Idelium AS](https://github.com/idelium/idelium-docker).

Idelium-CLI can be used through a continues integration software, such as Jenkins, GitLabs, Bamboo etc.

For more info: https://idelium.io

[![Introducing Idelium](https://img.youtube.com/vi/nGe3c_CU0NQ/0.jpg)](https://youtu.be/nGe3c_CU0NQ)

## Prerequisite

Python 3.8.X

## Installing

If you have pip on your system, you can simply install or upgrade the Python bindings:

```
pip install
```

## Run the script

idelium-cli can be used in two ways:

To directly launch a test cycle, useful for those who want to integrate integration tests with jenkins, bamboo or similar:

```
idelium --ideliumKey=1234 --idCycle=2 --idProject=8 --environment=prod
```

For use with [idelium-docker](https://github.com/idelium/idelium-docker):

```
idelium --ideliumKey=1234 --idCycle=2 --idProject=8 --environment=prod --ideliumwsBaseurl='https://localhost'
```

### idelium-cli server mode
for idelium-cli in server mode useful for those who want to buy idelium enterprise, and then configure different platforms and launch tests remotely:

```
idelium --ideliumServer
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

idelium-cli download automically the correct version

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
