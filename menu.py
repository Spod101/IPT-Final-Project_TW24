from tkinter import messagebox, simpledialog, ttk, PhotoImage
import customtkinter as ctk
from datetime import datetime
import mysql.connector
import re
import os

class FlightManagementSystem:
    # Initialization of the main menu
    def __init__(self):
        self.menu = ctk.CTk()
        self.menu.geometry("1200x750+250+100")
        self.menu.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.menu.title("Main Menu")
        
        # Database connection
        self.db_connection = mysql.connector.connect(
            host="localhost", database="dbflights", user="root", password=""
        )
        self.cursor = self.db_connection.cursor()
        
        self.create_widgets()

    # Function to create the widgets in the main menu
    def create_widgets(self):
        # Label to welcome the admin
        label = ctk.CTkLabel(master=self.menu, text="Welcome Admin to the Menu", font=("Helvetica", 46, "bold"))
        label.pack(padx=10, pady=30)

        # Tab view to add flights, view available flights and settings
        tab = ctk.CTkTabview(master=self.menu, height=600, width=900, corner_radius=32, border_color="#0b274e", border_width=5)
        tab.pack(padx=20, pady=10)

        tab.add("Add Flights")
        tab.add("Available Flights")
        tab.add("Settings")

        label1 = ctk.CTkLabel(master=tab.tab("Add Flights"), text="Add Flights", font=("Helvetica", 24, "bold"))
        label1.pack(padx=20, pady=20)

        frame = ctk.CTkFrame(master=tab.tab("Add Flights"))
        frame.pack(padx=20, pady=10)

        # Entry fields for adding a new flight
        self.origin_entry = ctk.CTkEntry(
            master=frame,
            placeholder_text="Origin",
            corner_radius=8,
            width=250,
            height=50,
            font=("Poppins", 16)
        )
        self.origin_entry.pack(side="left", padx=10, pady=10)

        self.destination_entry = ctk.CTkEntry(
            master=frame,
            placeholder_text="Destination",
            corner_radius=8,
            width=250,
            height=50,
            font=("Poppins", 16)
        )
        self.destination_entry.pack(side="left", padx=10, pady=10)

        self.date_entry = ctk.CTkEntry(
            master=tab.tab("Add Flights"),
            placeholder_text="Departure Date(mm/dd/yyyy)",
            corner_radius=8,
            width=520,
            height=50,
            font=("Poppins", 16)
        )
        self.date_entry.pack(padx=20, pady=10)

        travel_class_options = ["Economy Class", "Premium Economy", "Business Class", "First Class"]
        self.travel_class_combobox = ctk.CTkComboBox(
            master=tab.tab("Add Flights"),
            values=travel_class_options,
            font=("Poppins", 16),
            width=520,
            height=50,
            corner_radius=8,
        )
        self.travel_class_combobox.set("--Select Travel Class--")
        self.travel_class_combobox.pack(padx=20, pady=10)

        self.price_entry = ctk.CTkEntry(
            master=tab.tab("Add Flights"),
            placeholder_text="Price",
            corner_radius=8,
            width=520,
            height=50,
            font=("Poppins", 16)
        )
        self.price_entry.pack(padx=20, pady=10)

        # Submit button to add a new flight
        self.subButton = ctk.CTkButton(master=tab.tab("Add Flights"), corner_radius=8, width=520, height=50, text="Submit", font=("Poppins", 16), command=self.add_flight)
        self.subButton.pack(padx=20, pady=10)

        label2 = ctk.CTkLabel(master=tab.tab("Available Flights"), text="Available Flights", font=("Helvetica", 24, "bold"))
        label2.pack(padx=20, pady=20)
        
        label3 = ctk.CTkLabel(master=tab.tab("Settings"), text="Settings", font=("Helvetica", 24, "bold"))
        label3.pack(padx=20, pady=20)
        
        # Logout button
        logout_button = ctk.CTkButton(master=tab.tab("Settings"), text="Logout", corner_radius=8, width=200, height=50, fg_color="red", hover_color="#aa0000", font=("Poppins", 16), command=self.logout)
        logout_button.pack(padx=20, pady=10)

        # TreeView to display available flights
        self.tree = ttk.Treeview(
            master=tab.tab("Available Flights"),
            columns=("ID", "Origin", "Destination", "Departure Date", "Travel Class", "Price"),
            show="headings",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Origin", text="Origin")
        self.tree.heading("Destination", text="Destination")
        self.tree.heading("Travel Class", text="Travel Class")
        self.tree.heading("Departure Date", text="Departure Date")
        self.tree.heading("Price", text="Price")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#292933", foreground="#fff", fieldbackground="#242424", rowheight=30)
        style.map("Treeview", background=[("selected", "#1f6aa5")])
        
        self.flightTreeview()

        # Button to delete
        self.delButton = ctk.CTkButton(master=tab.tab("Available Flights"), corner_radius=8, width=200, height=50, text="Delete Flight", fg_color="red", hover_color="#aa0000", font=("Poppins", 16), command=self.delete_flight)
        self.delButton.pack(side="right", padx=20, pady=10)

        # Button to update
        self.updButton = ctk.CTkButton(master=tab.tab("Available Flights"), corner_radius=8, width=200, height=50, font=("Poppins", 16), text="Update Flight", command=self.update_flight)
        self.updButton.pack(side="right", padx=20, pady=10)
        
        # Button to search
        search_icon = PhotoImage(file="search.png")
        self.srchbutton = ctk.CTkButton(master=tab.tab("Available Flights"), corner_radius=8, width=100, height=50, text="Search", fg_color="#404040", hover_color="#555555", image=search_icon, compound="left", font=("Poppins", 16), command=self.searchFlight)
        self.srchbutton.pack(side="left", padx=10, pady=10)
        
        # Button to show
        self.showbutton = ctk.CTkButton(master=tab.tab("Available Flights"), corner_radius=8, width=120, height=50, fg_color="#404040", hover_color="#555555", font=("Poppins", 16), text="Show All Flights", command=self.showFlight)
        self.showbutton.pack(side="left", padx=10, pady=10)
        
    # Function to View flight data
    def flightTreeview(self):
        # Fetch flight data from the database
        sql = "SELECT * FROM `tblflights`"
        self.cursor.execute(sql)
        flights = self.cursor.fetchall()

        # Put fetched flight data in the TreeView
        for flight in flights:
            self.tree.insert("", "end", values=flight)
            
        style = ttk.Style()
        style.configure("Treeview", font=("Poppins", 14))
        
    # Function to add a new flight
    def add_flight(self):
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()
        departure_date_str = self.date_entry.get()
        travel_class = self.travel_class_combobox.get()
        price = self.price_entry.get()

        # Validate date format
        try:
            departure_date = datetime.strptime(departure_date_str, '%m/%d/%Y').date()
        except ValueError:
            messagebox.showerror("Error", "Please enter the date in the format mm/dd/yyyy.")
            return
        
        # Add the flight into the database
        sql = "INSERT INTO `tblflights` (`id`, `source`, `destination`, `date`, `class`, `price`) VALUES (NULL, %s, %s, %s, %s, %s)"
        flight_data = (origin, destination, departure_date, travel_class, price)

        # Check if any field is empty
        if not all([origin, destination, departure_date_str, travel_class, price]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            self.cursor.execute(sql, flight_data)
            self.db_connection.commit()
            last_row_id = self.cursor.lastrowid

            # Fetch the newly added flight from the database
            self.cursor.execute("SELECT * FROM `tblflights` WHERE `id` = %s", (last_row_id,))
            new_flight = self.cursor.fetchone()

            # Insert the newly added flight into the TreeView
            self.tree.insert("", "end", values=new_flight)
            messagebox.showinfo("Success", "Flight added successfully.")
        except Exception:
            messagebox.showerror("Error", "Failed to add flight!")

    # Function to delete a flight
    def delete_flight(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Get the ID of the selected item
            item_id = self.tree.item(selected_item)['values'][0]
            
            # Ask for confirmation
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this flight?")
            if confirm:
                # Delete the selected flight from the database
                sql = "DELETE FROM `tblflights` WHERE `id` = %s"
                flight_data = (item_id,)

                try:
                    self.cursor.execute(sql, flight_data)
                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Flight deleted successfully.")
                    self.tree.delete(selected_item)
                    
                except Exception:
                    messagebox.showerror("Error", "Failed to delete flight!")
        else:
            messagebox.showerror("Error", "Please select a flight to delete.")

    # Function to update a flight
    def update_flight(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Get the ID of the selected item
            item_id = self.tree.item(selected_item)['values'][0]

            # Ask for confirmation
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to update this flight?")
            if confirm:
                while True:
                    # Ask for new values for each field
                    new_origin = simpledialog.askstring("Update Origin", "Enter new origin:")
                    # Check if the user has entered a valid origin
                    if new_origin is None or new_origin.strip() == "":
                        if not messagebox.askretrycancel("Error", "Please enter a valid origin."):
                            return
                        continue

                    new_destination = simpledialog.askstring("Update Destination", "Enter new destination:")
                    # Check if the user has entered a valid destination
                    if new_destination is None or new_destination.strip() == "":
                        if not messagebox.askretrycancel("Error", "Please enter a valid destination."):
                            return
                        continue

                    new_departure_date = simpledialog.askstring("Update Departure Date", "Enter new departure date (yyyy-mm-dd):")
                    # Check if the user has entered a valid departure date
                    if new_departure_date is None or new_departure_date.strip() == "":
                        if not messagebox.askretrycancel("Error", "Please enter a valid departure date."):
                            return
                        continue
                    
                    # Validate date format
                    if not re.match(r'^\d{4}-\d{2}-\d{2}$', new_departure_date):
                        if not messagebox.askretrycancel("Error", "Please enter the date in yyyy-mm-dd format."):
                            return
                        continue

                    new_travel_class = simpledialog.askstring("Update Travel Class", "Enter new travel class:")
                    # Check if the user has entered a valid travel class
                    if new_travel_class is None or new_travel_class.strip() == "":
                        if not messagebox.askretrycancel("Error", "Please enter a valid travel class."):
                            return
                        continue

                    new_price = simpledialog.askfloat("Update Price", "Enter new price:")
                    # Check if the user has entered a valid price
                    if new_price is None:
                        if not messagebox.askretrycancel("Error", "Please enter a valid price."):
                            return
                        continue

                    break  # Exit the loop if all inputs are valid

                # Update the selected flight in the database
                sql = "UPDATE `tblflights` SET `source` = %s, `destination` = %s, `date` = %s, `class` = %s, `price` = %s WHERE `id` = %s"
                flight_data = (new_origin, new_destination, new_departure_date, new_travel_class, new_price, item_id)

                try:
                    self.cursor.execute(sql, flight_data)
                    self.db_connection.commit()

                    # Update the TreeView with the new data
                    updated_flight_data = (item_id, new_origin, new_destination, new_departure_date, new_travel_class, new_price)
                    self.tree.item(selected_item, values=updated_flight_data)

                    messagebox.showinfo("Success", "Flight updated successfully.")
                except Exception:
                    messagebox.showerror("Error", "Failed to update flight!")
        else:
            messagebox.showerror("Error", "Please select a flight to update.")
        
    # Function to search for a flight
    def searchFlight(self):
        # Functionality for searching flights
        search = simpledialog.askstring("Search Flight", "Enter origin or destination:")
        if search:
            # Search for flights based on origin or destination
            sql = "SELECT * FROM `tblflights` WHERE `source` LIKE %s OR `destination` LIKE %s"
            search_data = ("%" + search + "%", "%" + search + "%")

            self.cursor.execute(sql, search_data)
            flights = self.cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            for flight in flights:
                self.tree.insert("", "end", values=flight)

            if not flights:
                messagebox.showinfo("No Flights", "No flights found.")
        else:
            messagebox.showerror("Error", "Please enter a search term.")
    
    # Function to show all flights
    def showFlight(self):
        self.tree.delete(*self.tree.get_children())
        self.flightTreeview()
    
    # Function to logout
    def logout(self):
        self.menu.destroy()
        # Run the login script when the user logs out
        os.system("python login.py")
    
    # Function to run in loop
    def run(self):
        self.menu.mainloop()

# Main function
if __name__ == "__main__":
    app = FlightManagementSystem()
    app.run()
