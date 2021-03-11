""" Made by Dhruman Gupta """

import sys
import base64
import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import threading

filePath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads') + "\\meetings.txt"

event = threading.Event()


def init():
    OPS = webdriver.ChromeOptions()
    OPS.add_experimental_option("excludeSwitches", ["enable-automation"])
    OPS.add_experimental_option('useAutomationExtension', False)
    OPS.add_argument("headless")

    driver = webdriver.Chrome('./drivers/chromedriver.exe', options=OPS)
    driver.get('https://psn.wizemen.net/')
    login(driver)


def login(driver):
    file = open("credentials.txt", "r")
    email = decodeBase64(file.readline())
    password = decodeBase64(file.readline())
    file.close()

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
        print("incorrect password! Please fill in your credentials using 'setup'. For more information, use 'help'")
        driver.close()
        return

    print("logged in!")
    meetings(driver)

def meetings(driver):
    classesBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'WIZPOR6')))
    event.wait(0.4)
    classesBtn.click()

    meetingsBtn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[13]/aside/section/div[3]/ul[1]/li[2]/a")))
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
        data = row.find_element_by_xpath("./td[1]").text + " "
        data += row.find_element_by_xpath("./td[2]").text + " "
        data += row.find_element_by_xpath("./td[4]").text + " "
        data += "\n" + row.find_element_by_xpath("./td[7]/a").get_attribute('href')
        file_header.append(data + "\n\n")

    driver.close()
    file = open(filePath, "w")
    file.writelines(place for place in file_header)
    file.close()
    print("finished, please check: " + filePath)
    print("You may close this now")


def printCommands():
    com = "'run' : start the software. \n *note, that you need to setup using 'setup' and save your password in a " \
          "file\n\n'setup' : go through the setup process to save your password an email in a file\n(they are " \
          "converted to base64. Not very secure, but cmon its a wizemen password "
    print(com)


def setup():
    email = input("Wizemen email: ").lower()
    print(f"Email recieved: \"{email}\" , do you wish to proceed?")
    confirmed = input("[y/n]: ").lower() == 'y'
    while not confirmed:
        email = input("Wizemen email: ").lower()
        print(f"Email recieved: \"{email}\" , do you wish to proceed?")
        confirmed = input("[y/n]: ").lower() == 'y'

    confirmed = False

    password = input("Wizemen password: ")
    print(f"Password recieved: \"{password}\" , do you wish to proceed?")
    confirmed = input("[y/n]: ").lower() == 'y'
    while not confirmed:
        password = input("Wizemen password: ")
        print(f"Password recieved: \"{password}\" , do you wish to proceed?")
        confirmed = input("[y/n]: ").lower() == 'y'

    encodedEmail = encodeBase64(email)
    encodedPassword = encodeBase64(password)

    file = open("credentials.txt", "a")
    file.write(encodedEmail)
    file.write("\n")
    file.write(encodedPassword)
    file.close()

    print("Data saved successfully! Run again with the 'run' command to use the bot")


def encodeBase64(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decodeBase64(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


commands = {
    "run": init,
    "start": init,
    "help": printCommands,
    "setup": setup
}

if len(sys.argv) == 1:
    printCommands()
    exit(0)

if commands.__contains__(sys.argv[1].lower()):
    commands[sys.argv[1].lower()]()
