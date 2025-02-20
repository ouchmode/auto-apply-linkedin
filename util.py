from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pathlib import Path

import json
import os

def create_file_if_not_exists(json_path: Path):
    """
    Creates the 'applied_to.json' file if it doesn't exist or is empty.

    json_path : Path
    -The filesystem path where the 'applied_to.json' file is located.
    """
    if not json_path.exists() or os.stat(json_path).st_size == 0:
        with json_path.open("w") as f:
            json.dump([], f, indent=4)

def wait_for_element(driver, time_to_wait: float, xpath: str) -> WebElement:
    """ 
    Avoids having to type the below lines over and over.

    driver 
    -Browser controller to allow automated interaction,
    using it here as an argument in WebDriverWait().

    time_to_wait : float 
    -Used in WebDriverWait() to set the amount of time (in
    seconds) to wait for the element to be found.

    Returns
    - WebElement: The element that matches the given XPath.
    """
    return WebDriverWait(driver, time_to_wait).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
