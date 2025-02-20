from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import inquirer
import regex
import util

def job_and_location_search(driver, time_to_wait: float):
    """
    User input for the job (title, skill, company) and location search boxes.
    Clicks the search button after the information is entered.
    
    driver : WebDriver
    - Needed in order to search for the element and interact with it.

    time_to_wait : int 
    - Value for the seconds argument in WebDriverWait() 
    """ 
    job_search_box = util.wait_for_element(driver, time_to_wait, 
                                      "//input[contains(@aria-label, 'Search by title, skill, or company')]")
    
    loc_search_box = util.wait_for_element(driver, time_to_wait,
                                      "//input[contains(@aria-label, 'City, state, or zip code')]")
    
    print("-"*80)
    job_search_by_user = input(
"""
Enter any titles, skills, companies, etc. as you would normally on LinkedIn 
(i.e. 'analyst', excel, sql, microsoft). 
                              
**Anything in '' or \"\" means it must be found.**

>>"""
    )

    job_search_box.clear()
    job_search_box.send_keys(job_search_by_user)

    exclude_companies(job_search_box)
    
    print("\n")
    print("-"*80)
    loc_search_by_user = input(
"""
Enter the location you want to find jobs in (city, state, zip, country, etc.)
>>"""
    )

    loc_search_box.clear()
    loc_search_box.send_keys(loc_search_by_user)

    # don't need to wait for the element to appear here since it's loading at the same time as the inputs.
    search_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-search-box__submit-button')]") 
    search_btn.click()


def exclude_companies(job_search_box: WebElement):
    """
    Exclude companies from your search. Typically ones that are found spamming the board such as Dice and Jobot. 
    """
    comma_pattern = r"\s?,\s?"
    exclude = input(
"""
\nEnter a list of companies you'd like to avoid seeing listings for (comma-separated). 
>>"""
    ) 

    # doing this to replace all commas with the word "NOT" to 
    # be able to exclude specific companies from our search.
    comma_replace = regex.sub(comma_pattern, " NOT ", exclude)

    job_search_box.send_keys(Keys.END + " NOT " + comma_replace)     


def set_filter(driver):
    """
    Displays a console menu for each filter option using inquirer.
    These are set manually by the user via this menu and saved in a dict
    that is used for actually setting the filters on LinkedIn.
    """
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

    questions = [
        inquirer.List('date_posted',
                      message="Date Posted:",
                      choices=dp_opts),
        
        inquirer.Checkbox('experience_level',
                          message="Experience Level(s):",
                          choices=exp_opts),
        
        inquirer.Checkbox('job_type',
                          message="Job Type:",
                          choices=job_opts),
        
        inquirer.Checkbox('location_type',
                          message="Location Type:",
                          choices=loc_opts)
    ]

    answers = inquirer.prompt(questions)
    
    filters = {
        "date_posted": answers.get('date_posted', ''),
        "experience_level": answers.get('experience_level', []),
        "job_type": answers.get('job_type', []),
        "location_type": answers.get('location_type', [])
    }

    show_results_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'search-reusables__secondary-filters-show-results-button')]")
    show_results_btn.click()

    return filters



