#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QTabWidget,
    QFrame, QFileDialog, QMessageBox, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

from utils.data_loader import load_data, get_filter_options, apply_filters
from widgets.chart_widget import ChartWidget, CHART_NAMES
from widgets.table_widget import DataTableWidget
from widgets.stats_widget import StatsBarWidget

DARK_BG  = "#1A1D2E"
SURFACE  = "#252840"
SURFACE2 = "#2E3250"
ACCENT   = "#4C9BE8"
ACCENT2  = "#27AE88"
TEXT     = "#E8EAF6"
TEXT_DIM = "#8892B0"
DANGER   = "#E85D75"


COMBO_STYLE = f"""
    QComboBox {{
        background: {SURFACE};
        color: {TEXT};
        border: 1px solid {SURFACE2};
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 11px;
        min-width: 120px;
    }}
    QComboBox:hover {{ border-color: {ACCENT}; }}
    QComboBox::drop-down {{ border: none; width: 20px; }}
    QComboBox QAbstractItemView {{
        background: {SURFACE};
        color: {TEXT};
        selection-background-color: {ACCENT};
        selection-color: {DARK_BG};
        border: 1px solid {SURFACE2};
    }}
"""

BTN_PRIMARY = f"""
    QPushButton {{
        background: {ACCENT};
        color: {DARK_BG};
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-size: 11px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background: #6BB4F0; }}
    QPushButton:pressed {{ background: #3A8FD4; }}
"""

BTN_SUCCESS = f"""
    QPushButton {{
        background: {ACCENT2};
        color: {DARK_BG};
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-size: 11px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background: #34C89A; }}
    QPushButton:pressed {{ background: #1E9A70; }}
"""

TAB_STYLE = f"""
    QTabWidget::pane {{
        background: {SURFACE};
        border: 1px solid {SURFACE2};
        border-radius: 8px;
    }}
    QTabBar::tab {{
        background: {DARK_BG};
        color: {TEXT_DIM};
        padding: 8px 20px;
        font-size: 11px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background: {SURFACE};
        color: {ACCENT};
        font-weight: bold;
        border-bottom: 2px solid {ACCENT};
    }}
    QTabBar::tab:hover {{ color: {TEXT}; }}
"""


