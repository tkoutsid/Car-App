import sqlite3
import streamlit as st

conn = sqlite3.connect("Full_Car_Database.db")

st.title("Car Database")

st.table(conn.execute("SELECT * FROM Car_Database.Car").fetchall())

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
