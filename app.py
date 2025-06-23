# app.py
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfile
from pathlib import Path
from PIL import Image, ImageTk
import os, datetime, re
import shutil
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

    # Save qr code for database
    data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "qr-gen", "qr-codes")
    os.makedirs(data_dir, exist_ok=True)

    pattern = re.compile(r"qr-code-(\d+)\.png$")
    highest_idx  = 0

    for fname in os.listdir(data_dir):
        m = pattern.match(fname)
        if m:
            num = int(m.group(1))
            highest_idx = max(highest_idx, num)

    next_idx = highest_idx + 1
    filename = f"qr-code-{next_idx}.png"
    file_path = os.path.join(data_dir, filename)

    img.save(file_path, format="PNG")
    print("Saved QR-Code to", file_path)

    # Save qr code link for database
    data_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "qr-gen", "qr-code-links")
    os.makedirs(data_dir, exist_ok=True)

    pattern = re.compile(r"link-(\d+)\.txt$")
    highest_idx  = 0

    for fname in os.listdir(data_dir):
        m = pattern.match(fname)
        if m:
            num = int(m.group(1))
            highest_idx = max(highest_idx, num)

    next_idx = highest_idx + 1
    filename = f"link-{next_idx}.txt"
    file_path = os.path.join(data_dir, filename)

    # Save link to file
    link = input.get()
    with open(file_path, "w") as f:
        f.write(link)
    print("Saved QR-Code link to", file_path)

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

def on_save2(path, qr_code):
    # Copy the image from the path
    src = Path(path)
    if not src.exists():
        print("Source image not found:", src)
        return

    # User input
    file_obj = asksaveasfile(
        filetypes=[('PNG Image', '*.png'), ('All Files', '*.*')],
        mode='wb'
    )
    if not file_obj:
        return

    # Copy
    with src.open('rb') as fsrc:
        shutil.copyfileobj(fsrc, file_obj)
    file_obj.close()

    print("Saved a copy to", Path(file_obj.name))

    qr_code.destroy()


def on_delete(qr_code_image, qr_code_text, qr_code, database):
    # Delte qr code file
    try:
        os.remove(qr_code_image)
        print("deleted:", qr_code_image)
    except FileNotFoundError:
        print("file not found")

    # Delete qr code text or link
    try:
        os.remove(qr_code_text)
        print("deleted:", qr_code_text)
    except FileNotFoundError:
        print("file not found")

    # Reset qr-code and database
    qr_code.destroy()
    database.destroy()
    # Open updated database
    on_database()

def make_scrollable_grid(parent, cols=3, cell_minwidth=220, bg="#2E2E2E"):
    # Create container frame for proper layout
    container = tk.Frame(parent, bg=bg)
    container.pack(fill="both", expand=True)

    # Canvas + scrollbar
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    vbar = tk.Scrollbar(container, orient="vertical")

    # Pack scrollbar and canvas
    vbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Interior frame
    inner = tk.Frame(canvas, bg=bg)
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    # Update scroll region and configure scrollbar
    def update_scrollregion(event=None):
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Check if content is taller than canvas
        bbox = canvas.bbox("all")
        if bbox:
            content_height = bbox[3] - bbox[1]
            canvas_height = canvas.winfo_height()

            if content_height > canvas_height:
                canvas.configure(yscrollcommand=vbar.set)
                vbar.configure(command=canvas.yview)
                canvas.bind("<MouseWheel>", on_mousewheel)
            else:
                canvas.configure(yscrollcommand=None)
                vbar.configure(command=None)
                canvas.unbind("<MouseWheel>")
                canvas.yview_moveto(0)

    inner.bind("<Configure>", update_scrollregion)
    canvas.bind("<Configure>", update_scrollregion)

    # Initial configuration
    canvas.after(100, update_scrollregion)

    # Mouse wheel scrolling - standard direction
    def on_mousewheel(event):
        bbox = canvas.bbox("all")
        if bbox and (bbox[3] - bbox[1]) > canvas.winfo_height():
            canvas.yview_scroll(-1 * int(event.delta/120), "units")

    # Equal column widths
    for c in range(cols):
        inner.grid_columnconfigure(c, minsize=cell_minwidth, weight=0)

    # Simple counter to track widget placement
    counter = {"n": 0}
    def add_item(widget):
        r, c = divmod(counter["n"], cols)
        widget.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
        counter["n"] += 1

    return inner, add_item

