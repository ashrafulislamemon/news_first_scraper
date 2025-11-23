from selenium.webdriver.common.by import By
import time
def scrape_ittefaq(portal_name, driver, url="https://www.ittefaq.com.bd/latest-news"):
    driver.get(url)
    time.sleep(5)

    try:
        cards = driver.find_elements(By.CLASS_NAME, "col")
        print(f"\n==============================")
        print(f"Fetching: {portal_name}")
        print(f"==============================")
    except Exception as e:
        print(f"Failed to find cards: {e}")
        return

    for i, card in enumerate(cards[:5]):  # top 5 news
        try:
            # Title
            try:
                title_el = card.find_element(By.CLASS_NAME, "title")
                title = title_el.text.strip()
            except:
                title = "N/A"

            
            try:
                time_el = card.find_element(By.CSS_SELECTOR, "span.time, time")
                raw_time = time_el.text.strip()
            except:
                raw_time = None

            if raw_time:
                print(f"{i+1}. {title} ({raw_time})")
            else:
                print(f"{i+1}. {title}")
        except Exception as e:
            print(f"Error processing card #{i}: {e}")
            continue