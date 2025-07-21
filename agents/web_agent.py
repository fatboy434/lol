from agents.agent_base import AgentBase
import requests
from bs4 import BeautifulSoup

class WebAgent(AgentBase):
    def __init__(self, agent_manager):
        super().__init__(agent_manager)

    def run(self):
        # This agent is reactive, so it doesn't have a main loop.
        pass

    def receive_message(self, message):
        if message["type"] == "scrape_website":
            html = self.scrape_website(message["url"])
            if html:
                text = self.parse_html(html)
                self.send_message("ProfitSeekerAgent", {"type": "website_data", "data": text})

    def scrape_website(self, url):
        """
        Scrapes a website and returns the HTML content.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.send_message("SpeechAgent", f"Error scraping website: {e}")
            return None

    def parse_html(self, html):
        """
        Parses HTML content and returns the text.
        """
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
