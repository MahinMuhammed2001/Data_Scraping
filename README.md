# Electronica  Data Scraping 

## Overview 
This project is a web scraper built to collect exhibitor data from the Electronica Exhibitor Directory. The scraper extracts various data points about companies, including their contact details, products and services, industry category, and social media presence. The data is then stored in a MySQL database for further analysis and visualization.
(*adjust the pages)
## Features
- Scrapes company information such as name, website, address, email, contact numbers, insustry category, products/services and social media links.
- Stores data in a structured MySQL database.
- Provides insightful visualizations of the collected data:
  - Distribution of companies across industries.
  - Social media presence breakdown.
  - Analysis of products/services offered.
  - Distribution of profile descriptions by word count.

## Technology
- **Programming Language**: Python
- **Libraries**: BeautifulSoup, MySQL Connector, Pandas, Seaborn, Matplotlib
- **Database**: MySQL
- **Data Visualization**: Matplotlib and Seaborn


## Database Details

The electronica_scrape database stores detailed information about companies listed in the Electronica Exhibitor Directory. It includes a 'companies' table with key data points for each company, such as contact details, industry category, products and services offered, and links to social media profiles.

### Table: companies

-**id**:Unique identifier for each company (Primary Key).
- **company_name**: Name of the company.
- **industry_category**: Sector or category the company belongs to.
- **address**: Physical location of the company.
- **email**: Company’s main contact email.
- **phone**: Contact phone number.
- **website**: Official website URL.
- **linkedin, youtube, instagram, facebook, twitter**: URLs to the company's social media profiles, if available.
- **products_services**: List or description of the products and services offered.
- **company_profile**: Brief description of the company’s background and mission.



## My Experience

I started this project as a beginner in web scraping, and it has been an incredibly valuable learning experience. Initially, I had some basic exposure to scraping, having completed a small project using the Scrapy framework about six months ago. However, this task allowed me to deepen my understanding and expand my skills significantly.

At first, I chose Scrapy as my framework, but I found that many resources, especially YouTube tutorials, primarily used Beautiful Soup. After researching and exploring both, I decided to switch to Beautiful Soup for this project. I spent time studying various tutorials and also used ChatGPT and other online resources to enhance my knowledge and troubleshoot challenges along the way.

For this project, I successfully scraped data from two pages. I have currently limited the scraper to only two pages, but I can easily increase this limit to gather more data if required. I would appreciate any feedback or suggestions on this, and I’m happy to adjust the page count to meet additional data needs.

Overall, this experience has greatly boosted my confidence and sparked my interest in web scraping. I now feel much more equipped to take on complex scraping tasks in the future and explore more advanced techniques. Thank you for this opportunity to grow and improve my skills!


## Challenges Faced

1. **Version Compatibility with Selenium and ChromeDriver**: 
   Managing the compatibility between Selenium, Chrome, and ChromeDriver versions was a major challenge. My Chrome browser was initially at version 130, but I couldn't find a matching ChromeDriver version for it. To resolve this, I downgraded Chrome to version 114. However, I still encountered issues with version mismatches. After some troubleshooting, I discovered that Chrome was auto-updating, which was causing the problem to persist. I ultimately disabled auto-updates to stabilize the setup.

2. **Starting the Data Scraping Process**: 
   Beginning the data scraping itself was challenging, as I was unfamiliar with the initial steps. After watching  YouTube tutorials and gaining more understanding, I was able to extract the company names and other details .

3. **Connecting MySQL for Data Storage**: 
   Although I had connected to MySQL in previous Django projects, setting it up in this context presented a few unique challenges. With the guidance of ChatGPT and additional resources, I successfully configured the database and integrated it with my project.

4. **Handling Elements with the Same Class Names**:  
   Another challenge I encountered was dealing with elements that shared the same class name, particularly when extracting the company profile and industry category. Initially, this caused issues in correctly identifying and extracting data for each field. To overcome this, I attempted to locate the elements using unique IDs or more specific selectors when available. This approach improved the accuracy of my data extraction, allowing me to handle elements with duplicate classes effectively.

Each of these challenges provided valuable learning experiences, and overcoming them has enhanced my knowledge and skills in web scraping and data handling.


## Contact Information 
    Mahin Muhammed
    7593933432
    mahinmuhammed75@gmail.com
    