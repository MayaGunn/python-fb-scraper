from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import re

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(), options=options)

# Manual Facebook login
driver.get("https://www.facebook.com/")
input("🔐 Log in to Facebook in the browser window, then press ENTER here...")

# Go to the profile page (change this URL to the target)
driver.get("https://www.facebook.com/ram.orion.3")
time.sleep(5)  # Wait for profile to load

# Scroll to load more posts
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(f"🔽 Scrolled {i+1}/5 times...")
    time.sleep(3)

# Find all <a> tags with href containing 'youtube.com'
youtube_anchors = driver.find_elements(By.XPATH, "//a[contains(@href, 'youtube.com')]")
print(f"\n🔍 Found {len(youtube_anchors)} <a> elements containing 'youtube.com'")

youtube_links = set()

for a in youtube_anchors:
    href = a.get_attribute("href")
    if href:
        # Extract clean YouTube watch URL with regex (ignore extra parameters)
        match = re.search(r"(https?://(?:www\.)?youtube\.com/watch\?v=[\w\-]+)", href)
        if match:
            clean_url = match.group(1)
            youtube_links.add(clean_url)
        else:
            # Sometimes short youtu.be links or others, you can add more regex if needed
            youtube_links.add(href)

# Print results
print("\n🎥 Extracted YouTube links:")
if youtube_links:
    for link in youtube_links:
        print(link)
else:
    print("❌ No YouTube links found.")

driver.quit()
