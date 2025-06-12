import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta

class ProductivityTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Productivity Timer Pro")
        self.root.geometry("800x600")
        
        # Data storage
        self.data_file = "productivity_data.json"
        self.load_data()
        
        # Timer state
        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.current_activity = ""
        
        # Pomodoro settings
        self.pomodoro_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60     # 5 minutes in seconds
        self.long_break_duration = 15 * 60  # 15 minutes in seconds
        self.pomodoro_count = 0
        
        # Comfort counter
        self.comfort_choices = 0
        
        self.setup_ui()
        
    def load_data(self):
        """Load existing data from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "sessions": [],
                "comfort_choices": 0,
                "total_pomodoros": 0
            }
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def setup_ui(self):
        """Initialize the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Productivity Timer Pro", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Timer display
        self.time_var = tk.StringVar(value="00:00:00")
        time_display = ttk.Label(main_frame, textvariable=self.time_var, 
                                font=("Arial", 24, "bold"))
        time_display.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Activity selection
        ttk.Label(main_frame, text="Current Activity:").grid(row=2, column=0, sticky=tk.W)
        self.activity_var = tk.StringVar()
        self.activity_combo = ttk.Combobox(main_frame, textvariable=self.activity_var,
                                          values=["Work", "Study", "Exercise", "Reading", 
                                                 "Project", "Learning", "Other"])
        self.activity_combo.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ProductivityTimer()
    app.run()
