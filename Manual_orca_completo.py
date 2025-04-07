import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QStackedWidget, QTextEdit, QGridLayout, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

KEYWORD_DATA = {
    "RHF / RKS": [
        {
            "Keyword": "RHF / RKS",
            "Input Block": "SCF",
            "Variable": "HFTYP",
            "Comment": "Selects closed-shell SCF"
        },
       
    ],
    "UHF / UKS": [
        {
            "Keyword": "UHF / UKS",
            "Input Block": "",
            "Variable": "",
            "Comment": "Selects spin unrestricted SCF"
        },
       
    ],
    "ROHF or ROKS": [
        {
            "Keyword": "ROHF or ROKS",
            "Input Block": "",
            "Variable": "",
            "Comment": "Selects open-shell spin restricted SCF"
        }
    ],
    "RIJCOSX": [
        {
            "Keyword": "RIJCOSX",
            "Input Block": "METHOD/SCF",
            "Variable": "RI,KMatrix",
            "Comment": "Sets the flag for the efficient RIJCOSX algorithm \n(treat the Columb term via RI and the Exchange \nterm via seminumerical integration) "
        }
    ],
    "DIRECTCONV": [
        {
            "Keyword": "DIRECTCONV",
            "Input Block": "SCF",
            "Variable": "SCFMODE",
            "Comment": "Selects an integral direct calculation \nSelects an integral conventional calculation "
        }
    ],
    "HUECKEL": [
        {
            "Keyword": "HUECKEL",
            "Input Block": "",
            "Variable": "",
            "Comment": "Selects the extended Huckel guess"
        }
    ],
    "VERYTIGHTSCF": [
        {
            "Keyword": "VERYTIGHTSCF",
            "Input Block": "SCF",
            "Variable": "",
            "Comment": "Selects very tight SCF converge"
        }
    ],
    "SCFCONVn": [
        {
            "Keyword": "SCFCONVn",
            "Input Block": "",
            "Variable": "",
            "Comment": "Selects energy convergence check ans \n sets ETol to 10^-n(n=6-10). Also selects \nappropiate thresh, tcut and bfcut values"
        }
    ],
    "VERYTIGHTOPT": [
        {
            "Keyword": "VERYTIGHTOPT",
            "Input Block": "GEOM",
            "Variable": "TollE,TolRMSG",
            "Comment": "Selects very tight optimization convergence"
        }
    ],
    "DIIS": [
        {
            "Keyword": "DIIS",
            "Input Block": "SCF",
            "Variable": "DISS",
            "Comment": "Turns DISS on"
        }
    ],
    "NODIIS": [
        {
            "Keyword": "NODIIS",
            "Input Block": "",
            "Variable": "",
            "Comment": "Turns DISS off"
        }
    ],
    "SOSCF": [
        {
            "Keyword": "SOSCF",
            "Input Block": "SCF",
            "Variable": "SOSCF",
            "Comment": "Turns SOSCF on"
        }
    ],
    "NOSOSCF": [
        {
            "Keyword": "NOSOSCF",
            "Input Block": "",
            "Variable": "",
            "Comment": "Turns SOSCF off"
        }
    ],
    "DAMP": [
        {
            "Keyword": "DAMP",
            "Input Block": "SCF",
            "Variable": "CNVDAMP",
            "Comment": "Turns damping on"
        }
    ],
    "NODAMP": [
        {
            "Keyword": "NODAMP",
            "Input Block": "",
            "Variable": "",
            "Comment": "Turns damping off"
        }
    ],
    "LSHIFT": [
        {
            "Keyword": "LSHIFT",
            "Input Block": "SCF",
            "Variable": "CNVSHIFT",
            "Comment": "Turns level shifthing on"
        }
    ],
    "NOLSHIFT": [
        {
            "Keyword": "NOLSHIFT",
            "Input Block": "",
            "Variable": "",
            "Comment": "Turns level shifthing off"
        }
    ],
    "VerySlowConv": [
        {
            "Keyword": "VerySlowConv",
            "Input Block": "",
            "Variable": "",
            "Comment": "Selects appropriate SCF convenger criteria \nfor very difficult case"
        }
    ]
}
# === Basis Set Data ===
BASIS_SETS = """\
cc-pVDZ      - Dunning correlation-consistent polarized valence double-zeta
cc-pVTZ      - Dunning correlation-consistent polarized valence triple-zeta
cc-pVQZ      - Dunning correlation-consistent polarized valence quadruple-zeta
cc-pV5Z      - Dunning correlation-consistent polarized valence 5-zeta
cc-pV6Z      - Dunning correlation-consistent polarized valence 6-zeta

aug-cc-pVnZ  - (n= D,T,Q,5,6) Augmented with diffuse functions
cc-pCVnZ     - (n= D,T,Q,5,6) Core-polarized basis sets
aug-cc-pCVnZ - (n= D,T,Q,5,6) As above, augmented with diffuse functions
cc-pwCVnZ    - (n= D,T,Q,5) Core-polarized with weighted core functions
aug-cc-pwCVnZ- (n= D,T,Q,5) As above, augmented with diffuse functions 
cc-pVn(+d)Z  -(n= D,T,Q,5) With tight d functions
"""

