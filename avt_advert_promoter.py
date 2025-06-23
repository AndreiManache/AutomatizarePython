from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import sys

# === CONFIG ===
retry_only = '--retry-only' in sys.argv
csv_path = "C:\\Users\\AndreiManache\\Desktop\\Saved Data\\Automatizare\\AutomatizarePython\\ids.csv"
promotion_values = ['145']
base_url = 'https://www.autovit.ro/adminpanel/plata-prin-autovit/'
dropdown_selector = '#content > form:nth-child(2) > select'
submit_button_selector = '#content > form:nth-child(2) > input[type=submit]'
error_log_file = "C:\\Users\\AndreiManache\\Desktop\\Saved Data\\Automatizare\\AutomatizarePython\\promotii_esuate.csv"
retry_log_file = error_log_file.replace(".csv", "_final.csv")

# === LOAD IDS ===
advert_ids = []

if retry_only:
    if os.path.exists(error_log_file):
        with open(error_log_file, newline='', encoding='utf-8') as retryfile:
            reader = csv.reader(retryfile)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    advert_ids.append((row[0].strip(), row[1].strip()))
        if advert_ids:
            print(f"🔁 Loaded {len(advert_ids)} failed promotions for retry.")
        else:
            print("⚠️ Fișierul de retry este gol.")
            sys.exit()
    else:
        print("⚠️ Fișierul cu promovări eșuate nu există.")
        sys.exit()
else:
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                advert_ids.append(row[0].strip())
    print(f"📄 Loaded {len(advert_ids)} advert IDs.")

# === INIT SELENIUM ===
driver = webdriver.Chrome()
driver.get("https://www.autovit.ro/adminpanel/usercards/")

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
    ).click()
except:
    pass  # Cookie banner not found

# Login
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

print("🔐 Aștept confirmarea din aplicația Okta (10 sec)...")
time.sleep(10)

# === APPLY PROMOTIONS ===
if not retry_only:
    failed_promotions = []

    for promo_value in promotion_values:
        print(f"\n📢 Aplic opțiunea {promo_value}\n")
        for i, advert_id in enumerate(advert_ids, 1):
            try:
                driver.get(f"{base_url}{advert_id}")
                dropdown = Select(WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
                ))
                dropdown.select_by_value(promo_value)
                driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
                print(f"✅ {advert_id} - {promo_value} ({i}/{len(advert_ids)})")
            except Exception as e:
                print(f"❌ {advert_id} - {promo_value} — Eroare: {str(e)}")
                failed_promotions.append((advert_id, promo_value))

    if failed_promotions:
        with open(error_log_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Advert ID", "Promotion Value"])
            writer.writerows(failed_promotions)
        print(f"\n⚠️ {len(failed_promotions)} promovări eșuate — salvate în {error_log_file}")
    else:
        print("\n✅ Toate promovările au fost aplicate cu succes!")



# === RETRY MODE ===
if retry_only:
    retry_failures = []

    retry_ids = []
    with open(error_log_file, newline='', encoding='utf-8') as retryfile:
        reader = csv.reader(retryfile)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 2:
                retry_ids.append((row[0].strip(), row[1].strip()))

    if not retry_ids:
        print("⚠️ Fișierul de retry este gol.")
        sys.exit()

    print(f"\n🔁 Încep retry automat pentru {len(retry_ids)} promovări eșuate...\n")
    for advert_id, promo_value in retry_ids:
        try:
            driver.get(f'{base_url}{advert_id}')
            dropdown = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
            ))
            dropdown.select_by_value(promo_value)
            driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
            print(f'🔁 ✅ Retry OK: {advert_id} - {promo_value}')
        except Exception as e:
            print(f'🔁 ❌ Retry FAIL: {advert_id} - {promo_value} — {str(e)}')
            retry_failures.append((advert_id, promo_value))

    if retry_failures:
        with open(retry_log_file, mode='w', newline='', encoding='utf-8') as retryfile_out:
            writer = csv.writer(retryfile_out)
            writer.writerow(["Advert ID", "Promotion Value"])
            writer.writerows(retry_failures)
        print(f"\n⚠️ {len(retry_failures)} promovări tot NU au reușit — salvate în {retry_log_file}")
    else:
        print("\n✅ Toate promovările au mers cu succes la retry.")


# === DONE ===
driver.quit()
