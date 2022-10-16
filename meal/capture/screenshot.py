from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform # to check the os
from PIL import Image

#Imports paths
from dotenv import load_dotenv
load_dotenv()
import os

# New Version's import below now this file is using deprecated version of Selenium
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

def takeScreenshot():

    if(platform == "linux"):
        CHROME_PATH = os.getenv("CHROME_PATH_LINUX")
        CHROMEDRIVER_PATH = os.getenv("CHROME_DRIVER_PATH_LINUX")
    elif(platform == "win32"):
        CHROME_PATH = os.getenv("CHROME_PATH_WIN32")
        CHROMEDRIVER_PATH = os.getenv("CHROME_DRIVER_PATH_WIN32")

    WINDOW_SIZE = "1920,4500"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=chrome_options)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://kafemud.bilkent.edu.tr/monu_eng.html")
    driver.save_screenshot('meal/menu/weekly_menu.png')
    
    weekly = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[2]")
    byteImage = weekly.screenshot_as_png
    with open(f"meal\menu\weekly_menu.png", 'wb') as f:
        f.write(byteImage)

    for day in range(0,7):
        lunch = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[{(day+1)*2}]")
        dinner = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[{(day+1)*2+1}]")
        alternative = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr[{(day+1)+1}]")

        byteImage = lunch.screenshot_as_png
        with open(f"meal\daily-menus\ogle_{day}.png", 'wb') as f:
            f.write(byteImage)
        
        byteImage = dinner.screenshot_as_png
        with open(f"meal\daily-menus\\aksam_{day}.png", 'wb') as f:
            f.write(byteImage)

        byteImage = alternative.screenshot_as_png
        with open(f"meal\daily-menus\\secmeli_{day}.png", 'wb') as f:
            f.write(byteImage)
<<<<<<< HEAD
=======

takeScreenshot()
>>>>>>> d39890e37368c90280de502b8d7630feb1df3a4f
