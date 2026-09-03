#!/bin/bash
set -e

echo "Starting WinX installation..."

# 1. Install dependencies
if command -v apt &> /dev/null; then
    echo "Ubuntu/Debian detected. Updating and installing PyQt5..."
    sudo apt update && sudo apt install -y python3-pyqt5
elif command -v dnf &> /dev/null; then
    echo "Fedora detected. Installing python3-qt5..."
    sudo dnf install -y python3-qt5
elif command -v pacman &> /dev/null; then
    echo "Arch Linux detected. Installing python-pyqt5..."
    sudo pacman -S --noconfirm python-pyqt5
else
    echo "Warning: Unsupported package manager. Please ensure PyQt5 is installed for Python 3."
fi

# 2. Make script executable and copy to system
chmod +x winx.py
echo "Installing application to /usr/local/bin/winx..."
sudo cp winx.py /usr/local/bin/winx

echo ""
echo "✅ Installation Complete!"
echo "Please run './shortkey.sh' to automatically set up the Win+X shortcut."
