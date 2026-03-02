from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


# =========================
# MYNTRA
# =========================
def scrape_myntra(url, category):
    driver = get_driver()
    driver.get(url)
    time.sleep(6)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    results = []
    products = driver.find_elements(By.CLASS_NAME, "product-base")

    print("Myntra found:", len(products))

    for product in products[:8]:
        try:
            name = product.find_element(By.CLASS_NAME, "product-product").text
        except:
            name = "N/A"

        try:
            offer = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
        except:
            offer = "N/A"

        try:
            original = product.find_element(By.CLASS_NAME, "product-strike").text
        except:
            original = offer

        try:
            discount = product.find_element(By.CLASS_NAME, "product-discountPercentage").text
        except:
            discount = "0%"

        try:
            image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ""

        results.append({
            "Product": name,
            "Website": "Myntra",
            "Category": category,
            "Original Price": original,
            "Offer Price": offer,
            "Discount %": discount,
            "Image": image,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    driver.quit()
    return results


# =========================
# NYKAA (GENERIC SELECTOR)
# =========================
def scrape_nykaa(url, category):
    driver = get_driver()
    driver.get(url)
    time.sleep(6)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    results = []
    products = driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")

    print("Nykaa found:", len(products))

    for product in products[:8]:
        try:
            name = product.text.split("\n")[0]
        except:
            name = "N/A"

        try:
            price = product.text.split("₹")[1].split("\n")[0]
            offer = "₹" + price
        except:
            offer = "N/A"

        original = offer
        discount = "N/A"

        try:
            image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ""

        results.append({
            "Product": name,
            "Website": "Nykaa",
            "Category": category,
            "Original Price": original,
            "Offer Price": offer,
            "Discount %": discount,
            "Image": image,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    driver.quit()
    return results


# =========================
# PURPLLE (GENERIC)
# =========================
def scrape_purplle(url, category):
    driver = get_driver()
    driver.get(url)
    time.sleep(6)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    results = []
    products = driver.find_elements(By.XPATH, "//div[contains(@class,'product')]")

    print("Purplle found:", len(products))

    for product in products[:8]:
        text = product.text.split("\n")

        name = text[0] if len(text) > 0 else "N/A"

        offer = "N/A"
        for line in text:
            if "₹" in line:
                offer = line
                break

        original = offer
        discount = "N/A"

        try:
            image = product.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ""

        results.append({
            "Product": name,
            "Website": "Purplle",
            "Category": category,
            "Original Price": original,
            "Offer Price": offer,
            "Discount %": discount,
            "Image": image,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    driver.quit()
    return results


# =========================
# MAIN
# =========================
def run_scraper():

    results = []

    # Lipstick
    results += scrape_myntra("https://www.myntra.com/lakme-lipstick", "Lipstick")
    results += scrape_nykaa("https://www.nykaa.com/search/result/?q=lakme%20lipstick", "Lipstick")
    results += scrape_purplle("https://www.purplle.com/search?q=lakme%20lipstick", "Lipstick")

    # Foundation
    results += scrape_myntra("https://www.myntra.com/maybelline-foundation", "Foundation")
    results += scrape_nykaa("https://www.nykaa.com/search/result/?q=maybelline%20foundation", "Foundation")
    results += scrape_purplle("https://www.purplle.com/search?q=maybelline%20foundation", "Foundation")

    if results:
        df = pd.DataFrame(results)
        df.to_csv("cosmetic_offers.csv", index=False)
        print("✅ Total products saved:", len(results))
    else:
        print("❌ No data scraped")


if __name__ == "__main__":
    run_scraper()