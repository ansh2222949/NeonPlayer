NeonPlayer — Floating System Media Controller (Windows)

NeonPlayer is a lightweight, floating desktop media controller for Windows that automatically syncs with the system-wide media session (Spotify, YouTube, VLC, browser media, etc.) and provides a modern glassmorphism UI with real-time playback controls.

Built using Python + pywebview + Windows Media APIs, NeonPlayer runs as a small always-on-top widget without interrupting your workflow.

✨ Features

🎧 System-wide Media Sync

Automatically detects currently playing media

Works with Spotify, browsers, VLC, and other Windows media sources

▶️ Playback Controls

Play / Pause

Next / Previous track

Seek using progress slider

🎚 Live Progress & Metadata

Song title & artist

Playback progress & duration

Real-time play/pause state detection

🪟 Floating Widget UI

Frameless & transparent window

Capsule-style compact mode

Auto-minimize on inactivity

📌 Always-on-Top Mode

Pin/unpin the widget using a single click

🎨 Multiple Themes

Neon, Night, Cyber, Emerald, Sunset, Rose

One-click theme switching

💎 Dynamic Background

Album art is blurred and used as animated background

⚡ High Performance

Async media polling (non-blocking)

Thread-safe Windows API access

Minimal CPU & memory usage



```text
Python (Backend)
├─ MediaController
│  └─ Reads system media using Windows Media APIs
├─ PinHandler
│  └─ Always-on-top window logic
└─ pywebview
   └─ Python ↔ JavaScript bridge



Python handles system media, window behavior, and OS-level controls

JavaScript handles UI logic, animations, and user interactions

CSS provides glassmorphism, blur effects, and transitions

Communication happens via pywebview.api

📁 Project Structure
NeonPlayer/
├── core/
│   ├── media_control.py    # Windows media session controller
│   ├── pin_logic.py        # Always-on-top window logic
│   └── __init__.py
│
├── web/
│   ├── index.html          # UI layout
│   ├── script.js           # UI logic & animations
│   └── style.css           # Glassmorphism & themes
│
├── main.py                 # Application entry point
├── app_icon.ico            # Application icon
├── NeonPlayer.spec         # PyInstaller configuration
├── build.bat               # Build script
├── requirements.txt        # Python dependencies
└── README.md
