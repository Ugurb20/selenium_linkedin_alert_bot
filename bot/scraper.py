import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.common.exceptions import StaleElementReferenceException
from bot.email import EmailSender
from bot.constants import *
from selenium.webdriver.chrome.options import Options


class Booking(webdriver.Chrome):
    def __init__(self,
                 teardown=False):
        self.teardown = teardown
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        super(Booking, self).__init__(options=chrome_options)
    """
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            print("Quitting firefox...")
            self.quit()"""

    def land_first_page(self):
        self.implicitly_wait(5)
        self.get("https://www.linkedin.com/home")
        self.set_window_size(1920, 1080)
    
    def login(self):
        username = self.find_element(By.ID, "session_key" )
        username.send_keys(LINKEDIN_MAIL)

        password = self.find_element(By.ID, "session_password")
        password.send_keys(LINKEDIN_PASS)

        button =self.find_element(By.CLASS_NAME,"sign-in-form__submit-btn--full-width")
        button.click()

    def search(self):

        def search_btn():
            elements = self.find_elements(By.CSS_SELECTOR, '[data-control-name="filter_show_results"]')
            for i in range(len(elements)):
                try:
                    element = self.find_elements(By.CSS_SELECTOR, '[data-control-name="filter_show_results"]')[i]      
                    element.click()
                    break
                except :
                    print(i)

        wait = WebDriverWait(self, 20)
        search_bar =wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))

        search_bar.send_keys("software engineer")
        search_bar.send_keys(Keys.ENTER) 
        expand_btn = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'See all job results in')))
        expand_btn.click()

        location_bar = self.find_element(By.XPATH,'//*[contains(@id, "jobs-search-box-location-id")]')
        location_bar.send_keys(" Istanbul",Keys.ENTER)
        
        time.sleep(2)
        date_posted = self.find_element(By.XPATH,'//button[text()="Date posted"]')
        date_posted.click()

        checkbox = self.find_elements(By.CSS_SELECTOR,'input[name="date-posted-filter-value"]')[2]
        self.execute_script("arguments[0].click();", checkbox)

        search_btn()

        time.sleep(2)
        experience = self.find_element(By.XPATH,'//button[text()="Experience level"]')
        experience.click()

        checkboxe = self.find_elements(By.CSS_SELECTOR,'input[name="experience-level-filter-value"]')[0]
        self.execute_script("arguments[0].click();", checkboxe)

        checkboxe1 = self.find_elements(By.CSS_SELECTOR,'input[name="experience-level-filter-value"]')[1]
        self.execute_script("arguments[0].click();", checkboxe1)
        search_btn()
        time.sleep(2)

    
    def scrap_jobs(self):
        jobs = self.find_elements(By.CLASS_NAME, "job-card-container")
        job_links = self.find_elements(By.CLASS_NAME, "job-card-list__title")
        links = []
        names = []
        for j in range(len(jobs)):
            names.append(job_links[j].text)
            links.append(job_links[j].get_attribute("href"))
        email_sender = EmailSender(E_MAIL_SENDER, E_MAIL_SENDER_PASS)
        email_sender.create_html(list=links,list_names=names)
        email_sender.send_email(E_MAIL_RECIEVER,"daily linkedin")
                
 
        
        


        