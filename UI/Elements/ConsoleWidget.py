import ctypes
import os

from PyQt6.QtWidgets import (QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame, QScrollArea)
from PyQt6.QtCore import QProcess, Qt, QEvent, QTimer
from PyQt6.QtGui import QTextCursor, QKeyEvent, QColor, QTextCharFormat, QKeySequence, QShortcut
from UI import Language


class ConsoleColorScheme:
    COLORS = {
        'background': QColor(12, 12, 12),
        'text': QColor(204, 204, 204),
        'warning': QColor(255, 204, 0),
        'error': QColor(255, 0, 0),
        'system': QColor(0, 136, 204),
        'prompt': QColor(255, 153, 0),
        'success': QColor(0, 204, 102)
    }


class ProtectedConsole(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUndoRedoEnabled(False)
        self.protected_start = 0
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {ConsoleColorScheme.COLORS['background'].name()};
                color: {ConsoleColorScheme.COLORS['text'].name()};
                font-family: Consolas;
                font-size: 12px;
            }}
        """)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setProtectedStart(self, pos):
        self.protected_start = pos

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        pos = cursor.position()

        if event == QKeySequence.StandardKey.SelectAll:
            self.selectUserInput()
            return

        if event == QKeySequence.StandardKey.Copy:
            self.handleCopy()
            return

        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                self.handleCtrlC()
                return
            elif event.key() == Qt.Key.Key_V:
                self.handleCtrlV()
                return

        super().keyPressEvent(event)

    def selectUserInput(self):
        cursor = self.textCursor()
        cursor.setPosition(self.protected_start)
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def handleCopy(self):
        cursor = self.textCursor()
        if cursor.selectionStart() >= self.protected_start:
            super().copy()

    def handleCtrlC(self):
        if self.textCursor().hasSelection():
            self.handleCopy()
        else:
            self.parent().sendControlSignal(b'\x03')  # Ctrl+C

    def handleCtrlV(self):
        cursor = self.textCursor()
        if cursor.position() >= self.protected_start:
            super().paste()


class ConsoleWidget(QWidget):
    MAX_BUFFER_SIZE = 20000
    WARNING_THRESHOLD = 19800

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lastDirectory = os.getcwd()
        self.history = []
        self.history_index = 0
        self.output_buffer = ""
        self.input_buffer = ""
        self.warning_shown = False
        self.setup_ui()
        self.setup_process()
        self.setup_timer()
        self.setup_shortcuts()
        self.update_buttons_state()

    def setup_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.left_panel = QScrollArea()
        self.left_panel.setFixedWidth(110)
        self.left_panel.setWidgetResizable(True)

        self.control_widget = QWidget()
        self.control_layout = QVBoxLayout(self.control_widget)
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_layout.setSpacing(5)

        self.start_button = QPushButton(Language.Lang.Editor.Console.start)
        self.start_button.setFixedHeight(30)
        self.start_button.clicked.connect(self.start_process)

        self.stop_button = QPushButton(Language.Lang.Editor.Console.stop)
        self.stop_button.setFixedHeight(30)
        self.stop_button.clicked.connect(self.terminate_process)

        self.clear_button = QPushButton(Language.Lang.Editor.Console.clear)
        self.clear_button.setFixedHeight(30)
        self.clear_button.clicked.connect(self.clear_console)

        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.stop_button)
        self.control_layout.addWidget(self.clear_button)
        self.control_layout.addStretch()

        self.left_panel.setWidget(self.control_widget)
        self.main_layout.addWidget(self.left_panel)

        self.console = ProtectedConsole()
        self.console.setFrameStyle(QFrame.Shape.NoFrame)
        self.console.setPlaceholderText(Language.Lang.Editor.Console.placeholder)
        self.main_layout.addWidget(self.console)

        self.console.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.console.installEventFilter(self)

    def cd_path(self, path):
        if not os.path.isdir(path):
            self.output_buffer += f"\n[ERROR] Directory not found: {path}\n"
            self.sync_console()
            return

        self.terminate_process()
        self.start_process(working_dir=path)
        self.output_buffer = ""
        self.input_buffer = ""
        self.warning_shown = False
        self.sync_console()
        self.output_buffer += f"[SYSTEM] Changed working directory to: {path}\n"

    def setup_process(self, dir=None):
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.oem_encoding = self.get_oem_encoding()

    def setup_timer(self):
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.sync_console)
        self.update_timer.start(50)

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+A"), self.console, self.console.selectUserInput)

    def sync_console(self):
        current_text = self.output_buffer + self.input_buffer

        if self.console.toPlainText() != current_text:
            self.console.setPlainText(current_text)
            self.console.setProtectedStart(len(self.output_buffer))
            cursor = self.console.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.console.setTextCursor(cursor)

    def check_buffer_limit(self):
        buffer_len = len(self.output_buffer)

        if buffer_len >= self.MAX_BUFFER_SIZE:
            self.output_buffer = self.output_buffer[-200:] + "\n[SYSTEM] Console buffer cleared (max limit reached)\n"
            self.warning_shown = False
            return True

        if buffer_len >= self.WARNING_THRESHOLD and not self.warning_shown:
            self.output_buffer += f"\n[SYSTEM] Warning: Console buffer {buffer_len}/{self.MAX_BUFFER_SIZE}. Type 'clear' to reset\n"
            self.warning_shown = True

        return False

    def handle_stdout(self):
        raw = self.process.readAllStandardOutput().data()
        try:
            text = raw.decode(self.oem_encoding)
        except:
            text = raw.decode('utf-8', errors='replace')
        self.process_output(text)

    def handle_stderr(self):
        raw = self.process.readAllStandardError().data()
        try:
            text = raw.decode(self.oem_encoding)
        except:
            text = raw.decode('utf-8', errors='replace')
        self.process_output(text, is_error=True)

    def process_output(self, text, is_error=False):
        text = text.replace("\r", "").replace("\x08", "")
        if is_error:
            text = f"[ERROR] {text}"

        if self.check_buffer_limit():
            text = f"[SYSTEM] Output truncated\n{text[-200:]}"

        self.output_buffer += text
        self.check_buffer_limit()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                self.process_command()
                return True

            if event.key() == Qt.Key.Key_Backspace:
                if len(self.input_buffer) > 0:
                    self.input_buffer = self.input_buffer[:-1]
                return True

            if event.key() in [Qt.Key.Key_Up, Qt.Key.Key_Down]:
                self.navigate_history(event.key())
                return True

            if event.text():
                self.input_buffer += event.text()
                return True

        return super().eventFilter(obj, event)

    def process_command(self):
        if self.input_buffer.lower().strip() == 'cls':
            self.clear_console()
            return
        elif self.input_buffer.lower().strip() == 'exit':
            self.terminate_process()
        elif self.input_buffer:
            self.history.append(self.input_buffer)
            self.process.write(f"{self.input_buffer}\r\n".encode(self.oem_encoding))

        self.input_buffer = ""
        self.history_index = len(self.history)
        self.sync_console()

    def navigate_history(self, key):
        if not self.history: return

        if key == Qt.Key.Key_Up and self.history_index > 0:
            self.history_index -= 1
        elif key == Qt.Key.Key_Down and self.history_index < len(self.history) - 1:
            self.history_index += 1

        self.input_buffer = self.history[self.history_index]
        self.sync_console()

    def sendControlSignal(self, signal):
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.write(signal)

    def start_process(self, working_dir=None):
        if self.process.state() != QProcess.ProcessState.Running:
            self.process.setWorkingDirectory(working_dir if working_dir else self.lastDirectory)
            self.lastDirectory = working_dir if working_dir else self.lastDirectory
            self.process.start("cmd.exe", ['/K'])
            self.output_buffer += "\n[SYSTEM] Process started\n"
            self.update_buttons_state()
            self.clear_console()

    def terminate_process(self):
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
            self.output_buffer += "\n[SYSTEM] Process terminated by user\n"
            self.update_buttons_state()

    def clear_console(self):
        self.output_buffer = ""
        self.input_buffer = ""
        self.process.write(f"cmd\r\n".encode(self.oem_encoding))
        self.sync_console()

    def update_buttons_state(self):
        pass

    def get_oem_encoding(self):
        try:
            return f"cp{ctypes.windll.kernel32.GetOEMCP()}"
        except:
            return 'cp866'

    def closeEvent(self, event):
        self.terminate_process()
        super().closeEvent(event)