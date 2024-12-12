
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

# Selenium WebDriver setup
driver_path = 'C:/Users/mahin/Downloads/chromedriver_win32/chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
base_url = 'https://exhibitors.electronica.de/prj_807/view/?nv=2&lng=2'
driver.get(base_url)

# Wait for the first page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'urlShare')))

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL",
    database="electronica_data"
)
cursor = db.cursor()

# Pagination setup
page_number = 1
previous_page_content = None

while True:
    print(f"Scraping page {page_number}...")

    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    company_names = soup.find_all('a', class_='urlShare')

    # Validate page content to prevent duplication
    if previous_page_content == page_source:
        print("Page content repeated. Stopping...")
        break
    previous_page_content = page_source

    if not company_names:  # No more companies found, end scraping
        print("No more companies to scrape.")
        break

    for company in company_names:
        company_name = company.get_text(strip=True)
        print(f"Extracting details for: {company_name}")

        # Navigate to company details page
        company_link = company.get('href')
        driver.get(company_link)

        # Wait for the details page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ce_addr')))

        # Scroll to ensure full page loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))  # Random delay to mimic human behavior

        # Initialize data variables
        industry_category_details_page = "N/A"
        social_media = {'LinkedIn': 'Nill', 'YouTube': 'Nill', 'Instagram': 'Nill', 'Facebook': 'Nill', 'Twitter': 'Nill'}
        address = email = phone = website = 'Nill'
        products_services = []
        company_profile = 'Nill'

        # Extract details
        try:
            industry_category_details_element = driver.find_element(By.CSS_SELECTOR, '.ce_text')
            industry_category_details_page = industry_category_details_element.text.strip()
        except Exception:
            pass

        # Extract social media links
        social_media_selectors = {
            'LinkedIn': '.ce_smch.ce_LinkedIn a',
            'YouTube': '.ce_smch.ce_YouTube a',
            'Instagram': '.ce_smch.ce_Instagram a',
            'Facebook': '.ce_smch.ce_Facebook a',
            'Twitter': '.ce_smch.ce_Twitter a'
        }
        for platform, selector in social_media_selectors.items():
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                social_media[platform] = element.get_attribute('href').strip()
            except Exception:
                pass

        try:
            address_element = driver.find_element(By.CSS_SELECTOR, '.ce_addr')
            address = address_element.text.strip()
        except Exception:
            pass

        try:
            email_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ce_email a'))
            )
            email = email_element.get_attribute('href').replace('mailto:', '').strip()
        except Exception:
            pass

        try:
            phone_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ce_phone a'))
            )
            phone = phone_element.get_attribute('href').replace('tel:', '').strip()
        except Exception:
            pass

        try:
            website_element = driver.find_element(By.CSS_SELECTOR, '.ce_website a')
            website = website_element.get_attribute('href').strip()
        except Exception:
            pass

        try:
            products_section = driver.find_elements(By.CSS_SELECTOR, '.ce_head h2 a')
            for product in products_section:
                product_name = product.text.strip()
                products_services.append(product_name)
        except Exception:
            pass

        try:
            profile_element = driver.find_element(By.XPATH, "//div[contains(@class, 'ce_cntnt')]//div[contains(@class, 'ce_text')]")
            company_profile = profile_element.text.strip()
        except Exception:
            pass

        # Insert data into the database
        data = (company_name, industry_category_details_page, address, email, phone, website,
                social_media['LinkedIn'], social_media['YouTube'], social_media['Instagram'],
                social_media['Facebook'], social_media['Twitter'], ', '.join(products_services), company_profile)

        insert_query = """INSERT INTO companies (company_name, industry_category, address, email, phone, website,
                          linkedin, youtube, instagram, facebook, twitter, products_services, company_profile)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_query, data)
        db.commit()

        # Go back to the main page
        driver.back()

    # Handle cookie consent banner if it appears
    try:
        cookie_banner = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'usercentrics-root'))
        )
        if cookie_banner.is_displayed():
            print("Cookie consent found, accepting...")
            accept_button = driver.find_element(By.CSS_SELECTOR, 'button#uc-btn-accept')
            ActionChains(driver).move_to_element(accept_button).click().perform()
            time.sleep(2)
    except Exception as e:
        print("No cookie consent banner found:", e)

    # Wait for the "Next" button and click to go to the next page
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="SRField_next"][value="next"]'))
        )
        driver.execute_script("arguments[0].click();", next_button)

        # Wait for the page to load completely after AJAX request
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        page_number += 1
        time.sleep(random.uniform(2, 4))  # Random delay
    except Exception as e:
        print("No more pages to load or error navigating to next page:", e)
        break

# Close database connection and browser
cursor.close()
db.close()
driver.quit()
