import tkinter as tk
from tkinter import messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, tk.END)
    letters = list("abcdefghijklmnopqrstuvwxyz")
    cap_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numerals = list("1234567890")
    symbols = list("!#$%&*()+-_")

    num_letters = randint(4, 5)
    num_cap_letters = randint(4, 5)
    num_numerals = randint(2, 4)
    num_symbols = randint(2, 4)

    letters_list = [choice(letters) for _ in range(num_letters)]
    cap_letters_list = [choice(cap_letters) for _ in range(num_cap_letters)]
    numerals_list = [choice(numerals) for _ in range(num_numerals)]
    symbols_list = [choice(symbols) for _ in range(num_symbols)]

    list_password = letters_list + cap_letters_list + numerals_list + symbols_list
    shuffle(list_password)

    password_string = "".join(list_password)
    copy(password_string)
    password_entry.insert(0, password_string)


# ---------------------------- SEARCH WEBSITE ------------------------------ #


def search_website():
    ws_search = website_entry.get()
    try:
        with open("password_database.json", "r") as database:
            data = json.load(database)
            ws_info = data[ws_search]
    except KeyError:
        tk.messagebox.askokcancel(title="Error", message="Website not found")
    except FileNotFoundError:
        tk.messagebox.askokcancel(title="Error", message="Data file not found")
    else:
        tk.messagebox.showinfo(title=[ws_search],
                               message=
                               f"e-mail: {ws_info['email']}\n"
                               f"Password: {ws_info['password']}"
                               )


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website_data = website_entry.get()
    email_data = email_entry.get()
    password_data = password_entry.get()
    data_dict = {
        website_data: {
            "email": email_data,
            "password": password_data
        }
    }

    if len(website_data) > 0 and len(email_data) > 0 and len(password_data) > 0:
        try:
            with open("password_database.json", "r") as database:
                data = json.load(database)
        except FileNotFoundError:
            with open("password_database.json", "w") as database:
                json.dump(data_dict, database, indent=4)
        else:
            with open("password_database.json", "w") as database:
                data.update(data_dict)
                json.dump(data, database, indent=4)
        finally:
            email_entry.delete(0, tk.END)
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    else:
        tk.messagebox.showinfo(title="Invalid entry", message="Please do not leave blank fields")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

logo_image = tk.PhotoImage(file="logo.png")
logo_canvas = tk.Canvas(width=200, height=200)
logo_canvas.create_image(100, 100, image=logo_image)
logo_canvas.grid(row=0, column=1)

website_label = tk.Label(text="Website")
website_label.grid(row=1, column=0)
email_label = tk.Label(text="e-mail/Username")
email_label.grid(row=2, column=0)
password_label = tk.Label(text="Password")
password_label.grid(row=3, column=0)

website_entry = tk.Entry()
website_entry.grid(row=1, column=1)
website_entry.config(width=22)
website_entry.focus()
email_entry = tk.Entry()
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.config(width=35)
password_entry = tk.Entry()
password_entry.grid(row=3, column=1)
password_entry.config(width=22)

generate_button = tk.Button(text="Generate", command=generate_password)
generate_button.grid(row=3, column=2)
generate_button.config(width=10)
add_button = tk.Button(text="Add", command=save_password)
add_button.grid(row=4, column=0, columnspan=3)
add_button.config(width=54)
search_button = tk.Button(text="Search", command=search_website)
search_button.grid(row=1, column=2)
search_button.config(width=10)

window.mainloop()
