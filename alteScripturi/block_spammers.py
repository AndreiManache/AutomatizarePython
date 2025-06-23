from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Your user IDs
user_ids = []  # Replace with your actual user IDs

# Open the CSV file and read each row
with open("D:\\Proiecte\\Automatizari\\Automatizare Python\\user_ids.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Assuming the user ID is in the first column
        user_id = row[0]
        user_ids.append(user_id)

# Now user_ids contains all the user IDs from the CSV file
print(user_ids)

# URL template for Salesforce link (replace with user ID)
base_url = 'https://www.autovit.ro/adminpanel/salesforce/'

# Initialize WebDriver
driver = webdriver.Chrome()

# Login URL for the admin panel
login_url = "https://www.autovit.ro/adminpanel/usercards/"

# Navigate to the admin panel login page
driver.get(login_url)

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

total_users = len(user_ids)

# Iterate through the list of user IDs
for index, user_id in enumerate(user_ids, start=1):
    try:
        # Navigate to the Salesforce page for the current user
        driver.get(f'{base_url}{user_id}')

        # Step 1: Write "Spammer" in the #commentsText element
        comment_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#commentsText")))
        comment_box.send_keys("Spammer")
        
        # Step 2: Click the #userCommentBtn to submit the comment
        submit_comment_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#userCommentBtn")))
        submit_comment_button.click()

        # Step 3: Click the #spamuser button to mark as spam
        spam_user_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#spamuser")))
        spam_user_button.click()

         # Step 4: Handle the pop-up alert and accept it
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Small delay to ensure page loads properly after the action
        time.sleep(3)

        print(f'Actions completed for user {user_id} ({index}/{total_users}, {index/total_users:.2%} complete)')
    
    except Exception as e:
        print(f'Failed to perform actions for user {user_id}: {str(e)}')


# Close the driver
driver.quit()