# app.py
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import time

start_time = time.time()

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

def fade_in_label(label, text, delay=40):
    for i in range(len(text)):
        window.after(i * delay, lambda i=i: label.config(text=text[:i+1]))

# Window setup
window = tk.Tk()
window.geometry("700x500")
window.configure(bg="#2E2E2E")
window.resizable(False, False)

# Fonts
title_font = tkFont.Font(family="Times", size="27", weight="bold")
text_font = tkFont.Font(family="Helvetica", size=14)

# Grid
window.grid_columnconfigure(0, weight=1)

# Logo
pil_image = Image.open("qr-gen-logo.png")

# Greeting
greeting_text = random.choice(greetings)

greeting_label = tk.Label(
    window,
    text=greeting_text,
    fg="white",
    bg="#2E2E2E",
    font=title_font
)
greeting_label.grid(row=1, column=0, pady=30)
fade_in_label(greeting_label, greeting_text)

# Input box for qr code input
qr_code_label = tk.Label(
    window,
    text="Input text or link for conversion here:",
    fg="white",
    bg="#2E2E2E",
    font=text_font
)
qr_code_label.grid(row=2, column=0)

input = tk.Entry(
    window,
    fg="#2E2E2E",
    bg="white",
    width=50
)
input.grid(row=3, column=0, pady= 20)

#target_height = 140
#aspect_ratio = pil_image.width / pil_image.height
#target_width = int(target_height * aspect_ratio)

#pil_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
#logo_image = ImageTk.PhotoImage(pil_image)

#logo_label = tk.Label(window, image=logo_image, bg="#2E2E2E")
#logo_label.grid(row=0, column=0, pady=20)

window.mainloop()
