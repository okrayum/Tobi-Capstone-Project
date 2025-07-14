# main.py
"""Main application entry point"""

from dotenv import load_dotenv
import os
from gui.main_window import MainWindow
from core.api import WeatherAPI
from core.processor import DataProcessor
from core.storage import StorageManager
from features.activity_suggester import ActivitySuggester

class WeatherDashboardApp:
    """Main application controller"""

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            raise ValueError("Missing WEATHER_API_KEY in environment variables.")
        
        # Initialize core modules
        self.api = WeatherAPI(api_key)
        self.processor = DataProcessor()
        self.storage = StorageManager()
        self.activity_suggester = ActivitySuggester()

        # Initialize GUI
        self.window = MainWindow()

        # Store last fetched description for activity suggestions
        self.last_description = ""

        # Register GUI callbacks
        self.window.register_callback("search", self.handle_search)
        self.window.register_callback("activity_suggest", self.handle_activity_suggest)

    def handle_search(self, city: str):
        """Fetch, process, save weather and update GUI"""
        raw_data = self.api.fetch_weather(city)
        if not raw_data:
            return None

        weather_data = self.processor.process_api_response(raw_data)
        self.storage.save_weather(raw_data)

        # Update last description for activity suggestions
        self.last_description = weather_data.get('description', '')

        # Format display string
        display_text = f"{weather_data.get('city', city)}: {weather_data.get('temperature', 'N/A')}°C, {self.last_description}"
        return display_text

    def handle_activity_suggest(self, description: str):
        """Return activity suggestion based on weather description"""
        if not description:
            return None
        return self.activity_suggester.suggest(description)

    def run(self):
        """Start the application"""
        self.window.run()


if __name__ == "__main__":
    app = WeatherDashboardApp()
    app.run()
