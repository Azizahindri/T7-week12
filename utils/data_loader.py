#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

"""
Dataset: Supermarket Sales Dataset (Kaggle)
URL: https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales
"""

import os
import pandas as pd


CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "supermarket_sales.csv")


def load_data(csv_path: str = CSV_PATH) -> pd.DataFrame:
    """Muat CSV dan bersihkan kolom dasar."""
    df = pd.read_csv(csv_path)

    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")

    numeric_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs",
                    "gross margin percentage", "gross income", "Rating"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def get_filter_options(df: pd.DataFrame) -> dict:
   
    return {
        "Branch":        ["All"] + sorted(df["Branch"].dropna().unique().tolist()),
        "City":          ["All"] + sorted(df["City"].dropna().unique().tolist()),
        "Customer type": ["All"] + sorted(df["Customer type"].dropna().unique().tolist()),
        "Gender":        ["All"] + sorted(df["Gender"].dropna().unique().tolist()),
        "Product line":  ["All"] + sorted(df["Product line"].dropna().unique().tolist()),
        "Payment":       ["All"] + sorted(df["Payment"].dropna().unique().tolist()),
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered = df.copy()
    for col, val in filters.items():
        if val and val != "All":
            filtered = filtered[filtered[col] == val]
    return filtered
