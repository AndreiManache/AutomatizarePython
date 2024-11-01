from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv

# Your advert IDs
advert_ids = []  # Replace with your actual advert IDs

# Open the CSV file and read each row
with open("ids.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Assuming the ad ID is in the first column
        advert_id = row[0]
        advert_ids.append(advert_id)

# Now advert_ids contains all the ad IDs from the CSV file
print(advert_ids)

# URL and selectors (Replace with actual values)
base_url = 'https://www.autovit.ro/adminpanel/plata-prin-autovit/'
dropdown_selector = '#content > form:nth-child(2) > select'
submit_button_selector = '#content > form:nth-child(2) > input[type=submit]'

# Initialize WebDriver for Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Navigate to the admin panel login page
driver.get("https://www.autovit.ro/adminpanel/usercards/")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

# Handle the cookie consent banner first
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
    print("Cookie consent accepted")
except Exception as e:
    print("Cookie banner not found or already accepted.")

# Wait for the overlay to disappear
try:
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".onetrust-pc-dark-filter")))
    print("Overlay disappeared")
except Exception as e:
    print("Overlay not found or failed to disappear.")

# Now, try to click the Okta login button
try:
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".block > a:nth-child(1)")))
    driver.execute_script("arguments[0].click();", login_button)
    print("Okta login button clicked")
except Exception as e:
    print(f"Failed to click Okta login button: {str(e)}")


# Enter password and click 'Sign In' button
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input44")))
password_field.send_keys('Divinacomedie2!')
driver.find_element(By.CSS_SELECTOR, "#form36 > div.o-form-button-bar > input").click()

# Wait for 10 seconds to manually accept the push notification
time.sleep(10)

# Iterate through adverts
total_ads = len(advert_ids)
for index, advert_id in enumerate(advert_ids, start=1):
    try:
        # Navigate to the advert's promotion page
        driver.get(f'{base_url}{advert_id}')
        # Select the promotion from the dropdown
        dropdown = Select(driver.find_element(By.CSS_SELECTOR, dropdown_selector))
        dropdown.select_by_value('49') # Use the actual value for the option you wish to select
        # Click the submit button
        driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
        print(f'Successfully promoted advert {advert_id} ({index}/{total_ads}, {index/total_ads:.2%} complete)')
    except Exception as e:
        print(f'Failed to promote advert {advert_id}: {str(e)}')

# Close the driver
driver.quit()
