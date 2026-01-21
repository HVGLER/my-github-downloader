# main.py
import sys
import os

# 优先使用本地 bin/PyQt5
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bin'))

from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()