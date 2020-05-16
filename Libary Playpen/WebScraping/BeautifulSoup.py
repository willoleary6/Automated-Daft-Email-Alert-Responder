from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlretrieve)

from urllib.parse import urlunparse, urlparse
import os
import sys

def main(url, out_folder="/test/"):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url))
    parsed = list(urlparse(url))

    for image in soup.findAll("img"):
        print("Image: %(src)s" % image)
        filename = image["src"].split("/")[-1]
        parsed[2] = image["src"]
        outpath = os.path.join(out_folder, filename)
        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
        else:
            urlretrieve(urlunparse(parsed), outpath)

def _usage():
    print("usage: python dumpimages.py http://example.com [outpath]")

if __name__ == "__main__":
    url = 'https://www.daft.ie/dublin/flats-for-rent/rathmines/4-windsor-road-1a-rathmines-dublin-2006893/?utm_campaign=property_alert_email_residential_to_let&utm_medium=email&ea=1&utm_source=property_alert'
    out_folder = "C:\\Users\\willo\\Documents\\Html dump\\"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    main(url, out_folder)