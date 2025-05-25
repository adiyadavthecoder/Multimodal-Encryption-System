import sys
from PyQt5.QtWidgets import QApplication
from src.gui import GlassWindow
from src.auth import AuthWindow

def main():
    app = QApplication(sys.argv)
    main_window = {}

    def launch_main_gui():
        auth.close()  # close login window
        main_window['gui'] = GlassWindow()
        main_window['gui'].show()

    auth = AuthWindow(on_auth_success=launch_main_gui)
    auth.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
