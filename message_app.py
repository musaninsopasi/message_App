import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle("Mesaüstü Mesajlaşma Uygulaması")
        self.setCentralWidget(MainWidget(self))

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.username = None
        self.initUI()

    def initUI(self):
        self.connection = sqlite3.connect("user.db")
        self.cursor = self.connection.cursor()


        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()

        cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL
)


""")
   

        connection.commit()
        connection.close()

        self.usernameLabel = QLabel("Kullanıcı Adı:")
        self.usernameLineEdit = QLineEdit()
        self.passwordLabel = QLabel("Şifre:")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("Giriş Yap")
        self.loginButton.clicked.connect(self.login)

        usernameLayout = QHBoxLayout()
        usernameLayout.addWidget(self.usernameLabel)
        usernameLayout.addWidget(self.usernameLineEdit)

        passwordLayout = QHBoxLayout()
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordLineEdit)

        self.messagesTextEdit = QTextEdit()
        self.messageLineEdit = QLineEdit()
        self.sendButton = QPushButton("Gönder")
        self.sendButton.clicked.connect(self.send)

        messagesLayout = QVBoxLayout()
        messagesLayout.addWidget(self.messagesTextEdit)
        messagesLayout.addWidget(self.messageLineEdit)
        messagesLayout.addWidget(self.sendButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(usernameLayout)
        mainLayout.addLayout(passwordLayout)
        mainLayout.addLayout(messagesLayout)

        self.setLayout(mainLayout)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = self.cursor.fetchone()

        if result:
            self.username = username
            self.messagesTextEdit.setEnabled(True)
            self.messageLineEdit.setEnabled(True)
            self.sendButton.setEnabled(True)
        else:
            self.messagesTextEdit.setEnabled(False)
            self.messageLineEdit.setEnabled(False)
            self.sendButton.setEnabled(False)

    def send(self):
        message = self.messageLineEdit.text()

        self.cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (self.username, message))
        self.connection.commit()

        self.messagesTextEdit.append(f"{self.username}: {message}")
        self.messageLineEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


