from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from . import models
from brandon_slack import celery
from brandon_slack.settings import DRIVER_LOCATION, URL_CREATE, TIME_WAIT, TIME_MAX_WAIT_FOR_BROWSER, TIME_DELTA

import time


@celery.app.task
def create_workspace(email):

    def submit_code(code):
        input_fields = browser.find_elements_by_class_name('inline_input')
        for input_field, digit in zip(input_fields, code):
            input_field.clear()
            input_field.send_keys(digit)

    def chase_code(email):
        t = 0
        while t < TIME_MAX_WAIT_FOR_BROWSER:
            record = models.Email.objects.get(email=email)
            time.sleep(TIME_DELTA)
            t += TIME_DELTA
            if record.code:
                return record.code
        return ''

    browser = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    browser.get(URL_CREATE)
    try:
        sign_up_id = 'signup_email'
        email_input = WebDriverWait(browser, TIME_WAIT).until(expected_conditions
                                                              .presence_of_element_located((By.ID, sign_up_id)))
        email_input.clear()
        email_input.send_keys(email)
        submit_button = WebDriverWait(browser, TIME_WAIT).until(
            expected_conditions.element_to_be_clickable((By.ID, 'submit_btn')))
        submit_button.click()
        WebDriverWait(browser, TIME_WAIT).until(expected_conditions
                                                .presence_of_all_elements_located(
            (By.CLASS_NAME, 'inline_input')))

        code = chase_code(email)
        # code = str(random.randint(0, 999999))
        submit_code(code)
        input_company_name = WebDriverWait(browser, TIME_WAIT).until(expected_conditions
                                                                     .presence_of_element_located(
            (By.ID, 'signup_team_name')))

        input_company_name.clear()
        input_company_name.send_keys('')  # TODO add company name
        submit_button = WebDriverWait(browser, TIME_WAIT).until(
            expected_conditions.element_to_be_clickable((By.ID, 'submit_btn')))
        submit_button.click()
        input_project_name = WebDriverWait(browser, TIME_WAIT).until(expected_conditions
                                                                     .presence_of_element_located(
            (By.ID, 'channel_name')))
        input_project_name.clear()
        input_project_name.send_keys('')  # TODO project name. Max is 21 characters!
        submit_button = WebDriverWait(browser, TIME_WAIT).until(
            expected_conditions.element_to_be_clickable((By.ID, 'submit_btn')))
        submit_button.click()

    except TimeoutException as error:
        models.Email.objects.get(email=email).unused = True
        browser.close()

