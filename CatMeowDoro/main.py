import tkinter as tk
from tkinter import ttk

# Constants for durations (in seconds)
WORK_DURATION = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60  # Optional: Long break after 4 pomodoros

class CatPomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐱 CatMeowDoro")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)

        # Timer settings
        self.current_time = WORK_DURATION
        self.is_running = False
        self.is_break = False
        self.completed_sessions = 0
        self.timer_id = None

        # Emojis and messages
        self.cat_states = {
            'work': '🐱‍💻',
            'break': '😸'
        }
        self.messages = {
            'start': "Ready to be productive? Let’s go! 🚀",
            'work': "Focus time! Let's work together! 🐾",
            'break': "Great job! Time for a break! 🐱"
        }

        self.create_ui()
        self.update_ui()

    def create_ui(self):
        frame = tk.Frame(self.root, bg='#f0f8ff')
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        tk.Label(frame, text="🐱 Cat Pomodoro Timer", font=('Arial', 20, 'bold'), bg='#f0f8ff').pack(pady=10)

        self.cat_label = tk.Label(frame, text=self.cat_states['work'], font=('Arial', 60), bg='#f0f8ff')
        self.cat_label.pack(pady=10)

        self.message_label = tk.Label(frame, text=self.messages['start'], font=('Arial', 12), wraplength=300,
                                      bg='#f0f8ff', fg='#444')
        self.message_label.pack(pady=5)

        self.timer_label = tk.Label(frame, text="25:00", font=('Arial', 36, 'bold'), bg='#f0f8ff', fg='#333')
        self.timer_label.pack(pady=10)

        self.session_label = tk.Label(frame, text="Work Session", font=('Arial', 14), bg='#f0f8ff', fg='#4a90e2')
        self.session_label.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(frame, bg='#f0f8ff')
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start", command=self.toggle_timer,
                                   font=('Arial', 12), bg='#4a90e2', fg='white', padx=20, pady=10)
        self.start_btn.pack(side='left', padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_timer,
                                   font=('Arial', 12), bg='#e74c3c', fg='white', padx=20, pady=10)
        self.reset_btn.pack(side='left', padx=5)

        self.skip_btn = tk.Button(btn_frame, text="Skip", command=self.skip_session,
                                  font=('Arial', 12), bg='#f39c12', fg='white', padx=20, pady=10)
        self.skip_btn.pack(side='left', padx=5)

        # Progress tracking
        progress_frame = tk.Frame(frame, bg='#f0f8ff')
        progress_frame.pack(pady=10)

        self.pomodoro_label = tk.Label(progress_frame, text="Completed: 0 🍅", font=('Arial', 12), bg='#f0f8ff')
        self.pomodoro_label.pack()

        self.progress_bar = ttk.Progressbar(progress_frame, length=280, mode='determinate')
        self.progress_bar.pack(pady=5)

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def update_ui(self):
        self.timer_label.config(text=self.format_time(self.current_time))
        self.pomodoro_label.config(text=f"Completed: {self.completed_sessions} 🍅")

        total_time = SHORT_BREAK if self.is_break and self.completed_sessions % 4 != 0 else \
                     LONG_BREAK if self.is_break else WORK_DURATION

        if total_time > 0:
            progress = ((total_time - self.current_time) / total_time) * 100
            self.progress_bar['value'] = progress

        # Update labels and emoji based on session type
        if self.is_break:
            self.cat_label.config(text=self.cat_states['break'])
            self.message_label.config(text=self.messages['break'])
            self.session_label.config(text="Break Time", fg='#27ae60')
        else:
            self.cat_label.config(text=self.cat_states['work'])
            self.message_label.config(text=self.messages['work'])
            self.session_label.config(text="Work Session", fg='#4a90e2')

    def toggle_timer(self):
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_btn.config(text="Pause", bg='#e67e22')
        self.run_countdown()

    def pause_timer(self):
        self.is_running = False
        self.start_btn.config(text="Start", bg='#4a90e2')
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reset_timer(self):
        self.pause_timer()
        self.is_break = False
        self.current_time = WORK_DURATION
        self.message_label.config(text=self.messages['start'])
        self.update_ui()

    def skip_session(self):
        self.pause_timer()
        if self.is_break:
            self.start_work_session()
        else:
            self.completed_sessions += 1
            self.start_break_session()

    def run_countdown(self):
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            self.update_ui()
            self.timer_id = self.root.after(1000, self.run_countdown)
        elif self.current_time == 0:
            self.handle_session_end()

    def handle_session_end(self):
        self.is_running = False
        self.start_btn.config(text="Start", bg='#4a90e2')
        if self.is_break:
            self.start_work_session()
        else:
            self.completed_sessions += 1
            self.start_break_session()

    def start_work_session(self):
        self.is_break = False
        self.current_time = WORK_DURATION
        self.update_ui()

    def start_break_session(self):
        self.is_break = True
        self.current_time = SHORT_BREAK if self.completed_sessions % 4 != 0 else LONG_BREAK
        self.update_ui()

    def run(self):
        self.root.mainloop()

# Main entry point
if __name__ == "__main__":
    app = CatPomodoroTimer()
    app.run()
