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
base_url = 'https://www.olx.ro/adminpanel/payment/'
dropdown_selector = '#content > form:nth-child(2) > select'
submit_button_selector = '#content > form:nth-child(2) > input[type=submit]'

# Initialize WebDriver for Firefox using GeckoDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Navigate to the admin panel login page
driver.get("https://www.olx.ro/adminpanel/usercards/")

# Wait for the cookie consent banner and accept if it’s present
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
    print("Cookie consent accepted")
except Exception as e:
    print("Cookie banner not found or already accepted.")

# Wait for the overlay to disappear after accepting the cookie banner
try:
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".onetrust-pc-dark-filter")))
    print("Overlay disappeared")
except Exception as e:
    print("Overlay not found or failed to disappear.")

# Wait and click the Okta login button
try:
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.illustration > div > div > div > div.top > a"))).click()
    print("Okta login button clicked")
except Exception as e:
    print(f"Failed to click Okta login button: {str(e)}")

# Wait for the username field to be present and fill in the credentials
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input28"))).send_keys('andrei.manache@olx.ro')
driver.find_element(By.CSS_SELECTOR, "#input36").send_keys('Divinacomedie2!')

# Click on the 'Sign In' button
driver.find_element(By.CSS_SELECTOR, "#form20 > div.o-form-button-bar > input").click()

# Wait for and click the 'Get push notification' button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form60 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(2) > div.authenticator-description > div.authenticator-button > a"))).click()

# Wait for 20 seconds to manually accept the push notification
time.sleep(10)

total_ads = len(advert_ids)

# Iterate through adverts
for index, advert_id in enumerate(advert_ids, start=1):
    try:
        # Navigate to the advert's promotion page
        driver.get(f'{base_url}{advert_id}')
        
        # Select the promotion from the dropdown
        dropdown = Select(driver.find_element(By.CSS_SELECTOR, dropdown_selector))
        dropdown.select_by_value('269')  # Use the actual value for the option you wish to select
        # Value pt Pro 271, Value pt Standard 269
        # Click the submit button
        driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
        
        
        print(f'Successfully promoted advert {advert_id} ({index}/{total_ads}, {index/total_ads:.2%} complete)')
        time.sleep(1)
    except Exception as e:
        print(f'Failed to promote advert {advert_id}: {str(e)}')

# Close the driver
driver.quit()
