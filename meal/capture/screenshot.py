from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform # to check the os
from PIL import Image

# New Version's import below now this file is using deprecated version of Selenium
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

def takeScreenshot():

    if(platform == "linux"):
        CHROME_PATH = '/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/home/alpsencer/bilkent-super-bot/meal/capture/chromedriver'
    elif(platform == "win32"):
        CHROME_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
        CHROMEDRIVER_PATH = 'meal\screenshot\chromedriver.exe'

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

    for day in range(1,8):
        lunch = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[{day*2}]")
        dinner = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[{day*2+1}]")
        alternative = driver.find_element_by_xpath(f"/html/body/div/center/table/tbody/tr[3]/td[2]/div/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr[{day+1}]")

        byteImage = lunch.screenshot_as_png
        with open(f"meal\daily-menus\ogle_{day}.png", 'wb') as f:
            f.write(byteImage)
        
        byteImage = dinner.screenshot_as_png
        with open(f"meal\daily-menus\\aksam_{day}.png", 'wb') as f:
            f.write(byteImage)

        byteImage = alternative.screenshot_as_png
        with open(f"meal\daily-menus\\secmeli_{day}.png", 'wb') as f:
            f.write(byteImage)
