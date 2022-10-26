from lib2to3.pgen2 import driver
import time
import multiprocessing
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


def mint(values, isWindows):
    
    def selectWallet():
        print("Status - Selecting wallet on ME")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "/html[1]/body[1]/div[2]/div[2]/header[1]/nav[1]/div[2]/div[2]/div[1]/button[2]")))
        select_wallet = driver.find_element(
            By.XPATH, "/html[1]/body[1]/div[2]/div[2]/header[1]/nav[1]/div[2]/div[2]/div[1]/button[2]")
        select_wallet.click()

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Phantom')]")))
        phantom = driver.find_element(
            By.XPATH, "//span[contains(text(),'Phantom')]")
        phantom.click()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='sc-bqiRlB hLGcmi sc-hBUSln dhBqSt']")))
        popup_connect = driver.find_element(
            By.XPATH, "//button[@class='sc-bqiRlB hLGcmi sc-hBUSln dhBqSt']")
        popup_connect.click()
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'I understand')]")))
        agree = driver.find_element(
            By.XPATH, "//button[contains(text(),'I understand')]")
        agree.click()
        driver.refresh();
        print("Status - Finished Selecting Wallet on ME")



    def avaitMint(browser):
        main_window = browser.window_handles[0]
        browser.switch_to.window(main_window)
        print("Status - Waiting for Mint, maximum time wait is 24h, after that please restart bot")
        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Mint Now')]")))
        browser.find_element(
            By.XPATH, "//*[contains(text(), 'Mint Now')]").click()
        time.sleep(5)

        WebDriverWait(browser, 60).until(EC.number_of_windows_to_be(2))
        print('switch')
        browser.switch_to.window(browser.window_handles[1])

        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Cancel')]")))
        print('has approve')
        browser.find_element(
            By.XPATH, "//button[contains(text(), 'Cancel')]").click()

        time.sleep(5)

    def connectSuiStep(browser):
        print('sui click')
        browser.find_element(By.XPATH, "//*[contains(text(), 'Sui Wallet')]").click()

    def bluemoveMint(browser):
        browser.switch_to.window(browser.window_handles[0])
        print("Status - Waiting for Mint, maximum time wait is 24h, after that please restart bot")
        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint')]")))
        browser.find_element(
            By.XPATH, "//button[contains(text(), 'Mint')]").click()
        time.sleep(5)
        print('call mint')
        if len(browser.find_elements(By.XPATH, "//*[contains(text(), 'Sui Wallet')]")) > 0:
            connectSuiStep(browser)
            print('call mint again')
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[0])
            WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Mint')]")))
            browser.find_element(
            By.XPATH, "//button[contains(text(), 'Mint')]").click()
        else:
            print('no sui wallet click')

        WebDriverWait(browser, 60).until(EC.number_of_windows_to_be(2))
        print('switch')
        browser.switch_to.window(browser.window_handles[1])

        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Approve')]")))
        print('has approve')
        browser.find_element(
            By.XPATH, "//*[contains(text(), 'Approve')]").click()

        time.sleep(5)

    def clickClaim(browser):
        print("Status - Waiting for Claim, maximum time wait is 24h, after that please restart bot")
        WebDriverWait(browser, 60*60*24).until(EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Activate Faucet)]")))
        
        mint_your_token = browser.find_element(
            By.XPATH, "//*[contains(text(), 'Activate Faucet')]")
        browser.execute_script("arguments[0].click();", mint_your_token)

        original_window = browser.current_window_handle
        WebDriverWait(browser, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in browser.window_handles:
            if window_handle != original_window:
                browser.switch_to.window(window_handle)
                break

        WebDriverWait(browser, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='sc-bqiRlB hLGcmi sc-hBUSln dhBqSt']")))
        approve = browser.find_element(
            By.XPATH, "//button[@class='sc-bqiRlB hLGcmi sc-hBUSln dhBqSt']")
        approve.click()
        time.sleep(50)

    mnemonic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    def initWallet():
        print("Initializing wallet")
        # original_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        # for window_handle in driver.window_handles:
        #     if window_handle != original_window:
        #         driver.switch_to.window(window_handle)
        #         break
        print("Find import wallet")
        # click import
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@class='chakra-button css-d74vtl']")))

        driver.find_element(By.XPATH, "//*[contains(text(), 'Import Wallet')]").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Import mnemonic')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), 'Import mnemonic')]").click()
        # click phase
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@class='chakra-button css-lhf0dg']")))
        # recovery_phrase = driver.find_element(By.XPATH, "//button[@class='chakra-button css-lhf0dg']").click()
        
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@name='mnemonic-a']")))
        for i in range(0, 12):
            driver.find_element(By.XPATH, f"//*[@name='mnemonic-{mnemonic[i]}']").send_keys(values[1].split(' ')[i])
        # driver.find_element(By.XPATH, "//button[@type='Continue']").click()

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continue')]")))
        # time.sleep(5)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continue')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), 'Continue')]").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@name='initialPassword']")))
        password1 = driver.find_element(By.XPATH, "//input[@name='initialPassword']").send_keys('s2xEvilFucking')
        password2 = driver.find_element(By.XPATH, "//input[@name='confirmPassword']").send_keys('s2xEvilFucking')
        check_box = driver.find_element(By.XPATH, "//*[@class='chakra-checkbox__control css-omfrpb']").click()
        submit = driver.find_element(By.XPATH, "//*[contains(text(), 'Continue')]").click()
        time.sleep(10)
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        # continue__ = driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        #     (By.XPATH, "//button[@class='sc-eCImPb fimA-Dk']")))
        # finish = driver.find_element(
        #     By.XPATH, "//button[@class='sc-eCImPb fimA-Dk']")
        # finish.click()
        driver.close()
        print("Finished Initializing wallet")
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)

        return main_window

    def connectWallet(browser):
        print('Connect wallet')
        main_window = browser.window_handles[0]
        browser.switch_to.window(main_window)
        time.sleep(10)

        if browser.find_elements(By.XPATH, "//*[contains(text(), 'Connect Wallet')]").count() > 0:
            browser.find_element(By.XPATH, "//*[contains(text(), 'Connect Wallet')]").click()
            time.sleep(2)
        
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Petra Wallet')]")))
            browser.find_element(By.XPATH, "//*[contains(text(), 'Petra Wallet')]").click()
            original_window = browser.current_window_handle
            WebDriverWait(browser, 60).until(EC.number_of_windows_to_be(2))
            print('switch')
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(2)

            WebDriverWait(browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Approve')]")))
            print('has approve')
            browser.find_element(
                By.XPATH, "//button[contains(text(), 'Approve')]").click()
        else:
            print("already connected")

    def blueMoveConnectWallet(browser):
        print('Connect wallet')
        main_window = browser.window_handles[0]
        browser.switch_to.window(main_window)
        if len(browser.find_elements(By.XPATH, "//*[contains(text(), 'Connect Wallet')]")) > 0:
            browser.find_element(By.XPATH, "//*[contains(text(), 'Connect Wallet')]").click()
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sui Wallet')]")))
            print('found sui')
            browser.find_element(By.XPATH, "//*[contains(text(), 'Sui Wallet')]").click()
            original_window = browser.current_window_handle
            WebDriverWait(browser, 60).until(EC.number_of_windows_to_be(2))
            print('switch')
            browser.switch_to.window(browser.window_handles[1])
            WebDriverWait(browser, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Connect')]")))
            print('has approve')
            browser.find_element(
                By.XPATH, "//*[contains(text(), 'Connect')]").click()
        else:
            print("already connected")
    
    def initChrome(profile):
        options = Options()


        # options.add_extension("Petra-Aptos-Wallet.crx")
        options.add_argument("--disable-gpu")

        prefs = {"profile.managed_default_content_settings.images": 1}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        options.add_argument(r"--user-data-dir=/Users/angelit/Downloads/Chrome " + profile) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
        options.add_argument(r'--profile-directory=' + profile) #e.g. Profile 3

        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = "/Users/angelit/Downloads/chromedriver"
        driver = webdriver.Chrome(chrome_driver_binary, options=options)
        return driver

    def unlockWallet(browser):
        print("Unlock wallet")
        # original_window = driver.current_window_handle
        WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
        # for window_handle in driver.window_handles:
        #     if window_handle != original_window:
        #         driver.switch_to.window(window_handle)
        #         break
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password1 = browser.find_element(By.XPATH, "//input[@name='password']").send_keys('s2xEvilFucking')
        submit = browser.find_element(By.XPATH, "//*[contains(text(), 'Unlock')]").click()
        time.sleep(5)
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        # continue__ = driver.find_element(By.XPATH, "//button[@type='submit']").click()
        # WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        #     (By.XPATH, "//button[@class='sc-eCImPb fimA-Dk']")))
        # finish = driver.find_element(
        #     By.XPATH, "//button[@class='sc-eCImPb fimA-Dk']")
        # finish.click()
        browser.close()
        print("Finished unlock wallet")
        main_window = browser.window_handles[0]
        browser.switch_to.window(main_window)

        return main_window

    def unlockBluemoveWallet(browser):
        print("Unlock wallet")
        WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password1 = browser.find_element(By.XPATH, "//input[@name='password']").send_keys('s2xEvilFucking')
        submit = browser.find_element(By.XPATH, "//*[contains(text(), 'Unlock')]").click()
        time.sleep(5)
        browser.close()
        print("Finished unlock wallet")
        main_window = browser.window_handles[0]
        browser.switch_to.window(main_window)

        return main_window

    def openPetraWallet(browser):
        browser.get("chrome-extension://ejjladinnckdgjemekebdpeokbikhfci/index.html")

    def openSuiWallet(browser):
        browser.get("chrome-extension://opcgpfmipidbgpenhmajoajpbobppdil/ui.html")

    def runFlow(browser):
        browser.get(values[0])
        # Open a new window
        browser.execute_script("window.open('');")
        # Switch to the new window
        browser.switch_to.window(browser.window_handles[1])
        # openPetraWallet(browser)
        openSuiWallet(browser)
        # main_window = initWallet()
        unlockWallet(browser)
        # clickClaim(browser)
        blueMoveConnectWallet(browser)
        # selectWallet()

        # avaitMint(browser)
        bluemoveMint(browser)

    print("Bot started") 
    if isWindows:
        print("OS : Windows")
    else:
        print("OS : Mac")
    

    driver = initChrome('Profile 2')
    # driver2 = initChrome('Default')
    os.environ['WDM8LOCAL'] = '1'


    # driver = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", options=options)
    # driver = webdriver.Chrome(executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", options=options)
    
    print("Assertion - successfully found chrome driver")
    
    runFlow(driver)

    # process1 = multiprocessing.Process(target=runFlow, args=(driver,))
    # process2 = multiprocessing.Process(target=runFlow, args=(driver2,))
    # process1.start()
    # process2.start()

    print("Minting Finished")

