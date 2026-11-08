light_stylesheet = """
        QWidget { background: #f7f7f9; color: #2b2b2b; font-family: "Segoe UI", Arial; font-size: 14px; }
        QPushButton { background: #4a90e2; color: white; border: none; border-radius: 6px; padding: 8px 16px; }
        QPushButton:hover { background: #3d7cc4; }
        QLineEdit, QTextBrowser, QComboBox, QDateTimeEdit { background: white; border: 1px solid #d0d0d5; border-radius: 6px; padding: 6px 8px; }
        QTableWidget { background: white; border: 1px solid #d0d0d5; gridline-color: #ececf0; }
        QHeaderView::section { background: #eef2f7; border: none; padding: 6px; font-weight: bold; }
        """

dark_stylesheet = """
        QWidget { background: #1e1f22; color: #e4e6eb; font-family: "Segoe UI", Arial; font-size: 14px; }
        QPushButton { background: #3a7bd5; color: white; border: none; border-radius: 6px; padding: 8px 16px; }
        QPushButton:hover { background: #4a8be5; }
        QLineEdit, QTextBrowser, QComboBox, QDateTimeEdit { background: #2a2b2f; color: #e4e6eb; border: 1px solid #3a3b3f; border-radius: 6px; padding: 6px 8px; }
        QTableWidget { background: #2a2b2f; color: #e4e6eb; border: 1px solid #3a3b3f; gridline-color: #3a3b3f; selection-background-color: #2f4f7f; selection-color: white; }
        QHeaderView::section { background: #232427; color: #e4e6eb; border: none; padding: 6px; font-weight: bold; }
        QMenuBar { background: #232427; color: #e4e6eb; }
        QMenu { background: #2a2b2f; color: #e4e6eb; border: 1px solid #3a3b3f; }
        QMenu::item:selected { background: #3a7bd5; color: white; }
        QStatusBar { background: #232427; color: #b0b3b8; }
        """
