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
        element = self._driver.find_elements_by_class_name('PropertyImage__ImageHolder')[0]
        webdriver.ActionChains(self._driver).move_to_element(element).click(element).perform()
        uri = []
        image_elements = self._driver.find_elements_by_tag_name('img')
        for image in image_elements:
            link = image.get_attribute("src")
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            try:
                if str(link).startswith(config.daft_image_url):
                    uri.append(link)
                    pos = len(link) - link[::-1].index('/')
                    urlretrieve(link, "/".join([image_folder, link[pos:]]))
            except Exception as e:
                print('Invalid link')
                print(e)

    def scrape_details(self):
        details_folder = self._destination_folder + '\\details'
        details = ''

        details += '------------------------- Landlord  -----------------------------\n'

        detail_elements = self._driver.find_elements_by_class_name('ContactForm__negotiatorName')
        for element in detail_elements:
            details += element.text + '\n'

        details += '------------------------- Overview -----------------------------\n'

        detail_elements = self._driver.find_elements_by_class_name('PropertyOverview__propertyOverviewDetails')
        for element in detail_elements:
            details += element.text + '\n'

        details += '------------------------- description -----------------------------\n'
        detail_elements = self._driver.find_elements_by_class_name('PropertyDescription__propertyDescription')
        for element in detail_elements:
            details += str(element.text).replace('. ', '.\n') + '\n'

        details += '------------------------- Facilities -----------------------------\n'

        # have to expand list first...
        # ExpandMoreIndicator__expandLink

        parent_element = self._driver.find_element_by_class_name("PropertyFacilities__facilitiesList")
        element_list = parent_element.find_elements_by_tag_name("li")
        for element in element_list:
            details += element.text + '\n'

        details += '------------------------- Energy details -----------------------------\n'
        detail_elements = self._driver.find_elements_by_class_name('BERDetails__berDetailsContainer')
        for element in detail_elements:
            details += str(element.text).replace('. ', '.\n') + '\n'

        # have everything we need write to file

        # check that folder exists. if not create it
        if not os.path.exists(details_folder):
            os.makedirs(details_folder)

        # check if file exists, if not create it
        try:
            open(details_folder + '\details.txt', 'r')
        except FileNotFoundError:
            open(details_folder + '\details.txt', 'w')

        # write to file

        f = open(details_folder + '\details.txt', 'w')
        f.write(details)
        f.close()

