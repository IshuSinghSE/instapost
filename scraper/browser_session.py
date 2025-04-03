from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
import os

class BrowserSession:
    def __init__(self, session_file="session.pkl"):
        self.session_file = session_file
        self.driver = None

    def initialize_browser(self):
        options = webdriver.EdgeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Edge(options=options)

    def load_session(self):
        if os.path.exists(self.session_file):
            print("Loading session from file...")
            with open(self.session_file, "rb") as file:
                cookies = pickle.load(file)
            self.driver.get("https://www.instagram.com/")
            for cookie in cookies:
                # Ensure the cookie domain matches the current domain
                if "domain" in cookie and cookie["domain"].startswith("."):
                    cookie["domain"] = cookie["domain"].lstrip(".")
                try:
                    self.driver.add_cookie(cookie)
                    print(f"Added cookie: {cookie}")
                except Exception as e:
                    print(f"Error adding cookie: {e}")
            self.driver.refresh()
            print("Session loaded and browser refreshed.")
        else:
            print("No session file found. Starting fresh.")

    def save_session(self):
        try:
            cookies = self.driver.get_cookies()
            with open(self.session_file, "wb") as file:
                pickle.dump(cookies, file)
            print(f"Session saved successfully with {len(cookies)} cookies.")
        except Exception as e:
            print(f"Error saving session: {e}")

    def login(self, username, password):
        self.driver.get("https://www.instagram.com/")
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
            )
            password_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
            )
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_button.click()
            print("Login successful.")
        except Exception as e:
            print(f"Error during login: {e}")
            self.driver.quit()
            raise

    def close_browser(self):
        if self.driver:
            self.driver.quit()
