#!/usr/bin/env python3
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

class WinXPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("""
            #container {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 12px;
            }
            QLabel {
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Ubuntu', 'Helvetica', sans-serif;
            }
            .title {
                font-size: 18px;
                font-weight: bold;
                padding: 10px 10px 5px 10px;
                color: #ffffff;
            }
            .item {
                font-size: 14px;
                padding: 8px 20px;
            }
            .shortcut {
                color: #007acc;
                font-weight: bold;
            }
        """)
        
        vbox = QVBoxLayout(container)
        
        title = QLabel("WinX Menu")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(title)
        
        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        
        self.options = [
            ("Task Manager", "T", "t"),
            ("Terminal", "X", "x"),
            ("Night Light (Toggle)", "N", "n"),
            ("Mute/Unmute", "A", "a"),
            ("Lock Screen", "L", "l"),
            ("Logout", "K", "k"),
            ("Suspend / Sleep", "S", "s"),
            ("Restart", "R", "r"),
            ("Shutdown", "P", "p")
        ]
        
        for i, (name, key_disp, key_val) in enumerate(self.options):
            lbl_name = QLabel(name)
            lbl_name.setProperty("class", "item")
            
            lbl_key = QLabel(f"[{key_disp}]")
            lbl_key.setProperty("class", "item shortcut")
            lbl_key.setAlignment(Qt.AlignRight)
            
            grid.addWidget(lbl_name, i, 0)
            grid.addWidget(lbl_key, i, 1)
            
        vbox.addLayout(grid)
        layout.addWidget(container)
        self.setLayout(layout)
        
        self.adjustSize()
        self.centerOnScreen()

    def centerOnScreen(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def execute_command(self, key):
        commands = {
            't': ['gnome-system-monitor', 'ksysguard', 'xfce4-taskmanager', 'kitty -e top'],
            'x': ['x-terminal-emulator', 'gnome-terminal', 'konsole', 'alacritty', 'kitty'],
            'n': ['gsettings set org.gnome.settings-daemon.plugins.color night-light-enabled true'], 
            'a': ['wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle', 'amixer -q -D pulse sset Master toggle'],
            'l': ['loginctl lock-session', 'xdg-screensaver lock'],
            'k': ['loginctl terminate-user $USER'],
            's': ['systemctl suspend'],
            'r': ['systemctl reboot'],
            'p': ['systemctl poweroff'],
        }

        if key in commands:
            for cmd in commands[key]:
                try:
                    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    break
                except Exception:
                    continue
                    
        # Force the application to completely quit after execution
        QApplication.quit()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text().lower()
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Meta:
            QApplication.quit()
        elif key in [opt[2] for opt in self.options]:
            self.execute_command(key)
            
    def focusOutEvent(self, event):
        # Completely kill the process when clicking anywhere else
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setApplicationName("WinX")
    window = WinXPopup()
    window.show()
    window.activateWindow()
    window.setFocus()
    sys.exit(app.exec_())
