"""Claim zens from the Edyoda Website"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from conf import CHROMEDRIVER_PATH, USERNAME, PASSWORD


def connect(executable_path=CHROMEDRIVER_PATH):
    return webdriver.Chrome(executable_path=executable_path)


def login(driver: webdriver.Chrome, username=USERNAME, password=PASSWORD):
    driver.get("https://edyoda.com")  # Open Edyoda website
    # Wait for the popup as the popup appears only after the page loads
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/form/div[1]')))
    # click on login
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/header/div/div[1]/div/ul[2]/li[2]/button').click()

    login_div_xpath = '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/form/div'
    driver.find_element_by_xpath(f'{login_div_xpath}/div[1]/div/input').send_keys(username)  # Type username
    driver.find_element_by_xpath(f'{login_div_xpath}/div[2]/div/input').send_keys(password)  # Type password
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[4]/button[1]').click()  # Sign In


def claim(driver):
    # Wait and click on daily zens icon
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/header/div/div[1]/div/ul[2]/li[4]').click()
    # Wait and Claim zens
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/header/div/div[1]/div/ul[2]/li[4]'
                                 '/div[2]/div[2]/div/div/div/button[1]').click()

    # Click Done
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="root"]/div/div[1]/div[3]/div[2]/div[2]/div/div/button[1]'))).click()


if __name__ == '__main__':
    driver = connect()
    login(driver)
    claim(driver)
