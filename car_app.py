import pandas as pd
import sqlite3
import numpy as np
import streamlit as st

df = pd.read_csv("cars.csv")

df = df.dropna(subset=[column for column in df.columns if column != "price_drop"])

def make_boolean(row):
  row["accidents_or_damage"] = bool(row["accidents_or_damage"])
  row["one_owner"] = bool(row["one_owner"])
  row["personal_use_only"] = bool(row["personal_use_only"])
  return row

df = df.apply(make_boolean, axis = 1)

df = df.reset_index(drop=True)
