
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import time
from datetime import datetime, timedelta

class ModernClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Clock")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Variables
        self.mode = "clock"  # clock, stopwatch, timer
        self.stopwatch_running = False
        self.stopwatch_time = 0
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_set_seconds = 0
        self.settings_window = None
        
        # Color scheme - Modern dark theme
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_bg = "#313244"
        self.button_hover = "#45475a"
        self.danger_color = "#f38ba8"
        
        # Setup UI
        self.setup_ui()
        
        # Enable dragging (only on time display)
        self.time_label.bind('<Button-1>', self.start_drag)
        self.time_label.bind('<B1-Motion>', self.on_drag)
        
        # Start clock update
        self.update_display()
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container with rounded corners effect
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=12,
                                   highlightthickness=2, highlightbackground=self.accent_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Time display - Large and centered
        self.time_label = tk.Label(self.main_frame, text="00:00:00", 
                                   font=("Segoe UI", 56, "bold"),
                                   bg=self.bg_color, fg=self.accent_color,
                                   cursor="fleur")  # Move cursor
        self.time_label.pack(pady=(5, 5))
        
        # Bottom control bar - Small buttons
        bottom_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Mode indicator (small text)
        self.mode_label = tk.Label(bottom_frame, text="CLOCK", 
                                   font=("Segoe UI", 8),
                                   bg=self.bg_color, fg=self.fg_color)
        self.mode_label.pack(side=tk.LEFT)
        
        # Right side buttons
        button_frame = tk.Frame(bottom_frame, bg=self.bg_color)
        button_frame.pack(side=tk.RIGHT)
        
        # Settings button
        self.settings_btn = tk.Label(button_frame, text="⚙", font=("Segoe UI", 14),
                                     bg=self.bg_color, fg=self.fg_color, cursor="hand2",
                                     padx=4, pady=0)
        self.settings_btn.pack(side=tk.LEFT, padx=2)
        self.settings_btn.bind('<Button-1>', lambda e: self.open_settings())
        self.settings_btn.bind('<Enter>', lambda e: self.settings_btn.config(fg=self.accent_color))
        self.settings_btn.bind('<Leave>', lambda e: self.settings_btn.config(fg=self.fg_color))
        
        # Close button
        close_btn = tk.Label(button_frame, text="✕", font=("Segoe UI", 12),
                            bg=self.bg_color, fg=self.fg_color, cursor="hand2",
                            padx=4, pady=0)
        close_btn.pack(side=tk.LEFT, padx=2)
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg=self.danger_color))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg=self.fg_color))
        
    def open_settings(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
        
        # Create settings popup
        self.settings_window = Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.configure(bg=self.bg_color)
        self.settings_window.resizable(False, False)
        self.settings_window.attributes('-topmost', True)
        
        # Position near main window
        x = self.root.winfo_x() + self.root.winfo_width() + 10
        y = self.root.winfo_y()
        self.settings_window.geometry(f"+{x}+{y}")
        
        main_frame = tk.Frame(self.settings_window, bg=self.bg_color, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text="⚙ Settings", font=("Segoe UI", 12, "bold"),
                        bg=self.bg_color, fg=self.accent_color)
        title.pack(pady=(0, 15))
        
        # Mode selection
        mode_label = tk.Label(main_frame, text="Mode:", font=("Segoe UI", 10),
                             bg=self.bg_color, fg=self.fg_color)
        mode_label.pack(anchor=tk.W, pady=(0, 5))
        
        mode_frame = tk.Frame(main_frame, bg=self.bg_color)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        modes = [
            ("🕐 Clock", "clock"),
            ("⏱ Stopwatch", "stopwatch"),
            ("⏲ Timer", "timer")
        ]
        
        for text, mode in modes:
            btn = self.create_popup_button(mode_frame, text, 
                                          lambda m=mode: self.switch_mode_from_popup(m))
            btn.pack(side=tk.LEFT, padx=3)
        
        # Stopwatch controls (if in stopwatch mode)
        self.stopwatch_controls_frame = tk.Frame(main_frame, bg=self.bg_color)
        
        sw_label = tk.Label(self.stopwatch_controls_frame, text="Stopwatch Controls:", 
                           font=("Segoe UI", 10),
                           bg=self.bg_color, fg=self.fg_color)
        sw_label.pack(anchor=tk.W, pady=(0, 5))
        
        sw_btn_frame = tk.Frame(self.stopwatch_controls_frame, bg=self.bg_color)
        sw_btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.sw_start_btn = self.create_popup_button(sw_btn_frame, "▶ Start", 
                                                     self.toggle_stopwatch)
        self.sw_start_btn.pack(side=tk.LEFT, padx=3)
        
        sw_reset_btn = self.create_popup_button(sw_btn_frame, "⟲ Reset", 
                                                self.reset_stopwatch)
        sw_reset_btn.pack(side=tk.LEFT, padx=3)
        
        # Timer controls (if in timer mode)
        self.timer_controls_frame = tk.Frame(main_frame, bg=self.bg_color)
        
        timer_label = tk.Label(self.timer_controls_frame, text="Timer Settings:", 
                              font=("Segoe UI", 10),
                              bg=self.bg_color, fg=self.fg_color)
        timer_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Timer input
        timer_input_frame = tk.Frame(self.timer_controls_frame, bg=self.bg_color)
        timer_input_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(timer_input_frame, text="Minutes:", font=("Segoe UI", 9),
                bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=(0, 5))
        
        self.minutes_entry = tk.Entry(timer_input_frame, width=4, font=("Segoe UI", 10),
                                      justify='center', bg=self.button_bg, fg=self.fg_color,
                                      insertbackground=self.fg_color, relief=tk.FLAT)
        self.minutes_entry.pack(side=tk.LEFT, padx=2)
        self.minutes_entry.insert(0, "05")
        
        tk.Label(timer_input_frame, text="Seconds:", font=("Segoe UI", 9),
                bg=self.bg_color, fg=self.fg_color).pack(side=tk.LEFT, padx=(10, 5))
        
        self.seconds_entry = tk.Entry(timer_input_frame, width=4, font=("Segoe UI", 10),
                                      justify='center', bg=self.button_bg, fg=self.fg_color,
                                      insertbackground=self.fg_color, relief=tk.FLAT)
        self.seconds_entry.pack(side=tk.LEFT, padx=2)
        self.seconds_entry.insert(0, "00")
        
        # Timer buttons
        timer_btn_frame = tk.Frame(self.timer_controls_frame, bg=self.bg_color)
        timer_btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        timer_start_btn = self.create_popup_button(timer_btn_frame, "▶ Start", 
                                                   self.start_timer)
        timer_start_btn.pack(side=tk.LEFT, padx=3)
        
        timer_pause_btn = self.create_popup_button(timer_btn_frame, "⏸ Pause", 
                                                   self.pause_timer)
        timer_pause_btn.pack(side=tk.LEFT, padx=3)
        
        timer_reset_btn = self.create_popup_button(timer_btn_frame, "⟲ Reset", 
                                                   self.reset_timer)
        timer_reset_btn.pack(side=tk.LEFT, padx=3)
        
        # Update visibility based on current mode
        self.update_settings_visibility()
    
    def create_popup_button(self, parent, text, command):
        btn = tk.Label(parent, text=text, font=("Segoe UI", 9),
                      bg=self.button_bg, fg=self.fg_color,
                      padx=10, pady=5, cursor="hand2", relief=tk.FLAT)
        btn.bind('<Button-1>', lambda e: command())
        btn.bind('<Enter>', lambda e: btn.config(bg=self.button_hover))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.button_bg))
        return btn
    
    def switch_mode_from_popup(self, mode):
        self.switch_mode(mode)
        self.update_settings_visibility()
    
    def update_settings_visibility(self):
        if not self.settings_window or not self.settings_window.winfo_exists():
            return
        
        # Hide all control frames first
        self.stopwatch_controls_frame.pack_forget()
        self.timer_controls_frame.pack_forget()
        
        # Show relevant controls
        if self.mode == "stopwatch":
            self.stopwatch_controls_frame.pack(fill=tk.X, pady=(0, 10))
            # Update button text
            if self.stopwatch_running:
                self.sw_start_btn.config(text="⏸ Pause")
            else:
                self.sw_start_btn.config(text="▶ Start")
        elif self.mode == "timer":
            self.timer_controls_frame.pack(fill=tk.X, pady=(0, 10))
    
    def create_button(self, parent, text, command):
        btn = tk.Label(parent, text=text, font=("Segoe UI", 10),
                      bg=self.button_bg, fg=self.fg_color,
                      padx=12, pady=6, cursor="hand2", relief=tk.FLAT)
        btn.bind('<Button-1>', lambda e: command())
        btn.bind('<Enter>', lambda e: btn.config(bg=self.button_hover))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.button_bg if not self.is_active_mode(text) else self.accent_color))
        return btn
    
    def is_active_mode(self, button_text):
        if "Clock" in button_text and self.mode == "clock":
            return True
        if "Stopwatch" in button_text and self.mode == "stopwatch":
            return True
        if "Timer" in button_text and self.mode == "timer":
            return True
        return False
    
    def update_mode_buttons(self):
        # No longer needed - removed from UI
        pass
    
    def switch_mode(self, mode):
        self.mode = mode
        
        if mode == "clock":
            self.mode_label.config(text="CLOCK")
            self.stopwatch_running = False
            self.timer_running = False
            
        elif mode == "stopwatch":
            self.mode_label.config(text="STOPWATCH")
            self.timer_running = False
            
        else:  # timer
            self.mode_label.config(text="TIMER")
            self.stopwatch_running = False
    
    def toggle_stopwatch(self):
        self.stopwatch_running = not self.stopwatch_running
        if self.stopwatch_running:
            self.stopwatch_start_time = time.time() - self.stopwatch_time
        
        # Update button text in settings window if open
        if self.settings_window and self.settings_window.winfo_exists():
            if hasattr(self, 'sw_start_btn'):
                if self.stopwatch_running:
                    self.sw_start_btn.config(text="⏸ Pause")
                else:
                    self.sw_start_btn.config(text="▶ Start")
    
    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_time = 0
        
        # Update button text in settings window if open
        if self.settings_window and self.settings_window.winfo_exists():
            if hasattr(self, 'sw_start_btn'):
                self.sw_start_btn.config(text="▶ Start")
    
    def start_timer(self):
        if not self.timer_running:
            try:
                minutes = int(self.minutes_entry.get())
                seconds = int(self.seconds_entry.get())
                self.timer_set_seconds = minutes * 60 + seconds
                
                if self.timer_set_seconds > 0:
                    self.timer_seconds = self.timer_set_seconds
                    self.timer_running = True
                    self.timer_start_time = time.time()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for minutes and seconds")
    
    def pause_timer(self):
        self.timer_running = False
    
    def reset_timer(self):
        self.timer_running = False
        try:
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.timer_seconds = minutes * 60 + seconds
        except ValueError:
            self.timer_seconds = 0
        self.update_timer_display()
    
    def update_display(self):
        if self.mode == "clock":
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time, fg=self.accent_color)
            
        elif self.mode == "stopwatch":
            if self.stopwatch_running:
                self.stopwatch_time = time.time() - self.stopwatch_start_time
            
            hours = int(self.stopwatch_time // 3600)
            minutes = int((self.stopwatch_time % 3600) // 60)
            seconds = int(self.stopwatch_time % 60)
            milliseconds = int((self.stopwatch_time % 1) * 100)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
            self.time_label.config(text=time_str, fg=self.accent_color)
            
        else:  # timer
            if self.timer_running:
                elapsed = time.time() - self.timer_start_time
                self.timer_seconds = max(0, self.timer_set_seconds - int(elapsed))
                
                if self.timer_seconds == 0:
                    self.timer_running = False
                    self.time_label.config(fg=self.danger_color)
                    self.root.bell()  # Sound alert
                    messagebox.showinfo("Timer", "Time's up! ⏰")
                    
            self.update_timer_display()
        
        self.root.after(50, self.update_display)
    
    def update_timer_display(self):
        hours = self.timer_seconds // 3600
        minutes = (self.timer_seconds % 3600) // 60
        seconds = self.timer_seconds % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Change color based on remaining time
        if self.timer_seconds <= 10 and self.timer_seconds > 0:
            self.time_label.config(text=time_str, fg=self.danger_color)
        elif self.timer_seconds == 0:
            self.time_label.config(text=time_str, fg=self.danger_color)
        else:
            self.time_label.config(text=time_str, fg=self.accent_color)
    
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

def main():
    root = tk.Tk()
    root.configure(bg="#1e1e2e")
    app = ModernClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