def on_database():
    global database
    database = tk.Toplevel(window)
    database.title("Database")
    database.configure(bg="#2E2E2E")
    database.resizable(False, False)

    # Make database appear to the right of the main window
    window.update_idletasks()
    root_x = window.winfo_rootx()
    root_y = window.winfo_rooty()
    root_w = window.winfo_width()
    root_h = window.winfo_height()

    w = 700
    h = root_h
    new_x = root_x + root_w + 20
    new_y = root_y - 36

    database.geometry(f"{w}x{h}+{new_x}+{new_y}")

    text = "🗄️ Welcome to the Database"

    database_greeting = tk.Label(
        database,
        text=text,
        fg="white",
        bg="#2E2E2E",
        font=title_font
    )
    database_greeting.pack(pady=20)
    fade_in_label(database_greeting, text)

    clarification = tk.Label(
        database,
        text="QR-Codes appear from newest to oldest",
        fg="white",
        bg="#2E2E2E",
        font=text_font
    )
    clarification.pack()

    gallery_frame, gallery_add = make_scrollable_grid(database)

    window.gallery_add = gallery_add

    # Show all generated images
    qr_dir = Path.home() / ".local" / "share" / "qr-gen" / "qr-codes"
    qr_dir.mkdir(parents=True, exist_ok=True)

    images = sorted(qr_dir.glob("*.png"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True)

    # Icon size
    thumb_refs = []
    thumb_size = (200, 200)

    for path in images:
        try:
            img = Image.open(path)
        except Exception as err:
            print("Skipping", path.name, err)
            continue

        thumb = img.copy()
        thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        tk_thumb = ImageTk.PhotoImage(thumb)
        thumb_refs.append(tk_thumb)

        lbl = tk.Label(gallery_frame,
                       image=tk_thumb,
                       bg="#2E2E2E",
                       cursor="hand2",
                       bd=1, relief="ridge")
        gallery_add(lbl)

        lbl.bind("<Button-1>",
                 lambda _ev, p=path: load_image(p))

    # keep refs alive as long as the Database window lives
    database._thumb_refs = thumb_refs

def load_image(path):
    qr_code = tk.Toplevel(window)
    qr_code.title("QR-Code")
    qr_code.geometry("500x400")
    qr_code.configure(bg="#2E2E2E")
    qr_code.resizable(False, False)

    # Show image
    img = Image.open(path)
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(qr_code, image=tk_img, bg="#2E2E2E")
    label.image = tk_img
    label.pack(padx=10, pady=20)

    # Button frame
    btn_frame = tk.Frame(qr_code, bg="#2E2E2E")
    btn_frame.pack(pady=10, fill="x")

    # Save button
    save_btn = tk.Button(
        btn_frame,
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
        command=lambda p=path: on_save2(path, qr_code)
    )
    save_btn.pack(side="left", padx=70, pady=20)

    # Get link/text path
    name = Path(path).stem
    m = re.search(r"-(\d+)$", name)
    if m:
        number = int(m.group(1))
    else:
        print("no number found")

    text_path = Path.home() / ".local" / "share" / "qr-gen" / "qr-code-links" / f"link-{number}.txt"

    # Get link/text
    with text_path.open("r", encoding="utf-8") as f:
        text = f.read()

    # Corresponding link/text label
    qr_code.update_idletasks()
    wrap = qr_code.winfo_width() - 40

    text_link_label = tk.Label(
        qr_code,
        text=f"Corresponding link or text: {text}",
        fg="white",
        bg="#2E2E2E",
        font=text_font,
        wraplength=wrap,
        justify="left"
    )
    text_link_label.pack(pady=20, fill="x")

    # Delete button
    delete_btn = tk.Button(
        btn_frame,
        text="Delete",
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
        command=lambda: on_delete(path, text_path, qr_code, database)
    )
    delete_btn.pack(side="right", padx=70, pady=20)


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

# Database button
database_btn = tk.Button(
    window,
    text="Database",
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
    command=on_database
)
database_btn.grid(row=4, column=0, sticky="e", padx=68)

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
