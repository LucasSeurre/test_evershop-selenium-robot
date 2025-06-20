import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configTest import configTest



@pytest.fixture
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
class TestLogin:
    def test_login_success(self, driver):
        self.login_success(self, driver)

    def test_login_error(self, driver):
        driver.get(configTest.urlLocalTest+"/admin/login")
        driver.find_element(By.NAME, "email").send_keys("test@test.fr")
        driver.find_element(By.NAME, "password").send_keys("12345679")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.text-critical.py-4"))
        )
        assert "Invalid email or password" in error.text
    
    def login_success(driver):
        driver.get(configTest.urlLocalTest+"/admin/login")
        driver.find_element(By.NAME, "email").send_keys(configTest.login)
        driver.find_element(By.NAME, "password").send_keys(configTest.password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
        )
        assert driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text == "Dashboard"