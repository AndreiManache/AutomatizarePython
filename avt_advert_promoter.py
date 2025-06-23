from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Your advert IDs
advert_ids = []  # Replace with your actual advert IDs

# Open the CSV file and read each row
with open("C:\\Users\\AndreiManache\\Desktop\\Saved Data\\Automatizare\\AutomatizarePython\\ids.csv", newline='') as csvfile:
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

# # Wait for the username field to be present and fill in the credentials
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input45"))).send_keys('Divinacomedie3!')
# driver.find_element(By.CSS_SELECTOR, "#input45").send_keys('Divinacomedie3!')

# Click on the 'Sign In' button
driver.find_element(By.CSS_SELECTOR, "#form37 > div.o-form-button-bar > input").click()

# Wait for and click the 'Get push notification' button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#form62 > div.authenticator-verify-list.authenticator-list > div > div:nth-child(3) > div.authenticator-description > div.authenticator-button > a"))).click()

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
        dropdown.select_by_value('87')  # Use the actual value for the option you wish to select
        
        # Click the submit button
        driver.find_element(By.CSS_SELECTOR, submit_button_selector).click()
        
        print(f'Successfully promoted advert {advert_id} ({index}/{total_ads}, {index/total_ads:.2%} complete)')
        
    except Exception as e:
        print(f'Failed to promote advert {advert_id}: {str(e)}')

# Close the driver
driver.quit()
