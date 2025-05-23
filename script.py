from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re

# === Part 1: Open Facebook and let the user log in manually ===

driver = webdriver.Chrome()
driver.get("https://www.facebook.com")
input("🔐 Log in to Facebook in the browser window, then press ENTER here...")

# === Part 2: Go to the target profile ===

driver.get("https://www.facebook.com/ram.orion.3")  # change to any Facebook username
time.sleep(5)

# === Part 3: Scroll to load more posts ===

SCROLL_PAUSE_TIME = 3
scroll_times = 10  # increase this to load more posts

last_height = driver.execute_script("return document.body.scrollHeight")
for i in range(scroll_times):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# === Part 4: Grab the HTML source ===

html = driver.page_source
driver.quit()

# === Part 5: Extract YouTube links from the HTML ===

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all("a", href=True)

youtube_links = []
for link in links:
    href = link['href']
    if "youtube.com/watch" in href or "youtu.be/" in href:
        youtube_links.append(href)

youtube_links = list(set(youtube_links))  # remove duplicates
print(f"\n🎥 Found {len(youtube_links)} YouTube links.\n")

# === Part 6: Get video title and thumbnail ===

def extract_video_id(url):
    if "youtube.com/watch" in url:
        match = re.search(r"v=([^&]+)", url)
    elif "youtu.be/" in url:
        match = re.search(r"youtu\.be/([^?&]+)", url)
    else:
        return None
    return match.group(1) if match else None

def get_youtube_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.replace(" - YouTube", "").strip()
        video_id = extract_video_id(url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg" if video_id else None
        return {"title": title, "thumbnail": thumbnail_url, "url": url}
    except Exception as e:
        return {"title": "Error", "thumbnail": None, "url": url}

# === Part 7: Print out video info ===

for link in youtube_links:
    info = get_youtube_info(link)
    print(f"🎬 Title: {info['title']}")
    print(f"🖼️ Thumbnail: {info['thumbnail']}")
    print(f"🔗 Link: {info['url']}")
    print("------")
