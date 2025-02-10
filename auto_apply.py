#!/usr/bin/env python3
# coding: utf-8

""" TO DO: """
"""
- Display the job title and any key words and skills used in the description
  when actually applying for a job. 
  --- Add a confirm_override so a user can set if they want to confirm each 
      job to apply to or auto_apply to them all.

- Keep a count of every skill match to see in the end which jobs were the best 
  matches (according to LinkedIn).

- Limit to 20-25 jobs to apply to? I am not sure how long this will take to run at the moment.
  Some searches might even result in less than that so it may be good. 

- When applying 
"""

import pandas as pd
import regex
import time
import json
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from pathlib import Path
from pick import pick # module for the console menuing - https://github.com/aisk/pick

def main():
   
    json_path = Path("./applied_to.json")
    json_path.parent.mkdir(exist_ok=True, parents=True)
    json_path.write_text("some text")
    
    create_file_if_not_exists(json_path)

    jobs_applied_to = load_applied_jobs(json_path)

    DRIVER_PATH = r"C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
    website = """https://www.linkedin.com/jobs/search/
                ?currentJobId=4147206861&geoId=103644278
                &origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"""

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(website)
    
    login(driver, 5)
    
    all_filters_btn = wait_for_element(driver, 5, "//button[contains(@class, 'search')]")
    all_filters_btn.click()

    time.sleep(2)

    set_filter()


def create_file_if_not_exists(json_path):
    """
    Creates the 'applied_to.json' file if it doesn't exist.
    """
    if not json_path.exists():
        with json_path.open("w") as f:
            json.dump([], f, indent=4)


def load_applied_jobs():
    """
    Loads jobs already applied to from a JSON file 
    or return an empty list if the file doesn't exist.
    """
    
    JOBS_APPLIED_TO = "applied_to.json"
    
    if os.path.exists(JOBS_APPLIED_TO):
        with open(JOBS_APPLIED_TO, "r") as file:
            return json.load(file)
    return []


def already_applied(id, title, company):
    """
    Checks if the job ID is found in the 'applied_to.json' file.
    """
    jobs_applied_to = load_applied_jobs()

    for job in jobs_applied_to:
        if job["id"] == id:
            print(f"Job {title} at {company} has already been applied to.")
            return  # Exit the function if the job has been applied to already

def show_applied_jobs():
    """
    Displays a list of jobs already applied to from the 'applied_to.json' file.
    Printed out to the console.
    """
    jobs_applied_to = load_applied_jobs()
    if not jobs_applied_to:
        print("No jobs applied to yet.")
        return
    
    print("\n----------Applied Jobs----------")
    for job in jobs_applied_to:
        print(f"{job['date_applied']} - {job['job_title']} at {job['company']}")


def wait_for_element(driver: WebDriver, time_to_wait: float, xpath: str):
    """ 
    Avoids having to type the below lines over and over.

    driver : WebDriver 
    -Browser controller to allow automated interaction,
    using it here as an argument in WebDriverWait().

    time_to_wait : float 
    -Used in WebDriverWait() to set the amount of time (in
    seconds) to wait for the element to be found.

    Returns
    - WebElement: The element that matches the given XPath.
    """
    return WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )


def login(driver: WebDriver, time_to_wait: float):
    """ 
    Logging into LinkedIn using the user's manually input credentials.

    driver : WebDriver
    - Needed in order to search for the element and interact with it.

    time_to_wait : int 
    - Value for the seconds argument in WebDriverWait() 
    """
    login_txt = WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'username')]"))
    )
    password_txt = WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'password')]"))
    )
    
    user_login = input("Enter LinkedIn Email or Phone: ")
    user_password = input("Enter LinkedIn Password: ")
    
    login_txt.send_keys(user_login)
    password_txt.send_keys(user_password)

    driver.find_element(By.XPATH, "//button[contains(@data-litms-control-urn, 'login-submit')]").click()
    

