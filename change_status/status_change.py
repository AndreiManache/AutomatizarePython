from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Specify the user ID and desired status for this run
user_id = "2599831"  # Replace with the actual user ID
desired_status = "active"  # Change to "active" or "removed_by_user"

# Load ad IDs from CSV
advert_ids = []
with open("ids.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        advert_id = row[0]
        advert_ids.append(advert_id)

# URL and Selectors
base_url = 'https://www.autovit.ro/adminpanel/salesforce'
general_area_selector = "#adsDIV > table > tbody > tr > td:nth-child(2) > form > div"
status_dropdown_selector = 'select.adStatus'  # Replace with the actual selector if different
save_button_selector = 'button.changeAd'  # Replace with the actual selector if different

# Initialize WebDriver
driver = webdriver.Chrome()

# Log in to the admin panel
driver.get("https://www.autovit.ro/adminpanel/usercards/")
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
except:
    print("Cookie banner not found or already accepted.")

# Click Okta login button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainForm > fieldset > div > a"))).click()

# Enter credentials and sign in
password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input44")))
password_field.send_keys('Divinacomedie2!')
driver.find_element(By.CSS_SELECTOR, "#form36 > div.o-form-button-bar > input").click()

# Wait for the dashboard to load
time.sleep(5)

def update_status(advert_ids, user_id, status_value):
    for index, advert_id in enumerate(advert_ids, start=1):
        try:
            # Construct the URL with user ID and ad ID
            ad_url = f'{base_url}/{user_id}/{advert_id}'
            
            # Navigate to each ad's page
            driver.get(ad_url)

            if desired_status == "active":
                additional_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#userTabs > li:nth-child(4) > a")))
                additional_click.click()
                time.sleep(2)
            
            # Click on the general area to reveal elements
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, general_area_selector))).click()
            
            # Select the ad status
            dropdown = Select(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, status_dropdown_selector))))
            dropdown.select_by_value(status_value)
            
            # Click save button
            save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, save_button_selector)))
            save_button.click()
            time.sleep(1)
            
            print(f'Successfully updated status for advert {advert_id} ({index}/{len(advert_ids)}, {index/len(advert_ids):.2%} complete)')
            time.sleep(1)  # Brief pause to avoid overwhelming the server
        except Exception as e:
            print(f'Failed to update status for advert {advert_id}: {str(e)}')

# Run the update function with the specified status
update_status(advert_ids, user_id, desired_status)

# Close the driver
driver.quit()
