# Golf Simulator Bot, can autoreserve placement if given credentials.

import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from webdriver_manager.chrome import ChromeDriverManager

# If given, fill in username and password below.
# They will be prompted for otherwise
username = ""
password = ""

# Time slot desired, have set to what you want
time = "6:30 AM - 7:30 AM"

# login information if not static
if username == '' or password == '':
    print("Give username: ", end="")
    username = input()
    password = getpass.getpass("Enter password: ")

# connect to the browser
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get("https://recconnect.bc.edu/Program/GetProgramDetails?courseId=016a41e4-9e9b-48d7-8b5f-7aa13ef87108&semesterId=a62db87d-8b20-482e-97ee-58f0f161a54f")

# signing into the account
browser.find_element(By.ID, "loginLink").click()
# Need to wait for login window to load, will throw error otherwise
element = WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-user-account")))
element.send_keys(username)
browser.find_element(By.ID, "btnNextSignInFirst").click()
e = WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.ID, "txtSignInPassword")))
e.send_keys(password)
browser.find_element(By.ID, "btnSignIn").click()

# Cookies
browser.get("https://recconnect.bc.edu/Program/GetProgramDetails?courseId=016a41e4-9e9b-48d7-8b5f-7aa13ef87108&semesterId=a62db87d-8b20-482e-97ee-58f0f161a54f")
browser.find_element(By.ID, "gdpr-cookie-accept").click()

# start registration
timeSlots = browser.find_elements(By.CLASS_NAME, "program-schedule-card")
foundSlot = False
for card in timeSlots:
    # test for the time slot and if it is open
    # 0 is time, 1 is availability
    text = card.find_elements(By.CLASS_NAME, "card-text")
    if text[0].text == time and text[1].text != "No Spots Available":
        card.find_element(By.CLASS_NAME, "btn").click()
        foundSlot = True
        break
if not foundSlot: # If not slots available
    print("No slots available")
    sys.exit()
else: # Go through checkout portal
    browser.refresh()
    button = WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, "justify-content-end")))
    button = button.find_element(By.CLASS_NAME, "btn-primary")
    button.click()
    browser.find_element(By.ID, "checkoutButton").click()
    fButton = browser.find_element(By.ID, "CheckoutModal")
    fButton = fButton.find_element(By.CLASS_NAME, "modal-footer")
    fButton = fButton.find_element(By.CLASS_NAME, "btn-primary")
    fButton.click()