def job_and_location_search(driver: WebDriver, time_to_wait: float):
    """
    User input for the job (title, skill, company) and location search boxes.
    Clicks the search button after the information is entered.
    """ 
    job_search_box = WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@class, 'jobs-search-box__input--keyword')]")
        )
    )

    job_search_by_user = input("""Enter any titles, skills, companies, etc. 
                                    as you would normally on LinkedIn: """)
    job_search_box.clear()
    job_search_box.send_keys(job_search_by_user)

    
def set_filter():
    """
    Displays a console menu for each filter option. 
    These are set manually by the user via this menu and saved in a dict 
    that is used for actually setting the filters on linkedin.
    """
    dp_q = "Date Posted: "
    exp_q = "Experience Level(s): "
    job_q = "Job Type: "
    loc_q = "Location Type: "

    dp_opts = [
            'Any time', 
            'Past month', 
            'Past week', 
            'Past 24 hours'
    ]

    exp_opts = [
            'Associate', 
            'Entry level', 
            'Mid-Senior level', 
            'Director', 
            'Executive'
    ]

    job_opts = [
            'Full-time', 
            'Part-time', 
            'Contract', 
            'Temporary', 
            'Internship', 
            'Other'
    ]

    loc_opts = [
            'On-site', 
            'Hybrid', 
            'Remote'
    ]

    # pick() returns a dict because multiselect can be enabled, so the output
    # would be something like "[('Any time', '0')]" for date_posted as an
    # example. '0' being the index of the item in the dict. 
    date_posted, _  = pick(dp_opts, dp_q, indicator='»')
    exp_lvl, _      = pick(exp_opts, exp_q, indicator='»', multiselect=True)
    job_type, _     = pick(job_opts, job_q, indicator='»', multiselect=True)
    loc_type, _     = pick(loc_opts, loc_q, indicator='»', multiselect=True)
    
    filters = {
        "date_posted": date_posted,
        "experience_level": exp_lvl,
        "job_type": job_type,
        "location_type": loc_type
    }

    return filters


# def apply_filter(filters: dict):
#     pass    


def search_jobs_based_on_filter(filters: dict):
    dp_filter_el = 
    exp_filter_el = 
    job_filter_el = 
    loc_filter_el = 


def does_job_have_easy_apply(easy_override: bool) -> bool:
    """ 
    Applies through Easy Apply *instead* of the company's website. This is
    significantly faster, but the user will likely be limited in how much
    information they can input, such as a cover letter (usually).

    easy_override : bool 
    -A true / false value that determines whether or not
    the script should skip the Easy Apply and go straight to the company's
    website to apply. 
    """
    
    easy_apply_t_f = False

    # Check for the Easy Apply button here.

    if not easy_override:
        # Apply through Easy Apply and go to the next job.
        pass
    else:
        # Ignore Easy Apply and apply through the company's website instead.  
        # (probably impossible / very hard to do since some require signups
        # like workday) if easy_override is set to true. 
        pass       
    return easy_apply_t_f


def apply_on_company_site(**kwargs) -> dict:
    """ 
    Applying on company sites is hard because of how different each form
    can be.

    Each field name and it's input element / text box gets put into a dictonary
    to access and modify later. 
    """
    company_site_fields = {
        # "key: value for key, value in kwargs.items()"
    } # Any form fields that have titles and an input field most likely. 
    return company_site_fields


def scrape_job_info(filters: dict) -> dict:
    """ 
    Return a dictionary of the scraped data. i.e. different fields will be
    the key and the value will be the scraped info from those fields. 
    """
    job_info = {}
    return job_info


def save_to_spreadsheet(job_info: dict):
    """ 
    Save scraped job info to a spreadsheet. 
    """ 
    df = pd.DataFrame([job_info])
    df.to_excel(f"jobs_auto_applied_to_{date.today()}.xlsx")


if __name__ == '__main__':
    main()
