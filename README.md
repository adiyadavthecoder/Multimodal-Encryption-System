🔐 Multimodal Encryption System

This is a desktop application made using Python and PyQt5.  
It lets you encrypt and decrypt different types of data like:
- 📝 Text files
- 🖼️ Images
- 🎵 Audio files
- 🎬 Video files
It also has a login system.

💡 Features:

- Secure login/signup system
- Easy-to-use graphical interface (GUI)
- Encrypt and decrypt:
  - Text
  - Images
  - Audio
  - Videos
- Choose where to save your encrypted or decrypted files
- Everything runs locally on your computer

🛠️ How to Use:

Step 1. Install Python (if not already installed)
Download from: https://www.python.org/downloads/

Step 2. Install required libraries
Open terminal or command prompt and run: pip install -r requirements.txt

Step 3. Start the application
Run this command in the terminal: python main.py
The app window will open and you can start encrypting!

📁 Project Structure:

Hybrid-Encryption-System/
├── main.py               ← The main file to run the application
├── requirements.txt      ← Libraries needed for the application
├── README.md             ← This file
├── .gitignore            ← Files to be ignored by Git
└── src/
    ├── gui.py
    ├── auth.py
    ├── text_encryption.py
    ├── image_encryption.py
    ├── audio_encryption.py
    ├── video_encryption.py
    └── utils.py

📌 Note: 
This app works offline and keeps all your encrypted files safe on your computer.
