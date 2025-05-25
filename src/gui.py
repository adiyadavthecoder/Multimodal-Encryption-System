import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QLabel, QFileDialog, QFrame, QGraphicsDropShadowEffect, QGraphicsBlurEffect,
    QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QMovie
from PyQt5.QtCore import Qt

from src.text_encryption import encrypt_text, decrypt_text
from src.image_encryption import encrypt_image, decrypt_image
from src.audio_encryption import encrypt_audio, decrypt_audio
from src.video_encryption import encrypt_video, decrypt_video

class GlowButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.07);
                color: white;
                font-size: 15px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(0, 200, 255))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)

class GlassWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Multimodal Encryption Tool")
        self.setGeometry(150, 100, 1080, 720)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window)
        self.setWindowOpacity(1.0)

        self.bg_label = QLabel(self)
        self.bg_label.setScaledContents(True)
        self.bg_movie = QMovie("Documents/Multimodal Encryption/cyber.gif")
        self.bg_label.setMovie(self.bg_movie)
        self.bg_movie.start()

        self.blur_overlay = QFrame(self)
        self.blur_overlay.setStyleSheet("background-color: rgba(160, 100, 255, 0.3);")
        neon_blur = QGraphicsBlurEffect()
        neon_blur.setBlurRadius(100)
        self.blur_overlay.setGraphicsEffect(neon_blur)

        self.border = QFrame(self)
        self.border.setStyleSheet("""
            QFrame {
                border: 1px solid rgba(180, 180, 180, 0.2);
                border-radius: 10px;
            }
        """)

        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 15, 25, 0.85);
                border-radius: 30px;
            }
        """)
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(50, 50, 50, 50)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.container)

        main_layout = QVBoxLayout(self.container)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("💡 Multimodal Encryption Tool")
        title.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        button_layout = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()

        buttons = [
            ("📝 Encrypt Text", self.encrypt_text_ui),
            ("🖼️ Encrypt Image", self.encrypt_image_ui),
            ("🎵 Encrypt Audio", self.encrypt_audio_ui),
            ("🎞️ Encrypt Video", self.encrypt_video_ui),
            ("📖 Decrypt Text", self.decrypt_text_ui),
            ("🔍 Decrypt Image", self.decrypt_image_ui),
            ("🔉 Decrypt Audio", self.decrypt_audio_ui),
            ("🎬 Decrypt Video", self.decrypt_video_ui),
        ]

        for i, (text, func) in enumerate(buttons):
            btn = GlowButton(text)
            btn.clicked.connect(func)
            (column1 if i < 4 else column2).addWidget(btn)

        button_layout.addLayout(column1)
        button_layout.addLayout(column2)
        main_layout.addLayout(button_layout)

        self.output_box = QTextEdit()
        self.output_box.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.6);
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.output_box.setPlaceholderText("💬 Output will appear here...")
        main_layout.addWidget(self.output_box)

    def resizeEvent(self, event):
        size = self.size()
        self.bg_label.resize(size)
        self.blur_overlay.resize(size)
        self.border.resize(size)
        super().resizeEvent(event)

    def display_message(self, msg):
        self.output_box.clear()
        self.output_box.setPlainText(msg)

    def file_dialog(self, prompt):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        return QFileDialog.getOpenFileName(self, prompt, "", "All Files (*)", options=options)[0]

    def save_dialog(self, prompt, default_name):
        return QFileDialog.getSaveFileName(self, prompt, default_name)[0]

    def encrypt_text_ui(self):
        file = self.file_dialog("Select Text File to Encrypt")
        if file:
            enc, key = encrypt_text(file)
            enc_path = self.save_dialog("Save Encrypted File As", "encrypted.txt")
            key_path = self.save_dialog("Save Key File As", "key.txt")
            if enc_path: os.rename(enc, enc_path)
            if key_path: os.rename(key, key_path)
            self.display_message(f"Encrypted File: {enc_path}\nKey File: {key_path}")

    def decrypt_text_ui(self):
        enc = self.file_dialog("Select Encrypted Text File")
        if not enc:
            return
        key = self.file_dialog("Select Key File for Text")
        if key:
            result = decrypt_text(enc, key)
            save_path = self.save_dialog("Save Decrypted File As", "decrypted.txt")
            if save_path:
                with open(save_path, "w") as f:
                    f.write(result)
                self.display_message(f"Decrypted File: {save_path}")

    def encrypt_image_ui(self):
        file = self.file_dialog("Select Image File to Encrypt")
        if file:
            enc, key = encrypt_image(file)
            enc_path = self.save_dialog("Save Encrypted Image As", "encrypted.png")
            key_path = self.save_dialog("Save Key File As", "key.txt")
            if enc_path: os.rename(enc, enc_path)
            if key_path: os.rename(key, key_path)
            self.display_message(f"Encrypted Image: {enc_path}\nKey File: {key_path}")

    def decrypt_image_ui(self):
        enc = self.file_dialog("Select Encrypted Image File")
        if not enc:
            return
        key = self.file_dialog("Select Key File for Image")
        if key:
            result = decrypt_image(enc, key)
            save_path = self.save_dialog("Save Decrypted Image As", "decrypted.png")
            if save_path:
                os.rename(result, save_path)
                self.display_message(f"Decrypted Image: {save_path}")

    def encrypt_audio_ui(self):
        file = self.file_dialog("Select Audio File to Encrypt")
        if file:
            enc, key = encrypt_audio(file)
            enc_path = self.save_dialog("Save Encrypted Audio As", "encrypted.wav")
            key_path = self.save_dialog("Save Key File As", "key.txt")
            if enc_path: os.rename(enc, enc_path)
            if key_path: os.rename(key, key_path)
            self.display_message(f"Encrypted Audio: {enc_path}\nKey File: {key_path}")

    def decrypt_audio_ui(self):
        enc = self.file_dialog("Select Encrypted Audio File")
        if not enc:
            return
        key = self.file_dialog("Select Key File for Audio")
        if key:
            result = decrypt_audio(enc, key)
            save_path = self.save_dialog("Save Decrypted Audio As", "decrypted.wav")
            if save_path:
                os.rename(result, save_path)
                self.display_message(f"Decrypted Audio: {save_path}")

    def encrypt_video_ui(self):
        file = self.file_dialog("Select Video File to Encrypt")
        if file:
            enc, key = encrypt_video(file)
            enc_path = self.save_dialog("Save Encrypted Video As", "encrypted.mp4")
            key_path = self.save_dialog("Save Key File As", "key.txt")
            if enc_path: os.rename(enc, enc_path)
            if key_path: os.rename(key, key_path)
            self.display_message(f"Encrypted Video: {enc_path}\nKey File: {key_path}")

    def decrypt_video_ui(self):
        enc = self.file_dialog("Select Encrypted Video File")
        if not enc:
            return
        key = self.file_dialog("Select Key File for Video")
        if key:
            result = decrypt_video(enc, key)
            save_path = self.save_dialog("Save Decrypted Video As", "decrypted.mp4")
            if save_path:
                os.rename(result, save_path)
                self.display_message(f"Decrypted Video: {save_path}")
