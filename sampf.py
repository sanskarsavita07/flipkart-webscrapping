# Flipkart Smart Watch Scraper (Modeled After Amazon Scraper)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# -------------------------------
# Setup Chrome Driver
# -------------------------------
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# -------------------------------
# Open Flipkart
# -------------------------------
driver.get("https://www.flipkart.com/")
print("Flipkart page loaded successfully.")
time.sleep(3)

# Close login popup if it appears
try:
    close_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))
    )
    close_button.click()
    print("Login popup closed.")
except:
    print("No login popup detected.")

# -------------------------------
# Search for Smart Watches
# -------------------------------
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)
search_box.clear()
search_box.send_keys("Smart Watches" + Keys.ENTER)
print("Smart Watches search initiated.")
time.sleep(5)

# -------------------------------
# Collect product data
# -------------------------------
data = []

# Scrape first 5 pages
for page in range(1, 6):
    print(f"\nScraping Page {page}...")

    # Wait until at least one product card is visible
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class,'_1AtVbE') or contains(@class,'_13oc-S') or contains(@class,'_2kHMtA')]")
            )
        )
    except:
        print("⚠️ No products loaded — page took too long or layout changed.")
        break

    # Locate all product cards
    products = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'_1AtVbE') or contains(@class,'_13oc-S') or contains(@class,'_2kHMtA')]"
    )
    print(f"Found {len(products)} product elements on page {page}.")

    for product in products:
        try:
            # Product name
            try:
                name = product.find_element(By.XPATH, ".//a[contains(@class,'IRpwTa') or contains(@class,'s1Q9rs') or contains(@class,'_2WkVRV') or contains(@class,'_4rR01T')]").text
            except:
                name = "N/A"

            # Product price
            try:
                price = product.find_element(By.XPATH, ".//div[contains(@class,'_30jeq3')]").text
            except:
                price = "N/A"

            # Product image
            try:
                image = product.find_element(By.XPATH, ".//img").get_attribute("src")
            except:
                image = "N/A"

            # Product link
            try:
                link = product.find_element(By.XPATH, ".//a[contains(@class,'IRpwTa') or contains(@class,'s1Q9rs') or contains(@class,'_1fQZEK')]").get_attribute("href")
            except:
                link = "N/A"

            data.append({
                "Name": name,
                "Price": price,
                "Image": image,
                "Link": link
            })

        except Exception as e:
            print("Error extracting a product:", e)

    print(f" Page {page} done — collected {len(products)} items.")

    # Click next page
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a/span[text()='Next']"))
        )
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
    except:
        print("🚫 No more pages found or 'Next' button missing.")
        break

# -------------------------------
# Close browser
# -------------------------------
driver.quit()

# -------------------------------
# Save data to CSV
# -------------------------------
print("\nAll collected product data as list:\n")
print(data)

df = pd.DataFrame(data)
df.to_csv("flipkart_smartwatches.csv", index=False, encoding='utf-8')
print("\nScraping completed successfully!")
print("Data saved in: flipkart_smartwatches.csv")
