# Flipkart Smart Watch Scraper (With Per-Page Product Printing + find_element for Speed)
# Modified to take user input for search term and page limit, similar to the Amazon scraper
# Updated XPaths based on error analysis (name/link/price not found; pagination may need adjustment)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Take user input for search term and page limit
search_term = input("Enter the search term (e.g., 'Smart Watches'): ")
try:
    page_limit = int(input("Enter the number of pages to scrape (e.g., 5): "))
    if page_limit < 1:
        raise ValueError("Page limit must be at least 1.")
except ValueError as e:
    print(f"Invalid input for page limit: {e}")
    exit()

# Setup Chrome Driver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Go to Flipkart home page
driver.get("https://www.flipkart.com/")
print("Flipkart page loaded successfully.")
print(f"Current URL: {driver.current_url}")  # Debug: Check if it redirected

# Wait for and assign search box element
search_box = None
try:
    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "Pke_EE")))
    print("Search box found by class name.")
except:
    print("Search box not found. Page might have changed or redirected. Check manually.")
    driver.quit()
    exit()

# Search for the user-specified term (using the assigned element)
search_box.clear()
search_box.send_keys(search_term + Keys.ENTER)
print(f"{search_term} search initiated.")
time.sleep(5)

# Collect product data (list of dictionaries)
data = []

# Loop through the specified number of pages
for page in range(1, page_limit + 1):
    print(f"\nScraping Page {page}...")
    
    if page > 1:
        # Try to click the "Next" button for pagination (updated XPath for better matching)
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, '_1LKTO3') and .//span[text()='Next']]"))
            )
            next_button.click()
            time.sleep(5)
        except:
            print(f"Could not navigate to page {page}. Stopping at page {page-1}.")
            break
    
    # Wait until product containers appear (using a common XPath for Flipkart product listings)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-id]"))  # Adjust if Flipkart changes structure
    )
    
    products = driver.find_elements(By.XPATH, "//div[@data-id]")  # Common product container
    print(f"Found {len(products)} products on page {page}.")
    
    # Temporary list for this page's products
    page_data = []
    
    for idx, product in enumerate(products, start=1):
        # Extract product details using find_element (faster) - Updated XPaths based on Flipkart's structure
        try:
            # For name and link: Try common classes for product titles (e.g., IRpwTa for mobiles, _1fQZEK for others)
            link_elem = product.find_element(By.XPATH, ".//a[contains(@class, 'IRpwTa') or contains(@class, '_1fQZEK') or contains(@class, 's1Q9rs')]")
            link = link_elem.get_attribute("href")
            name = link_elem.text.strip() if link_elem.text else "N/A"
        except:
            name = "N/A"
            link = "N/A"

        try:
            # For price: Common class _30jeq3 _1_WHN1
            price_elem = product.find_element(By.XPATH, ".//div[contains(@class, '_30jeq3')]")
            price = price_elem.text.strip()
        except:
            price = "N/A"

        try:
            # For image: Standard img tag
            image = product.find_element(By.XPATH, ".//img").get_attribute("src")
        except:
            image = "N/A"

        # Create product dictionary
        product_dict = {
            "Name": name,
            "Price": price,
            "Image": image,
            "Link": link
        }
        
        # Add to page list and global data
        page_data.append(product_dict)
        data.append(product_dict)
        
        # Print each product for this page
        print(f"Product {idx} on Page {page}: {product_dict}")

    print(f"Page {page} done — collected {len(products)} items.")

# Close the browser
driver.quit()

# Print all collected data (full list of dictionaries)
print("\nAll collected product data as list of dictionaries:\n")
print(data)

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("flipkart_smartwatches.csv", index=False, encoding='utf-8')
print("\nScraping completed successfully!")
print("Data saved in: flipkart_smartwatches.csv")
