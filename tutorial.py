import quick_firefox
from selenium.webdriver.firefox.webdriver import WebDriver
def callback(_driver: WebDriver, arguments):
  # use this _driver object to do anything you want
  return 1 
if __name__=='__main__':
    result=quick_firefox.run_sync(work=callback, args=())  # args will be callback function's parameters
    print('result:',result)