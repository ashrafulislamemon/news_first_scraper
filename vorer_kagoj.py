from selenium.webdriver.common.by import By
import time

def scrape_bhorerkagoj(portal_name, driver, url="https://www.bhorerkagoj.com/latest"):
    try:
        driver.get(url)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to open {url}: {e}")
        return

    try:
        container = driver.find_element(By.CLASS_NAME, "desktopSectionListMedia")
        cards = container.find_elements(By.CLASS_NAME, "media")
        print(f"\n==============================")
        print(f"Fetching: {portal_name}")
        print(f"==============================")
    except Exception as e:
        print(f"Failed to find news container: {e}")
        return

    for i, card in enumerate(cards[:5]):  # top 5 news
        try:
            # Title
            try:
                title_el = card.find_element(By.TAG_NAME, "h4")
                title = title_el.text.strip()
            except:
                title = "N/A"

            # Published time
            try:
                time_el = card.find_element(By.CSS_SELECTOR, "p.desktopTime")
                published_time = time_el.text.strip()
            except:
                published_time = None

            if published_time:
                print(f"{i+1}. {title} ({published_time})")
            else:
                print(f"{i+1}. {title}")

        except Exception as e:
            print(f"Error processing card #{i}: {e}")
            continue
