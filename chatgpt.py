#!/bin/python3

# simple Selenium driver to use the chatgpt site from a command line
# works most of the time, but not always
# alnwlsn 2023

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import textwrap


def word_wrap(text, width=80):
    paragraphs = text.split('\n')
    wrapped_paragraphs = []
    for paragraph in paragraphs:
        wrapped_paragraph = textwrap.fill(paragraph, width=width)
        wrapped_paragraphs.append(wrapped_paragraph)
    wrapped_text = '\n'.join(wrapped_paragraphs)
    return wrapped_text


def get_chats(printing=False):
    global open_chats
    try:
        chat_container = driver.find_element(
            By.XPATH, '//div[contains(@class, "flex-col") and contains(@class, "flex-1") and contains(@class, "transition-opacity") and contains(@class, "duration-500") and contains(@class, "overflow-y-auto")]')
        open_chats = chat_container.find_elements(By.XPATH, './/a')
        if (printing):
            # print("open chats are:")
            for i, a in enumerate(open_chats, start=1):
                text_content = a.text
                print(f'{i} {text_content}')
    except:
        open_chats = None
        print("found no open chats")


def select_chat(chatnumber):
    chatnumber = int(chatnumber)
    if open_chats == None:
        get_chats(True)
        return
    if chatnumber >= 1 and chatnumber <= len(open_chats):
        get_chats()
        selected_item = open_chats[chatnumber - 1]
        textname = selected_item.text
        selected_item.click()
        time.sleep(0.5)
        print("using ", textname)
    else:
        print("no such chat")
        get_chats()
        pass


def del_chat():  # delete current chat
    button = driver.find_elements(
        By.XPATH, '//button[contains(@class, "p-1 hover:text-white")]')[2]  # this is trash can
    button.click()
    time.sleep(1.5)
    button = driver.find_elements(
        By.XPATH, '//button[contains(@class, "p-1 hover:text-white")]')[0]  # this is check box
    button.click()
    print("deleted")


try:
    chrome_options = Options()
    # open chrome with
    # chromium --remote-debugging-port=9222
    chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
    # chrome_options.add_argument('--user-data-dir=~')
    driver = webdriver.Chrome(options=chrome_options)
except:
    print("connection to browser failed")
    quit()

open_chats = None

while True:
    try:
        inputT = input(":")
        if inputT.lower() in ['exit', 'quit', 'stop', 'q', 'x']:
            print("exit")
            quit()

        waited = True
        if inputT.lower() in ['new', 'n']:
            new_chat_link = driver.find_element(
                By.XPATH, "//a[contains(text(), 'New chat')]")
            new_chat_link.click()
            print("new chat")
        elif inputT.lower() in ['old', 'open', 'o']:
            get_chats(True)
        elif inputT.lower() in ['del', 'delete', 'rm']:
            del_chat()
        elif inputT.lower() in ['f']:
            driver.refresh()
        elif all(char.isdigit() for char in inputT):
            select_chat(inputT)
        elif inputT.lower() in ['?', 'h', 'help']:
            print("commands:\n n - new chat\n o - list current chats\n (number of chat) - select existing chat\n r - recall last response\n del - delete current chat\n f - refresh browser\n q - exit\n anything else - send to ChatGPT")
        else:
            waittime = 60
            if inputT.lower() not in ['refresh', 'ref', 'ans', 'a', 'r']:
                textarea = driver.find_element(
                    By.XPATH, '//textarea[contains(@id, "prompt-textarea")]')
                textarea.send_keys(inputT)
                time.sleep(0.5)
                textarea.send_keys(Keys.RETURN)
                #print("-",end='')
            else:
                print("last response:")
                waittime = 3

            wait = WebDriverWait(driver, waittime)
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
                text2 = f'({len(text2)} chars) ' + text2
                text2 = word_wrap(text2, width=80)

                print(text2)
    except Exception as e:
        # print(f"An exception occurred: {e}")
        print("error")
