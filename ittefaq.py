from selenium.webdriver.common.by import By
import time
from time_utils import convert_relative_time


def scrape_ittefaq(portal_name, driver, url="https://www.ittefaq.com.bd/latest-news"):
    """Return a list of formatted news lines for Ittefaq (instead of printing)."""
    out = []
    try:
        driver.get(url)
        time.sleep(5)

        cards = driver.find_elements(By.CLASS_NAME, "col")
    except Exception as e:
        out.append(f"Error fetching {portal_name}: {e}")
        return out

    out.append("\n==============================")
    out.append(f"Fetching: {portal_name}")
    out.append("==============================")

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
                ts = convert_relative_time(raw_time)
                out.append(f"{i+1}. {title} ({ts})")
            else:
                out.append(f"{i+1}. {title}")
        except Exception as e:
            out.append(f"Error processing card #{i}: {e}")
            continue

    return out