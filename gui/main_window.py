# gui/main_window.py
"""Main application window"""

import tkinter as tk
from typing import Callable, Dict


class MainWindow:
    """Main application window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")

        # Callbacks storage
        self.callbacks: Dict[str, Callable] = {}

        # Store last fetched weather description
        self.last_description = ""

        self.setup_ui()

    def setup_ui(self):
        """Initialize UI components"""
        # Header
        self.header_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        self.header_frame.pack(fill=tk.X)
        title_label = tk.Label(self.header_frame, text="Weather Dashboard", bg='#2196F3', fg="white", font=("Arial", 20))
        title_label.pack(pady=10)

        # Content Frame
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(pady=20)

        # City entry
        city_label = tk.Label(self.content_frame, text="Enter city:")
        city_label.grid(row=0, column=0, padx=5)
        self.city_entry = tk.Entry(self.content_frame)
        self.city_entry.grid(row=0, column=1, padx=5)

        # Search button
        search_button = tk.Button(self.content_frame, text="Get Weather", command=self.handle_search)
        search_button.grid(row=0, column=2, padx=5)

        # Activity Suggester Button
        self.activity_button = tk.Button(self.content_frame, text="Suggest Activity", command=self.handle_activity_suggest)
        self.activity_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Activity suggestion display label
        self.activity_label = tk.Label(self.content_frame, text="", font=("Arial", 12), fg="green", wraplength=500, justify="left")
        self.activity_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Result display
        self.result_label = tk.Label(self.content_frame, text="", font=("Arial", 14), wraplength=500, justify="left")
        self.result_label.grid(row=1, column=0, columnspan=3, pady=10)

    def register_callback(self, event: str, callback: Callable):
        """Register event callbacks"""
        self.callbacks[event] = callback

    def trigger_callback(self, event: str, *args, **kwargs):
        """Trigger a registered callback"""
        if event in self.callbacks:
            return self.callbacks[event](*args, **kwargs)

    def handle_search(self):
        city = self.city_entry.get()
        if city and "search" in self.callbacks:
            result = self.trigger_callback("search", city)
            if result:
                self.result_label.config(text=result)
                # Save description from result string if possible
                # Assume result format: "City: 22°C, clear sky" 
                # We'll parse description as substring after last comma
                if ',' in result:
                    self.last_description = result.split(',')[-1].strip()
                else:
                    self.last_description = ""
            else:
                self.result_label.config(text="Could not fetch weather.")
                self.last_description = ""
        else:
            self.result_label.config(text="Please enter a city name.")
            self.last_description = ""

    def handle_activity_suggest(self):
        if not self.last_description:
            self.activity_label.config(text="Get weather first to suggest activity.")
            return

        if "activity_suggest" in self.callbacks:
            suggestion = self.trigger_callback("activity_suggest", self.last_description)
            if suggestion:
                self.activity_label.config(text=f"Suggested activity: {suggestion}")
            else:
                self.activity_label.config(text="No suggestions available.")
        else:
            self.activity_label.config(text="Activity suggest feature not available.")        

    def run(self):
        """Start the main event loop"""
        self.root.mainloop()
