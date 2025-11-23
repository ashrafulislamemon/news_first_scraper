
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
from time_utils import convert_relative_time



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


all_lines = []

for paper in newspapers:
    lines = []
    lines.append("\n==============================")
    lines.append(f" Fetching: {paper['name']}")
    lines.append("==============================")

    try:
        driver.get(paper["url"])
        time.sleep(5)

        news_elements = driver.find_elements(By.CSS_SELECTOR, paper["news_selector"])
        if len(news_elements) == 0:
            lines.append(f"No news found for {paper['name']}.")
            all_lines.extend(lines)
            continue

        if paper["time_selector"] == "time":
            time_elements = driver.find_elements(By.TAG_NAME, "time")
        else:
            time_elements = driver.find_elements(By.CSS_SELECTOR, paper["time_selector"])

        for i in range(min(5, len(news_elements))):
            title = news_elements[i].text.strip()

            raw_time = time_elements[i].text.strip() if i < len(time_elements) else ""

            # Always try to normalize the reported time; if parsing fails, the
            # converter will return the original raw string.
            if raw_time:
                news_time = convert_relative_time(raw_time)
            else:
                news_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            lines.append(f"{i + 1}. {title} ({news_time})")

        all_lines.extend(lines)

    except Exception as e:
        all_lines.append(f" Error fetching {paper['name']}: {e}")

try:
    it_lines = scrape_ittefaq("doinik ittefaq", driver, url="https://www.ittefaq.com.bd/latest-news")
    if it_lines:
        all_lines.extend(it_lines)
except Exception as e:
    all_lines.append(f"Error scraping Ittefaq: {e}")

try:
    bk_lines = scrape_bhorerkagoj("bhorer kagoj", driver, url="https://www.bhorerkagoj.com/latest")
    if bk_lines:
        all_lines.extend(bk_lines)
except Exception as e:
    all_lines.append(f"Error scraping Bhorer Kagoj: {e}")

try:
    am_lines = scrape_amadershomoy(driver, portal_name="Dainik Amader Shomoy", url="https://www.dainikamadershomoy.com/latest/all")
    if am_lines:
        all_lines.extend(am_lines)
except Exception as e:
    all_lines.append(f"Error scraping Amader Shomoy: {e}")

driver.quit()

# Write all collected lines to a file, overwriting any previous content.
output_path = "latest_news.txt"
try:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines).lstrip())
except Exception as e:
    print(f"Failed to write output file {output_path}: {e}")

from datetime import datetime, timedelta
import re

INPUT_FILE = "latest_news.txt"
OUTPUT_FILE = "new_news_with_source.txt"
TIME_WINDOW_MINUTES = 5

def parse_time(timestr):
    """Parse absolute timestamp only, ignore relative like '১ ঘণ্টা আগে'"""
    try:
        return datetime.strptime(timestr.strip(), "%Y-%m-%d %H:%M:%S")
    except:
        return None

now = datetime.now()
window_start = now - timedelta(minutes=TIME_WINDOW_MINUTES)

new_news = []

current_source = None
current_serial = 1

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Detect source: normal or 📰
        if "Fetching:" in line:
            current_source = line.split("Fetching:")[1].strip()
            current_serial = 1
            continue

        # Detect news line with timestamp in parentheses
        if "(" in line and line.endswith(")"):
            try:
                title_part, timestr = line.rsplit("(", 1)
                timestr = timestr.rstrip(")")
                news_time = parse_time(timestr)
                if news_time and news_time >= window_start:
                    # Remove old serial like "1. Title"
                    if ". " in title_part:
                        _, title_only = title_part.split(". ", 1)
                    else:
                        title_only = title_part
                    new_news.append(f"[{current_source}] {current_serial}. {title_only.strip()} ({timestr})")
                    current_serial += 1
            except:
                continue

# Write new news to output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for news in new_news:
        f.write(news + "\n")

print(f"{len(new_news)} news found in last {TIME_WINDOW_MINUTES} minutes.")

