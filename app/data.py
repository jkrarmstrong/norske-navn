# --- Imports ---
import pandas as pd

# Read the CSV-file
df_girl = pd.read_csv("data/renset_jentenavn.csv", sep=",", encoding="utf-8")
df_boy = pd.read_csv("data/renset_guttenavn.csv", sep=",", encoding="utf-8")

# --- Standardize column names ---
df_girl.columns = df_girl.columns.str.strip().str.lower()
df_boy.columns = df_boy.columns.str.strip().str.lower()

# --- Add gender column (useful for later) ---
# df_girl["gender"] = "girl"
# df_boy["gender"] = "boy"

# --- Combine datasets ---
df = pd.concat([df_girl, df_boy], ignore_index=True)
