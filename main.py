import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import itertools

chromedriver_location = os.path.join(os.getcwd(), 'chromedriver')
driver = webdriver.Chrome(chromedriver_location)

def get_time(zc1, zc2):
    """given two zipcodes, go to google maps to parse the travelling time"""
    driver.get(f'https://www.google.com/maps/dir/Singapore+{zc1}/Singapore+{zc2}')
    time.sleep(0.6)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    grabbed = page.find_all('div', {'class':'section-directions-trip-duration'})
    parsed =  re.findall('(?:(\d+) hr)? ?(?:(\d+) min)', ' '.join(str(i) for i in grabbed))
    processed = []
    for h, m in parsed:
        if not h:
            h = 0
        if not m:
            m = 0
        processed.append((int(h), int(m)))
    return processed


#testing
TESTCODES = ['680112', '188065', '119077']
#if you need it to be both ways, just change it to permutations
combinations = itertools.combinations(TESTCODES, 2)

for c1, c2 in combinations:
    print(c1, c2, get_time(c1, c2))
input('whatever 2 close:')
driver.close()