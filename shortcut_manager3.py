import sys
import json
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QScrollArea, QHeaderView

# Charger les raccourcis depuis le fichier JSON
def load_raccourcis():
    try:
        with open("raccourcis.json", "r", encoding="utf-8") as f:  # Assurer que le fichier est lu avec UTF-8
            data = json.load(f)
        return data.get("raccourcis", [])
    except FileNotFoundError:
        return []

class ShortcutWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Raccourcis Clavier")
        
        # Permettre à la fenêtre d'être redimensionnée
        self.setMinimumSize(QSize(200, 100))  # Taille minimale
        self.resize(300, 400)  # Taille initiale

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer une table
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Raccourci"])
        
        # Désactiver l'affichage de la numérotation des lignes
        self.table.verticalHeader().setVisible(False)

        # Ajuster la taille des colonnes proportionnellement à la fenêtre
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Première colonne (75%)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Deuxième colonne (25%)
        
        # Ajouter des données au tableau
        raccourcis = load_raccourcis()
        for raccourci in raccourcis:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # Vérifier si "systeme" est égal à 1 et ajouter "Raccourci système" en italique si nécessaire
            description = raccourci["name"]
            if raccourci.get("systeme") == 1:
                font = QFont("Arial", 10)
                font.setItalic(True)  # Appliquer la police en italique
            else:
                font = QFont("Arial", 10)  # Police normale

            # Ajouter la description en italique si nécessaire
            self.table.setItem(row_position, 0, QTableWidgetItem(description))
            self.table.item(row_position, 0).setFont(font)
            
            # Ajouter le raccourci à la deuxième colonne
            raccourci_item = QTableWidgetItem(raccourci["raccourci"])
            raccourci_item.setTextAlignment(Qt.AlignCenter)  # Centrer le texte
            self.table.setItem(row_position, 1, raccourci_item)

        # Personnalisation du tableau
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Désactive l'édition des cellules
        self.table.setSelectionMode(QTableWidget.NoSelection)  # Désactive la sélection des cellules
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # Désactive la sélection par item

        # Créer un layout vertical et ajouter la table
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)

        # Ajouter un scroll si nécessaire
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        # Appliquer un style CSS pour arrondir les cellules et supprimer la sélection
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            QTableWidget::item {
                border-radius: 8px;
                padding: 5px;
                margin: 5px;
            }
            QHeaderView::section {
                border-radius: 10px;
                background-color: #dddddd;
            }
            QTableWidget::item:selected {
                background-color: transparent;  /* Désactive l'effet de sélection */
            }
            QTableWidget:focus {
                outline: none;  /* Désactive la bordure focus qui peut apparaître */
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShortcutWindow()
    window.show()
    sys.exit(app.exec())