def make_label(text: str, style: str = "") -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(style)
    return lbl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Supermarket Sales Dashboard")
        self.resize(1280, 800)
        self.setMinimumSize(900, 600)

        self._df_full = None  
        self._df_filtered = None

        self._build_palette()
        self._build_ui()
        self._load_data()

    def _build_palette(self):
        pal = QPalette()
        pal.setColor(QPalette.ColorRole.Window, QColor(DARK_BG))
        pal.setColor(QPalette.ColorRole.WindowText, QColor(TEXT))
        pal.setColor(QPalette.ColorRole.Base, QColor(SURFACE))
        pal.setColor(QPalette.ColorRole.AlternateBase, QColor(SURFACE2))
        pal.setColor(QPalette.ColorRole.Text, QColor(TEXT))
        pal.setColor(QPalette.ColorRole.Button, QColor(SURFACE))
        pal.setColor(QPalette.ColorRole.ButtonText, QColor(TEXT))
        self.setPalette(pal)
        self.setStyleSheet(f"QMainWindow {{ background: {DARK_BG}; }}")

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        root.addWidget(self._build_header())
        root.addWidget(self._build_filter_bar())
        root.addWidget(self._build_stats_bar())
        root.addWidget(self._build_tabs(), stretch=1)
        root.addWidget(self._build_status_bar())

    def _build_header(self) -> QWidget:
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {SURFACE}, stop:1 #1B2B4B);
                border-radius: 10px;
                border-left: 4px solid {ACCENT};
            }}
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 10, 16, 10)

        title = QLabel("🏪  Supermarket Sales Dashboard")
        title.setStyleSheet(f"color: {TEXT}; font-size: 20px; font-weight: bold; background: transparent;")

        subtitle = QLabel("Kaggle Dataset · 1000 Transaksi · Jan–Mar 2019")
        subtitle.setStyleSheet(f"color: {TEXT_DIM}; font-size: 11px; background: transparent;")

        col = QVBoxLayout()
        col.setSpacing(2)
        col.addWidget(title)
        col.addWidget(subtitle)

        layout.addLayout(col)
        layout.addStretch()

        lbl_url = QLabel('<a href="https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales" '
                         f'style="color:{ACCENT}; font-size:10px;">🔗 Sumber Dataset Kaggle</a>')
        lbl_url.setOpenExternalLinks(True)
        lbl_url.setStyleSheet("background: transparent;")
        layout.addWidget(lbl_url)

        return frame

    def _build_filter_bar(self) -> QWidget:
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background: {SURFACE}; border-radius: 8px; }}")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        layout.addWidget(make_label("Filter:", f"color:{TEXT_DIM}; font-size:11px; font-weight:bold;"))

        self._filter_combos: dict[str, QComboBox] = {}
        filter_labels = {
            "Branch": "Cabang",
            "City": "Kota",
            "Customer type": "Tipe Pelanggan",
            "Gender": "Gender",
            "Product line": "Lini Produk",
            "Payment": "Pembayaran",
        }
        for col, label in filter_labels.items():
            lbl = make_label(f"{label}:", f"color:{TEXT_DIM}; font-size:10px; background: transparent;")
            cb = QComboBox()
            cb.addItem("All")
            cb.setStyleSheet(COMBO_STYLE)
            cb.currentTextChanged.connect(self._on_filter_changed)
            layout.addWidget(lbl)
            layout.addWidget(cb)
            self._filter_combos[col] = cb

        layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        btn_reset = QPushButton("↺  Reset Filter")
        btn_reset.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_DIM};
                border: 1px solid {SURFACE2};
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 11px;
            }}
            QPushButton:hover {{ border-color: {ACCENT}; color: {TEXT}; }}
        """)
        btn_reset.clicked.connect(self._reset_filters)
        layout.addWidget(btn_reset)

        return frame

    def _build_stats_bar(self) -> StatsBarWidget:
        self.stats_bar = StatsBarWidget()
        return self.stats_bar

    def _build_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setStyleSheet(TAB_STYLE)

        chart_tab = QWidget()
        chart_tab.setStyleSheet(f"background: {SURFACE};")
        ct_layout = QVBoxLayout(chart_tab)
        ct_layout.setContentsMargins(10, 10, 10, 10)
        ct_layout.setSpacing(8)

        ctrl = QHBoxLayout()
        ctrl.setSpacing(10)

        ctrl.addWidget(make_label("Chart A:", f"color:{TEXT_DIM}; font-size:11px; background:transparent;"))
        self.combo_chart_a = QComboBox()
        self.combo_chart_a.addItems(CHART_NAMES)
        self.combo_chart_a.setCurrentIndex(0)
        self.combo_chart_a.setStyleSheet(COMBO_STYLE)
        self.combo_chart_a.currentTextChanged.connect(self._on_chart_changed)
        ctrl.addWidget(self.combo_chart_a)

        ctrl.addWidget(make_label("Chart B:", f"color:{TEXT_DIM}; font-size:11px; background:transparent;"))
        self.combo_chart_b = QComboBox()
        self.combo_chart_b.addItems(CHART_NAMES)
        self.combo_chart_b.setCurrentIndex(2)
        self.combo_chart_b.setStyleSheet(COMBO_STYLE)
        self.combo_chart_b.currentTextChanged.connect(self._on_chart_changed)
        ctrl.addWidget(self.combo_chart_b)

        ctrl.addStretch()

        btn_refresh = QPushButton("🔄  Refresh")
        btn_refresh.setStyleSheet(BTN_PRIMARY)
        btn_refresh.clicked.connect(self._refresh_charts)
        ctrl.addWidget(btn_refresh)

        btn_export = QPushButton("📸  Export PNG")
        btn_export.setStyleSheet(BTN_SUCCESS)
        btn_export.clicked.connect(self._export_chart)
        ctrl.addWidget(btn_export)

        ct_layout.addLayout(ctrl)

        self.chart_widget = ChartWidget()
        ct_layout.addWidget(self.chart_widget, stretch=1)

        tabs.addTab(chart_tab, "📈  Visualisasi")

        table_tab = QWidget()
        table_tab.setStyleSheet(f"background: {SURFACE};")
        tt_layout = QVBoxLayout(table_tab)
        tt_layout.setContentsMargins(10, 10, 10, 10)
        self.table_widget = DataTableWidget()
        tt_layout.addWidget(self.table_widget)
        tabs.addTab(table_tab, "📋  Data Mentah")

        return tabs

    def _build_status_bar(self) -> QLabel:
        self.status_lbl = QLabel("Siap")
        self.status_lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 10px; padding: 2px 4px;")
        return self.status_lbl

    def _load_data(self):
        self.status_lbl.setText("⏳ Memuat dataset...")
        try:
            self._df_full = load_data()
            self._populate_filters()
            self._apply_and_render()
            self.status_lbl.setText(
                f"✅ {len(self._df_full):,} baris dimuat dari supermarket_sales.csv"
            )
        except Exception as e:
            QMessageBox.critical(self, "Gagal Memuat Data", str(e))
            self.status_lbl.setText(f"❌ Error: {e}")

    def _populate_filters(self):
        if self._df_full is None:
            return
        options = get_filter_options(self._df_full)
        for col, cb in self._filter_combos.items():
            cb.blockSignals(True)
            cb.clear()
            cb.addItems(options.get(col, ["All"]))
            cb.blockSignals(False)

    def _get_current_filters(self) -> dict:
        return {
            col: cb.currentText()
            for col, cb in self._filter_combos.items()
        }

    def _on_filter_changed(self):
        self._apply_and_render()

    def _reset_filters(self):
        for cb in self._filter_combos.values():
            cb.blockSignals(True)
            cb.setCurrentIndex(0)
            cb.blockSignals(False)
        self._apply_and_render()

    def _apply_and_render(self):
        if self._df_full is None:
            return
        filters = self._get_current_filters()
        self._df_filtered = apply_filters(self._df_full, filters)

        self.stats_bar.update_stats(self._df_filtered)
        self.chart_widget.set_data(self._df_filtered)
        self.chart_widget.set_charts(
            self.combo_chart_a.currentText(),
            self.combo_chart_b.currentText(),
        )
        self.table_widget.load_data(self._df_filtered)
        self.status_lbl.setText(
            f"📊 Menampilkan {len(self._df_filtered):,} dari {len(self._df_full):,} baris"
        )

    def _on_chart_changed(self):
        self.chart_widget.set_charts(
            self.combo_chart_a.currentText(),
            self.combo_chart_b.currentText(),
        )

    def _refresh_charts(self):
        self._apply_and_render()

    def _export_chart(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Chart", "supermarket_chart.png",
            "PNG Image (*.png)"
        )
        if path:
            try:
                self.chart_widget.export_png(path)
                QMessageBox.information(self, "Berhasil", f"Chart disimpan:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Gagal Export", str(e))
