#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

import os
import numpy as np
import pandas as pd
import os
import matplotlib

if not os.environ.get("MPLBACKEND"):
    matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

PALETTE = ["#4C9BE8", "#E85D75", "#F5A623", "#27AE88", "#9B59B6", "#E67E22"]
BG      = "#1A1D2E"
SURFACE = "#252840"
TEXT    = "#E8EAF6"
GRID    = "#2E3250"


def _apply_dark_style(ax, title: str):
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.title.set_color(TEXT)
    ax.title.set_fontsize(11)
    ax.title.set_fontweight("bold")
    ax.set_title(title, pad=10)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.grid(color=GRID, linestyle="--", linewidth=0.5, alpha=0.7)


def _bar_sales_by_branch(ax, df: pd.DataFrame):
    grp = df.groupby("Branch")["Total"].sum()
    bars = ax.bar(grp.index, grp.values, color=PALETTE[:len(grp)], width=0.5,
                  edgecolor=BG, linewidth=0.8)
    for bar, val in zip(bars, grp.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + grp.values.max() * 0.01,
                f"${val:,.0f}", ha="center", va="bottom", color=TEXT, fontsize=8, fontweight="bold")
    ax.set_xlabel("Cabang (Branch)")
    ax.set_ylabel("Total Penjualan ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _apply_dark_style(ax, "Total Penjualan per Cabang")


def _pie_payment_method(ax, df: pd.DataFrame):
    grp = df.groupby("Payment")["Total"].sum()
    wedges, texts, autotexts = ax.pie(
        grp.values, labels=grp.index, autopct="%1.1f%%",
        colors=PALETTE[:len(grp)], startangle=140,
        wedgeprops=dict(edgecolor=BG, linewidth=1.5),
        textprops=dict(color=TEXT, fontsize=8),
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight("bold")
        at.set_color(BG)
    ax.set_facecolor(SURFACE)
    ax.set_title("Distribusi Metode Pembayaran", pad=10,
                 fontsize=11, fontweight="bold", color=TEXT)


def _line_sales_trend(ax, df: pd.DataFrame):
    daily = df.groupby("Date")["Total"].sum().sort_index()
    if daily.empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center",
                color=TEXT, transform=ax.transAxes)
        _apply_dark_style(ax, "Tren Penjualan Harian")
        return
    ax.plot(daily.index, daily.values, color=PALETTE[0], linewidth=1.8,
            marker="o", markersize=3, markerfacecolor=PALETTE[1])
    ax.fill_between(daily.index, daily.values, alpha=0.15, color=PALETTE[0])
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Penjualan ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.tick_params(axis="x", rotation=30)
    _apply_dark_style(ax, "Tren Penjualan Harian")


def _bar_product_line(ax, df: pd.DataFrame):
    grp = df.groupby("Product line")["Total"].sum().sort_values(ascending=True)
    colors = PALETTE[:len(grp)]
    bars = ax.barh(grp.index, grp.values, color=colors, edgecolor=BG, linewidth=0.8)
    for bar, val in zip(bars, grp.values):
        ax.text(val + grp.values.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", color=TEXT, fontsize=7.5, fontweight="bold")
    ax.set_xlabel("Total Penjualan ($)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    _apply_dark_style(ax, "Penjualan per Lini Produk")


def _bar_rating_distribution(ax, df: pd.DataFrame):
    bins = np.arange(4, 10.5, 0.5)
    n, bin_edges, patches = ax.hist(df["Rating"].dropna(), bins=bins,
                                     color=PALETTE[2], edgecolor=BG, linewidth=0.8)
    for patch, val in zip(patches, n):
        if val > 0:
            ax.text(patch.get_x() + patch.get_width() / 2, patch.get_height() + 0.3,
                    str(int(val)), ha="center", va="bottom", color=TEXT, fontsize=7)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Transaksi")
    _apply_dark_style(ax, "Distribusi Rating Pelanggan")


def _bar_gender_product(ax, df: pd.DataFrame):
    pivot = df.pivot_table(values="Total", index="Product line",
                            columns="Gender", aggfunc="sum", fill_value=0)
    x = np.arange(len(pivot.index))
    w = 0.35
    for i, (col, color) in enumerate(zip(pivot.columns, PALETTE)):
        bars = ax.bar(x + i * w, pivot[col], width=w, label=col,
                      color=color, edgecolor=BG, linewidth=0.8)
    ax.set_xticks(x + w / 2)
    ax.set_xticklabels(pivot.index, rotation=25, ha="right", fontsize=7)
    ax.set_ylabel("Total Penjualan ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    legend = ax.legend(fontsize=8, facecolor=SURFACE, edgecolor=GRID, labelcolor=TEXT)
    _apply_dark_style(ax, "Penjualan per Produk berdasarkan Gender")


CHART_BUILDERS = {
    "Penjualan per Cabang":          _bar_sales_by_branch,
    "Metode Pembayaran (Pie)":       _pie_payment_method,
    "Tren Penjualan Harian":         _line_sales_trend,
    "Penjualan per Lini Produk":     _bar_product_line,
    "Distribusi Rating":             _bar_rating_distribution,
    "Gender & Produk (Grouped Bar)": _bar_gender_product,
}

CHART_NAMES = list(CHART_BUILDERS.keys())

class ChartWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._df: pd.DataFrame | None = None
        self._chart_a = CHART_NAMES[0]
        self._chart_b = CHART_NAMES[2]

        self.figure = Figure(facecolor=BG, tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def set_data(self, df: pd.DataFrame):
        self._df = df
        self.refresh()

    def set_charts(self, chart_a: str, chart_b: str):
        self._chart_a = chart_a
        self._chart_b = chart_b
        self.refresh()

    def refresh(self):
        if self._df is None or self._df.empty:
            return
        self.figure.clear()

        ax1 = self.figure.add_subplot(1, 2, 1)
        ax2 = self.figure.add_subplot(1, 2, 2)

        builder_a = CHART_BUILDERS.get(self._chart_a)
        builder_b = CHART_BUILDERS.get(self._chart_b)

        if builder_a:
            try:
                builder_a(ax1, self._df)
            except Exception as e:
                ax1.text(0.5, 0.5, f"Error:\n{e}", ha="center", va="center",
                         color="red", transform=ax1.transAxes, fontsize=8)
                _apply_dark_style(ax1, self._chart_a)

        if builder_b:
            try:
                builder_b(ax2, self._df)
            except Exception as e:
                ax2.text(0.5, 0.5, f"Error:\n{e}", ha="center", va="center",
                         color="red", transform=ax2.transAxes, fontsize=8)
                _apply_dark_style(ax2, self._chart_b)

        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def export_png(self, filepath: str):
        """Simpan chart saat ini ke file PNG."""
        self.figure.savefig(filepath, dpi=150, facecolor=BG,
                            bbox_inches="tight", pad_inches=0.2)
