import datetime
import config
from selenium import webdriver
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
        self._chrome_options.add_argument('headless')

        self._driver = webdriver.Chrome(config.chrome_driver, options=self._chrome_options, service_log_path='NUL')
        self._driver.get(self._url)

    def scrape_images(self):
        image_folder = self._destination_folder + '\\images'

        element = self._driver.find_element_by_xpath("//div[@data-testid='headerImageClickArea']")
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

    def scrape_details(self):
        self._driver.implicitly_wait(0.5)
        details_folder = self._destination_folder + '\\details'

        self._driver.execute_script("return document.getElementById('js-cookie-consent').remove();")
        element = self._driver.find_elements_by_tag_name('html')[0]

        details = element.get_attribute('innerHTML')
        '''
        details = ''
        
        details += '------------------------- Landlord  -----------------------------\n'

        detail_elements = self._driver.find_element_by_xpath("//p[@class='ContactPanel__ImageLabel-sc-18zt6u1-6 dYjBri']")
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

