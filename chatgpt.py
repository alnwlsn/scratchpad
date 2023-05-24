#!/bin/python3

#simple Selenium driver to use the chatgpt site from a command line
#alnwlsn 2023

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

chrome_options = Options()
#open chrome with
#chromium --remote-debugging-port=9222
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
# chrome_options.add_argument('--user-data-dir=~')
driver = webdriver.Chrome(options=chrome_options)

while True:
    inputT = input(">")
    if inputT.lower() in ['exit', 'quit', 'stop', 'q', 'x']:
        quit()

    waited = True
    if inputT.lower() in ['new', 'n']:
        new_chat_link = driver.find_element(
            By.XPATH, "//a[contains(text(), 'New chat')]")
        new_chat_link.click()
    else:
        if inputT.lower() not in ['refresh', 'ref', 'ans', 'a', 'r']:
            textarea = driver.find_element(
                By.XPATH, '//textarea[contains(@id, "prompt-textarea")]')
            textarea.send_keys(inputT)
            time.sleep(0.5)
            textarea.send_keys(Keys.RETURN)
            print("thinking...")
        else:
            print("last response:")

        wait = WebDriverWait(driver, 60)
        try:
            div_element = wait.until(expected_conditions.visibility_of_element_located(
                (By.XPATH, '//div[text()="Regenerate response"]')))
            # print("done")
        except:
            print("timed out waiting for response")
            waited = False
        if (waited):
            # get chat container div
            parent_div = driver.find_element(
                By.XPATH, './/div[contains(@class, "flex flex-col text-sm dark:bg-gray-800")]')
            # then the last block in there (contains the response)
            response_div = parent_div.find_elements(By.XPATH, "./div")[-2]

            # html = response_div.get_attribute('innerHTML')
            text = response_div.text

            # make sure response has only ascii characters
            text2 = ""
            for char in text:
                if ord(char) < 128:  # Check if character is within ASCII range
                    text2 += char
                else:
                    text2 += '?'
            text2 = text2.expandtabs(4)

            print(f'({len(text2)} chars) {text2}')