# === DFT Methods Data ===
DENSITY_FUNCTIONAL_METHODS_DATA = {
    "Hybrid functionals": [
        {"Keyword": "B3LYP and B3LYP/G", "Comment": "Popular B3LYP functional (20% HF exchange)."},
        
    ],
    "Range-separate hybrid functions": [
        {"Keyword": "wB97", "Comment": "Head-Gordon's fully variableDF wB97."},
        
    ]
}

class OrcaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORCA Manual Viewer")
        self.setGeometry(300, 150, 850, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #ffe6f0; }
            QLabel { color: #880e4f; }
            QPushButton {
                background-color: #f8bbd0;
                color: #4a004d;
                border: 1px solid #d48bb6;
                padding: 6px 12px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 140px;
            }
            QPushButton:hover { background-color: #f48fb1; }
            QTableWidget { background-color: #fff0f5; border: 1px solid #d48bb6; }
            QHeaderView::section {
                background-color: #f8bbd0;
                padding: 4px;
                font-weight: bold;
                color: #4a004d;
                border: 1px solid #d48bb6;
            }
            QTextEdit {
                background-color: #fff0f5;
                border: 1px solid #d48bb6;
                color: #4a004d;
                padding: 10px;
            }
        """)

        self.stacked_widget = QStackedWidget()
        self.start_page = QWidget()
        self.keyword_page = QWidget()
        self.basis_page = QWidget()
        self.density_page = QWidget()

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.keyword_page)
        self.stacked_widget.addWidget(self.basis_page)
        self.stacked_widget.addWidget(self.density_page)
        self.setCentralWidget(self.stacked_widget)

        self.init_start_page()
        self.init_keyword_page()
        self.init_basis_page()
        self.init_density_page()
        self.stacked_widget.setCurrentWidget(self.start_page)

    def init_start_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("<h2>ORCA Manual Viewer</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        keyword_button = QPushButton("Keywords")
        keyword_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.keyword_page))
        basis_button = QPushButton("Basis Sets")
        basis_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.basis_page))
        density_button = QPushButton("Density Functional Methods")
        density_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.density_page))

        button_layout.addWidget(keyword_button)
        button_layout.addWidget(basis_button)
        button_layout.addWidget(density_button)

        layout.addLayout(button_layout)
        self.start_page.setLayout(layout)

    def init_keyword_page(self):
        layout = QVBoxLayout()
        title = QLabel("Keywords")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin: 10px;")
        layout.addWidget(title)

        button_grid = QGridLayout()
        for i, name in enumerate(KEYWORD_DATA):
            btn = QPushButton(name)
            btn.clicked.connect(self.make_button_callback(name))
            button_grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(button_grid)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Keyword", "Input Block", "Variable", "Comment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.keyword_page.setLayout(layout)

    def make_button_callback(self, name):
        def callback():
            data = KEYWORD_DATA[name]
            self.table.setRowCount(len(data))
            for row, item in enumerate(data):
                for col, key in enumerate(["Keyword", "Input Block", "Variable", "Comment"]):
                    cell = QTableWidgetItem(item[key])
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    cell.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    cell.setFont(QFont("Consolas", 10))
                    self.table.setItem(row, col, cell)
                self.table.setRowHeight(row, 28 * (item["Comment"].count('\n') + 1))
        return callback

    def init_basis_page(self):
        layout = QVBoxLayout()
        title = QLabel("Correlation-consistent basis sets")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin-bottom: 10px;")
        layout.addWidget(title)

        basis_text = QTextEdit()
        basis_text.setReadOnly(True)
        basis_text.setFont(QFont("Consolas", 11))
        basis_text.setText(BASIS_SETS)
        layout.addWidget(basis_text)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.basis_page.setLayout(layout)

    def init_density_page(self):
        layout = QVBoxLayout()
        title = QLabel("Density Functional Methods")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin: 10px;")
        layout.addWidget(title)

        button_grid = QGridLayout()
        for i, name in enumerate(DENSITY_FUNCTIONAL_METHODS_DATA):
            btn = QPushButton(name)
            btn.clicked.connect(self.make_density_callback(name))
            button_grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(button_grid)

        self.density_table = QTableWidget()
        self.density_table.setColumnCount(2)
        self.density_table.setHorizontalHeaderLabels(["Keyword", "Comment"])
        self.density_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.density_table.verticalHeader().setVisible(False)
        layout.addWidget(self.density_table)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.density_page.setLayout(layout)

    def make_density_callback(self, name):
        def callback():
            data = DENSITY_FUNCTIONAL_METHODS_DATA[name]
            self.density_table.setRowCount(len(data))
            for row, item in enumerate(data):
                for col, key in enumerate(["Keyword", "Comment"]):
                    cell = QTableWidgetItem(item[key])
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    cell.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    cell.setFont(QFont("Consolas", 10))
                    self.density_table.setItem(row, col, cell)
                self.density_table.setRowHeight(row, 28 * (item["Comment"].count('\n') + 1))
        return callback


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = OrcaViewer()
    viewer.show()
    sys.exit(app.exec_())