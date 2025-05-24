from selenium import webdriver
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
