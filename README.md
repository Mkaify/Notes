# 🗒️ Sticky Notes App

A lightweight desktop sticky notes app built with **PySide6**. Notes live on your screen, survive app restarts via a local SQLite database, and are accessible from the system tray.

## Features

- Frameless, always-on-top sticky note windows
- Drag notes anywhere on screen
- Notes auto-save on every edit and move
- Persisted across restarts with SQLite
- System tray icon — left-click to add a new note
- Right-click tray menu with Add Note and Quit

## Requirements

- Python 3.9+
- PySide6
- SQLAlchemy

## Setup

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd sticky-notes
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install PySide6 sqlalchemy
   ```

4. **(Optional) Configure database path:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if you want to store the database somewhere other than the project folder.

5. **Add the tray icon:**
   Place a `sticky-note.png` file in the project root (any small square PNG works).

6. **Run:**
   ```bash
   python notes.py
   ```

## Project Structure

```
sticky-notes/
├── notes.py        # Main app — UI, tray, note windows
├── database.py     # SQLAlchemy Note model and session setup
├── sticky-note.png # Tray icon image
├── notes.db        # Auto-created SQLite database (gitignored)
├── .env.example    # Environment variable template
└── .gitignore
```

## Usage

| Action | Result |
|---|---|
| Left-click tray icon | Create a new note |
| Right-click tray icon | Open menu (Add Note / Quit) |
| Click `×` on a note | Delete note permanently |
| Drag a note | Move it; position is saved |
| Type in a note | Auto-saved instantly |
