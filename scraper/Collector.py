import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException



class Collector:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_request(self, url, use_selenium=False):
        # Setup Selenium driver only if needed
        if use_selenium:
            options = Options()
            options.add_argument("--headless")  # run browser in headless mode
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
                time.sleep(1)  # give time for JS to load
                print(f"✅ (Selenium) Request successful: {url}")
                return BeautifulSoup(driver.page_source, "html.parser")
            except (TimeoutException, WebDriverException) as e:
                print(f"❌ Selenium error: {e}")
                return None
            finally:
                driver.quit()
        else:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }

            try:
                import requests  # placed here to avoid unnecessary import when using Selenium
                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()

                if "captcha" in response.text.lower() or "access denied" in response.text.lower():
                    print("⚠️ Site may be blocking your request.")
                    return None

                print(f"✅ Request successful: {url}")
                return BeautifulSoup(response.content, "html.parser")

            except requests.exceptions.HTTPError as http_err:
                print(f"❌ HTTP error: {http_err}")
            except requests.exceptions.ConnectionError:
                print("❌ Connection error.")
            except requests.exceptions.Timeout:
                print("❌ Request timed out.")
            except requests.exceptions.RequestException as err:
                print(f"❌ Request error: {err}")

            return None

    def get_categories(self):
        main_soup = self.make_request(self.base_url, False)
        category_soup_objs = {}

        if main_soup:
            for a in main_soup.find_all("a"):
                p_tag = a.find("p")
                category_name = p_tag.text if p_tag else None

                if category_name and category_name != "Movie":
                    cleaned_url = self.base_url[:-3]
                    full_url = cleaned_url + a['href']
                    category_soup_objs[category_name] = self.make_request(full_url, True)

        return category_soup_objs
