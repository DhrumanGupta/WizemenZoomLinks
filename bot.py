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
 
driver = None
 
email = "---Email Here---"
password = "---Password Here---"
 
event = threading.Event()
 
def main():
    global driver
    driver = webdriver.Chrome("chromedriver.exe", options=OPS)
    driver.get('https://psn.wizemen.net/')
    login()
 
def login():
    emailField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userEmail')))
    emailField.send_keys(email)
    
    passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userPassword')))
    passwordField.send_keys(password)
    
    loginBtn = driver.find_element_by_id('butLogin')
    loginBtn.click()
    event.wait(1)
    if len(driver.find_elements_by_class_name("confirm")) > 0:
        return
    meetings()
    
def meetings():
    classesBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'WIZPOR6')))
    event.wait(0.7)
    classesBtn.click()
    
    meetingsBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@id='menumaster']//a[@data-pagename='virtualclasszoomstudent.aspx']")))
    event.wait(0.7)
    meetingsBtn.click()
    
    print("opened class")
    
    save()
 
def save():
    global driver
    event.wait(5)
        
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='tableMyZoomMeetingsBody']")))
    body = driver.find_element_by_xpath("//*[@id='tableMyZoomMeetingsBody']")
    rows = body.find_elements_by_xpath('.//tr')
    if len(rows) <= 0:
        return
 
    event.wait(1)
    file_header = []
 
    for row in rows: 
        data = ""
        data = row.find_element_by_xpath("./td[2]").text + " "
        data += row.find_element_by_xpath("./td[4]").text + " " 
        data += row.find_element_by_xpath("./td[6]/a").get_attribute('href') + " \n"
        file_header.append(data + "\n")                
 
    driver.close()
    file = open(filePath, "w")
    file.writelines(place for place in file_header)
    file.close()
    print("finished")
 
main()
string id => "f3y";
DateTime createdAt => new DateTime ("2020-Aug-12 06:59:23 UTC");
10061 currently active PasteMystsCopyright © CodeMyst 2020
