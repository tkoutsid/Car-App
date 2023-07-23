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

conn = sqlite3.connect("Full_Car_Database.db")

c = conn.cursor()
c.execute("""CREATE TABLE Car (
  car_id INTEGER PRIMARY KEY,
  manufacturer VARCHAR(255) NOT NULL,
  model VARCHAR(255) NOT NULL,
  year INTEGER(4) NOT NULL
)""")

c.execute("""CREATE TABLE CarAttributes (
  car_id INTEGER,
  mileage FLOAT(10, 1) NOT NULL,
  engine VARCHAR(255) NOT NULL,
  transmission VARCHAR(255) NOT NULL,
  drivetrain VARCHAR(255) NOT NULL,
  fuel_type VARCHAR(255) NOT NULL,
  mpg VARCHAR(255) NOT NULL,
  exterior_color VARCHAR(255) NOT NULL,
  interior_color VARCHAR(255) NOT NULL,
  FOREIGN KEY (car_id) REFERENCES Car (car_id)
)""")

c.execute("""CREATE TABLE CarHistory (
  car_id INTEGER,
  accidents_or_damage BOOLEAN NOT NULL,
  one_owner BOOLEAN NOT NULL,
  personal_use_only BOOLEAN NOT NULL,
  FOREIGN KEY (car_id) REFERENCES Car (car_id)
)""")

c.execute("""CREATE TABLE Dealer (
  car_id INTEGER,
  seller_name VARCHAR(255) NOT NULL,
  seller_rating FLOAT(2, 1) NOT NULL CHECK (seller_rating >= 0.0 AND seller_rating <= 5.0),
  driver_rating FLOAT(10, 1) NOT NULL CHECK (driver_rating >= 0.0 AND driver_rating <= 5.0),
  driver_reviews_num FLOAT(10, 1),
  FOREIGN KEY (car_id) REFERENCES Car (car_id)
)""")

c.execute("""CREATE TABLE Price (
  car_id INTEGER,
  price_drop FLOAT(10, 2),
  price FLOAT(10, 2) NOT NULL,
  FOREIGN KEY (car_id) REFERENCES Car (car_id)
)""")

#Insert data into each table
for i in range(len(df)):
  car_id = i

  c.execute("INSERT INTO Car (car_id, manufacturer, model, year) VALUES (?, ?, ?, ?)",
            (car_id, df.loc[i, "manufacturer"], df.loc[i, "model"], int(df.loc[i, "year"])))

  c.execute("INSERT INTO CarAttributes (car_id, mileage, engine, transmission, drivetrain, fuel_type, mpg, exterior_color, interior_color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (car_id, df.loc[i, "mileage"], df.loc[i, "engine"], df.loc[i, "transmission"], df.loc[i, 'drivetrain'], df.loc[i, 'fuel_type'], df.loc[i, 'mpg'], df.loc[i, "exterior_color"], df.loc[i, "interior_color"]))

  c.execute("INSERT INTO CarHistory (car_id, accidents_or_damage, one_owner, personal_use_only) VALUES (?, ?, ?, ?)",
            (car_id, df.loc[i, "accidents_or_damage"], df.loc[i, "one_owner"], df.loc[i, "personal_use_only"]))

  c.execute("INSERT INTO Dealer (car_id, seller_name, seller_rating, driver_rating, driver_reviews_num) VALUES (?, ?, ?, ?, ?)",
            (car_id, df.loc[i, "seller_name"], df.loc[i, "seller_rating"], df.loc[i, "driver_rating"], df.loc[i, "driver_reviews_num"]))

  c.execute("INSERT INTO Price (car_id, price_drop, price) VALUES (?, ?, ?)",
           (car_id, df.loc[i, "price_drop"], df.loc[i, "price"]))


st.title("Car Database")

st.table(conn.execute("SELECT * FROM Car").fetchall())

def add_record():
    manufacturer = st.text_input("Manufacturer")
    model = st.text_input("Model")
    year = st.number_input("Year")
    conn.execute("INSERT INTO Car (manufacturer, model, year) VALUES (?, ?, ?)", (manufacturer, model, year))

def update_record():
    car_id = st.number_input("Car ID")
    manufacturer = st.text_input("Manufacturer")
    model = st.text_input("Model")
    year = st.number_input("Year")
    conn.execute("UPDATE Car SET manufacturer = ?, model = ?, year = ? WHERE car_id = ?", (manufacturer, model, year, car_id))

def delete_record():
    car_id = st.number_input("Car ID")
    conn.execute("DELETE FROM Car WHERE car_id = ?", (car_id,))

if st.sidebar.button("Add Record"):
    add_record()
if st.sidebar.button("Update Record"):
    update_record()
if st.sidebar.button("Delete Record"):
    delete_record()
