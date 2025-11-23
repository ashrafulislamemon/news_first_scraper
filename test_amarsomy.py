from selenium.webdriver.common.by import By
import time


def scrape_amadershomoy(driver, portal_name="Dainik Amader Shomoy", url="https://www.dainikamadershomoy.com/latest/all"):
    driver.get(url)


    try:
        cards = driver.find_elements(By.CSS_SELECTOR, ".random-news")
        print(f"\n==============================")
        print(f"📰 Fetching: {portal_name}")
        print(f"==============================")
    except:
        return

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
            print(f"{i+1}. {title} ({published_time})")
        else:
            print(f"{i+1}. {title}")