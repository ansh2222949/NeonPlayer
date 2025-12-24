import webview
import os
import sys
from core.media_control import MediaController
from core.pin_logic import PinHandler

# Core instances initialized once
mc = MediaController()
ph = PinHandler()
window = None

# -------------------------------
# JS <-> Python API Bridge
# -------------------------------
class Api:
    def control(self, action):
        """Play, Pause, Next, Prev controls"""
        mc.call(action)

    def get_music_data(self):
        """Sends metadata and progress to JS"""
        return mc.fetch_data()

    def seek_music(self, percent):
        """Updates playback position"""
        mc.seek_to(percent)

    # ================= VOLUME API (ADDED) =================
    def set_volume(self, percent):
        """Sets system volume (0-100)"""
        mc.set_volume(percent)

    def get_volume(self):
        """Gets current system volume"""
        return mc.get_volume()
    # ======================================================

    def resize_window(self, w, h):
        """🚀 Physically resizes the OS window for the capsule effect"""
        if window:
            window.resize(w, h)

    def toggle_pin(self):
        """Always on top logic"""
        if window:
            return ph.toggle(window)
        return False

    def close_app(self):
        """Terminates the application cleanly"""
        if window:
            window.destroy()
            sys.exit(0)

# -------------------------------
# App Launcher
# -------------------------------
def start_app():
    global window

    # Absolute path logic for reliability
    base_path = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_path, 'web', 'index.html')

    # 🚀 NATIVE WIDGET CONFIGURATION
    window = webview.create_window(
        title='Neon Liquid Player',
        url=html_path,
        js_api=Api(),
        
        # Dimensions (Capsule Width Locked)
        width=310, 
        height=220,
        min_size=(310, 80),
        
        # Ghost Mode Settings
        frameless=True,       # ❌ Removes OS title bar
        transparent=True,     # ❌ 100% Invisible container
        background_color='#000000', # ✅ Fixed: Standard hex triplet
        
        easy_drag=True,       # ✅ Drag window from anywhere
        on_top=False,         # Managed by toggle_pin
        text_select=False     # Professional feel
    )

    # 🛠️ GUI ENGINE: 'edgehtml' is most stable for transparency on Windows
    webview.start(gui='edgehtml', debug=False)

# -------------------------------
if __name__ == '__main__':
    start_app()