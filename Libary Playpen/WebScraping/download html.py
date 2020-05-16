import datetime

from selenium import webdriver
from urllib.request import (urlretrieve)
import os

default_destination_super_folder = 'C:\\Users\\willo\\Documents\\Html dump\\'


def scrape_images(url, destination_folder):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe", options=chrome_options)
    driver.get(url)
    destination_folder += '\\images'
    element = driver.find_elements_by_class_name('PropertyImage__ImageHolder')[0]
    webdriver.ActionChains(driver).move_to_element(element).click(element).perform()
    uri = []
    r = driver.find_elements_by_tag_name('img')
    for image in r:
        link = image.get_attribute("src")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        try:
            if str(link).startswith('https://b.dmlimg.com/'):
                uri.append(link)
                pos = len(link) - link[::-1].index('/')
                urlretrieve(link, "/".join([destination_folder, link[pos:]]))
        except Exception as e:
            print('Invalid link')
            print(e)


def scrape_details(url, destination_folder):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe", options=chrome_options)
    driver.get(url)
    destination_folder += '\\details'
    details = ''

    details += '------------------------- Landord  -----------------------------\n'

    product_titles = driver.find_elements_by_class_name('ContactForm__negotiatorName')
    for title in product_titles:
        details += title.text + '\n'

    details += '------------------------- Overview -----------------------------\n'

    product_titles = driver.find_elements_by_class_name('PropertyOverview__propertyOverviewDetails')
    for title in product_titles:
        details += title.text + '\n'

    details += '------------------------- description -----------------------------\n'
    product_titles = driver.find_elements_by_class_name('PropertyDescription__propertyDescription')
    for title in product_titles:
        details += str(title.text).replace('. ', '.\n') + '\n'

    details += '------------------------- Facilities -----------------------------\n'

    # have to expand list first...
    # ExpandMoreIndicator__expandLink

    parent_element = driver.find_element_by_class_name("PropertyFacilities__facilitiesList")
    element_list = parent_element.find_elements_by_tag_name("li")
    for title in element_list:
        details += title.text + '\n'

    details += '------------------------- Energy details -----------------------------\n'
    product_titles = driver.find_elements_by_class_name('BERDetails__berDetailsContainer')
    for title in product_titles:
        details += str(title.text).replace('. ', '.\n') + '\n'

    # have everything we need write to file

    # check that folder exists. if not create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # check if file exists, if not create it
    try:
        open(destination_folder + '\details.txt', 'r')
    except FileNotFoundError:
        open(destination_folder + '\details.txt', 'w')

    # write to file

    f = open(destination_folder + '\details.txt', 'w')
    f.write(details)
    f.close()


if __name__ == "__main__":
    subject_of_email = 'Ringsend, Apartment To Let, €2,600 per month'

    destination_folder = default_destination_super_folder + subject_of_email + ' ' + \
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
