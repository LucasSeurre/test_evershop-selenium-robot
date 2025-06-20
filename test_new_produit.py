import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from test_login import TestLogin

def test_create_modify_delete_product():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    TestLogin.login_success(driver)


    # Aller dans Products
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href$="/admin/products"]'))).click()

    # New Product
    wait.until(EC.element_to_be_clickable((
        By.XPATH, '//a[contains(text(), "New product") or contains(text(), "New Product")]'
    ))).click()

    # Infos produit
    wait.until(EC.visibility_of_element_located((By.NAME, "name"))).send_keys("Chaussures")
    driver.find_element(By.NAME, "sku").send_keys("123456")
    driver.find_element(By.NAME, "price").send_keys("50")
    driver.find_element(By.NAME, "weight").send_keys("3")
    driver.find_element(By.ID, "qty").send_keys("50")

    # Image
   # Cliquer sur l'icône pour ouvrir le sélecteur de fichier
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg.h-5.w-5'))).click()

# Uploader une image depuis le disque
    image_path = os.path.join(
    os.path.expanduser("~"), "Desktop", "TP", "Tp-evershop", "Img_chaussures.webp"
)   
    input_file = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
    input_file.send_keys(image_path)

# Attendre que le fichier soit bien visible ou reconnu par l’interface
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='chaussures']")))



    # SEO
    driver.find_element(By.ID, "urlKey").send_keys("chaussures")
    driver.find_element(By.ID, "metaTitle").send_keys("Chaussures")
    driver.find_element(By.ID, "metaKeywords").send_keys("Chaussures")
    driver.find_element(By.ID, "meta_description").send_keys("Voici des Chaussures Pour Femme")

    # Sauvegarde
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]")))
    driver.execute_script("arguments[0].click();", save_btn)

    # Vérifie s’il y a un message d'erreur
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-red-500"))
        )
        print("❌ Erreur après sauvegarde :", error_msg.text)
        assert False, "Erreur détectée après tentative de sauvegarde"
    except:
        pass

    # Retour à la liste des produits manuellement
    driver.get("http://localhost:3000/admin/products")
    
    # Attendre que le tableau des produits soit visible (important)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

# Cherche tous les liens de nom de produit dans la table
    links = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "table.listing a.font-semibold")))

# Boucle pour trouver le lien dont le texte est "Chaussures"
    for link in links:
        if link.text.strip() == "Chaussures":
            link.click()
        break
    


    # Modifier le produit
    wait.until(EC.visibility_of_element_located((By.NAME, "price"))).clear()
    driver.find_element(By.NAME, "price").send_keys("60")
    driver.find_element(By.ID, "qty").clear()
    driver.find_element(By.ID, "qty").send_keys("70")

    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]")))
    save_btn.click()

    
   # Vérifier mise à jour
    popupresult = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, ".Toastify__toast--success .Toastify__toast-body")))

# vérifier que le texte est correct
    assert "Product saved successfully!" in popupresult.text
    print("✅ Notification affichée correctement")
    
    # Suppression du produit
    driver.get("http://localhost:3000/admin/products")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

    trouvé = False
    produits = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "table.listing tbody tr"))
    )

   

    for tr in produits:
        try:
            # Vérifie si cette ligne contient "Chaussures"
            nom = tr.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
            if nom.text.strip() == "Chaussures":
                # Trouve la checkbox dans la première colonne
                checkbox = tr.find_element(By.CSS_SELECTOR, "td:first-child input[type='checkbox']")

                # Clique avec ActionChains (plus robuste)
                ActionChains(driver).move_to_element(checkbox).click().perform()
                trouvé = True
                break
        except Exception as e:
            continue

    assert trouvé, "❌ Produit 'Chaussures' non trouvé pour suppression"
    
     # Bandeau Delete
       # Attente du bandeau avec les actions (Delete, Enable, etc.)
    action_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.inline-flex")))

    # Chercher tous les spans dans ce bandeau
    spans = action_bar.find_elements(By.CSS_SELECTOR, "span")

    delete_cliqué = False
    for span in spans:
        if span.text.strip().lower() == "delete":
            span.click()
            delete_cliqué = True
            break

    assert delete_cliqué, "❌ Bouton 'Delete' non trouvé dans le bandeau d'actions"

    # Attendre la modale de confirmation
# Cliquer sur le bouton Delete dans la modale
    try:
        delete_modal_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button.critical')))
        delete_modal_button.click()
        print("✅ Bouton 'Delete' cliqué dans la modale")

    except TimeoutException:
        raise AssertionError("❌ Bouton 'Delete' de la modale non trouvé ou modale pas fermée")
    
    wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, '.modal')))

    
    # 1. Saisir "Chaussures" dans l'input
    input_recherche = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
    input_recherche.clear()
    input_recherche.send_keys("Chaussures")
    input_recherche.send_keys(Keys.ENTER)
    print("✅ Recherche lancée pour 'Chaussures'")

    # 2. Attendre que la table se recharge (facultatif si animation/ajax)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))

    # 3. Vérifier la première ligne du tableau
    try:
        première_ligne = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))
        texte_ligne = première_ligne.text.lower()
        assert "chaussures" not in texte_ligne, "❌ Le produit 'Chaussures' est encore présent dans le tableau"
        print("✅ Le produit 'Chaussures' n'est plus présent dans la première ligne")
    except TimeoutException:
        print("✅ Aucun résultat affiché après la recherche — le produit a bien été supprimé")