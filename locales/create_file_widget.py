import io
import sys
from datetime import datetime
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtWidgets import (
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
from locales.languages import ru_widget, eng_widget


class Create_file(QDialog):
    data_ready = pyqtSignal(list)

    def __init__(self, language, parent=None):
        super().__init__(parent)
        if language == "ru":
            self.titles = ru_widget
        else:
            self.titles = eng_widget
        self.setWindowTitle("Form")
        self.resize(857, 767)
        root = QVBoxLayout(self)
        hbox = QHBoxLayout()
        root.addLayout(hbox, 1)
        v1 = QVBoxLayout()
        hbox.addLayout(v1, 1)
        self.label = QLabel(self.titles["date_time"])
        v1.addWidget(self.label)
        self.dateTimeEdit = QDateTimeEdit()
        v1.addWidget(self.dateTimeEdit)
        v1.addStretch()
        v2 = QVBoxLayout()
        hbox.addLayout(v2, 2)
        self.label_3 = QLabel(self.titles["title"])
        v2.addWidget(self.label_3)
        self.lineEdit = QLineEdit()
        v2.addWidget(self.lineEdit)
        self.label_2 = QLabel(self.titles["description"])
        v2.addWidget(self.label_2)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setReadOnly(False)
        v2.addWidget(self.textBrowser, 1)
        v3 = QVBoxLayout()
        hbox.addLayout(v3, 1)
        self.label_4 = QLabel(self.titles["importance"])
        v3.addWidget(self.label_4)
        self.horizontalSlider = QSlider(Qt.Orientation.Horizontal)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(3)
        self.horizontalSlider.setPageStep(1)
        v3.addWidget(self.horizontalSlider)
        v3.addStretch()
        self.pushButton_2 = QPushButton(self.titles["done"])
        v3.addWidget(self.pushButton_2)
        self.pushButton_2.clicked.connect(self.run)
        self.dateTimeEdit.setDisplayFormat("dd.MM.yyyy HH:mm")
        now = datetime.now()
        now_dt = QDateTime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        self.dateTimeEdit.setDateTime(now_dt)
        self.textBrowser.installEventFilter(self)
        self.textBrowser.setTabChangesFocus(True)

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

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.AltModifier):
            if event.key() == Qt.Key.Key_Left:
                self.horizontalSlider.setValue(self.horizontalSlider.value() - 1)
            elif event.key() == Qt.Key.Key_Right:
                self.horizontalSlider.setValue(self.horizontalSlider.value() + 1)
        if event.modifiers() == (Qt.KeyboardModifier.ControlModifier):
            if event.key() == Qt.Key.Key_S:
                self.run()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Create_file()
    ex.show()
    sys.exit(app.exec())
