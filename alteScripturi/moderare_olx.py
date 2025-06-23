from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Your advert IDs
advert_ids = []

# Open the CSV file and read each row
with open("ids.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Assuming the ad ID is in the first column
        advert_id = row[0]
        advert_ids.append(advert_id)

# Now advert_ids contains all the ad IDs from the CSV file
print(advert_ids)

# URL components
base_url = 'https://www.olx.ro/adminpanel/ajax/moderation/remove/?adID='
ban_reason_id = '30'  # Assuming '30' is the correct ban reason ID for "continut duplicat"
hash_value = '1730381322315'  # Replace with the correct hash value if it changes

# Initialize WebDriver
driver = webdriver.Chrome()

# Navigate to the admin panel login page
driver.get("https://www.olx.ro/adminpanel/usercards/")

# Wait for the cookie consent banner and accept if it’s present
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
except Exception as e:
    print("Cookie banner not found or already accepted.")

# Wait and click the Okta login button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.illustration > div > div > div > div.top > a"))).click()

# Wait for the username field to be present and fill in the credentials
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input28"))).send_keys('andrei.manache@olx.ro')
driver.find_element(By.CSS_SELECTOR, "#input36").send_keys('Divinacomedie2!')

# Click on the 'Sign In' button
driver.find_element(By.CSS_SELECTOR, "#form20 > div.o-form-button-bar > input").click()

# Wait for and click the 'Get push notification' button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form60 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(2) > div.authenticator-description > div.authenticator-button > a"))).click()

# Wait for 10 seconds to manually accept the push notification
time.sleep(10)

total_ads = len(advert_ids)

# Iterate through adverts and ban each one
for index, advert_id in enumerate(advert_ids, start=1):
    try:
        # Construct the URL for the specific advert ban action
        ban_url = f'{base_url}{advert_id}&banID={ban_reason_id}&hash={hash_value}'
        
        # Visit the ban URL to execute the ban action
        driver.get(ban_url)

        print(f'Successfully banned advert {advert_id} ({index}/{total_ads}, {index/total_ads:.2%} complete)')
        time.sleep(1)  # Optional: wait briefly to avoid overwhelming the server
    except Exception as e:
        print(f'Failed to ban advert {advert_id}: {str(e)}')

# Close the driver
driver.quit()
