import tkinter as tk
import sqlite3
from tkinter import ttk

global vehicle_model
global vehicle_motorcode
global first_registration
global transmission

def create_vin_database():
    global cursor_vin
    global conn_vin
    
    conn_vin = sqlite3.connect("vin_database.db")
    cursor_vin = conn_vin.cursor()
    
    cursor_vin.execute("""
                       CREATE TABLE IF NOT EXISTS vin_database (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       VIN TEXT,
                       Modellreihe TEXT,
                       Motorbezeichnung TEXT,
                       Erstzulassung TEXT,
                       Getriebeart TEXT
                       )
                       """)
                       
    conn_vin.commit()
    
def add_entry_vin_database():
    vin_number = vin_number_entry.get()
    vehicle_model = vehicle_model_entry.get()
    vehicle_motorcode = vehicle_motorcode_entry.get()
    first_registration = first_registration_entry.get()
    transmission = transmission_entry.get()
    
    cursor_vin.execute("INSERT INTO vin_database (VIN, Modellreihe, Motorbezeichnung, Erstzulassung, Getriebeart) VALUES (?, ?, ?, ?, ?)",
                       (vin_number, vehicle_model, vehicle_motorcode, first_registration, transmission))
    conn_vin.commit()
    
def delete_entry_vin_database():
    selected_entry = vin_database_treeview.selection()
    
    if selected_entry:
        for item in selected_entry:
            values = vin_database_treeview.item(item, 'values')
            cursor_vin.execute("DELETE FROM vin_database WHERE VIN=? AND Modellreihe=? AND Motorbezeichnung=? AND Erstzulassung=? AND Getriebeart=?",
                               (values[0], values[1], values[2], values[3], values[4]))
            conn_vin.commit()
        vin_database_treeview.delete(selected_entry)
        
def load_vin_database():   
    vin_database_treeview.delete(*vin_database_treeview.get_children())  
    
    cursor_vin.execute("SELECT * FROM vin_database")
    rows = cursor_vin.fetchall()
    
    if rows:
        for row in rows:
            vin_number = row[1]
            vehicle_model = row[2]
            vehicle_motorcode = row[3]
            first_registration = row[4]
            transmission = row[5]
            vin_database_treeview.insert("", "end", values=(vin_number, vehicle_model, vehicle_motorcode, first_registration, transmission))
    else:
        pass
        
root = tk.Tk()
root.title("Codename Fjord")
root.attributes("-fullscreen", True)
root.configure(background = "white")

create_vin_database()   

window_banner = tk.Frame(root, bg = "#007CC1", height = 50)
window_banner.pack(fill = "x")

label_banner = tk.Label(window_banner, text = "Workshop Service System", font = ("Open Sans Bold", 14), bg = "#007CC1", fg = "white")
label_banner.place(relx = 0.5, rely = 0.5, anchor = "center")

tabs = {}

def close_window():
    root.destroy()
    
close_button = tk.Button(window_banner, text = "X", font = ("Open Sans Bold", 12), bg = "#007CC1", fg = "white", bd = 0, command = close_window)
close_button.place(relx = 0.98, rely = 0.5, anchor = "e")

# Creating ttk.Notebook
notebook = ttk.Notebook(root)
notebook.pack(fill = "both", expand = True)

# Adding vehicle information tab
vehicle_information = ttk.Frame(notebook)
notebook.add(vehicle_information, text = "Vehicle information")

# Adding vehicle coding tab
vehicle_coding = ttk.Frame(notebook)
notebook.add(vehicle_coding, text = "Vehicle coding")

# Adding retrofit tab
vehicle_retrofit = ttk.Frame(notebook)
notebook.add(vehicle_retrofit, text = "Retrofit")

# Treeview VIN database
vin_database_treeview = ttk.Treeview(vehicle_information, columns=("VIN", "Vehicle model", "Vehicle motorcode", "First registration", "Transmission"), show="headings")
vin_database_treeview.pack(fill="both", expand=True, padx=10, pady=5)

# Add headings and bind them to columns
vin_database_treeview.heading("VIN", text = "VIN")
vin_database_treeview.heading("Vehicle model", text="Vehicle model")
vin_database_treeview.heading("Vehicle motorcode", text="Vehicle motorcode")
vin_database_treeview.heading("First registration", text="First registration")
vin_database_treeview.heading("Transmission", text="Transmission")

# Entry fields for VIN database
vin_number_label = tk.Label(vehicle_information, text = "VIN")
vin_number_label.pack(side = "left", padx = 10, pady = 5)
vin_number_entry = tk.Entry(vehicle_information)
vin_number_entry.pack(side = "left", padx = 10, pady = 5)

vehicle_model_label = tk.Label(vehicle_information, text = "Vehicle model")
vehicle_model_label.pack(side = "left", padx = 10, pady = 5)
vehicle_model_entry = tk.Entry(vehicle_information)
vehicle_model_entry.pack(side = "left", padx = 10, pady = 5)

vehicle_motorcode_label = tk.Label(vehicle_information, text = "Vehicle motorcode")
vehicle_motorcode_label.pack(side = "left", padx = 10, pady = 5)
vehicle_motorcode_entry = tk.Entry(vehicle_information)
vehicle_motorcode_entry.pack(side = "left", padx = 10, pady = 5)

first_registration_label = tk.Label(vehicle_information, text = "First registration")
first_registration_label.pack(side = "left", padx = 10, pady = 5)
first_registration_entry = tk.Entry(vehicle_information)
first_registration_entry.pack(side = "left", padx = 10, pady = 5)

transmission_label = tk.Label(vehicle_information, text = "Transmission")
transmission_label.pack(side = "left", padx = 10, pady = 5)
transmission_entry = tk.Entry(vehicle_information)
transmission_entry.pack(side = "left", padx = 10, pady = 5)

# Buttons (Vehicle information tab)
vehicle_model_add_button = tk.Button(vehicle_information, text = "Add", bg = "#009900", fg = "white", command = add_entry_vin_database)
vehicle_model_add_button.pack(side = "left", padx = 10, pady = 5)

vehicle_model_delete_button = tk.Button(vehicle_information, text = "Delete", bg = "#CC0000", fg = "white", command = delete_entry_vin_database)
vehicle_model_delete_button.pack(side = "left", padx = 10, pady = 5)

# Load database
load_button = tk.Button(window_banner, text = "Load database", bg = "#007CC1", fg = "white", bd = 0, command = load_vin_database)
load_button.place(relx = 0.94, rely = 0.5, anchor = "e")

root.mainloop()