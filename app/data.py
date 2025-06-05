# --- Imports ---
import pandas as pd


# Read the CSV-file
df = pd.read_csv("data/renset_jentenavn.csv", sep=",", encoding="utf-8")
df.columns = df.columns.str.strip().str.lower()
