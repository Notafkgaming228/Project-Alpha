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
    QStackedWidget,
    QComboBox,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtGui import QFont
from create_file_widget import Create_file


class Taskplanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.titles = {
            "welcome_title": "Добро пожаловать в Project alpha",
            "delete_event": "Удалить событие",
            "open_table": "Открыть список задач",
            "preferences": "Настройки",
            "select_file": "Выберите файл",
            "file_format": "базы данных (*.db);",
            "back": "Назад",
            "exit": "Выйти",
            "create_event": "Создать событие",
            "acception": "Подтверждение",
            "exit_acception": "Вы уверены, что хотите выйти?",
            "project_alpha": "Project alpha",
            "select_theme": "Выберите тему",
            "light_theme": "Светлая",
            "dark_theme": "Тёмная",
            "wrong_format": "Неверный формат",
            "nothing_found": "Ничего не нашлось",
            "unredactable": "Нельзя редактировать id",
            "headers": {
                "id": "id",
                "date": "Дата",
                "time": "Время",
                "name": "Название",
                "description": "Описание",
                "level": "Уровень",
            },
        }
        self.setWindowTitle(self.titles["project_alpha"])
        self.setGeometry(100, 100, 1000, 700)
        try:
            with open("preferences.csv", "r", encoding="utf8") as preferences:
                pass
        except FileNotFoundError:
            with open("preferences.csv", "w", encoding="utf8") as preferences:
                writer = csv.writer(preferences, delimiter=";")
                writer.writerow(["light"])

        container = QWidget()  # меню
        self.setCentralWidget(container)
        self.start_layout = QVBoxLayout(container)

        self.stacked_widget = QStackedWidget(self)
        self.start_layout.addWidget(self.stacked_widget)

        self.start_page = QWidget()
        start_page_layout = QVBoxLayout(self.start_page)

        start_font = QFont("Arial", 18)

        self.start_label = QLabel(self.titles["welcome_title"])
        self.start_label.setFont(start_font)
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_page_layout.addWidget(self.start_label)
        start_page_layout.addStretch()

        self.open_file_button = QPushButton(self.titles["open_table"])
        self.open_file_button.setFont(start_font)
        self.open_file_button.clicked.connect(self.open_task_table)
        start_page_layout.addWidget(self.open_file_button)

        self.preferences_button = QPushButton(self.titles["preferences"])
        self.preferences_button.setFont(start_font)
        start_page_layout.addWidget(self.preferences_button)
        self.preferences_button.clicked.connect(self.open_preferences)

        self.exit_button = QPushButton(self.titles["exit"])
        self.exit_button.setFont(start_font)
        self.exit_button.clicked.connect(self.exit)
        start_page_layout.addWidget(self.exit_button)
        start_page_layout.addStretch()

        self.stacked_widget.addWidget(self.start_page)

        self.page_preferences = QWidget()  # настройки

        page_preferences_layout = QVBoxLayout(self.page_preferences)
        preferences_label = QLabel(self.titles["preferences"])
        preferences_label.setFont(start_font)
        page_preferences_layout.addWidget(preferences_label)

        select_theme_layout = QHBoxLayout()
        select_theme_label = QLabel(self.titles["select_theme"])

        back_button = QPushButton(self.titles["back"])
        back_button.setFont(start_font)
        back_button.clicked.connect(self.start_menu)

        select_theme_layout.addWidget(select_theme_label)

        theme_select = QComboBox(self)
        theme_select.addItems([self.titles["light_theme"], self.titles["dark_theme"]])
        select_theme_layout.addWidget(theme_select)

        page_preferences_layout.addLayout(select_theme_layout)
        page_preferences_layout.addStretch()
        page_preferences_layout.addWidget(back_button)

        self.stacked_widget.addWidget(self.page_preferences)

        self.task_menu_page = QWidget()  # список задач
        self.task_menu_layout = QHBoxLayout(self.task_menu_page)
        self.tableWidget = QTableWidget()
        self.task_menu_layout.addWidget(self.tableWidget)
        self.tableWidget.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableWidget.itemChanged.connect(self.update_table)
        self.button_layout = QVBoxLayout()

        back_button = QPushButton(self.titles["back"])
        back_button.setFont(start_font)
        back_button.clicked.connect(self.start_menu)

        add_button = QPushButton(self.titles["create_event"])
        add_button.setFont(start_font)
        add_button.clicked.connect(self.create_new_task)

        del_button = QPushButton(self.titles["delete_event"])
        del_button.setFont(start_font)
        del_button.clicked.connect(self.delete_task)

        self.button_layout.addWidget(add_button)
        self.button_layout.addWidget(del_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(back_button)

        self.task_menu_layout.addLayout(self.button_layout)
        self.stacked_widget.addWidget(self.task_menu_page)

    def exit(self):
        answer = QMessageBox.question(
            self,
            self.titles["acception"],
            self.titles["exit_acception"],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            sys.exit(app.exec())

    def open_preferences(self):
        self.stacked_widget.setCurrentWidget(self.page_preferences)

    def open_task_table(self):
        self.tableWidget.blockSignals(True)
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            level INTEGER CHECK (level >= 1 AND level <= 3) NOT NULL
        )
        """)
        connection.commit()
        connection.close()
        self.stacked_widget.setCurrentWidget(self.task_menu_page)
        self.con = sqlite3.connect("tasks.db")
        cur = self.con.cursor()
        result = cur.execute(
            "SELECT * FROM tasks",
        ).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage(self.titles["nothing_found"])
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.title = [description[0] for description in cur.description]
        headers_map = self.titles.get("headers", {})
        self.tableWidget.setHorizontalHeaderLabels(
            [headers_map.get(col, col) for col in self.title]
        )
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.blockSignals(False)
        self.modified = {}

    def start_menu(self):
        self.stacked_widget.setCurrentWidget(self.start_page)
        self.statusBar().clearMessage()

    def create_new_task(self):
        task = Create_file(self)
        if task.exec():
            connection = sqlite3.connect("tasks.db")
            cursor = connection.cursor()
            cursor.execute(
                """
            INSERT INTO tasks (date, time, name, description, level) 
            VALUES (?, ?, ?, ?, ?)
            """,
                task.data,
            )
            self.statusBar().clearMessage()
            connection.commit()
            connection.close()
            self.open_task_table()

    def delete_task(self):
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        if not selected_indexes:
            return
        delete = sorted(set(index.row() for index in selected_indexes), reverse=True)
        with sqlite3.connect("tasks.db") as table:
            cursor = table.cursor()
            for row in delete:
                id = self.tableWidget.item(row, 0)
                if id is not None:
                    table_id = int(id.text())
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (table_id,))
                self.tableWidget.removeRow(row)
            table.commit()
            self.open_task_table()

    def update_table(self, item):
        row = item.row()
        col = item.column()
        new_value = item.text().strip()
        id = self.tableWidget.item(row, 0)
        if not id:
            return
        try:
            table_id = int(id.text())
        except ValueError:
            self.statusBar().showMessage(self.titles["unredactable"])
            self.open_task_table()
        column_names = {
            1: "date",
            2: "time",
            3: "name",
            4: "description",
            5: "level",
        }

        name = column_names.get(col)
        if not name:
            return
        with sqlite3.connect("tasks.db") as table:
            try:
                table.execute(
                    f"UPDATE tasks SET {name} = ? WHERE id = ?", (new_value, table_id)
                )
                table.commit()
            except sqlite3.IntegrityError:
                self.statusBar().showMessage(self.titles["wrong_format"])
        self.open_task_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Taskplanner()
    ex.show()
    sys.exit(app.exec())
