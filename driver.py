from selenium import webdriver
import secrets
from selenium.webdriver.common.by import By
from time import sleep


class Driver:
    __LOGIN_URL = "https://account.emofid.com/Login"
    __DESTINATION_URL = "https://d.orbis.easytrader.ir/"

    def logged_in_driver(self):
        """
        Create a WebDriver instance, log in using provided credentials,
        and navigate to a destination URL.

        Returns:
            webdriver: An object of webdriver logged in and navigated to the destination URL.
        """
        driver = webdriver.Chrome()
        driver.get(self.__LOGIN_URL)
        username_field = driver.find_element(By.ID, "Username")
        password_field = driver.find_element(By.ID, "Password")
        username_field.send_keys(secrets.username)
        password_field.send_keys(secrets.password)
        login_button = driver.find_element(By.ID, "submit_btn")
        login_button.click()
        driver.get(self.__DESTINATION_URL)
        sleep(2)
        return driver
