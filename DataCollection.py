import os
import json
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def load_config(config_file="config.json"):
    with open(config_file, "r") as file:
        return json.load(file)

def extract_zip(zip_path, extract_to):
    with ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(extract_to)

def download_spp_data(base_url, year, output_dir, zip_name, wait_time):
    os.makedirs(output_dir, exist_ok=True)
    yearly_zip_path = os.path.join(output_dir, zip_name)

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.path.abspath(output_dir)}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(base_url)
        wait = WebDriverWait(driver, 60)
        year_folder = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{year}')]")))
        driver.execute_script("arguments[0].click();", year_folder)
        time.sleep(5)
        zip_file = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[contains(@class, 'item-name') and contains(text(), '{zip_name}')]")))
        driver.execute_script("arguments[0].scrollIntoView();", zip_file)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", zip_file)
        print("Waiting for download to complete...")
        time.sleep(wait_time)
    except Exception as e:
        print(f"Error downloading {zip_name}: {e}")
    finally:
        driver.quit()

    if os.path.exists(yearly_zip_path):
        extract_zip(yearly_zip_path, output_dir)
        os.remove(yearly_zip_path)

if __name__ == "__main__":
    config = load_config()
    os.makedirs("./data/BC", exist_ok=True)
    os.makedirs("./data/lmp", exist_ok=True)

    download_spp_data(config["base_url"], config["year"], "./data/BC", f"{config['year']}.zip", config["bc_wait_time"])
    download_spp_data(config["lmp_url"], config["year"], "./data/lmp", f"{config['year']}.zip", config["lmp_wait_time"])
