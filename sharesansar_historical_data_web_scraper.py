import csv
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

driver = webdriver.Firefox()

url = "https://www.sharesansar.com/company/ebl"
driver.get(url)

wait = WebDriverWait(driver, 20)

def priceHistory():
    try:
        price_history_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn_cpricehistory"]')))
    except Exception as e:
        print("Price history not found")
        driver.quit()

    price_history_button.click()

def dropdownButton():
    try:
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="myTableCPriceHistory_length"]/label/select')))
        print("dropdown found")
    except Exception as e:
        print(f"Error finding dropdown {e}")
        driver.quit()

    try:
        select = Select(dropdown)
        select.select_by_value("50")
        print("Selected 50")
    except Exception as e:
        print(f"Error selecting 50")
        driver.quit()


def extractData(writer, fieldnames):
    try:
        table = driver.find_element(By.XPATH, '//*[@id="myTableCPriceHistory"]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if not columns:
                continue

            row_data = {field: col.text.strip() for field, col in zip(fieldnames, columns)}
            writer.writerow(row_data)

    except Exception as e:
        print(f"Error extracting data {e}")

def nextButton():
    try:
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="myTableCPriceHistory_next"]')))
        print("Next Button found")

        if "disabled" in next_button.get_attribute("class"):
            print("No more pages left")
            return False
        
        next_button.click()
        time.sleep(2)
        return True
    
    except Exception as e:
        print(f"Error finding next button {e}")
        return False

    
def main():
    priceHistory()
    dropdownButton()

    with open("Everest_bank_ltd_historical_data.csv", "w", newline="") as f:
        fieldnames = ["S.N.", "Date", "Open", "High", "Low", "Ltp", "% Change", "Qty", "Turnover"]
        
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        writer.writeheader()

        while True:
            time.sleep(2)
            extractData(writer, fieldnames)
        
            if not nextButton():
                break

if __name__ == "__main__":
    main()
    driver.quit()