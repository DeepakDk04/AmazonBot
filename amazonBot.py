from bot import DkBot

class AmazonBot(DkBot):
    ''' Go to amazon and scrap details of newly released Products  '''

    def __init__(self, chromeDriverPath):

        super().__init__()
        #Base Class constructor must be called befor start method
        self.URL = "https://www.amazon.in/"
        self.start(chromeDriverPath)


    def clickNewReleases(self):
        """checks for any new release on amazon.in"""

        navXpath =  "/html/body/div[1]/header/div/div[5]/div[2]/div/div/a[5]"
        newReleasesNav = self.driver.find_element_by_xpath(navXpath)
        newReleasesNav.click()
        self.waitUntilBodyTagFound()


    def scrapNewReleases(self):
        ''' scrape data of new relaesd product '''

        soup = self.scrap()
        items = soup.find_all("div", class_="zg_item zg_homeWidgetItem")
        for item in items:
            print(item,end="\n\n")


    def newReleasedItems(self):   
        ''' Navigate to the each item of newly released '''
         
        items = self.driver.find_elements_by_class_name("zg_rankInfo")

        for item in items:

            print("Item Found")

            rank = item.find_element_by_class_name("zg_rank")
            section = item.find_element_by_class_name("a-section")
            link = section.find_element_by_tag_name("a")
            itemURL = link.get_attribute("href")
            itemTitle = link.find_element_by_class_name("p13n-sc-truncated")

            print(f"Rank {rank.text}\nTitle {itemTitle.text}")
                
            self.newTab()
            self.switchTab(self.driver.window_handles[1])
            self.driver.get(itemURL)
            self.waitUntilBodyTagFound()                
            self.scrapReleaseItem()
            self.closeTab()
                
            # Switching to old tab
            self.switchTab(self.driver.window_handles[0])

        self.driver.back()
        self.waitUntilBodyTagFound()


    def scrapReleaseItem(self):
        ''' Scrape the details of released item '''
        
        soup = self.scrap()
        body = soup.find("body")
        # print(body.prettify())


if __name__ == "__main__":

    CHROME_DRIVER_PATH = "C:/Users/ELCOT/WebDriver/bin/chromedriver"
    # Must be given the correct path of chromedriver.exe
    isError = 0
    try:
        bot = AmazonBot(CHROME_DRIVER_PATH)
        bot.clickNewReleases()
        bot.scrapNewReleases()
        bot.newReleasedItems()
    except Exception as e:
        print(e)
        isError = 1
    finally:
        bot.terminateBot(status=isError)