import io
import sys
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDateTimeEdit,
    QLineEdit,
    QTextBrowser,
    QSlider,
    QPushButton,
)
from PyQt6.QtCore import Qt


class Create_file(QDialog):
    data_ready = pyqtSignal(list)

    def __init__(self, parent=None):
        self.titles = [
            "Дата, время",
            "Название:",
            "Описание:",
            "Уровень важности(от 1 до 3):",
            "Готово",
        ]
        super().__init__(parent)
        self.setWindowTitle("Form")
        self.resize(857, 767)
        root = QVBoxLayout(self)
        hbox = QHBoxLayout()
        root.addLayout(hbox, 1)
        v1 = QVBoxLayout()
        hbox.addLayout(v1, 1)
        self.label = QLabel(self.titles[0])
        v1.addWidget(self.label)
        self.dateTimeEdit = QDateTimeEdit()
        v1.addWidget(self.dateTimeEdit)
        v1.addStretch()
        v2 = QVBoxLayout()
        hbox.addLayout(v2, 2)
        self.label_3 = QLabel(self.titles[1])
        v2.addWidget(self.label_3)
        self.lineEdit = QLineEdit()
        v2.addWidget(self.lineEdit)
        self.label_2 = QLabel(self.titles[2])
        v2.addWidget(self.label_2)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setReadOnly(False)
        v2.addWidget(self.textBrowser, 1)
        v3 = QVBoxLayout()
        hbox.addLayout(v3, 1)
        self.label_4 = QLabel(self.titles[3])
        v3.addWidget(self.label_4)
        self.horizontalSlider = QSlider(Qt.Orientation.Horizontal)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(3)
        self.horizontalSlider.setPageStep(1)
        v3.addWidget(self.horizontalSlider)
        v3.addStretch()
        self.pushButton_2 = QPushButton(self.titles[4])
        v3.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.run)
        self.dateTimeEdit.setDisplayFormat("dd.MM.yyyy HH:mm")
        now = datetime.now()
        now_dt = QDateTime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        self.dateTimeEdit.setDateTime(now_dt)

    def run(self):
        result = []
        dt = self.dateTimeEdit.dateTime()
        result.append(dt.toString("yyyy-MM-dd HH:mm:ss").split()[0])
        result.append(dt.toString("yyyy-MM-dd HH:mm:ss").split()[1])
        name = self.lineEdit.text()
        result.append(name)
        description = self.textBrowser.toPlainText()
        result.append(description)
        level = self.horizontalSlider.value()
        result.append(level)
        self.data = result
        self.data_ready.emit(result)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Create_file()
    ex.show()
    sys.exit(app.exec())
