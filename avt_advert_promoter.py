from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from typing import List, Optional


def load_values(path: str) -> Optional[List[str]]:
    """Return a list of values read from a CSV file or ``None`` if missing."""
    try:
        with open(path, newline="") as csv_file:
            reader = csv.reader(csv_file)
            return [row[0].strip() for row in reader if row]
    except FileNotFoundError:
        return None

# List of promotion codes, loaded from ``promotions.csv`` if present.
promotion_values = load_values("promotions.csv") or ["49"]

# Your advert IDs loaded from ``ids.csv``. Fallback to a Windows-specific path
# if the file is not found in the current directory.
advert_ids = load_values("ids.csv")
if advert_ids is None:
    advert_ids = load_values(r"D:\\Proiecte\\Automatizari\\Automatizare Python\\ids.csv") or []

# Now advert_ids contains all the ad IDs from the CSV file
print(advert_ids)

# URL and selectors (Replace with actual values)
base_url = 'https://www.autovit.ro/adminpanel/plata-prin-autovit/'
dropdown_selector = '#content > form:nth-child(2) > select'
submit_button_selector = '#content > form:nth-child(2) > input[type=submit]'

# Initialize WebDriver
driver = webdriver.Chrome()

# Navigate to the admin panel login page
driver.get("https://www.autovit.ro/adminpanel/usercards/")

# Wait for the cookie consent banner and accept if it’s present
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
except Exception as e:
    print("Cookie banner not found or already accepted.")

# Wait and click the Okta login button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainForm > fieldset > div > a"))).click()

# Wait for the username field to be present and fill in the credentials
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input43"))).send_keys('andrei.manache@olx.ro')
driver.find_element(By.CSS_SELECTOR, "#input51").send_keys('Divinacomedie2!')

# Click on the 'Sign In' button
driver.find_element(By.CSS_SELECTOR, "#form35 > div.o-form-button-bar > input").click()

# Wait for and click the 'Get push notification' button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form75 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(2) > div.authenticator-description > div.authenticator-button > a"))).click()

# Wait for 20 seconds to manually accept the push notification
time.sleep(10)

total_ads = len(advert_ids)

# Iterate through adverts
for index, advert_id in enumerate(advert_ids, start=1):
    try:
        for promo in promotion_values:
            # Navigate to the advert's promotion page for each promotion
            driver.get(f"{base_url}{advert_id}")

            # Select the promotion from the dropdown
            dropdown = Select(driver.find_element(By.CSS_SELECTOR, dropdown_selector))
            dropdown.select_by_value(promo)

            # Click the submit button
            driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()

            # Small pause between promotions
            time.sleep(1)

        print(
            f"Successfully promoted advert {advert_id} ({index}/{total_ads}, {index/total_ads:.2%} complete)"
        )

    except Exception as e:
        print(f"Failed to promote advert {advert_id}: {str(e)}")

# Close the driver
driver.quit()
