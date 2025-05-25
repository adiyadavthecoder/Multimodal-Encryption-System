import json
import hashlib
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QStackedLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt

ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump({}, f)
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AuthWindow(QWidget):
    def __init__(self, on_auth_success):
        super().__init__()
        self.setWindowTitle("🔐 User Authentication")
        self.setGeometry(600, 300, 400, 300)
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.on_auth_success = on_auth_success

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.init_main_menu()
        self.init_login_menu()
        self.init_register_menu()

        self.stack.setCurrentWidget(self.main_menu)

    def init_main_menu(self):
        self.main_menu = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome!")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.login_menu))
        layout.addWidget(login_btn)

        register_btn = QPushButton("Create New Account")
        register_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.register_menu))
        layout.addWidget(register_btn)

        self.main_menu.setLayout(layout)
        self.stack.addWidget(self.main_menu)

    def init_login_menu(self):
        self.login_menu = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel("👤 Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("🔒 Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        back_btn = QPushButton("⬅ Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(back_btn)

        self.login_menu.setLayout(layout)
        self.stack.addWidget(self.login_menu)

    def init_register_menu(self):
        self.register_menu = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel("👤 New Username:"))
        self.new_user_input = QLineEdit()
        layout.addWidget(self.new_user_input)

        layout.addWidget(QLabel("🔒 New Password:"))
        self.new_pass_input = QLineEdit()
        self.new_pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_pass_input)

        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.create_account)
        layout.addWidget(register_btn)

        back_btn = QPushButton("⬅ Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        layout.addWidget(back_btn)

        self.register_menu.setLayout(layout)
        self.stack.addWidget(self.register_menu)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        accounts = load_accounts()

        if username in accounts and accounts[username] == hash_password(password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.on_auth_success()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

    def create_account(self):
        username = self.new_user_input.text().strip()
        password = self.new_pass_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password cannot be empty!")
            return

        accounts = load_accounts()
        if username in accounts:
            QMessageBox.warning(self, "Error", "Username already exists!")
        else:
            accounts[username] = hash_password(password)
            save_accounts(accounts)
            QMessageBox.information(self, "Success", "Account created! Please log in.")
            self.stack.setCurrentWidget(self.main_menu)
