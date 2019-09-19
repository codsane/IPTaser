from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from loguru import logger
import configparser
import time
import sys
import os

if sys.version_info[0] < 3:
    # Tested with 3.7.4
    raise Exception("Python 3 or higher required")

config = configparser.ConfigParser()
config.read('config.ini')
USERNAME = config['creds']['username']
PASSWORD = config['creds']['password']

logger.add("logs/file_{time}.log")

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)

logger.debug('Attempting to login to IPT...')
driver.get('https://iptorrents.com/login.php')

logger.debug('Waiting for username field to be clickable (cloudflare)...')
# Todo: Handle captcha here if served
username_field = wait.until(EC.element_to_be_clickable(
    (By.CLASS_NAME, 'username')))
username_field.send_keys(USERNAME)

driver.find_element_by_class_name('password').send_keys(PASSWORD)
driver.find_element_by_class_name('button').click()
logger.info('Attempting sign-in...')

logger.debug('Waiting for stats div to be clickable (successful login)')
try:
    banner_field = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "bannerPlaceholder")))
    logger.info('Successfully logged in!')
except Exception as e:
    logger.exception('There was a problem while logging in: ', e)

logger.debug('Moving to zap page (seeding_required.php)')
driver.get('https://iptorrents.com/seeding_required.php')

logger.debug(
    'Waiting for presence of sReq div element (successful page load)...')
# sReq div - https://i.imgur.com/4dcf4JY.png
current_bonus_element = wait.until(EC.element_to_be_clickable(
    (By.ID, 'sReq')))

logger.debug('Successfully loaded seeding_required.php!')

# Collect torrents, then zap
# Todo: Clean this up and properly log each torrent with name
zap_buttons = driver.find_elements_by_xpath('//*[@rel="0"]')
logger.info('Collected {} torrents to zap'.format(str(len(zap_buttons))))
for zap_button in zap_buttons:
    # Todo: Make determination of bonus points vs. upload surplus based on ratio (very late todo, as I don't have many bonus points)
    zap_button.click()
    previous_zap_button = wait.until(EC.invisibility_of_element(zap_button))

    zap_button.parent

logger.info('Finished zapping torrents!')

# Todo: Sent push notifications

driver.quit()
