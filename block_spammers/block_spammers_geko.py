from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv

# Your user IDs
user_ids = []  # Replace with your actual user IDs

# Open the CSV file and read each row
with open("C:\\Users\\AndreiManache\\Desktop\\Automatizare\\Automatizare Python\\user_ids.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Assuming the user ID is in the first column
        user_id = row[0]
        user_ids.append(user_id)

# Now user_ids contains all the user IDs from the CSV file
print(user_ids)

# URL template for Salesforce link (replace with user ID)
base_url = 'https://www.autovit.ro/adminpanel/salesforce/'
dropdown_selector = "#commentsText"  # Adjust as needed
submit_button_selector = "#userCommentBtn"
spam_button_selector = "#spamuser"

# Initialize WebDriver for Firefox using GeckoDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Navigate to the admin panel login page
driver.get("https://www.autovit.ro/adminpanel/usercards/")

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
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".block > a:nth-child(1)"))).click()
    print("Okta login button clicked")
except Exception as e:
    print(f"Failed to click Okta login button: {str(e)}")

# Navigate to the admin panel login page
driver.get("https://www.autovit.ro/adminpanel/usercards/")

# Wait for the cookie consent banner and accept if it’s present
try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))).click()
except Exception as e:
    print("Cookie banner not found or already accepted.")

# Wait and click the Okta login button
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainForm > fieldset > div > a"))).click()

password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#input44")))
password_field.send_keys('Divinacomedie2!') 

# Click on the 'Sign In' button
driver.find_element(By.CSS_SELECTOR, "#form36 > div.o-form-button-bar > input").click()

# Wait for 5 seconds to load
time.sleep(5)

total_users = len(user_ids)

# Iterate through the list of user IDs
for index, user_id in enumerate(user_ids, start=1):
    try:
        # Navigate to the Salesforce page for the current user
        driver.get(f'{base_url}{user_id}')

        # Step 1: Write "Spammer" in the #commentsText element
        comment_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, dropdown_selector)))
        comment_box.send_keys("Spammer")
        
        # Step 2: Click the #userCommentBtn to submit the comment
        submit_comment_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector)))
        submit_comment_button.click()

        # Step 3: Click the #spamuser button to mark as spam
        spam_user_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, spam_button_selector)))
        spam_user_button.click()

         # Step 4: Handle the pop-up alert and accept it
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        print(f'Successfully marked user {user_id} as spam ({index}/{total_users}, {index/total_users:.2%} complete)')
        time.sleep(1)
    except Exception as e:
        print(f'Failed to perform actions for user {user_id}: {str(e)}')

# Close the driver
driver.quit()
