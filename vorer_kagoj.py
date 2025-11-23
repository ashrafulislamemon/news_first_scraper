from selenium.webdriver.common.by import By
import time
from time_utils import convert_relative_time


def scrape_bhorerkagoj(portal_name, driver, url="https://www.bhorerkagoj.com/latest"):
    """Return list of formatted news lines for Bhorer Kagoj."""
    out = []
    try:
        driver.get(url)
        time.sleep(5)
    except Exception as e:
        out.append(f"Failed to open {url}: {e}")
        return out

    try:
        container = driver.find_element(By.CLASS_NAME, "desktopSectionListMedia")
        cards = container.find_elements(By.CLASS_NAME, "media")
    except Exception as e:
        out.append(f"Failed to find news container: {e}")
        return out

    out.append("\n==============================")
    out.append(f"Fetching: {portal_name}")
    out.append("==============================")

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
                ts = convert_relative_time(published_time)
                out.append(f"{i+1}. {title} ({ts})")
            else:
                out.append(f"{i+1}. {title}")

        except Exception as e:
            out.append(f"Error processing card #{i}: {e}")
            continue

    return out
