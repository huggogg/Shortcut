import json
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QLabel, QLineEdit,
    QFormLayout, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "config/raccourcis.json")

class AddShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un script")

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.raccourci_input = QLineEdit()
        self.systeme_input = QSpinBox()
        self.systeme_input.setRange(0, 1)
        self.path_input = QLineEdit()
        self.hide_input = QSpinBox()
        self.hide_input.setRange(0, 1)

        layout.addRow("Nom", self.name_input)
        layout.addRow("Raccourci", self.raccourci_input)
        layout.addRow("Système (0 ou 1)", self.systeme_input)
        layout.addRow("Path", self.path_input)
        layout.addRow("Hide (0 ou 1)", self.hide_input)

        self.submit_button = QPushButton("Ajouter")
        self.submit_button.clicked.connect(self.accept)

        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "raccourci": self.raccourci_input.text().strip(),
            "systeme": self.systeme_input.value(),
            "path": self.path_input.text().strip(),
            "hide": self.hide_input.value()
        }

class ShortcutViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shortcut_Manager")
        self.resize(400, 500)

        self.is_dark = False
        self.shortcuts_data = self.load_data()
        self.filtered_data = self.shortcuts_data

        self.init_ui()
        self.apply_theme()
        self.populate_table()

    def load_data(self):
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"raccourcis": []}, f, indent=2)
        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)["raccourcis"]
            return [item for item in data if item.get("hide", 0) == 0]

    def save_data(self):
        all_data = self.shortcuts_data.copy()
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump({"raccourcis": all_data}, f, indent=2, ensure_ascii=False)

    def init_ui(self):
        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Tous", "Système", "Personnel"])
        self.combo_type.currentIndexChanged.connect(self.filter_data)

        self.theme_button = QPushButton("☀️")
        self.theme_button.setFixedSize(20, 20)
        self.theme_button.clicked.connect(self.toggle_theme)

        header_layout.addWidget(self.combo_type)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_button)

        layout.addLayout(header_layout)

        # Bouton Ajouter
        self.add_button = QPushButton("Ajouter un script")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Raccourci"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Désactiver l'affichage de la numérotation des lignes
        self.table.verticalHeader().setVisible(False)

        self.setLayout(layout)

    def filter_data(self):
        current = self.combo_type.currentText()
        if current == "Tous":
            self.filtered_data = [s for s in self.shortcuts_data if s["hide"] == 0]
        elif current == "Système":
            self.filtered_data = [s for s in self.shortcuts_data if s["systeme"] == 1 and s["hide"] == 0]
        elif current == "Personnel":
            self.filtered_data = [s for s in self.shortcuts_data if s["systeme"] == 0 and s["hide"] == 0]
        self.populate_table()

    def populate_table(self):
        self.table.setRowCount(0)
        for row_data in self.filtered_data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            desc_item = QTableWidgetItem(row_data["name"])
            if row_data["systeme"] == 1:
                font = QFont()
                font.setItalic(True)
                desc_item.setFont(font)

            shortcut_item = QTableWidgetItem(row_data["raccourci"])
            self.table.setItem(row, 0, desc_item)
            self.table.setItem(row, 1, shortcut_item)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.theme_button.setText("🌙" if self.is_dark else "☀️")
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: white; }
                QTableWidget { background-color: #3c3c3c; alternate-background-color: #2b2b2b; }
                QHeaderView::section { background-color: #444; color: white; }
            """)
        else:
            self.setStyleSheet("")

    def open_add_dialog(self):
        dialog = AddShortcutDialog(self)
        if dialog.exec() == QDialog.Accepted:
            new_entry = dialog.get_data()
            self.shortcuts_data.append(new_entry)
            self.save_data()
            self.filter_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ShortcutViewer()
    viewer.show()
    sys.exit(app.exec())
