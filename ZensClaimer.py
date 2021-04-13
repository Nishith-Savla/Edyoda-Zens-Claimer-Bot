"""Claim zens from the Edyoda Website."""
import time
import sys.exit

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from conf import CHROMEDRIVER_PATH, PASSWORD, USERNAME


def connect(executable_path=CHROMEDRIVER_PATH) -> webdriver.Chrome:
    """Connect to the webdriver and returns the driver.

    Parameters
    ----------
    executable_path: str
        The path to the chromedriver executable.

    Returns
    -------
    driver: webdriver.Chrome
        A webdriver(chromedriver) instance.
    """
    return webdriver.Chrome(executable_path=executable_path)


def login(driver: webdriver.Chrome, username=USERNAME, password=PASSWORD):
    """Log in to the Edyoda account.

    Parameters
    ----------
    driver: webdriver.Chrome
        The chromedriver instance.
    username: str
        Edyoda account username.
    password: str
        Edyoda account password.
    """
    driver.get("https://edyoda.com")  # Open Edyoda website
    wait: WebDriverWait = WebDriverWait(driver, 15)

    wait.until(ec.invisibility_of_element(
        (By.XPATH, '//div[contains(@class, "Loader")]/svg')))

    wait.until(
        ec.element_to_be_clickable(
            (By.XPATH,
             '//button[contains(text(), "Log") or contains(@id, "login")]'))
    ).click()

    wait.until(ec.presence_of_element_located(  # Type username
        (By.XPATH,
         '//div[contains(@class, "Input")]/label[contains(text(), "sername")]/'
         'following-sibling::input')
    )).send_keys(username)

    driver.find_element_by_xpath(  # Type password
        '//div[contains(@class, "Input")]/label[contains(text(), "assword")]/'
        'following-sibling::input'
    ).send_keys(password)

    driver.find_element_by_xpath(  # Sign In
        '//button[contains(text(), "SIGN IN") and '
        'contains(@class, "NonMobile")]').click()


def claim(driver: webdriver.Chrome) -> bool:
    """Try to claim the daily Zens and return True if successfully claimed,
    else False.

    Parameters
    ----------
    driver: webdriver.Chrome
        The chromedriver instance.

    Returns
    =======
    bool
        True if Zens claimed successfully, else False.
    """
    time.sleep(3)
    try:
        driver.find_element_by_xpath(  # Click on daily zens icon
            '//li[contains(@class, "Container_")]//img[contains(@alt, '
            '"EdYoda Daily")]').click()
        driver.find_element_by_xpath(  # Claim zens
            '//li[contains(@class, "Container_")]//button[contains(text(), '
            '"CLAIM") and contains(@class, "NonMobile")]'
        ).click()
    except NoSuchElementException:
        return False
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(  # Click Done
                (By.XPATH,
                 '//button[contains(text(), "DONE") and '
                 'contains(@class, "NonMobile")]'))).click()
    except TimeoutException:
        print("Done dialog not found")
        return False
    return True


if __name__ == '__main__':
    driver = connect()
    login(driver)
    if claim(driver):
        driver.close()
        print("Claim Success")
        sys.exit(0)
