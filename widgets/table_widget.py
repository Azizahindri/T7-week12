#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont


DARK_BG      = "#1A1D2E"
SURFACE      = "#252840"
SURFACE2     = "#2E3250"
ACCENT       = "#4C9BE8"
TEXT         = "#E8EAF6"
TEXT_DIM     = "#8892B0"
ROW_ODD      = "#1E2136"
ROW_EVEN     = "#252840"
HEADER_BG    = "#0D1117"


class DataTableWidget(QWidget):

    DISPLAY_COLS = [
        "Invoice ID", "Branch", "City", "Customer type", "Gender",
        "Product line", "Unit price", "Quantity", "Total",
        "Date", "Payment", "Rating"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        info_bar = QHBoxLayout()
        self.lbl_count = QLabel("0 baris ditampilkan")
        self.lbl_count.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px;")
        self.lbl_total = QLabel("Total: $0.00")
        self.lbl_total.setStyleSheet(
            f"color: {ACCENT}; font-size: 11px; font-weight: bold;"
        )
        info_bar.addWidget(self.lbl_count)
        info_bar.addStretch()
        info_bar.addWidget(self.lbl_total)
        layout.addLayout(info_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.DISPLAY_COLS))
        self.table.setHorizontalHeaderLabels(self.DISPLAY_COLS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(True)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        hh.setStretchLastSection(True)

        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {DARK_BG};
                alternate-background-color: {ROW_ODD};
                color: {TEXT};
                border: 1px solid {SURFACE2};
                border-radius: 8px;
                gridline-color: {SURFACE2};
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {SURFACE2};
            }}
            QTableWidget::item:selected {{
                background-color: {ACCENT};
                color: {DARK_BG};
            }}
            QHeaderView::section {{
                background-color: {HEADER_BG};
                color: {TEXT};
                padding: 6px 8px;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-bottom: 2px solid {ACCENT};
            }}
            QScrollBar:vertical {{
                background: {SURFACE};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {SURFACE2};
                border-radius: 4px;
            }}
        """)

        layout.addWidget(self.table)

    def load_data(self, df: pd.DataFrame):
        """Isi tabel dengan data dari DataFrame."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        cols = [c for c in self.DISPLAY_COLS if c in df.columns]
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)

        for row_idx, row in df.iterrows():
            self.table.insertRow(self.table.rowCount())
            for col_idx, col in enumerate(cols):
                val = row.get(col, "")
                if col == "Date" and hasattr(val, "strftime"):
                    display = val.strftime("%d/%m/%Y")
                elif isinstance(val, float):
                    if col in ("Unit price", "Total"):
                        display = f"${val:,.2f}"
                    elif col == "Rating":
                        display = f"{val:.1f}"
                    else:
                        display = f"{val:,.2f}"
                else:
                    display = str(val)

                item = QTableWidgetItem(display)
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    if isinstance(val, (int, float)) else
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )

                if col == "Branch":
                    colors = {"A": "#4C9BE8", "B": "#27AE88", "C": "#E85D75"}
                    item.setForeground(QColor(colors.get(str(val), TEXT)))
                    item.setFont(QFont("", -1, QFont.Weight.Bold))

                self.table.setItem(self.table.rowCount() - 1, col_idx, item)

        self.table.setSortingEnabled(True)

        total = df["Total"].sum() if "Total" in df.columns else 0
        self.lbl_count.setText(f"{len(df):,} baris ditampilkan")
        self.lbl_total.setText(f"Total Pendapatan: ${total:,.2f}")
