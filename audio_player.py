# audio_player.py（修改版）
import os
import pygame

class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path

    def start(self):
        try:
            pygame.mixer.init()
            if os.path.exists(self.file_path):
                pygame.mixer.music.load(self.file_path)
                pygame.mixer.music.play(-1)
            else:
                print(f"[Audio] 文件不存在: {self.file_path}")
        except Exception as e:
            print(f"[Audio] 播放失败: {e}")