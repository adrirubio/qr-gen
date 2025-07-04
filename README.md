# qr-gen
Instantly generate and save QR codes from any text or URL.

<p align="left">
  <img src="qr-gen-logo.png"
       alt="qr-gen-logo"
       width="200">
</p>

## Demo

Watch a quick preview below (GIF)

### 🔹 Preview (GIF)
![QR Gen - Preview](https://github.com/adrirubio/demo-files/raw/main/demo-qr-gen.gif)

## Features

#### Core Features
- Instant QR Code Generation: Generates QR Codes from any text or link instantly
- Built in Database: Automatically saves all QR Codes generated
- Save Functionality: Export QR Codes to custom locations as PNG files
- Global Hotkey Support: Launch the app from anywhere using the F5 key
- Right-click Copy and Paste: Copy/paste functionality in the input field

#### Database Features:
- Automatic Storage: Saves qr codes to ~/.local/share/qr-gen/
- Link Preservation: Stores both the QR image and original text/link
- Chronological Storage: View QR Codes from latest to oldest
- Individual QR Management: Open, save, or delete specific QR Cod

## Installation

### Prerequisites
- Python 3.8 or higher

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/adrirubio/qr-gen.git
   cd qr-gen
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


3. **Run the application**
   ```bash
   python app.py
   ```

### Optional: Global Hotkey Setup (F5)

To launch QR Gen with the f5 key from anywhere on your system:

1. **Start the hotkey daemon**
   ```bash
   python hotkey_daemon.py
   ```

2. **Keep it running in the background**
   - The daemon will listen for F5 key presses
   - Press F5 anytime to launch QR Gen
   - Press Ctrl-C to stop the daemon

3. **Auto-start on boot (Linux)**
    Add to your startup applications or create a systemd service:
    ```bash
    # Create a systemd service file
    sudo nano /etc/systemd/system/qr-gen-hotkey.service
    ```

    Add the following content:
    ```ini
    [Unit]
    Description=QR Gen Hotkey Daemon
    After=graphical.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/python3 /path/to/qr-gen/hotkey_daemon.py
    Restart=on-failure
    User=YOUR_USERNAME

    [Install]
    WantedBy=default.target
    ```

    Enable and start service:
    ```bash
    sudo systemctl enable qr-gen-hotkey
    sudo systemctl start qr-gen-hotkey
    ```

## Usage

### Running in GitHub Codespaces or Headless Environments

If you're running in GitHub Codespaces or a headless environment, you'll need a virtual display:

1. **Option A: Use the DevContainer (Recommended)**
   - The repository includes a `.devcontainer/devcontainer.json` configuration
   - When you open in Codespaces, it will automatically set up a desktop environment
   - Access the GUI at the forwarded port 6080 in your browser

2. **Option B: Use Xvfb manually**
   ```bash
   # Install Xvfb
   sudo apt-get update && sudo apt-get install -y xvfb

   # Run the app with virtual display
   xvfb-run -a python app.py
   ```

### Running on Desktop

1. **Launch the app** using either:
   - Direct command: `python app.py`
   - F5 hotkey (if daemon is running)

2. **Enter your text or link** in the entry widget

3. **Get instant QR Codes** with the qrcode library

4. **Find past QR Codes** in the database section

## Screenshots

Home:<br>
![Home](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/home.png)

Copy/paste:<br>
![Copy/paste](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/copy-paste.png)

QR Code:<br>
![QR Code](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/qr-code.png)

Save:<br>
![Save](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/save.png)

Database:<br>
![Database](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/database.png)

Database QR Code:<br>
![Database QR Code](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/database-qr-code.png)

Farewell:<br>
![Farewell](https://raw.githubusercontent.com/adrirubio/demo-files/main/qr-gen-screenshots/goodbye.png)
