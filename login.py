from customtkinter import *
import os
from tkinter import messagebox, PhotoImage, Label
from PIL import *

# Login Function
def login():
    username = "admin"
    password = "admin123"
    if usernameEntry.get() == username and passEntry.get() == password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        app.destroy()
        os.system("python menu.py")
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

# Show Password Function
def toggle_password():
    if checkbox.get() == 1:
        passEntry.configure(show="")
    else:
        passEntry.configure(show="*")

# Window Specifications
app = CTk()
wa = 1000
ha = 700
app.geometry("{}x{}+{}+{}".format(wa, ha, 400, 100))
app.resizable(False, False)
app.title("Login Page")

set_appearance_mode("dark")

# Frame Style
frame = CTkFrame(master=app, width=900, height=600, border_color="#0b274e", border_width=5, corner_radius=32)
frame.pack(expand=True)
lbl = CTkLabel(master=frame, text="Admin Sign In", font=("Helvetica", 32, "bold"))
lbl.place(relx=0.7, rely=0.2, anchor="center")

image1 = PhotoImage(file="login2.png")
image1 = image1.zoom(1)
image1_lbl = Label(master=frame, image=image1, bg="#2b2b2b")
image1_lbl.place(relx=0.25, rely=0.5, anchor="center")

# User Input
usernameEntry = CTkEntry(master=frame, placeholder_text="Username", corner_radius=8, width=400, height=50, font=("Arial", 16))
usernameEntry.place(relx=0.7, rely=0.4, anchor="center")
passEntry = CTkEntry(master=frame, placeholder_text="Password", show="*", corner_radius=8, width=400, height=50, font=("Arial", 16))
passEntry.place(relx=0.7, rely=0.51, anchor="center")

# Show Password Toggle
checkbox = CTkCheckBox(master=frame, text="Show Password", width=5, height=5, font=("Arial", 12), command=toggle_password)
checkbox.place(relx=0.54, rely=0.6, anchor="center")

btn = CTkButton(master=frame, text="Login", command=login, corner_radius=32, fg_color="#0b274e", hover_color="#437ead", width=400, height=50, font=("Arial", 16))

btn.place(relx=0.7, rely=0.8, anchor="center")

app.mainloop()
