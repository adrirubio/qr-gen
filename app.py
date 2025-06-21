# app.py
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfile
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

def show_logo():
    target_height = 140
    aspect_ratio = pil_image.width / pil_image.height
    target_width = int(target_height * aspect_ratio)

    resized_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def on_clear():
    # Remove all text inside of the input widget
    input.delete(0, tk.END)
    # Remove any image inside of the qr-code label
    qr_code_label.config(
        image="",
        compound=None
    )

    # Add logo to qr-code label
    qr_code_label.config(image=logo_image, compound="bottom")
    qr_code_label.image = logo_image


def on_save():
    files = [('PNG Image', '*.png'), ('All Files', '*.*')]
    file = asksaveasfile(filetypes=files, defaultextension='.png', mode='wb')

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
greeting_label.grid(row=1, column=0, pady=20)
fade_in_label(greeting_label, greeting_text)

# Input box for qr code input
qr_code_label = tk.Label(
    window,
    text="🔗 Input text or link for conversion here:",
    fg="white",
    bg="#2E2E2E",
    font=text_font
)
qr_code_label.grid(row=2, column=0)

input = tk.Entry(
    window,
    fg="#2E2E2E",
    bg="grey70",
    font=text_font,
    width=40,
    relief="groove",
    bd=10,
    highlightthickness=1,
    highlightbackground="#CCCCCC",
    highlightcolor="#4A90E2",
    insertbackground="#2E2E2E"
)
input.grid(row=3, column=0, pady=20, ipadx=5, ipady=1)

# Generate button
button_font = ("Helvetica", 12, "bold")

generate_btn = tk.Button(
    window,
    text="Generate",
    font=button_font,
    bg="white",
    fg="#2E2E2E",
    activebackground="#4A90E2",
    activeforeground="white",
    width=14,
    height=1,
    relief="raised",
    bd=7,
    cursor="hand2"
)
generate_btn.grid(row=4, column=0, pady=20)

# Add different colour span row
row5 = tk.Frame(window, bg="#4A90E2")
row5.grid(row=5, column=0, sticky="nsew")
window.grid_rowconfigure(5, weight=1)
row5.grid_columnconfigure(0, weight=1)
row5.grid_columnconfigure(1, weight=1)

text="QR Codes will appear here:"

# Create label to display QR codes
logo_image = show_logo()

qr_code_label = tk.Label(
    row5,
    text="QR Codes will appear here:",
    image=logo_image,
    compound="bottom",  # image above text
    bg="grey60",
    anchor="n",
    pady=10,
    font=text_font
)
qr_code_label.image = logo_image
qr_code_label.grid(row=0, column=0, sticky="nsew", padx=(20, 0), pady=(20, 20))

# Clear button
clear_btn = tk.Button(
    row5,
    text="Clear",
    font=button_font,
    bg="white",
    fg="black",
    activebackground="#2E2E2E",
    activeforeground="white",
    width=7,
    height=1,
    relief="raised",
    bd=7,
    cursor="hand2",
    command=on_clear
)
clear_btn.grid(row=0, column=1, sticky="n", pady=40)

# Save button
save_btn = tk.Button(
    row5,
    text="Save",
    font=button_font,
    bg="white",
    fg="black",
    activebackground="#2E2E2E",
    activeforeground="white",
    width=7,
    height=1,
    relief="raised",
    bd=7,
    cursor="hand2",
    command=on_save
)
save_btn.grid(row=0, column=1, sticky="s", pady=50)

window.mainloop()
