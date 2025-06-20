# Test de paiement en Selenium (avec WebDriverWait)
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
class TestPaiement:
    def setup_method(self, method):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def teardown_method(self, method):
        self.driver.quit()

    def test_paiement(self):
        self.driver.get("http://localhost:3000/")

        # Cliquer sur le premier produit
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".listing-tem:nth-child(1) .product-name span"))).click()

        # Ajouter au panier
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button > span"))).click()

        # Voir le panier
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "VIEW CART (1)"))).click()

        # Checkout
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "CHECKOUT"))).click()

        # Email
        self.wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("test@test.fr")
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-submit-button span"))).click()

        # Adresse
        self.wait.until(EC.visibility_of_element_located((By.NAME, "address[full_name]"))).send_keys("Lucas")
        self.driver.find_element(By.NAME, "address[telephone]").send_keys("0606060606")
        self.driver.find_element(By.NAME, "address[address_1]").send_keys("1 rue du test")
        self.driver.find_element(By.NAME, "address[city]").send_keys("Lyon")

        # Pays
        country = self.driver.find_element(By.ID, "address[country]")
        country.find_element(By.CSS_SELECTOR, "option[value='FR']").click()

        # Région
        # Attente explicite
        province_select = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.ID, "address[province]")
        )

        # Utilisation du Select de Selenium
        select = Select(province_select)
        select.select_by_visible_text("Auvergne-Rhone-Alpes")

        self.driver.find_element(By.NAME, "address[postcode]").send_keys("69000")

        # Transport
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".radio-unchecked"))).click()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-submit-button span"))).click()

        # Paiement
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".feather"))).click()

        # Remplir formulaire Stripe (dans iframe)
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']")))
        self.wait.until(EC.visibility_of_element_located((By.ID, "Field-numberInput"))).send_keys("4242 4242 4242 4242")
        self.driver.find_element(By.ID, "Field-expiryInput").send_keys("04 / 26")
        self.driver.find_element(By.ID, "Field-cvcInput").send_keys("424")
        self.driver.switch_to.default_content()

        # Valider le paiement
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-submit-button span"))).click()

        # Attendre la redirection ou confirmation
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "div"), "Thank you Lucas"
            )
        )
