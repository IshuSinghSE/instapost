from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

class InstagramScraper:
    def __init__(self, driver):
        self.driver = driver

    def search_account(self, account):
        try:
            time.sleep(2)  # Allow page to load
            search_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='Search']"))
            )
            search_icon.click()
            time.sleep(2)  # Allow search box to appear
            searchbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
            )
            searchbox.clear()
            searchbox.send_keys(account)
            time.sleep(2)  # Allow search results to load
            first_result = self.driver.find_element(By.XPATH, f'//span[text()="{account.lstrip("@")}"]')
            first_result.click()
        except Exception as e:
            print(f"Error during account search: {e}")
            raise

    def scrape_posts(self):
        soups = []
        initial_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            html = self.driver.page_source
            soups.append(BeautifulSoup(html, 'html.parser'))
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_height == initial_height:
                break
            initial_height = current_height

        post_urls = []
        for soup in soups:
            anchors = soup.find_all('a', href=True)
            post_urls.extend([a['href'] for a in anchors if a['href'].startswith(("/p/", "/reel/"))])
        return list(set(post_urls))

    def fetch_post_data(self, post_urls):
        json_list = []
        query_parameters = "__a=1&__d=dis"
        for url in post_urls:
            try:
                self.driver.get(f"https://www.instagram.com{url}?{query_parameters}")
                time.sleep(1)
                pre_tag = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//pre'))
                )
                json_data = json.loads(pre_tag.text)
                json_list.append(json_data)
            except Exception as e:
                print(f"Error fetching post data for {url}: {e}")
        return json_list
