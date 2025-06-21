# app.py
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
import qrcode
import random

current_image = None

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
    global current_image
    target_height = 140
    aspect_ratio = pil_image.width / pil_image.height
    target_width = int(target_height * aspect_ratio)

    resized_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    current_image = resized_image
    return ImageTk.PhotoImage(resized_image)

def on_generate():
    global current_image
    # Generate QR Code
    data = input.get()
    if not data.strip():
        return

    # Generate QR code image
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    fixed_size = (140, 140)
    img = img.resize(fixed_size, Image.Resampling.LANCZOS)

    # Store the image so it can be saved later
    current_image = img

    # Convert to ImageTk and update label
    qr_img_tk = ImageTk.PhotoImage(img)
    qr_code_label.config(text="Here’s your QR code, ready to scan! ", image=qr_img_tk, compound="bottom")
    qr_code_label.image = qr_img_tk

def on_clear():
    # Remove all text inside of the input widget
    input.delete(0, tk.END)
    # Remove any image and text inside of the qr-code label
    qr_code_label.config(
        text="",
        image="",
        compound=None
    )

    # Add logo and default text to qr-code label
    global current_image
    current_image = pil_image
    qr_code_label.config(image=logo_image, text="Enter your link or text, then generate!", compound="bottom")
    qr_code_label.image = logo_image

def on_save():
    files = [('PNG Image', '*.png'), ('All Files', '*.*')]
    file = asksaveasfile(filetypes=files, defaultextension='.png', mode='wb')
    if file:
        current_image.save(file, format='PNG')
        file.close()

def on_library():
    library = tk.Toplevel(window)
    library.title("Library")
    library.geometry("700x500")
    library.configure(bg="#2E2E2E")
    library.resizable(False, False)

    text = "📚 Welcome to the library"

    library_greeting = tk.Label(
        library,
        text=text,
        fg="white",
        bg="#2E2E2E",
        font=title_font
    )
    library_greeting.pack(pady=20)
    fade_in_label(library_greeting, text)

def fade_in_label(label, text, delay=40):
    for i in range(len(text)):
        window.after(i * delay, lambda i=i: label.config(text=text[:i+1]))

# Window setup
window = tk.Tk()
window.title("QR-Gen")
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
    cursor="hand2",
    command=on_generate
)
generate_btn.grid(row=4, column=0, pady=20)

# Library button
library_btn = tk.Button(
    window,
    text="library",
    font=button_font,
    bg="green2",
    fg="#2E2E2E",
    activebackground="green4",
    activeforeground="white",
    width=7,
    height=1,
    relief="raised",
    bd=7,
    cursor="hand2",
    command=on_library
)
library_btn.grid(row=4, column=0, sticky="e", padx=68)

# Add different colour span row
row5 = tk.Frame(window, bg="#4A90E2")
row5.grid(row=5, column=0, sticky="nsew")
window.grid_rowconfigure(5, weight=1)
row5.grid_columnconfigure(0, weight=1)
row5.grid_columnconfigure(1, weight=1)

# Create label to display QR codes
logo_image = show_logo()
text = "Enter your link or text, then generate!"

qr_code_label = tk.Label(
    row5,
    text=text,
    image=logo_image,
    compound="bottom",
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
