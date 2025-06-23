from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# === CONFIG ===

csv_path = "C:\\Users\\AndreiManache\\Desktop\\Saved Data\\Automatizare\\AutomatizarePython\\ids.csv"
promotion_values = ['137']
base_url = 'https://www.autovit.ro/adminpanel/plata-prin-autovit/'
dropdown_selector = '#content > form:nth-child(2) > select'
submit_button_selector = '#content > form:nth-child(2) > input[type=submit]'
error_log_file = "C:\\Users\\AndreiManache\\Desktop\\Saved Data\\Automatizare\\AutomatizarePython\\promotii_esuate.csv"

# === LOAD ADVERT IDS ===

advert_ids = []

with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            advert_ids.append(row[0])

print(f"Loaded {len(advert_ids)} advert IDs.")

# === INIT SELENIUM ===

driver = webdriver.Chrome()
driver.get("https://www.autovit.ro/adminpanel/usercards/")

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
    ).click()
except Exception:
    print("Cookie banner not found or already accepted.")

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainForm > fieldset > div > a"))
).click()

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#input45"))
).send_keys('Divinacomedie3!')

driver.find_element(By.CSS_SELECTOR, "#form37 > div.o-form-button-bar > input").click()

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#form62 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(3) > div.authenticator-description > div.authenticator-button > a"))
).click()

print("🔐 Aștept confirmarea din aplicația Okta (10 secunde)...")
time.sleep(10)

# === APPLY PROMOTIONS ===

total_ads = len(advert_ids)
total_promos = len(promotion_values)
failed_promotions = []

for promo_index, promo_value in enumerate(promotion_values, start=1):
    print(f"\n📢 Aplic opțiunea de promovare {promo_value} ({promo_index}/{total_promos})\n")
    for index, advert_id in enumerate(advert_ids, start=1):
        try:
            driver.get(f'{base_url}{advert_id}')
            
            dropdown = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
            ))
            dropdown.select_by_value(promo_value)
            
            driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
            
            print(f'✅ {advert_id} - opțiunea {promo_value} ({index}/{total_ads})')
        
        except Exception as e:
            print(f'❌ {advert_id} - eroare cu opțiunea {promo_value}: {str(e)}')
            failed_promotions.append(advert_id)

# === SAVE FAILED PROMOTIONS ===

if failed_promotions:
    with open(error_log_file, mode='w', newline='', encoding='utf-8') as errorfile:
        writer = csv.writer(errorfile)
        writer.writerow(["Advert ID", "Promotion Value", "Error"])
        writer.writerows(failed_promotions)
    print(f"\n⚠️ {len(failed_promotions)} anunțuri au eșuat și au fost salvate în {error_log_file}")
else:
    print("\n✅ Toate promovările au fost aplicate cu succes!")

# === DONE ===
driver.quit()
