import sys
import csv
import sqlite3
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
    QStackedWidget,
    QComboBox,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtGui import QFont
from create_file_widget import Create_file


class Taskplanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.all_titles = [
            "Выберите тему приложения.",
            "Выберите тему",
            "Тёмная",
            "Светлая",
            "Добро пожаловать в Project alpha",
            "Deleted",
            "Открыть список задач",
            "Настройки",
            "Выберите файл",
            "базы данных (*.db);",
            "Назад",
            "Выйти",
            "Создать событие",
            "Подтверждение",
            "Вы уверены, что хотите выйти?"
        ]
        self.setWindowTitle("Project alpha")
        self.setGeometry(100, 100, 1000, 700)
        try:
            with open("preferences.csv", "r", encoding="utf8") as preferences:
                pass
        except FileNotFoundError:

            theme, ok_pressed = QInputDialog.getItem(
                self,
                self.all_titles[0],
                self.all_titles[1],
                (self.all_titles[2], self.all_titles[3]),
                0,
                False,
            )
            if ok_pressed:
                with open("preferences.csv", "w", encoding="utf8") as preferences:
                    writer = csv.writer(preferences, delimiter=";")
                    writer.writerow(["dark"] if theme ==
                                    "Тёмная" else ["light"])

        container = QWidget()  # меню
        self.setCentralWidget(container)
        self.start_layout = QVBoxLayout(container)

        self.stacked_widget = QStackedWidget(self)
        self.start_layout.addWidget(self.stacked_widget)

        self.start_page = QWidget()
        start_page_layout = QVBoxLayout(self.start_page)

        start_font = QFont("Arial", 18)

        self.start_label = QLabel(self.all_titles[4])
        self.start_label.setFont(start_font)
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_page_layout.addWidget(self.start_label)
        start_page_layout.addStretch()

        self.open_file_button = QPushButton(self.all_titles[6])
        self.open_file_button.setFont(start_font)
        self.open_file_button.clicked.connect(self.open_task_table)
        start_page_layout.addWidget(self.open_file_button)

        self.preferences_button = QPushButton(self.all_titles[7])
        self.preferences_button.setFont(start_font)
        start_page_layout.addWidget(self.preferences_button)
        self.preferences_button.clicked.connect(self.open_preferences)

        self.exit_button = QPushButton(self.all_titles[11])
        self.exit_button.setFont(start_font)
        self.exit_button.clicked.connect(self.exit)
        start_page_layout.addWidget(self.exit_button)
        start_page_layout.addStretch()

        self.stacked_widget.addWidget(self.start_page)

        self.page_preferences = QWidget()  # настройки

        page_preferences_layout = QVBoxLayout(self.page_preferences)
        preferences_label = QLabel(self.all_titles[7])
        preferences_label.setFont(start_font)
        page_preferences_layout.addWidget(preferences_label)

        select_theme_layout = QHBoxLayout()
        select_theme_label = QLabel(self.all_titles[1])

        back_button = QPushButton(self.all_titles[10])
        back_button.setFont(start_font)
        back_button.clicked.connect(self.start_menu)

        select_theme_layout.addWidget(select_theme_label)

        theme_select = QComboBox(self)
        theme_select.addItems([self.all_titles[2], self.all_titles[3]])
        select_theme_layout.addWidget(theme_select)

        page_preferences_layout.addLayout(select_theme_layout)
        page_preferences_layout.addStretch()
        page_preferences_layout.addWidget(back_button)

        self.stacked_widget.addWidget(self.page_preferences)

        self.task_menu_page = QWidget()  # список задач
        self.task_menu_layout = QHBoxLayout(self.task_menu_page)
        self.task_table = QTableWidget()  # временно пустой
        self.task_menu_layout.addWidget(self.task_table)
        self.button_layout = QVBoxLayout()

        back_button = QPushButton(self.all_titles[10])
        back_button.setFont(start_font)
        back_button.clicked.connect(self.start_menu)

        add_button = QPushButton(self.all_titles[12])
        add_button.setFont(start_font)
        add_button.clicked.connect(self.create_new_task)

        self.button_layout.addWidget(add_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(back_button)

        self.task_menu_layout.addLayout(self.button_layout)
        self.stacked_widget.addWidget(self.task_menu_page)

    def exit(self):
        answer = QMessageBox.question(
            self,
            self.all_titles[13],
            self.all_titles[14],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            sys.exit(app.exec())

    def open_table(self):
        file = QFileDialog.getOpenFileNames(
            self, self.all_titles[8], "", self.all_titles[9]
        )[0]

    def open_preferences(self):
        self.stacked_widget.setCurrentWidget(self.page_preferences)

    def open_task_table(self):
        self.stacked_widget.setCurrentWidget(self.task_menu_page)

    def start_menu(self):
        self.stacked_widget.setCurrentWidget(self.start_page)

    def create_new_task(self):
        task = Create_file(self)
        if task.exec():
            data = task.result()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Taskplanner()
    ex.show()
    sys.exit(app.exec())
