from selenium.webdriver.common.by import By
import time
from time_utils import convert_relative_time


def scrape_amadershomoy(driver, portal_name="Dainik Amader Shomoy", url="https://www.dainikamadershomoy.com/latest/all"):
    """Return list of formatted news lines for Amader Shomoy."""
    out = []
    try:
        driver.get(url)
        cards = driver.find_elements(By.CSS_SELECTOR, ".random-news")
    except Exception as e:
        out.append(f"Error fetching {portal_name}: {e}")
        return out

    out.append("\n==============================")
    out.append(f"📰 Fetching: {portal_name}")
    out.append("==============================")

    for i in range(5):  # fixed top 5 news
        card = cards[i] if i < len(cards) else None

        title = "N/A"
        link = "N/A"
        published_time = None

        if card:
            try:
                content = card.find_element(By.CSS_SELECTOR, ".content")
            except:
                content = None

            if content:
                # Title and link
                try:
                    a_tag = content.find_element(By.TAG_NAME, "a")
                    title = a_tag.text.strip() if a_tag else "N/A"
                    link = a_tag.get_attribute("href") if a_tag else "N/A"
                except:
                    pass

                # Published time
                try:
                    time_el = content.find_element(By.CSS_SELECTOR, ".inf")
                    published_time = time_el.text.strip()
                except:
                    pass

        if published_time:
            ts = convert_relative_time(published_time)
            out.append(f"{i+1}. {title} ({ts})")
        else:
            out.append(f"{i+1}. {title}")

    return out