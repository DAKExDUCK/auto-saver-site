import json
import os
import shutil
import time
from os import listdir
from os.path import isdir, isfile, join

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


if not os.path.exists('pdf'):
    os.mkdir('pdf')
else:
    shutil.rmtree('pdf')
    os.mkdir('pdf')

path_loc = os.path.join(os.getcwd(), "pdf")
chrome_options = webdriver.ChromeOptions()
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": ""
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "mediaSize": {
        "height_microns": 210000,
        "name": "ISO_A5",
        "width_microns": 148000,
        "custom_display_name": "A5"
    },
    "customMargins": {},
    "marginsType": 2,
    "scaling": 100,
    "scalingType": 3,
    "scalingTypePdf": 3,
    "isCssBackgroundEnabled": False
}
prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
    'savefile.default_directory': path_loc
}
chrome_options.add_argument('--enable-print-browser')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

main_url = input('Set URL:\n')
driver.get(main_url)
accept = input('Next link? Y/N:\n')
if accept == "N":
    time.sleep(1)
else:
    main_url = input('Set URL:\n')
    driver.get(main_url)

js = "var aa=document.getElementsByClassName('tag-feed')[1];" \
    "aa.parentNode.removeChild(aa)"
driver.execute_script(js)
tag_links = driver.find_elements(By.CLASS_NAME, 'tag-link')
categories = [tag_link.get_attribute('href') for tag_link in tag_links]

for category in categories:
    cat_name = category.split("/")[-2]
    driver.get(category)
    try:
        button_more = driver.find_element(By.CLASS_NAME, 'infinite-scroll-button')
        button_more.click()
    except:
        pass
    time.sleep(1)
    a_tags = driver.find_elements(By.CLASS_NAME, 'post-link')
    links = [a_tag.get_attribute('href') for a_tag in a_tags]

    for link in links:
        driver.get(link)
        time.sleep(1)
        js = "window.onafterprint = function(){const newDiv = document.createElement('div');newDiv.classList.add('bar');document.body.appendChild(newDiv)};" \
            "window.print();"
        driver.execute_script(js)
        while 1:
            time.sleep(1)
            bar = driver.find_elements(By.CLASS_NAME, 'bar')
            if len(bar)==1:
                break
    files = [f for f in listdir(path_loc) if isfile(join(path_loc, f))]
    if not os.path.exists(f'{path_loc}/{cat_name}'):
        os.makedirs(f'{path_loc}/{cat_name}')

    for file in files:
        os.replace(f"{path_loc}/{file}", f"{path_loc}/{cat_name}/{file}")
    

driver.close()
driver.quit()
