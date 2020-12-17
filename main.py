import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import itertools
import PySimpleGUI as sg

chromedriver_location = os.path.join(os.getcwd(), 'chromedriver')
driver = webdriver.Chrome(chromedriver_location)

def get_times(zc1, zc2):
    """given two zipcodes, go to google maps to parse the travelling time in (hour, minute) format"""
    
    #go to the google maps page and select driving
    driver.get(f'https://www.google.com/maps/dir/Singapore+{zc1}/Singapore+{zc2}')
    time.sleep(0.1)
    driver.find_elements_by_css_selector("[aria-label='Driving']")[0].click()

    #dont spam google + increasing delay to make the html load properly i think
    time.sleep(1.2)

    #parse out times on the browser after taking the html
    page = BeautifulSoup(driver.page_source, 'html.parser')
    grabbed = page.find_all('div', {'class':'section-directions-trip-duration'})
    parsed =  re.findall('(?:(\d+) hr)? ?(?:(\d+) min)', ' '.join(str(i) for i in grabbed))

    #get (hour:int, minute:int) format
    processed = []
    for h, m in parsed:
        if not h:
            h = 0
        if not m:
            m = 0
        processed.append((int(h), int(m)))
    return processed



def find_min_time(zipcodes):
    """return the 2 zipcode combination that has the shortest travelling time"""
    
    #if you need it to be both ways, just change it to permutations
    combinations = itertools.combinations(zipcodes, 2)
    times = {}
    for c1, c2 in combinations:
        times[(c1, c2)] = min(get_times(c1, c2))

    return min(times.items(), key=lambda i:i[1])

    

def main():
    """the gui that uses the above functions to find the shortest time"""
    layout = [
        [sg.Text("Enter zipcodes here!")], 
        [sg.Input(key='-IN-')], 
        [sg.Text('Zipcode 1: '), sg.Text('_______________', key="zc1")],
        [sg.Text('Zipcode 2: '), sg.Text('_______________', key="zc2")],
        [sg.Text('Hours: '), sg.Text('_______________', key="h")],
        [sg.Text('Minutes: '), sg.Text('_______________', key="m")],
        [sg.Button('Read'), sg.Exit()]
        ]

    # Create the window
    window = sg.Window("Zipcode stuff", layout)

    try:
        # Create an event loop
        while True:
            event, values = window.read()
            # End program if user closes window or
            # presses the OK button
            if event == 'Read':
                zipcodes = re.split(' *, *', values['-IN-'])
                (z1, z2), (hr, min_) = find_min_time(zipcodes)
                window['zc1'].update(z1)
                window['zc2'].update(z2)
                window['h'].update(hr)
                window['m'].update(min_)

            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

    except Exception as e:
        print(e)
        
    finally:
        driver.close()
        window.close()

main()