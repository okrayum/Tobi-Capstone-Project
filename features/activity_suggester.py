# features/activity_suggester.py

import random

class ActivitySuggester:
    def __init__(self):
        self.activity_map = {
            "clear": ["Go for a walk", "Have a picnic"],
            "clouds": ["Visit a museum", "Go to a coffee shop"],
            "rain": ["Read a book", "Watch a movie"],
            "snow": ["Build a snowman", "Drink hot chocolate"],
            "default": ["Relax at home", "Do some journaling"]
        }
    
    def suggest(self, description):
        key = next((k for k in self.activity_map if k in description.lower()), "default")
        return random.choice(self.activity_map[key])
