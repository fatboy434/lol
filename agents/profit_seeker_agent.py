from agents.agent_base import AgentBase
import logging
import time
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ProfitSeekerAgent(AgentBase):
    def __init__(self, agent_manager, ai_core):
        super().__init__(agent_manager)
        self.ai_core = ai_core
        self.profit_log = "profit_opportunities.log"
        logging.basicConfig(filename=self.profit_log, level=logging.INFO, format='%(asctime)s - %(message)s')
        self.is_scraping = False
        self.patterns = []

    def start_scraping(self):
        """
        Starts the real-time screen scraping.
        """
        self.is_scraping = True
        self.send_message("SpeechAgent", "Starting real-time screen scraping.")
        while self.is_scraping:
            text = self.ai_core.capture_screen_text()
            self.receive_message(text)
            time.sleep(5)

    def stop_scraping(self):
        """
        Stops the real-time screen scraping.
        """
        self.is_scraping = False
        self.send_message("SpeechAgent", "Stopping real-time screen scraping.")

    def fetch_api_data(self, url):
        """
        Fetches data from an API.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.send_message("SpeechAgent", f"Error fetching API data: {e}")
            return None

    def add_pattern(self, pattern):
        """
        Adds a new pattern to the list of patterns.
        """
        self.patterns.append(pattern)
        self.send_message("SpeechAgent", f"Added new pattern: {pattern}")

    def log_opportunity(self, opportunity):
        """
        Logs a profit opportunity to the profit log.
        """
        logging.info(opportunity)
        self.send_message("SpeechAgent", f"Found a new profit opportunity: {opportunity}")

    def match_patterns(self, text):
        """
        Matches the patterns against the given text.
        """
        for pattern in self.patterns:
            matches = re.findall(pattern, text)
            if matches:
                self.log_opportunity(f"Found matches for pattern '{pattern}': {matches}")

    def parse_html(self, html):
        """
        Parses HTML content and returns the text.
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()

    def scrape_dynamic_website(self, url):
        """
        Scrapes a dynamic website using Selenium.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        text = self.parse_html(driver.page_source)
        driver.quit()
        return text

    def analyze_data(self, data):
        """
        Analyzes the scraped data and decides what to do with it.
        """
        # In a real implementation, this would be a call to an LLM API.
        # For now, we'll just log the data as a profit opportunity.
        self.log_opportunity(f"Analyzed data: {data}")
        # In a real implementation, the LLM would return an action to take.
        # For now, we'll just return a mock action.
        return "alert"

    def receive_message(self, message):
        """
        This plugin will be responsible for scraping websites and APIs for profitable trends, prices, or signals.
        """
        if isinstance(message, dict) and message.get("type") == "website_data":
            action = self.analyze_data(message["data"])
            self.take_action(action, message["data"])
        elif "start scraping" in message:
            self.start_scraping()
        elif "stop scraping" in message:
            self.stop_scraping()
        elif "add pattern" in message:
            pattern = message.split("add pattern ")[1]
            self.add_pattern(pattern)
        elif "fetch api" in message:
            url = message.split("fetch api ")[1]
            api_data = self.fetch_api_data(url)
            if api_data:
                action = self.analyze_data(str(api_data))
                self.take_action(action, str(api_data))
        else:
            self.match_patterns(message)

    def take_action(self, action, data):
        """
        Takes action based on the analyzed data.
        """
        if action == "alert":
            self.send_message("SpeechAgent", f"Alert: {data}")
        elif action == "save":
            with open("saved_data.txt", "a") as f:
                f.write(data + "\n")
            self.send_message("SpeechAgent", "Data saved.")
        else:
            self.send_message("SpeechAgent", f"Unknown action: {action}")
