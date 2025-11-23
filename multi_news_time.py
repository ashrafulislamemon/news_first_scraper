
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from datetime import datetime, timedelta
from ittefaq import scrape_ittefaq
from vorer_kagoj import scrape_bhorerkagoj
from test_amarsomy import scrape_amadershomoy
# ===============================
# Convert Bangla Relative Time
# ===============================
def convert_relative_time(text):
    now = datetime.now()

    bn2en = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
    text = text.translate(bn2en)

    match = re.search(r"(\d+)\s*(মিনিট|ঘন্টা|দিন)", text)
    if not match:
        return now.strftime("%Y-%m-%d %H:%M:%S")

    value = int(match.group(1))
    unit = match.group(2)

    if unit == "মিনিট":
        dt = now - timedelta(minutes=value)
    elif unit == "ঘন্টা":
        dt = now - timedelta(hours=value)
    elif unit == "দিন":
        dt = now - timedelta(days=value)
    else:
        dt = text

    return dt.strftime("%Y-%m-%d %H:%M:%S")



chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

newspapers = [
    {
        "name": "Prothom Alo",
        "url": "https://www.prothomalo.com/collection/latest",
        "news_selector": ".tilte-no-link-parent",
        "time_selector": ".published-time"
    },
    {
        "name": "Kaler Kantho",
        "url": "https://www.kalerkantho.com/special/recent",
        "news_selector": ".card-title",
        "time_selector": "time"
    },
    {
        "name": "Dainik Amader Shomoy",
        "url": "https://www.dainikamadershomoy.com/latest/all",
        "news_selector": ".random-news .content a",
        "time_selector": ".random-news .content .inf"
    }

]


for paper in newspapers:
    print("\n==============================")
    print(f"📰 Fetching: {paper['name']}")
    print("==============================")

    try:
        driver.get(paper["url"])
        time.sleep(5)

        news_elements = driver.find_elements(By.CSS_SELECTOR, paper["news_selector"])
        if len(news_elements) == 0:
            print(f"No news found for {paper['name']}.")
            continue

        if paper["time_selector"] == "time":
            time_elements = driver.find_elements(By.TAG_NAME, "time")
        else:
            time_elements = driver.find_elements(By.CSS_SELECTOR, paper["time_selector"])

        for i in range(min(5, len(news_elements))):
            title = news_elements[i].text.strip()

            raw_time = time_elements[i].text.strip() if i < len(time_elements) else ""

            if any(x in raw_time for x in ["মিনিট", "ঘন্টা", "দিন"]):
                news_time = convert_relative_time(raw_time)

                news_time=raw_time
            else:
                news_time = raw_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"{i + 1}. {title} ({news_time})")

    except Exception as e:
        print(f" Error fetching {paper['name']}: {e}")

scrape_ittefaq("doinik ittefaq" ,driver,url="https://www.ittefaq.com.bd/latest-news")        
scrape_bhorerkagoj("bhorer kagoj", driver, url="https://www.bhorerkagoj.com/latest")
scrape_amadershomoy(driver, portal_name="Dainik Amader Shomoy", url="https://www.dainikamadershomoy.com/latest/all")

driver.quit()



