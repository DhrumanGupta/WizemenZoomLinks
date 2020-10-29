""" Made by Dhruman Gupta """

import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import threading


filePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads') + "\\meetings.txt"

OPS = webdriver.ChromeOptions()
OPS.add_experimental_option("excludeSwitches", ["enable-automation"])
OPS.add_experimental_option('useAutomationExtension', False)
OPS.add_argument("headless")

email = "email"
password = "password"

event = threading.Event()

def main():
    driver = webdriver.Chrome('./driver/chromedriver.exe', options=OPS)
    driver.get('https://psn.wizemen.net/')
    login(driver)

def login(driver):
    emailField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userEmail'))) 
    emailField.send_keys(email)

    passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userPassword')))
    passwordField.send_keys(password)
    
    if len(driver.find_elements_by_class_name("confirm")) > 0:
        driver.find_element_by_class_name("confirm").click()
    
    loginBtn = driver.find_element_by_id('butLogin')
    loginBtn.click()
    event.wait(0.75)
    if len(driver.find_elements_by_class_name("confirm")) > 0:
        print("incorrect password! Please fill in your credentials in drivers/credentails.txt")
        print("You may close this now")
        driver.close()
        return
    print("logged in!")
    meetings(driver)
    
def meetings(driver):
    classesBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'WIZPOR6')))
    event.wait(0.4)
    classesBtn.click()
    
    meetingsBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[13]/aside/section/div[3]/ul[1]/li[2]/a")))
    event.wait(0.4)
    meetingsBtn.click()
    
    print("opened classes")
    
    save(driver)

def save(driver):
    event.wait(5)
        
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='tableMyZoomMeetingsBody']")))
    body = driver.find_element_by_xpath("//*[@id='tableMyZoomMeetingsBody']")
    rows = body.find_elements_by_xpath('.//tr')
    if len(rows) <= 0:
        print("no meetings scheduled!")
        print("You may close this now")
        driver.close()
        return

    event.wait(0.5)
    file_header = []

    for row in rows: 
        data = ""
        data = row.find_element_by_xpath("./td[2]").text + " "
        data += row.find_element_by_xpath("./td[4]").text + " " 
        data += "\n" + row.find_element_by_xpath("./td[6]/a").get_attribute('href')
        file_header.append(data + "\n\n")                

    driver.close()
    file = open(filePath, "w")
    file.writelines(place for place in file_header)
    file.close()
    print("finished, please check: " + filePath)
    print("You may close this now")

main()
   