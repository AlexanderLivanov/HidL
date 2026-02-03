import sys
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import pygame

pygame.mixer.init()
pygame.mixer.music.load("ach.wav")


class AchievementPopup(QWidget):
    def __init__(self, app, title, text):
        super().__init__()
        self.app = app

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(320, 80)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("container")

        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(16, 12, 16, 12)
        container_layout.setSpacing(14)

        icon = QLabel()
        pix = QPixmap("logo_new.png").scaled(
            64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icon.setPixmap(pix)
        icon.setFixedSize(64, 64)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(Qt.cyan)
        glow.setOffset(0, 0)
        icon.setGraphicsEffect(glow)

        text_box = QVBoxLayout()
        text_box.setSpacing(2)

        title_label = QLabel("Получено новое достижение")
        title_label.setFont(QFont("Segoe UI", 9))
        title_label.setStyleSheet("color: #66c0f4;")

        desc_label = QLabel(text)
        desc_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        desc_label.setStyleSheet("color: white;")

        text_box.addWidget(title_label)
        text_box.addWidget(desc_label)

        container_layout.addWidget(icon)
        container_layout.addLayout(text_box)

        root.addWidget(container)

        self.setStyleSheet("""
            QFrame#container {
                background-color: #1b1b1b;
                border-top: 2px solid #66c0f4;
            }
        """)

        screen = QApplication.primaryScreen().availableGeometry()

        self.start_rect = QRect(
            screen.width(),
            screen.height() - self.height(),
            self.width(),
            self.height()
        )
        self.end_rect = QRect(
            screen.width() - self.width(),
            screen.height() - self.height(),
            self.width(),
            self.height()
        )

        self.setGeometry(self.start_rect)
        self.setWindowOpacity(0)

        self.anim_pos = QPropertyAnimation(self, b"geometry")
        self.anim_pos.setDuration(400)
        self.anim_pos.setStartValue(self.start_rect)
        self.anim_pos.setEndValue(self.end_rect)

        self.anim_opacity = QPropertyAnimation(self, b"windowOpacity")
        self.anim_opacity.setDuration(400)
        self.anim_opacity.setStartValue(0)
        self.anim_opacity.setEndValue(1)

        self.anim_pos.start()
        self.anim_opacity.start()

        pygame.mixer.music.play()
        QTimer.singleShot(3500, self.close_anim)

    def close_anim(self):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(self.geometry())
        anim.setEndValue(self.start_rect)
        anim.finished.connect(self.exit)
        anim.start()
        self.anim = anim

    def exit(self):
        self.close()
        self.app.quit()


if __name__ == "__main__":
    time.sleep(1)
    app = QApplication(sys.argv)

    popup = AchievementPopup(
        app,
        "Achievement unlocked",
        "Привет, мир!"
    )
    popup.show()
    sys.exit(app.exec())
