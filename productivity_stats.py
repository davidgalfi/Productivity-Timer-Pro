# statistics.py - Create a new file for statistics functionality
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import numpy as np

class ProductivityStatsManager:
    def __init__(self, data_file="productivity_data.json"):
        self.data_file = data_file
        self.load_data()
        
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"sessions": [], "comfort_choices": 0, "total_pomodoros": 0}
    
    def get_daily_stats(self, days=7):
        """Get statistics for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_data = {}
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            daily_data[date_str] = {
                "total_time": 0,
                "sessions": 0,
                "pomodoros": 0,
                "activities": {}
            }
        
        for session in self.data.get("sessions", []):
            session_date = datetime.fromisoformat(session["start_time"]).strftime("%Y-%m-%d")
            if session_date in daily_data:
                daily_data[session_date]["total_time"] += session["duration"]
                daily_data[session_date]["sessions"] += 1
                
                if session.get("type") == "pomodoro":
                    daily_data[session_date]["pomodoros"] += 1
                
                activity = session["activity"]
                if activity not in daily_data[session_date]["activities"]:
                    daily_data[session_date]["activities"][activity] = 0
                daily_data[session_date]["activities"][activity] += session["duration"]
        
        return daily_data
    
    def get_activity_breakdown(self):
        """Get breakdown by activity type"""
        activities = {}
        for session in self.data.get("sessions", []):
            activity = session["activity"]
            if activity not in activities:
                activities[activity] = {"time": 0, "sessions": 0}
            activities[activity]["time"] += session["duration"]
            activities[activity]["sessions"] += 1
        return activities
    
    def get_productivity_score(self):
        """Calculate productivity score based on various metrics"""
        total_sessions = len(self.data.get("sessions", []))
        total_time = sum(s["duration"] for s in self.data.get("sessions", []))
        comfort_choices = self.data.get("comfort_choices", 0)
        pomodoros = self.data.get("total_pomodoros", 0)
        
        if total_sessions == 0:
            return 0
        
        # Calculate score (0-100)
        time_score = min(total_time / 3600, 10) * 10  # Max 10 points for 10+ hours
        session_score = min(total_sessions, 20) * 2   # Max 40 points for 20+ sessions
        pomodoro_score = min(pomodoros, 10) * 3       # Max 30 points for 10+ pomodoros
        comfort_penalty = min(comfort_choices * 2, 20) # Max -20 points
        
        score = max(0, time_score + session_score + pomodoro_score - comfort_penalty)
        return min(100, score)

class ProductivityStatsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.stats_manager = ProductivityStatsManager()
        self.create_window()
        
    def create_window(self):
        """Create the statistics window with animations"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Productivity Statistics")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f0f0f0")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_overview_tab()
        self.create_charts_tab()
        self.create_insights_tab()
        
        # Add fade-in animation
        self.fade_in_animation()
    
    def create_overview_tab(self):
        """Create overview tab with key metrics"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📈 Overview")
        
        # Title with animation
        title_frame = tk.Frame(overview_frame, bg="#2c3e50", height=80)
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎯 Productivity Dashboard", 
                              font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Metrics cards
        metrics_frame = tk.Frame(overview_frame, bg="#f0f0f0")
        metrics_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_metric_cards(metrics_frame)
        
        # Recent activity
        self.create_recent_activity(overview_frame)
    
    def create_metric_cards(self, parent):
        """Create animated metric cards"""
        cards_frame = tk.Frame(parent, bg="#f0f0f0")
        cards_frame.pack(fill="x", pady=20)
        
        # Calculate metrics
        total_time = sum(s["duration"] for s in self.stats_manager.data.get("sessions", []))
        total_sessions = len(self.stats_manager.data.get("sessions", []))
        productivity_score = self.stats_manager.get_productivity_score()
        comfort_choices = self.stats_manager.data.get("comfort_choices", 0)
        
        metrics = [
            ("⏱️", "Total Time", f"{total_time/3600:.1f}h", "#3498db"),
            ("📝", "Sessions", str(total_sessions), "#2ecc71"),
            ("🎯", "Productivity", f"{productivity_score:.0f}%", "#e74c3c"),
            ("😴", "Comfort Choices", str(comfort_choices), "#f39c12")
        ]
        
        self.metric_cards = []
        for i, (icon, title, value, color) in enumerate(metrics):
            card = self.create_animated_card(cards_frame, icon, title, value, color, i)
            self.metric_cards.append(card)
    
    def create_animated_card(self, parent, icon, title, value, color, index):
        """Create an animated metric card"""
        card_frame = tk.Frame(parent, bg="white", relief="raised", bd=2)
        card_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Icon
        icon_label = tk.Label(card_frame, text=icon, font=("Arial", 32), 
                             bg="white", fg=color)
        icon_label.pack(pady=(20, 5))
        
        # Title
        title_label = tk.Label(card_frame, text=title, font=("Arial", 12, "bold"), 
                              bg="white", fg="#34495e")
        title_label.pack()
        
        # Value with counter animation
        value_label = tk.Label(card_frame, text="0", font=("Arial", 24, "bold"), 
                              bg="white", fg=color)
        value_label.pack(pady=(5, 20))
        
        # Animate the value
        self.animate_counter(value_label, value, index * 200)
        
        # Hover effects
        self.add_hover_effect(card_frame, color)
        
        return card_frame
    
    def animate_counter(self, label, target_value, delay):
        """Animate counter from 0 to target value"""
        def start_animation():
            if target_value.replace(".", "").replace("%", "").replace("h", "").isdigit():
                target_num = float(target_value.replace("%", "").replace("h", ""))
                self.counter_animation(label, 0, target_num, target_value, 50)
            else:
                label.config(text=target_value)
        
        label.after(delay, start_animation)
    
    def counter_animation(self, label, current, target, original_text, steps):
        """Animate counter with smooth transition"""
        if steps > 0:
            increment = (target - current) / steps
            new_value = current + increment
            
            if "%" in original_text:
                label.config(text=f"{new_value:.0f}%")
            elif "h" in original_text:
                label.config(text=f"{new_value:.1f}h")
            else:
                label.config(text=f"{new_value:.0f}")
            
            label.after(20, lambda: self.counter_animation(label, new_value, target, original_text, steps-1))
        else:
            label.config(text=original_text)
    
    def add_hover_effect(self, widget, color):
        """Add hover effect to cards"""
        def on_enter(e):
            widget.config(bg="#ecf0f1", relief="raised", bd=3)
        
        def on_leave(e):
            widget.config(bg="white", relief="raised", bd=2)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
        for child in widget.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
    
    def create_recent_activity(self, parent):
        """Create recent activity section"""
        activity_frame = tk.LabelFrame(parent, text="📋 Recent Activity", 
                                     font=("Arial", 14, "bold"), bg="#f0f0f0")
        activity_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for recent sessions
        columns = ("Time", "Activity", "Duration", "Type")
        tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Add recent sessions
        recent_sessions = sorted(self.stats_manager.data.get("sessions", []), 
                               key=lambda x: x["start_time"], reverse=True)[:10]
        
        for session in recent_sessions:
            start_time = datetime.fromisoformat(session["start_time"]).strftime("%H:%M")
            duration = f"{session['duration']/60:.0f}m"
            session_type = session.get("type", "manual").title()
            
            tree.insert("", "end", values=(start_time, session["activity"], duration, session_type))
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(activity_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    
    def create_charts_tab(self):
        """Create charts tab with matplotlib visualizations"""
        charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(charts_frame, text="📊 Charts")
        
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.patch.set_facecolor('#f0f0f0')
        
        self.create_activity_pie_chart()
        self.create_daily_trend_chart()
        self.create_productivity_score_chart()
        self.create_pomodoro_chart()
        
        # Embed in tkinter
        canvas = FigureCanvasTkinter(self.fig, charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_activity_pie_chart(self):
        """Create activity breakdown pie chart"""
        activities = self.stats_manager.get_activity_breakdown()
        
        if activities:
            labels = list(activities.keys())
            sizes = [activities[activity]["time"]/3600 for activity in labels]
            colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
            
            wedges, texts, autotexts = self.ax1.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                                   colors=colors, startangle=90)
            self.ax1.set_title("📊 Time by Activity", fontsize=14, fontweight='bold')
            
            # Animate pie chart
            for wedge in wedges:
                wedge.set_linewidth(2)
                wedge.set_edgecolor('white')
        else:
            self.ax1.text(0.5, 0.5, "No data available", ha='center', va='center', transform=self.ax1.transAxes)
            self.ax1.set_title("📊 Time by Activity", fontsize=14, fontweight='bold')
    
    def create_daily_trend_chart(self):
        """Create daily productivity trend"""
        daily_stats = self.stats_manager.get_daily_stats(7)
        
        dates = list(daily_stats.keys())
        times = [daily_stats[date]["total_time"]/3600 for date in dates]
        
        self.ax2.plot(dates, times, marker='o', linewidth=3, markersize=8, color='#3498db')
        self.ax2.fill_between(dates, times, alpha=0.3, color='#3498db')
        self.ax2.set_title("📈 Daily Productivity (Hours)", fontsize=14, fontweight='bold')
        self.ax2.set_ylabel("Hours")
        self.ax2.tick_params(axis='x', rotation=45)
        self.ax2.grid(True, alpha=0.3)
    
    def create_productivity_score_chart(self):
        """Create productivity score gauge"""
        score = self.stats_manager.get_productivity_score()
        
        # Create gauge chart
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        # Background arc
        self.ax3.plot(theta, r, color='lightgray', linewidth=20)
        
        # Score arc
        score_theta = np.linspace(0, np.pi * (score/100), int(score))
        score_r = np.ones_like(score_theta)
        
        if score >= 80:
            color = '#2ecc71'
        elif score >= 60:
            color = '#f39c12'
        else:
            color = '#e74c3c'
        
        self.ax3.plot(score_theta, score_r, color=color, linewidth=20)
        
        # Add score text
        self.ax3.text(0, 0, f"{score:.0f}%", ha='center', va='center', 
                     fontsize=24, fontweight='bold', color=color)
        self.ax3.set_title("🎯 Productivity Score", fontsize=14, fontweight='bold')
        self.ax3.set_ylim(0, 1.2)
        self.ax3.axis('off')
    
    def create_pomodoro_chart(self):
        """Create Pomodoro sessions chart"""
        daily_stats = self.stats_manager.get_daily_stats(7)
        
        dates = list(daily_stats.keys())
        pomodoros = [daily_stats[date]["pomodoros"] for date in dates]
        
        bars = self.ax4.bar(dates, pomodoros, color='#e74c3c', alpha=0.8)
        self.ax4.set_title("🍅 Daily Pomodoros", fontsize=14, fontweight='bold')
        self.ax4.set_ylabel("Pomodoros")
        self.ax4.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, pomodoros):
            if value > 0:
                self.ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                             str(int(value)), ha='center', va='bottom', fontweight='bold')
    
    def create_insights_tab(self):
        """Create insights and recommendations tab"""
        insights_frame = ttk.Frame(self.notebook)
        self.notebook.add(insights_frame, text="💡 Insights")
        
        # Create scrollable frame
        canvas = tk.Canvas(insights_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(insights_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.generate_insights(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def generate_insights(self, parent):
        """Generate AI-like insights and recommendations"""
        insights = self.calculate_insights()
        
        for i, insight in enumerate(insights):
            self.create_insight_card(parent, insight, i)
    
    def calculate_insights(self):
        """Calculate insights based on user data"""
        insights = []
        
        # Analyze productivity patterns
        daily_stats = self.stats_manager.get_daily_stats(7)
        activities = self.stats_manager.get_activity_breakdown()
        score = self.stats_manager.get_productivity_score()
        comfort_choices = self.stats_manager.data.get("comfort_choices", 0)
        
        # Productivity score insight
        if score >= 80:
            insights.append({
                "icon": "🌟",
                "title": "Excellent Productivity!",
                "message": "You're maintaining high productivity levels. Keep up the great work!",
                "type": "success"
            })
        elif score >= 60:
            insights.append({
                "icon": "📈",
                "title": "Good Progress",
                "message": "You're on the right track. Consider increasing your Pomodoro sessions for better focus.",
                "type": "info"
            })
        else:
            insights.append({
                "icon": "🎯",
                "title": "Room for Improvement",
                "message": "Try setting smaller, achievable goals and use the Pomodoro technique more frequently.",
                "type": "warning"
            })
        
        # Comfort choices insight
        if comfort_choices > 5:
            insights.append({
                "icon": "💪",
                "title": "Comfort Zone Challenge",
                "message": f"You've chosen comfort {comfort_choices} times. Remember: growth happens outside your comfort zone!",
                "type": "warning"
            })
        
        # Activity diversity insight
        if len(activities) > 3:
            insights.append({
                "icon": "🎨",
                "title": "Great Activity Diversity",
                "message": "You're working on multiple types of activities. This helps prevent burnout and keeps you engaged!",
                "type": "success"
            })
        
        # Time-based insights
        total_time = sum(s["duration"] for s in self.stats_manager.data.get("sessions", []))
        if total_time > 7200:  # More than 2 hours
            insights.append({
                "icon": "⏰",
                "title": "Consistent Time Investment",
                "message": f"You've logged {total_time/3600:.1f} hours of productive time. Consistency is key to success!",
                "type": "success"
            })
        
        return insights
    
    def create_insight_card(self, parent, insight, index):
        """Create an animated insight card"""
        card_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        card_frame.pack(fill="x", padx=20, pady=10)
        
        # Color based on type
        colors = {
            "success": "#2ecc71",
            "info": "#3498db", 
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        color = colors.get(insight["type"], "#3498db")
        
        # Left border
        border_frame = tk.Frame(card_frame, bg=color, width=5)
        border_frame.pack(side="left", fill="y")
        
        # Content frame
        content_frame = tk.Frame(card_frame, bg="white")
        content_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        # Icon and title
        header_frame = tk.Frame(content_frame, bg="white")
        header_frame.pack(fill="x", pady=(0, 10))
        
        icon_label = tk.Label(header_frame, text=insight["icon"], font=("Arial", 20), bg="white")
        icon_label.pack(side="left")
        
        title_label = tk.Label(header_frame, text=insight["title"], 
                              font=("Arial", 14, "bold"), bg="white", fg="#2c3e50")
        title_label.pack(side="left", padx=(10, 0))
        
        # Message
        message_label = tk.Label(content_frame, text=insight["message"], 
                                font=("Arial", 11), bg="white", fg="#34495e", 
                                wraplength=400, justify="left")
        message_label.pack(fill="x")
        
        # Slide-in animation
        self.slide_in_animation(card_frame, index * 100)
    
    def slide_in_animation(self, widget, delay):
        """Animate widget sliding in from the right"""
        original_x = widget.winfo_x()
        widget.place(x=1000, y=widget.winfo_y())
        
        def animate():
            current_x = widget.winfo_x()
            if current_x > original_x:
                new_x = current_x - 50
                widget.place(x=max(new_x, original_x))
                widget.after(20, animate)
            else:
                widget.pack(fill="x", padx=20, pady=10)
        
        widget.after(delay, animate)
    
    def fade_in_animation(self):
        """Fade in the entire window"""
        self.window.attributes('-alpha', 0.0)
        self.fade_step(0.0)
    
    def fade_step(self, alpha):
        """Step function for fade animation"""
        alpha += 0.05
        self.window.attributes('-alpha', alpha)
        if alpha < 1.0:
            self.window.after(30, lambda: self.fade_step(alpha))
