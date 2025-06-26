# core/storage.py
"""Data storage module"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class StorageManager:
    """Manages all data persistence"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def save_weather(self, weather_data: Dict) -> None:
        """Save weather data to file"""
        filename = self.data_dir / "weather_history.csv"
        
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                weather_data.get('name', ''),
                weather_data.get('main', {}).get('temp', ''),
                weather_data.get('weather', [{}])[0].get('description', '')
            ])
    
    def load_history(self, limit: int = 10) -> List[Dict]:
        """Load recent weather history"""
        filename = self.data_dir / "weather_history.csv"
        
        if not filename.exists():
            return []
            
        history = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 4:
                    history.append({
                        'timestamp': row[0],
                        'city': row[1],
                        'temperature': float(row[2]),
                        'description': row[3]
                    })
        
        return history[-limit:]  # Return most recent entries
