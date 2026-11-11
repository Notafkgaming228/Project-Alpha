import sys
import csv
import os
import sqlite3
from PyQt6.QtCore import Qt, QProcess
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
from PyQt6.QtGui import QColor, QBrush, QFont, QIcon, QCloseEvent
from locales.create_file_widget import Create_file
from locales.languages import ru_titles, en_titles
from locales.stylesheets import light_stylesheet, dark_stylesheet


class Taskplanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.light_stylesheet = light_stylesheet
        self.dark_stylesheet = dark_stylesheet

        self.ru_titles = ru_titles
        self.en_titles = en_titles
        self.titles = dict()

        self.setWindowTitle("project_alpha")
        self.setGeometry(100, 100, 1000, 700)
        if os.path.isdir("data"):
            pass
        else:
            os.mkdir("data")
        self.is_restarting = False
        try:
            with open("data/preferences.csv", "r", encoding="utf8") as preferences:
                row = next(csv.reader(preferences, delimiter=";"), None)
                self.current_theme = (
                    row[0] if row and row[0] in ("light", "dark") else "light"
                )
                self.current_lang = row[1] if row and row[1] in ("ru", "eng") else "eng"
        except FileNotFoundError:
            self.current_theme = "light"
            self.current_lang = "eng"
            with open(
                "data/preferences.csv", "w", encoding="utf8", newline=""
            ) as preferences:
                csv.writer(preferences, delimiter=";").writerow(["light", "eng"])

        QApplication.instance().setStyleSheet(
            self.light_stylesheet
            if self.current_theme == "light"
            else self.dark_stylesheet
        )
        if self.current_lang == "ru":
            self.titles = self.ru_titles
        else:
            self.titles = self.en_titles

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
        self.exit_button.clicked.connect(self.exit)
        start_page_layout.addWidget(self.exit_button)
        start_page_layout.addStretch()

        self.stacked_widget.addWidget(self.start_page)

        self.page_preferences = QWidget()  # настройки

        page_preferences_layout = QVBoxLayout(self.page_preferences)
        preferences_label = QLabel(self.titles["preferences"])
        page_preferences_layout.addWidget(preferences_label)

        select_theme_layout = QHBoxLayout()
        select_theme_label = QLabel(self.titles["select_theme"])

        back_button = QPushButton(self.titles["back"])
        back_button.clicked.connect(self.start_menu)

        select_theme_layout.addWidget(select_theme_label)

        self.theme_select = QComboBox(self)
        self.theme_select.addItems(
            [self.titles["light_theme"], self.titles["dark_theme"]]
        )
        self.theme_select.activated.connect(self.theme_swap)

        select_lang_layout = QHBoxLayout()
        select_lang_label = QLabel(self.titles["select_lang"])

        rus_button = QPushButton()
        rus_button.setIcon(QIcon("locales/rus_flag.png"))
        rus_button.clicked.connect(self.set_ru_language)

        eng_button = QPushButton()
        eng_button.setIcon(QIcon("locales/eng_flag.png"))
        eng_button.clicked.connect(self.set_eng_language)

        select_lang_layout.addWidget(select_lang_label)
        select_lang_layout.addWidget(rus_button)
        select_lang_layout.addWidget(eng_button)
        page_preferences_layout.addLayout(select_lang_layout)

        select_theme_layout.addWidget(self.theme_select)

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
        QApplication.quit()

    def open_preferences(self):
        self.stacked_widget.setCurrentWidget(self.page_preferences)
        self.theme_select.blockSignals(True)
        self.theme_select.setCurrentIndex(0 if self.current_theme == "light" else 1)
        self.theme_select.blockSignals(False)

    def open_task_table(self):
        self.tableWidget.blockSignals(True)
        try:
            connection = sqlite3.connect("data/tasks.db")
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
            self.con = sqlite3.connect("data/tasks.db")
            cur = self.con.cursor()
            result = cur.execute("SELECT * FROM tasks").fetchall()
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
            self.color_rows()
            self.make_columns_readonly()
            self.tableWidget.resizeColumnsToContents()
            for col in range(self.tableWidget.columnCount()):
                if self.tableWidget.columnWidth(col) > 300:
                    self.tableWidget.setColumnWidth(col, 300)
            self.modified = {}
        finally:
            self.tableWidget.blockSignals(False)

    def start_menu(self):
        self.stacked_widget.setCurrentWidget(self.start_page)
        self.statusBar().clearMessage()

    def create_new_task(self):
        task = Create_file(self.current_lang, self)
        if task.exec():
            connection = sqlite3.connect("data/tasks.db")
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
        with sqlite3.connect("data/tasks.db") as table:
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
        with sqlite3.connect("data/tasks.db") as table:
            try:
                table.execute(
                    f"UPDATE tasks SET {name} = ? WHERE id = ?", (new_value, table_id)
                )
                table.commit()
            except sqlite3.IntegrityError:
                self.statusBar().showMessage(self.titles["wrong_format"])
        self.open_task_table()

    def make_columns_readonly(self):
        blocked = self.tableWidget.blockSignals(True)
        try:
            for row in range(self.tableWidget.rowCount()):
                for col in (1, 2):
                    item = self.tableWidget.item(row, col)
                    if item:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        finally:
            self.tableWidget.blockSignals(blocked)

    def color_rows(self):
        colors = {
            "1": QColor(0, 125, 0),
            "2": QColor(125, 125, 0),
            "3": QColor(125, 0, 0),
        }
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 5)
            if item:
                item.setBackground(
                    QBrush(colors.get(item.text().strip(), QColor(255, 255, 255)))
                )

    def theme_swap(self, index):
        new_theme = "light" if index == 0 else "dark"
        if new_theme == self.current_theme:
            return
        self.current_theme = new_theme
        with open("data/preferences.csv", "w", encoding="utf8", newline="") as file:
            csv.writer(file, delimiter=";").writerow([new_theme, self.current_lang])
        QApplication.instance().setStyleSheet(
            self.light_stylesheet if new_theme == "light" else self.dark_stylesheet
        )
        if self.stacked_widget.currentWidget() is self.task_menu_page:
            self.color_rows()

    def set_eng_language(self):
        self.is_restarting = True
        new_lang = "eng"
        if self.current_lang == new_lang:
            pass
        else:
            self.current_lang = new_lang
            self.titles = self.en_titles
            with open("data/preferences.csv", "w", encoding="utf8", newline="") as file:
                csv.writer(file, delimiter=";").writerow(
                    [self.current_theme, self.current_lang]
                )
            self.restart_app()

    def set_ru_language(self):
        self.is_restarting = True
        new_lang = "ru"
        if self.current_lang == new_lang:
            pass
        else:
            self.current_lang = new_lang
            self.titles = self.ru_titles
            with open("data/preferences.csv", "w", encoding="utf8", newline="") as file:
                csv.writer(file, delimiter=";").writerow(
                    [self.current_theme, self.current_lang]
                )
            self.restart_app()

    def restart_app(self):
        QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.ControlModifier):
            if event.key() == Qt.Key.Key_I:
                self.open_preferences()
            elif event.key() == Qt.Key.Key_O:
                self.open_task_table()
            elif event.key() == Qt.Key.Key_X:
                self.exit()
            elif event.key() == Qt.Key.Key_X:
                self.exit()
            elif (
                self.stacked_widget.currentIndex() == 2 and event.key() == Qt.Key.Key_N
            ):
                self.create_new_task()
            elif (
                self.stacked_widget.currentIndex() == 1 and event.key() == Qt.Key.Key_E
            ):
                self.set_eng_language()
            elif (
                self.stacked_widget.currentIndex() == 1 and event.key() == Qt.Key.Key_R
            ):
                self.set_ru_language()
            elif (
                self.stacked_widget.currentIndex() == 1 and event.key() == Qt.Key.Key_D
            ):
                self.theme_select.setCurrentIndex(1)
                self.theme_swap(1)
            elif (
                self.stacked_widget.currentIndex() == 1 and event.key() == Qt.Key.Key_L
            ):
                self.theme_select.setCurrentIndex(0)
                self.theme_swap(0)
        elif (
            self.stacked_widget.currentIndex() == 2 and event.key() == Qt.Key.Key_Delete
        ):
            self.delete_task()
        elif event.key() == Qt.Key.Key_Backspace:
            self.start_menu()
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

    def closeEvent(self, event: QCloseEvent):
        if self.is_restarting:
            event.accept()
            return
        answer = QMessageBox.question(
            self,
            self.titles["acception"],
            self.titles["exit_acception"],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Taskplanner()
    ex.show()
    sys.exit(app.exec())
