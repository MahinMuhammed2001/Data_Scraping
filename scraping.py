from selenium import webdriver       #Used for automating web browsing. It's used here to control a browser to interact with dynamic pages.
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


driver_path = 'C:/Users/mahin/Downloads/chromedriver_win32/chromedriver.exe'  

service = Service(driver_path)
driver = webdriver.Chrome(service=service) #Initializes a Chrome browser session using the WebDriver service


base_url = 'https://exhibitors.electronica.de/prj_807/view/?nv=2&lng=2' # The URL of the page to scrape
driver.get(base_url) #Opens the provided URL in the Chrome browser controlled by Selenium.


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'urlShare'))) #Ensures the page has fully loaded by waiting for an element (urlShare class) to appear.

page_number = 1
total_pages = 2  # Adjust this total page number as needed, i set now only two pages

while page_number <= total_pages:
    print(f"Scraping page {page_number}...")

    page_source = driver.page_source #Fetches the HTML source of the current page.
    soup = BeautifulSoup(page_source, 'html.parser')  # Parses the HTML content to make it easier to navigate and search for elements.
    
    company_names = soup.find_all('a', class_='urlShare')
    for company in company_names:
        company_name = company.get_text(strip=True) #Extracts the text of each company name, stripping any leading/trailing whitespace.
        print(f"Extracting details for: {company_name}")

        company_link = company.get('href') #Extracts the link of each company.
        driver.get(company_link) #Opens the link of each company in the Chrome browser controlled by Selenium.

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ce_addr')))
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        
        industry_category_details_page = "N/A"
        try:
            # Look for the industry category on the company details page
            industry_category_details_element = driver.find_element(By.CSS_SELECTOR, '.ce_text')
            if industry_category_details_element:
                industry_category_details_page = industry_category_details_element.text.strip()
        except Exception as e:
            print(f"Industry category not found on details page for {company_name}. Error: {e}")

        
        social_media = {
            'LinkedIn': 'Nill',
            'YouTube': 'Nill',
            'Instagram': 'Nill',
            'Facebook': 'Nill',
            'Twitter': 'Nill'
        }
        try:
            linkedin_element = driver.find_element(By.CSS_SELECTOR, '.ce_smch.ce_LinkedIn a')
            social_media['LinkedIn'] = linkedin_element.get_attribute('href').strip()
        except Exception as e:
            print(f"LinkedIn not found for {company_name}. Error: {e}")

        try:
            # Extract YouTube link
            youtube_element = driver.find_element(By.CSS_SELECTOR, '.ce_smch.ce_YouTube a')
            social_media['YouTube'] = youtube_element.get_attribute('href').strip()
        except Exception as e:
            print(f"YouTube not found for {company_name}. Error: {e}")

        try:
            # Extract Instagram link (not found make as nill)
            instagram_element = driver.find_element(By.CSS_SELECTOR, '.ce_smch.ce_Instagram a')
            social_media['Instagram'] = instagram_element.get_attribute('href').strip()
        except Exception as e:
            print(f"Instagram not found for {company_name}. Error: {e}")

        try:
            # Extract Facebook link
            facebook_element = driver.find_element(By.CSS_SELECTOR, '.ce_smch.ce_Facebook a')
            social_media['Facebook'] = facebook_element.get_attribute('href').strip()
        except Exception as e:
            print(f"Facebook not found for {company_name}. Error: {e}")

        try:
            # Extract Twitter link
            twitter_element = driver.find_element(By.CSS_SELECTOR, '.ce_smch.ce_Twitter a')
            social_media['Twitter'] = twitter_element.get_attribute('href').strip()
        except Exception as e:
            print(f"Twitter not found for {company_name}. Error: {e}")

        # Extract the address
        try:
            address_element = driver.find_element(By.CSS_SELECTOR, '.ce_addr')
            address = address_element.text.strip()
            print(f"Address for {company_name}: {address}")
        except Exception as e:
            address = 'Nill'
            print(f"Address not found for {company_name}. Error: {e}")

        # Extract the email
        try:
            email_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ce_email a'))
            )
            email = email_element.get_attribute('href').replace('mailto:', '').strip()
        except Exception as e:
            email = 'Nill'
            print(f"Email not found for {company_name}. Error: {e}")

        # Extract the phone number
        try:
            phone_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ce_phone a'))
            )
            phone = phone_element.get_attribute('href').replace('tel:', '').strip()
        except Exception as e:
            phone = 'Nill'
            print(f"Phone not found for {company_name}. Error: {e}")
        
        # Extract the website URL
        try:
            website_element = driver.find_element(By.CSS_SELECTOR, '.ce_website a')
            website = website_element.get_attribute('href').strip()
        except Exception as e:
            website = 'Nill'
            print(f"Website not found for {company_name}. Error: {e}")

        # Extract the products and services
        products_services = []
        try:
            products_section = driver.find_elements(By.CSS_SELECTOR, '.ce_head h2 a')
            for product in products_section:
                product_name = product.text.strip()
                products_services.append(product_name)
        except Exception as e:
            print(f"Products/Services not found for {company_name}. Error: {e}")

        




        company_profile = 'Nill' 
        try:
    
            profile_element = driver.find_element(By.XPATH, "//div[contains(@class, 'ce_cntnt')]//div[contains(@class, 'ce_text')]")
            company_profile = profile_element.text.strip()
        except Exception as e:
            print(f"Company profile not found for {company_name}. Error: {e}")

        print(f"Details for {company_name}:")
        print(f"  Industry Category (Details page): {industry_category_details_page}")
        print(f"  Address: {address}")
        print(f"  Email: {email}")
        print(f"  Phone: {phone}")
        print(f"  Website: {website}")
        print(f"  Social Media Links: {social_media}")
        print(f"  Products/Services: {products_services}")
        
        print(f"Company Profile for {company_name}: {company_profile}")
        
        time.sleep(2)
        

        driver.back() #Navigates back to the previous page (list of companies).
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'input[name="SRField_next"][value="next"]')
        next_button.click()
        time.sleep(5)
        page_number += 1
    except Exception as e:
        print("No more pages or unable to navigate to the next page.")
        break  

    
driver.quit() #Closes the browser session.
