import datetime

from selenium import webdriver
from urllib.request import (urlretrieve)
import os


class DaftScraper:
    def _init_(self, subject_of_email, url):
        self._url = url
        self._default_destination_super_folder = 'C:\\Users\\willo\\Google Drive\\Daft Automated responder'
        self._subject_of_email = subject_of_email
        self._formatted_datetime = str(datetime.datetime.now()).replace('.', '-').replace(':', '-')
        self._destination_folder = self._default_destination_super_folder + '\\' + \
                                   self._subject_of_email + ' ' + self._formatted_datetime
        if not os.path.exists(self._destination_folder):
            os.makedirs(self._destination_folder)

        # initialising scraper
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument('headless')

        self._driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe", options=self._chrome_options)
        self._driver.get(self._url)

    def _scrape_images(self):
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
                if str(link).startswith('https://b.dmlimg.com/'):
                    uri.append(link)
                    pos = len(link) - link[::-1].index('/')
                    urlretrieve(link, "/".join([image_folder, link[pos:]]))
            except Exception as e:
                print('Invalid link')
                print(e)

    def _scrape_details(self):
        details_folder = self._destination_folder + '\\details'
        details = ''

        details += '------------------------- Landord  -----------------------------\n'

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


'''
if __name__ == "__main__":
    subject_of_email = 'Ringsend, Apartment To Let, €2,600 per month'

    destination_folder = default_destination_super_folder + '\\' + subject_of_email + ' ' + \
                         str(datetime.datetime.now()).replace('.', '-').replace(':', '-')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    scrape_images(
        'https://www.daft.ie/dublin/flats-for-rent/rathmines/4-windsor-road-1a-rathmines-dublin-2006893'
        '/?utm_campaign=property_alert_email_residential_to_let&utm_medium=email&ea=1&utm_source=property_alert',
        destination_folder
    )

    scrape_details('https://www.daft.ie/dublin/flats-for-rent/rathmines/4-windsor-road-1a-rathmines-dublin-2006893'
                   '/?utm_campaign=property_alert_email_residential_to_let&utm_medium=email&ea=1&utm_source=property_alert',
                   destination_folder
                   )
'''
