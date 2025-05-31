from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import urllib.parse


def extract_youtube_links_and_titles(html):
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a", href=True)

    results = []
    for a in anchors:
        raw_href = a["href"]
        if "l.facebook.com/l.php?u=" in raw_href and "youtu" in raw_href:
            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_href).query)
            actual_url = parsed.get("u", [""])[0]
            # Try to find the text that looks like a title nearby
            title = a.get_text(strip=True)
            if not title:
                title = a.find_next(string=True)
            results.append((actual_url, title))
    return results


def make_clean_html(yt_links):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>YouTube Links Extracted from Facebook</title>
    <style>
        body { font-family: sans-serif; padding: 2em; background: #f9f9f9; }
        .entry { margin-bottom: 1.5em; padding: 1em; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        a { color: #0654ba; text-decoration: none; font-weight: bold; display: block; margin-bottom: 0.5em; }
    </style>
</head>
<body>
<h1>YouTube Links Extracted from Facebook</h1>
"""

    for url, title in yt_links:
        html += f'<div class="entry">\n<a href="{url}" target="_blank">{url}</a>\n<p>{title}</p>\n</div>\n'

    html += "</body>\n</html>"
    return html


def main():
    options = Options()
    options.add_argument("--width=1200")
    options.add_argument("--height=800")

    # Launch Firefox
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://www.facebook.com")
        input("🔐 Please log in manually, then press ENTER here...")

        profile_url = "https://www.facebook.com/ram.orion.3"
        print(f"➡️ Navigating to profile: {profile_url}")
        driver.get(profile_url)

        # Scroll many times to load content
        scroll_count = 12
        for i in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"🔽 Scrolled {i+1}/{scroll_count} times...")
            time.sleep(2.5)

        input("⏳ Wait a bit if needed, then press ENTER to extract YouTube links...")

        # Save full HTML source
        html_source = driver.page_source
        with open("fb_profile_source.html", "w", encoding="utf-8") as f:
            f.write(html_source)
        print("✅ Saved full page source to fb_profile_source.html")

        # Extract YouTube links and titles
        yt_links = extract_youtube_links_and_titles(html_source)
        print(f"🎵 Found {len(yt_links)} YouTube links.")

        # Save nicely formatted HTML with only the links
        clean_html = make_clean_html(yt_links)
        with open("youtube_links.html", "w", encoding="utf-8") as f:
            f.write(clean_html)
        print("✅ Saved cleaned HTML to youtube_links.html")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()