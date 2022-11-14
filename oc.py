from lib2to3.pgen2 import driver
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

url = 'https://oc.app'

numOfMessageToSend = 0

with open('content.txt') as f:
    lines = f.readlines()


def run(config, profile):
    global numOfMessageToSend
    profileName = profile["name"]
    groupName = profile["group"]
    numOfMessageToSend = config["numberOfMessageToSend"]
    print("Bot started with profile "+profile["name"])

    def autoChatOC(browser):
        global numOfMessageToSend
        browser.switch_to.window(browser.window_handles[0])
        print('(' + str(numOfMessageToSend) + ') click on group chat')
        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), '" + groupName + "')]")))
        browser.find_element(
            By.XPATH, "//*[contains(text(), '" + groupName + "')]").click()
        time.sleep(1)
        print('click on input chat')
        if len(browser.find_elements(
                By.XPATH, "//*[@placeholder='Nhập tin nhắn']")) > 0:
            inputEle = browser.find_element(
                By.XPATH, "//*[@placeholder='Nhập tin nhắn']")
        else:
            inputEle = browser.find_element(
                By.XPATH, "//*[@placeholder='Enter a message']")
        print('Input content')
        # driver.execute_script(
        #     "var ele=arguments[0]; ele.innerHTML = 'Google';", inputEle)
        inputEle.click()
        content = random.choice(lines)
        for char in content:
            inputEle.send_keys(char)
        print("Sleep " + str(config["timeToChat"]) + " seconds")
        time.sleep(config["timeToChat"])
        numOfMessageToSend = numOfMessageToSend - 1
        browser.close()

    def initChrome(profile):
        options = Options()

        # options.add_extension("Petra-Aptos-Wallet.crx")
        options.add_argument("--disable-gpu")

        prefs = {"profile.managed_default_content_settings.images": 1}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        options.add_argument(
            r"--user-data-dir=" + config["dir"])
        options.add_argument(r'--profile-directory=' +
                             profile)  # e.g. Profile 3

        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = config["driver"]
        driver = webdriver.Chrome(chrome_driver_binary, options=options)
        return driver

    def runFlow(browser):
        global numOfMessageToSend
        browser.switch_to.window(browser.window_handles[0])
        browser.get(url)
        while numOfMessageToSend > 0:
            autoChatOC(browser)

    driver = initChrome(profileName)
    print("Assertion - successfully found chrome driver")
    runFlow(driver)
