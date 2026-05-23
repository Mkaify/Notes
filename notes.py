import sys

from database import Note, session
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

# Store references to the NoteWindow objects in this, keyed by id.
active_notewindows = {}


class NoteWindow(QWidget):
    def __init__(self, note=None):
        super().__init__()

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setStyleSheet(
            "background: #FFFF99; color: #62622f; border: 0; font-size: 16pt;"
        )
        layout = QVBoxLayout()

        buttons = QHBoxLayout()
        self.close_btn = QPushButton("×")
        self.close_btn.setStyleSheet(
            "font-weight: bold; font-size: 25px; width: 25px; height: 25px;"
        )
        self.close_btn.clicked.connect(self.delete)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        buttons.addStretch()  # Add stretch on left to push button right.
        buttons.addWidget(self.close_btn)
        layout.addLayout(buttons)

        self.text = QTextEdit()
        layout.addWidget(self.text)
        self.setLayout(layout)

        self.text.textChanged.connect(self.save)

        # Store a reference to this note in the active_notewindows
        active_notewindows[id(self)] = self

        # If no note is provided, create one.
        if note is None:
            self.note = Note()
            self.save()
        else:
            self.note = note
            self.load()

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPosition()

    def mouseMoveEvent(self, e):
        delta = e.globalPosition() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPosition()

    def mouseReleaseEvent(self, e):
        self.save()

    def load(self):
        self.move(self.note.x, self.note.y)
        self.text.setText(self.note.text)

    def save(self):
        self.note.x = self.x()
        self.note.y = self.y()
        self.note.text = self.text.toPlainText()
        # Write the data to the database, adding the Note object to the
        # current session and committing the changes.
        session.add(self.note)
        session.commit()

    def delete(self):
        session.delete(self.note)
        session.commit()
        del active_notewindows[id(self)]
        self.close()


def create_notewindow(note=None):
    note = NoteWindow(note)
    note.show()


existing_notes = session.query(Note).all()

if existing_notes:
    for note in existing_notes:
        create_notewindow(note)
else:
    create_notewindow()

# Create the icon
icon = QIcon("sticky-note.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)


def handle_tray_click(reason):
    # If the tray is left-clicked, create a new note.
    if (
        QSystemTrayIcon.ActivationReason(reason)
        == QSystemTrayIcon.ActivationReason.Trigger
    ):
        create_notewindow()


tray.activated.connect(handle_tray_click)


# Don't automatically close app when the last window is closed.
app.setQuitOnLastWindowClosed(False)

# Create the menu
menu = QMenu()
# Add the Add Note option to the menu.
add_note_action = QAction("Add note")
add_note_action.triggered.connect(create_notewindow)
menu.addAction(add_note_action)

# Add a Quit option to the menu.
quit_action = QAction("Quit")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)
# Add the menu to the tray
tray.setContextMenu(menu)


app.exec()