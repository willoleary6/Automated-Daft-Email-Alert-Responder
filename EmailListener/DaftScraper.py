import datetime
import config 
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import (urlretrieve)
import os


class DaftScraper:
    def __init__(self, subject_of_email, url):
        self._url = url
        self._default_destination_super_folder = config.default_destination_super_folder
        self._subject_of_email = subject_of_email
        self._formatted_datetime = str(datetime.datetime.now()).replace('.', '-').replace(':', '-')
        self._destination_folder = self._default_destination_super_folder + '\\' + \
                                   self._subject_of_email + ' ' + self._formatted_datetime
        if not os.path.exists(self._destination_folder):
            os.makedirs(self._destination_folder)

        # initialising scraper
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument("--window-size=3840,2160")
        self._chrome_options.add_argument("--headless")
        self._chrome_options.add_argument("--disable-gpu")
        self._chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")


        self._driver = webdriver.Chrome(config.chrome_driver, options=self._chrome_options, service_log_path='NUL')
        self._driver.get(self._url)
        #self._driver.switch_to.default_content()
        #ui.WebDriverWait(self._driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#contants>iframe")))

    def scrape_images(self):
        image_folder = self._destination_folder + '\\images'
        element = self._driver.find_elements_by_tag_name('html')[0]
        screenshot = element.screenshot_as_png
        f = open(image_folder+"screenshot.png", 'wb')
        f.write(screenshot)
        f.close()
        '''
        try:
            element = self._driver.find_element_by_xpath("//div[@data-testid='headerImageClickArea']")
        except Exception as e:
            print(e)
        webdriver.ActionChains(self._driver).move_to_element(element).click().perform()
        uri = []
        image_elements = self._driver.find_elements_by_tag_name('img')
        index = 0
        for image in image_elements:
            link = image.get_attribute("src")
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            try:
                if str(link).startswith(config.daft_image_url):
                    index += 1
                    uri.append(link)
                    pos = len(link) - link[::-1].index('/')
                    path = "/".join([image_folder, link[pos:]])
                    urlretrieve(link, path)
                    os.rename(path, "/".join([image_folder, str(index) + '.jpeg']))
            except Exception as e:
                print('Invalid link')
                print(e)
        '''
    def scrape_details(self):
        self._driver.implicitly_wait(0.5)
        details_folder = self._destination_folder + '\\details'

        self._driver.execute_script("return document.getElementById('js-cookie-consent').remove();")
        element = self._driver.find_elements_by_tag_name('html')[0]
        screenshot = element.screenshot_as_png
        f = open('C:\\Users\\willo\\Documents\\PngFiles\\here.png', 'wb')
        f.write(screenshot)
        f.close()
        details = element.get_attribute('body')
        print("test")
        '''
        details = ''
        
        details += '------------------------- Landlord  -----------------------------\n'
        
        detail_elements = self._driver.find_element_by_xpath("//p[@class='PropertyPage__ContactFormSection-sc-14jmnho-13 DThnS']")
        #for element in detail_elements:
        details += detail_elements.text + '\n'

        details += '------------------------- Overview -----------------------------\n'
        try:
            detail_elements = self._driver.find_elements_by_class_name('PropertyOverview__propertyOverviewDetails')
            for element in detail_elements:
                details += element.text + '\n'
        except:
            details += '-no overview \n'

        details += '------------------------- description -----------------------------\n'
        try:
            detail_elements = self._driver.find_elements_by_class_name('PropertyDescription__propertyDescription')
            for element in detail_elements:
                details += str(element.text).replace('. ', '.\n') + '\n'
        except:
            details += '-no description \n'
        details += '------------------------- Facilities -----------------------------\n'

        # have to expand list first...
        # ExpandMoreIndicator__expandLink
        try:
            parent_element = self._driver.find_element_by_class_name("PropertyFacilities__facilitiesList")
            element_list = parent_element.find_elements_by_tag_name("li")
            for element in element_list:
                details += element.text + '\n'
        except:
            details += '-no facilities \n'

        details += '------------------------- Energy details -----------------------------\n'
        try:
            detail_elements = self._driver.find_elements_by_class_name('BERDetails__berDetailsContainer')
            for element in detail_elements:
                details += str(element.text).replace('. ', '.\n') + '\n'
        except:
            details += '-no Energy details \n'

        # have everything we need write to file
        '''
        # check that folder exists. if not create it
        if not os.path.exists(details_folder):
            os.makedirs(details_folder)

        # check if file exists, if not create it
        try:
            open(details_folder + '\details.html', 'r')
        except FileNotFoundError:
            open(details_folder + '\details.html', 'w')

        # write to file

        f = open(details_folder + '\details.html', 'w')
        f.write(details)
        f.close()

