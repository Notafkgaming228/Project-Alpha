import sys
import csv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QInputDialog,
)
from PyQt6.QtGui import QFont


class Taskplanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main()

    def main(self):
        self.setWindowTitle("Project alpha")
        self.setGeometry(100, 100, 1000, 700)

        try:
            with open("preferences.csv", "r", encoding="utf8") as preferences:
                pass
        except FileNotFoundError:
            theme, ok_pressed = QInputDialog.getItem(
                self,
                "Выберите тему приложения.",
                "Выберите тему",
                ("Тёмная", "Светлая"),
                0,
                False,
            )
            if ok_pressed:
                with open("preferences.csv", "w", encoding="utf8") as preferences:
                    writer = csv.writer(preferences, delimiter=";")
                    writer.writerow(["dark"] if theme == "Тёмная" else ["light"])

        container = QWidget()
        self.setCentralWidget(container)
        self.start_layout = QVBoxLayout(container)

        start_font = QFont("Arial", 18)
        self.start_label = QLabel("Добро пожаловать в Project alpha", self)
        self.start_label.resize(900, 150)
        self.start_label.setFont(start_font)
        self.start_layout.addWidget(self.start_label)
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_layout.addStretch()

        self.open_new_button = QPushButton("Создать новый файл", self)
        self.open_new_button.setFont(start_font)
        self.start_layout.addWidget(self.open_new_button)

        self.open_file_button = QPushButton("Открыть файл", self)
        self.open_file_button.setFont(start_font)
        self.start_layout.addWidget(self.open_file_button)
        self.open_file_button.clicked.connect(self.open_file)

        self.preferences_button = QPushButton("Настройки", self)
        self.preferences_button.setFont(start_font)
        self.start_layout.addWidget(self.preferences_button)
        self.start_layout.addStretch()

    def open_file(self):
        file = QFileDialog.getOpenFileNames(
            self, "Выберите файл", "", "базы данных (*.db);"
        )[0]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Taskplanner()
    ex.show()
    sys.exit(app.exec())
