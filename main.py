import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta

from productivity_stats import ProductivityStatsWindow

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

        # Add statistics button to the main UI
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Analytics", padding="10")
        stats_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        stats_btn = ttk.Button(stats_frame, text="📈 View Statistics", 
                              command=self.show_statistics,
                              style="Accent.TButton")
        stats_btn.grid(row=0, column=0, padx=5)
        
        export_btn = ttk.Button(stats_frame, text="📤 Export Data", 
                               command=self.export_data)
        export_btn.grid(row=0, column=1, padx=5)

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
        
        # Timer controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=3, column=0, columnspan=3, pady=(10, 20))
        
        self.start_btn = ttk.Button(controls_frame, text="Start", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(controls_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(controls_frame, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        self.reset_btn = ttk.Button(controls_frame, text="Reset", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        # Pomodoro controls
        pomodoro_frame = ttk.LabelFrame(main_frame, text="Pomodoro Timer", padding="10")
        pomodoro_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.pomodoro_btn = ttk.Button(pomodoro_frame, text="Start Pomodoro (25 min)", 
                                      command=self.start_pomodoro)
        self.pomodoro_btn.grid(row=0, column=0, padx=5)
        
        self.break_btn = ttk.Button(pomodoro_frame, text="Take Break (5 min)", 
                                   command=self.start_break, state="disabled")
        self.break_btn.grid(row=0, column=1, padx=5)
        
        # Comfort choice counter
        comfort_frame = ttk.LabelFrame(main_frame, text="Productivity Tracking", padding="10")
        comfort_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.comfort_var = tk.StringVar(value=f"Comfort Choices: {self.data.get('comfort_choices', 0)}")
        comfort_label = ttk.Label(comfort_frame, textvariable=self.comfort_var)
        comfort_label.grid(row=0, column=0, padx=5)
        
        self.comfort_btn = ttk.Button(comfort_frame, text="I Chose Comfort", 
                                     command=self.increment_comfort, 
                                     style="Accent.TButton")
        self.comfort_btn.grid(row=0, column=1, padx=5)
        
        # Start the timer update loop
        self.update_timer()
    
    def start_timer(self):
        """Start the timer"""
        if not self.activity_var.get():
            tk.messagebox.showwarning("Warning", "Please select an activity first!")
            return
            
        self.is_running = True
        self.start_time = datetime.now()
        self.current_activity = self.activity_var.get()
        
        # Update button states
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.pomodoro_btn.config(state="disabled")
    
    def pause_timer(self):
        """Pause/resume the timer"""
        if self.is_running:
            self.is_running = False
            self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
            self.pause_btn.config(text="Resume")
            self.start_btn.config(state="normal")
        else:
            self.is_running = True
            self.start_time = datetime.now()
            self.pause_btn.config(text="Pause")
            self.start_btn.config(state="disabled")
    
    def stop_timer(self):
        """Stop the timer and save session"""
        if self.is_running:
            self.elapsed_time += (datetime.now() - self.start_time).total_seconds()
            self.is_running = False
        
        # Save session data
        if self.elapsed_time > 0:
            session = {
                "activity": self.current_activity,
                "duration": self.elapsed_time,
                "start_time": (datetime.now() - timedelta(seconds=self.elapsed_time)).isoformat(),
                "end_time": datetime.now().isoformat(),
                "type": "manual"
            }
            self.data["sessions"].append(session)
            self.save_data()
        
        self.reset_timer()
    
    def reset_timer(self):
        """Reset the timer to initial state"""
        self.is_running = False
        self.elapsed_time = 0
        self.start_time = None
        self.time_var.set("00:00:00")
        
        # Reset button states
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="Pause")
        self.stop_btn.config(state="disabled")
        self.pomodoro_btn.config(state="normal")
    
    def start_pomodoro(self):
        """Start a Pomodoro session"""
        if not self.activity_var.get():
            tk.messagebox.showwarning("Warning", "Please select an activity first!")
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        self.current_activity = self.activity_var.get()
        self.pomodoro_mode = True
        self.pomodoro_end_time = datetime.now() + timedelta(seconds=self.pomodoro_duration)
        
        # Update button states
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.pomodoro_btn.config(state="disabled")
    
    def start_break(self):
        """Start a break session"""
        self.activity_var.set("Break")
        self.is_running = True
        self.start_time = datetime.now()
        self.current_activity = "Break"
        self.break_mode = True
        self.break_end_time = datetime.now() + timedelta(seconds=self.break_duration)
        
        self.break_btn.config(state="disabled")
    
    def increment_comfort(self):
        """Increment the comfort choice counter"""
        self.data["comfort_choices"] = self.data.get("comfort_choices", 0) + 1
        self.comfort_var.set(f"Comfort Choices: {self.data['comfort_choices']}")
        self.save_data()
        
        # Show a motivational message
        tk.messagebox.showinfo("Comfort Choice Recorded", 
                              "Remember: Every small step towards your goals matters! 💪")
    
    def update_timer(self):
        """Update the timer display"""
        if self.is_running and self.start_time:
            current_elapsed = self.elapsed_time + (datetime.now() - self.start_time).total_seconds()
            
            # Check for Pomodoro completion
            if hasattr(self, 'pomodoro_mode') and self.pomodoro_mode:
                if datetime.now() >= self.pomodoro_end_time:
                    self.complete_pomodoro()
                    return
            
            # Check for break completion
            if hasattr(self, 'break_mode') and self.break_mode:
                if datetime.now() >= self.break_end_time:
                    self.complete_break()
                    return
        else:
            current_elapsed = self.elapsed_time
        
        # Format and display time
        hours = int(current_elapsed // 3600)
        minutes = int((current_elapsed % 3600) // 60)
        seconds = int(current_elapsed % 60)
        self.time_var.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Schedule next update
        self.root.after(1000, self.update_timer)
    
    def complete_pomodoro(self):
        """Handle Pomodoro completion"""
        self.data["total_pomodoros"] = self.data.get("total_pomodoros", 0) + 1
        self.pomodoro_count += 1
        
        # Save the session
        session = {
            "activity": self.current_activity,
            "duration": self.pomodoro_duration,
            "start_time": (self.pomodoro_end_time - timedelta(seconds=self.pomodoro_duration)).isoformat(),
            "end_time": self.pomodoro_end_time.isoformat(),
            "type": "pomodoro"
        }
        self.data["sessions"].append(session)
        self.save_data()
        
        # Reset timer state
        self.pomodoro_mode = False
        self.reset_timer()
        
        # Enable break button
        self.break_btn.config(state="normal")
        
        tk.messagebox.showinfo("Pomodoro Complete!", 
                              f"Great job! You completed a Pomodoro session.\nTotal Pomodoros today: {self.pomodoro_count}")
    
    def complete_break(self):
        """Handle break completion"""
        # Save break session
        session = {
            "activity": "Break",
            "duration": self.break_duration,
            "start_time": (self.break_end_time - timedelta(seconds=self.break_duration)).isoformat(),
            "end_time": self.break_end_time.isoformat(),
            "type": "break"
        }
        self.data["sessions"].append(session)
        self.save_data()
        
        # Reset timer state
        self.break_mode = False
        self.reset_timer()
        self.break_btn.config(state="disabled")
        
        tk.messagebox.showinfo("Break Complete!", "Break time is over. Ready for another Pomodoro?")

    def run(self):
        """Start the application"""
        self.root.mainloop()


    def show_statistics(self):
        """Show statistics window"""
        ProductivityStatsWindow(self.root)

    def export_data(self):
        """Export data to CSV"""
        import csv
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Start Time", "End Time", "Activity", "Duration (minutes)", "Type"])
                
                for session in self.data["sessions"]:
                    writer.writerow([
                        session["start_time"],
                        session["end_time"], 
                        session["activity"],
                        round(session["duration"] / 60, 2),
                        session.get("type", "manual")
                    ])
            
            tk.messagebox.showinfo("Export Complete", f"Data exported to {filename}")
              
if __name__ == "__main__":
    app = ProductivityTimer()
    app.run()
