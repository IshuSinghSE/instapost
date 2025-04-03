# %%
#Import dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import requests
from bs4 import BeautifulSoup
import re
import config
import json
import os
from urllib.parse import urlparse
import csv
from browser_session import BrowserSession
from instagram_scraper import InstagramScraper
from downloader import Downloader

def main():
    session = BrowserSession()
    session.initialize_browser()
    try:
        session.load_session()
        if not session.driver.get_cookies():
            print("No cookies found. Logging in...")
            session.login(config.username, config.password)
            session.save_session()
        else:
            print("Cookies loaded successfully. Skipping login.")

        scraper = InstagramScraper(session.driver)
        scraper.search_account(config.account)
        post_urls = scraper.scrape_posts()
        print(f"Found {len(post_urls)} posts.")

        json_data = scraper.fetch_post_data(post_urls)
        all_urls, all_dates = [], []
        for data in json_data:
            items = data.get('items', [])
            for item in items:
                date_taken = item.get('taken_at')
                carousel_media = item.get('carousel_media', [])
                for media in carousel_media:
                    image_url = media.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
                    if image_url:
                        all_urls.append(image_url)
                        all_dates.append(date_taken)
                    video_versions = media.get('video_versions', [])
                    if video_versions:
                        video_url = video_versions[0].get('url')
                        if video_url:
                            all_urls.append(video_url)
                            all_dates.append(date_taken)
                image_url = item.get('image_versions2', {}).get('candidates', [{}])[0].get('url')
                if image_url:
                    all_urls.append(image_url)
                    all_dates.append(date_taken)
                video_versions = item.get('video_versions', [])
                if video_versions:
                    video_url = video_versions[0].get('url')
                    if video_url:
                        all_urls.append(video_url)
                        all_dates.append(date_taken)

        downloader = Downloader(config.account.lstrip("@"))
        downloader.download_files(all_urls, all_dates)
    finally:
        session.close_browser()

if __name__ == "__main__":
    main()