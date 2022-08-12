import time
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
    def initWallet():
        print("Status - Initializing wallet")
        # add wallet to chrome

        if (
            driver.current_url
            != "chrome-extension://gfoeaaijjjdneafnjccohndgdljjoemp/onboarding.html"
        ):
            driver.switch_to.window(driver.window_handles[0])
        if (
            driver.current_url
            != "chrome-extension://gfoeaaijjjdneafnjccohndgdljjoemp/onboarding.html"
        ):
            driver.switch_to.window(driver.window_handles[1])

        print("Event - switch window")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")
            )
        )
        recovery_phrase = driver.find_element(
            By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]"
        ).click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//textarea[@placeholder='Secret phrase']")
            )
        )
        text_area = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Secret phrase']"
        ).send_keys(values[1])
        import_btn = driver.find_element(
            By.XPATH, "//button[@class='sc-bdfBQB bzlPNH']"
        ).click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Password']")
            )
        )
        password1 = driver.find_element(
            By.XPATH, "//input[@placeholder='Password']"
        ).send_keys(values[2])
        password2 = driver.find_element(
            By.XPATH, "//input[@placeholder='Confirm Password']"
        ).send_keys(values[2])
        check_box = driver.find_element(By.XPATH, "//input[@type='checkbox']").click()
        submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Continue')]")
            )
        )
        continue_ = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue')]"
        )
        driver.execute_script("arguments[0].click();", continue_)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Finish')]")
            )
        )
        finish = driver.find_element(By.XPATH, "//button[contains(text(),'Finish')]")
        driver.execute_script("arguments[0].click();", finish)
        print("Status - Finished Initializing wallet")
        driver.switch_to.window(driver.window_handles[0])

    def selectWallet():
        print("Status - Selecting wallet on ME")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Connect Wallet')]")
            )
        )
        select_wallet = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Connect Wallet')]"
        )
        select_wallet.click()

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button/div/span[contains(text(),'Phantom')]")
            )
        )
        phantom = driver.find_element(
            By.XPATH, "//button/div/span[contains(text(),'Phantom')]"
        )
        phantom.click()

        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Connect')]")
            )
        )
        popup_connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]"
        )
        popup_connect.click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'I understand')]")
            )
        )
        agree = driver.find_element(
            By.XPATH, "//button[contains(text(),'I understand')]"
        )
        agree.click()
        print("Status - Finished Selecting Wallet on ME")

    def avaitMint():
        print(
            "Status - Waiting for Mint, maximum time wait is 24h, after that please restart bot"
        )
        WebDriverWait(driver, 60 * 60 * 24).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Mint your token!')]")
            )
        )
        print("Found the mint button")
        trys = 0
        while trys < 10:  # Try to mint 10 times
            mint_your_token = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Mint your token!')]"
            )
            driver.execute_script("arguments[0].click();", mint_your_token)
            print("Found the button")

            original_window = driver.current_window_handle
            WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(), 'Approve')]")
                )
            )
            approve = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Approve')]"
            )
            approve.click()
            trys += 1

    print("Bot started")
    if isWindows:
        print("OS : Windows")
    else:
        print("OS : Mac")

    options = Options()

    options.add_extension("Phantom.crx")
    options.add_argument("--disable-gpu")

    # to keep window open after mint uncomment option below, side effect, will open alot of chrome windows
    # options.add_experimental_option("detach", True)

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # options for chrome install
    os.environ["WDM8LOCAL"] = "1"

    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), options=options
    )
    print("Assertion - successfully found chrome driver")

    # opens the launchpad page
    driver.get(values[0])
    driver.maximize_window()

    # Actions - Initialize wallet
    initWallet()

    # Actions - select wallet on magic eden
    selectWallet()

    # Actions - close popup
    # closePopup()

    # Actions - MINTS WHEN TIMER IS UP
    avaitMint()

    print("Minting Finished")
