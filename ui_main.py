# ui_main.py
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QMessageBox, QProgressBar, QTextEdit
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from github_logic import fetch_repos
from downloader import download_repo_zip
from audio_player import AudioPlayer
from config import BG_MUSIC_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub 仓库下载器（图形版）")
        self.resize(600, 500)

        # 初始化音频播放
        self.audio_player = AudioPlayer(BG_MUSIC_PATH)
        self.audio_player.start()

        # UI 组件
        self.username_input = QLineEdit()
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("(可选) GitHub Token")
        self.repo_list = QListWidget()
        self.status_bar = QTextEdit()
        self.status_bar.setReadOnly(True)
        self.download_btn = QPushButton("下载选中仓库")
        self.fetch_btn = QPushButton("获取仓库列表")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(QLabel("GitHub 用户名："))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Token（可选）："))
        layout.addWidget(self.token_input)
        layout.addWidget(self.fetch_btn)
        layout.addWidget(QLabel("仓库列表："))
        layout.addWidget(self.repo_list)
        layout.addWidget(self.download_btn)
        layout.addWidget(QLabel("状态："))
        layout.addWidget(self.status_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 信号连接
        self.fetch_btn.clicked.connect(self.on_fetch_repos)
        self.download_btn.clicked.connect(self.on_download)

        self.repos = []  # 存储仓库名

    def log(self, msg):
        self.status_bar.append(msg)

    def on_fetch_repos(self):
        username = self.username_input.text().strip()
        token = self.token_input.text().strip()
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入 GitHub 用户名！")
            return

        self.log("正在获取仓库列表...")
        self.thread = FetchReposThread(username, token)
        self.thread.result.connect(self.on_repos_fetched)
        self.thread.error.connect(self.log)
        self.thread.start()

    def on_repos_fetched(self, repos):
        self.repos = repos
        self.repo_list.clear()
        self.repo_list.addItems(repos)
        self.log(f"成功获取 {len(repos)} 个仓库。")

    def on_download(self):
        current = self.repo_list.currentItem()
        if not current:
            QMessageBox.warning(self, "未选择", "请先选择一个仓库！")
            return
        repo_name = current.text()
        username = self.username_input.text().strip()
        self.log(f"开始下载 {username}/{repo_name} ...")
        save_path = f"C:\\Users\\{repo_name}.zip"
        self.download_thread = DownloadThread(username, repo_name, save_path)
        self.download_thread.finished.connect(lambda: self.log(f"下载完成！保存至：{save_path}"))
        self.download_thread.error.connect(self.log)
        self.download_thread.start()


# ———————— 多线程支持 ————————

class FetchReposThread(QThread):
    result = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, username, token):
        super().__init__()
        self.username = username
        self.token = token

    def run(self):
        try:
            repos = fetch_repos(self.username, self.token)
            self.result.emit(repos)
        except Exception as e:
            self.error.emit(f"获取失败: {str(e)}")


class DownloadThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, username, repo, path):
        super().__init__()
        self.username = username
        self.repo = repo
        self.path = path

    def run(self):
        try:
            download_repo_zip(self.username, self.repo, self.path)
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"下载失败: {str(e)}")