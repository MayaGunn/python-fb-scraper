'''from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def main():
    chrome_driver_path = "/opt/homebrew/bin/chromedriver"  # explicit chromedriver path

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--auto-open-devtools-for-tabs")  # optional: open DevTools (inspect)

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.facebook.com")
        input("🔐 Please log in manually, then press ENTER here...")

        profile_url = "https://www.facebook.com/ram.orion.3"
        print(f"➡️ Navigating to profile: {profile_url}")
        driver.get(profile_url)

        # Scroll down a few times
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"🔽 Scrolled {i+1}/5 times...")
            time.sleep(2)

        input("⏳ Wait a bit, then press ENTER to dump page source...")

        # Dump page source (HTML) into a file
        html_source = driver.page_source
        with open("fb_profile_source.html", "w", encoding="utf-8") as f:
            f.write(html_source)
        print("✅ Saved page source to fb_profile_source.html")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

## script with raw HTML ends here!


## script to only modify the HTML!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from bs4 import BeautifulSoup
import html
from urllib.parse import urlparse, parse_qs, unquote

input_file = "fb_profile_source.html"   # Your original saved HTML file
output_file = "youtube_links_and_titles.html"  # New clean file with YouTube links + titles

def extract_youtube_links_and_titles(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = html.unescape(a_tag['href'])
        text = a_tag.get_text(strip=True)  # extract visible text inside the <a>

        # Handle Facebook redirect URLs
        if "l.facebook.com/l.php" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            if 'u' in qs:
                real_url = unquote(qs['u'][0])
                if "youtube.com/watch" in real_url or "youtu.be/" in real_url:
                    links.add((real_url, text if text else real_url))
        else:
            if "youtube.com/watch" in href or "youtu.be/" in href:
                links.add((href, text if text else href))

    return links

def make_clean_html(links):
    html_links = "\n".join(
        f'<li><a href="{url}" target="_blank">{title}</a></li>'
        for url, title in sorted(links, key=lambda x: x[1].lower())
    )
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>YouTube Links with Titles</title>
</head>
<body>
<h1>YouTube Links Extracted with Titles</h1>
<ul>
{html_links}
</ul>
</body>
</html>
"""

def main():
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    yt_links = extract_youtube_links_and_titles(html_content)
    print(f"Found {len(yt_links)} YouTube links with titles.")

    clean_html = make_clean_html(yt_links)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(clean_html)

    print(f"Clean HTML saved to '{output_file}'")

if __name__ == "__main__":
    main()
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import html
from urllib.parse import urlparse, parse_qs, unquote

def extract_youtube_links_and_titles(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = html.unescape(a_tag['href'])
        text = a_tag.get_text(strip=True)

        # Handle Facebook redirect URLs
        if "l.facebook.com/l.php" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            if 'u' in qs:
                real_url = unquote(qs['u'][0])
                if "youtube.com/watch" in real_url or "youtu.be/" in real_url:
                    links.add((real_url, text if text else real_url))
        else:
            if "youtube.com/watch" in href or "youtu.be/" in href:
                links.add((href, text if text else href))

    return links

def make_clean_html(links):
    html_links = "\n".join(
        f'<li><a href="{url}" target="_blank">{title}</a></li>'
        for url, title in sorted(links, key=lambda x: x[1].lower())
    )
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>YouTube Links Extracted</title>
</head>
<body>
<h1>YouTube Links Extracted from Facebook</h1>
<ul>
{html_links}
</ul>
</body>
</html>
"""

def main():
    chrome_driver_path = "/opt/homebrew/bin/chromedriver"  # Your chromedriver path

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--auto-open-devtools-for-tabs")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.facebook.com")
        input("🔐 Please log in manually, then press ENTER here...")

        profile_url = "https://www.facebook.com/ram.orion.3"
        print(f"➡️ Navigating to profile: {profile_url}")
        driver.get(profile_url)

        # Scroll a lot
        scroll_count = 10
        for i in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"🔽 Scrolled {i+1}/{scroll_count} times...")
            time.sleep(2.5)

        input("⏳ Wait a bit if needed, then press ENTER to extract YouTube links...")

        # Dump HTML and extract
        html_source = driver.page_source
        with open("fb_profile_source.html", "w", encoding="utf-8") as f:
            f.write(html_source)
        print("✅ Saved page source to fb_profile_source.html")

        yt_links = extract_youtube_links_and_titles(html_source)
        print(f"🎵 Found {len(yt_links)} YouTube links with titles.")

        clean_html = make_clean_html(yt_links)
        with open("youtube_links.html", "w", encoding="utf-8") as f:
            f.write(clean_html)
        print("✅ Saved clean HTML with YouTube links to youtube_links.html")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
