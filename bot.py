from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, sys, requests
from bs4 import BeautifulSoup


class DkBot:
    '''A Base Class for all utility functions
            <Developed By Deepak Dk>
    '''

    def __init__(self):
        ''' Option Initializations for chromedriver '''

        self.driver = None
        self.opt = Options()
        self.opt.add_argument("--disable-infobars")
        self.opt.add_argument("--disable-extensions")
        self.opt.add_argument("start-maximized")
        self.opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1
        })
        self.opt.add_experimental_option("useAutomationExtension", False)
    

    def terminateBot(self, status=0):
        ''' A Method to close Browser window safely '''

        print("Browser will be closed in 5 seconds...")
        time.sleep(5)
        if self.driver is not None:
            self.driver.quit()
        sys.exit(status)


    def start(self, chromeDriverPath):
        '''Initiated the Automation Process'''  

        self.chromeDriverPath = chromeDriverPath
        try:
            self.driver = webdriver.Chrome(
                                executable_path=self.chromeDriverPath,
                                options=self.opt,
                                service_log_path='NUL'
                            )
            self.driver.get(self.URL)
        except Exception as e:
            msg = f'''\nProcess cannot be initiated,
                        ensure the chrome driver path,
                        :{self.chromeDriverPath}'''
            # print(e, msg, sep="\n\n")
            raise Exception(e+msg)

        self.waitUntilBodyTagFound()

        if(self.URL in self.driver.current_url):
            print("Process initated sucessfully")
        else:
            raise Exception(
                '''Unexpected happening,
                URL is redirected, 
                tryafter sometime or check everything''')
            

    def waitUntilBodyTagFound(self, timeOutSecond=120):
        ''' waits until the body tag found in the current url,
         timout will end the wait,
         timeout defaults to 120 seconds,
         Advisable to use when loads a new window '''
        
        if self.driver is not None:
            WebDriverWait(self.driver, timeOutSecond).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'body')))


    def scrap(self):
        '''Scraps the webpage of current url and return the soup'''

        response = requests.get(self.driver.current_url)
        return BeautifulSoup(response.text, "html.parser")


    def newTab(self):
        '''Opens a new tab'''

        if self.driver is not None:
            self.driver.execute_script("window.open('');")


    def closeTab(self):
        ''' Closes a current tab '''

        if self.driver is not None:
            self.driver.close()


    def switchTab(self, window_handles):
        ''' Switch to the new window '''

        if self.driver is not None:
            try:
                self.driver.switch_to.window(window_handles)
            except Exception as e:
                print(e)
                self.driver.switch_to.window(self.driver.window_handles[0])