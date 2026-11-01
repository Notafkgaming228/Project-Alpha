import io
import sys
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog

titles = ["Дата, время", "Название:", "Описание:", "Уровень важности(от 1 до 3):"]

template = f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>857</width>
    <height>767</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout_6">
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_3">
     <property name="sizeConstraint">
      <enum>QLayout::SetMaximumSize</enum>
     </property>
     <item>
      <layout class="QVBoxLayout" name="verticalLayout_5">
       <item>
        <widget class="QLabel" name="label">
         <property name="text">
          <string>{titles[0]}</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QDateTimeEdit" name="dateTimeEdit"/>
       </item>
       <item>
        <spacer name="verticalSpacer">
         <property name="orientation">
          <enum>Qt::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>20</width>
           <height>40</height>
          </size>
         </property>
        </spacer>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QVBoxLayout" name="verticalLayout_4">
       <item>
        <widget class="QLabel" name="label_3">
         <property name="text">
          <string>{titles[1]}</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLineEdit" name="lineEdit"/>
       </item>
       <item>
        <widget class="QLabel" name="label_2">
         <property name="text">
          <string>{titles[2]}</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QTextBrowser" name="textBrowser">
         <property name="readOnly">
          <bool>false</bool>
         </property>
        </widget>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QVBoxLayout" name="verticalLayout_3">
       <property name="sizeConstraint">
        <enum>QLayout::SetMaximumSize</enum>
       </property>
       <item>
        <widget class="QLabel" name="label_4">
         <property name="text">
          <string>{titles[3]}</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QSlider" name="horizontalSlider">
         <property name="minimum">
          <number>1</number>
         </property>
         <property name="maximum">
          <number>3</number>
         </property>
         <property name="pageStep">
          <number>1</number>
         </property>
         <property name="orientation">
          <enum>Qt::Horizontal</enum>
         </property>
        </widget>
       </item>
       <item>
        <spacer name="verticalSpacer_2">
         <property name="orientation">
          <enum>Qt::Vertical</enum>
         </property>
         <property name="sizeHint" stdset="0">
          <size>
           <width>20</width>
           <height>40</height>
          </size>
         </property>
        </spacer>
       </item>
       <item>
        <widget class="QPushButton" name="pushButton_2">
         <property name="text">
          <string>Готово</string>
         </property>
        </widget>
       </item>
      </layout>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>

"""


class Create_file(QDialog):
    data_ready = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.pushButton_2.clicked.connect(self.run)

    def run(self):
        result = []
        dt = self.dateTimeEdit.dateTime()
        result.append(dt.toString("yyyy-MM-dd HH:mm:ss"))
        name = self.lineEdit.text()
        result.append(name)
        description = self.textBrowser.toPlainText()
        result.append(description)
        level = self.horizontalSlider.value()
        result.append(level)
        print(result)
        self.data_ready.emit(result)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Create_file()
    ex.show()
    sys.exit(app.exec())
