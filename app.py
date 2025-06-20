# app.py
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import random

# Greeting list
greetings = [
    "Hello there! Ready to create?",
    "Welcome! Let's make some magic happen.",
    "Hey! So glad you're here.",
    "Ready for takeoff? Let's get creative.",
    "What's up? Let's get started.",
    "Welcome in! What will you create today?",
    "It's go time! Let's make a QR code.",
    "Hey there! Let the creation begin.",
    "Ready to roll? Fire up the generator!",
    "Greetings! Your QR adventure starts now.",
    "Hope you're having a great day!",
    "All systems go! Ready when you are.",
    "Hello! Let's build something cool.",
    "Good to see you! What's the plan?",
    "Hey, let's get this QR party started!",
    "Let the creativity flow!",
]

# Window setup
window = tk.Tk()
window.geometry("700x500")
window.configure(bg="#2E2E2E")
window.resizable(False, False)
window.tk.call("ttk::setTheme", "classic")

# Grid
window.grid_columnconfigure(0, weight=1)   # left  column
window.grid_columnconfigure(1, weight=1)   # right column



# Fonts
title_font = tkFont.Font(family="Times", size="27", weight="bold")
text_font = tkFont.Font(family="Helvetica", size=12)

# Greeting
greeting_text = random.choice(greetings)

greeting_label = tk.Label(
    window,
    text=greeting_text,
    fg="white",
    bg="#2E2E2E",
    font=title_font
)
greeting_label.pack(pady=30)

window.mainloop()
