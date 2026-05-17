#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

import pandas as pd
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


DARK_BG  = "#1A1D2E"
SURFACE  = "#252840"
TEXT     = "#E8EAF6"
TEXT_DIM = "#8892B0"

CARDS = [
    ("💰", "Total Pendapatan",  "total_revenue",  "#4C9BE8"),
    ("🧾", "Jumlah Transaksi",  "total_tx",       "#27AE88"),
    ("⭐", "Rating Rata-rata",  "avg_rating",      "#F5A623"),
    ("📦", "Total Qty Terjual", "total_qty",       "#E85D75"),
    ("💹", "Avg Transaksi",     "avg_tx",          "#9B59B6"),
    ("🏪", "Cabang Aktif",      "branches",        "#E67E22"),
]


class StatCard(QFrame):
    def __init__(self, icon, label, color, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(120)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            StatCard {{
                background: {SURFACE};
                border-radius: 10px;
                border-left: 3px solid {color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        top = QHBoxLayout()
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet(f"font-size: 20px; background: transparent;")
        top.addWidget(lbl_icon)
        top.addStretch()
        layout.addLayout(top)

        self.lbl_value = QLabel("—")
        self.lbl_value.setStyleSheet(
            f"color: {color}; font-size: 18px; font-weight: bold; background: transparent;"
        )
        layout.addWidget(self.lbl_value)

        self.lbl_label = QLabel(label)
        self.lbl_label.setStyleSheet(
            f"color: {TEXT_DIM}; font-size: 10px; background: transparent;"
        )
        layout.addWidget(self.lbl_label)

    def set_value(self, text: str):
        self.lbl_value.setText(text)


class StatsBarWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background: {DARK_BG};")

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(10)

        self._cards: dict[str, StatCard] = {}
        for icon, label, key, color in CARDS:
            card = StatCard(icon, label, color)
            self._cards[key] = card
            self._layout.addWidget(card)

    def update_stats(self, df: pd.DataFrame):
        if df.empty:
            for card in self._cards.values():
                card.set_value("—")
            return

        self._cards["total_revenue"].set_value(f"${df['Total'].sum():,.0f}")
        self._cards["total_tx"].set_value(f"{len(df):,}")
        self._cards["avg_rating"].set_value(f"{df['Rating'].mean():.2f}")
        self._cards["total_qty"].set_value(f"{df['Quantity'].sum():,}")
        self._cards["avg_tx"].set_value(f"${df['Total'].mean():,.2f}")
        self._cards["branches"].set_value(str(df["Branch"].nunique()))
