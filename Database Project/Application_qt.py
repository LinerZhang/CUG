import customtkinter as ctk
import tkinter as tk
import psycopg2
from PIL import Image
import os
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
import bcrypt
from PIL import Image, ImageTk
from tkcalendar import DateEntry 
import tkinter as tk
import customtkinter as ctk 

import customtkinter as ctk
from functools import partial

import tkinter as tk
from tkinter import ttk
from functools import partial
import random
import tkinter.messagebox as messagebox
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DatabaseManager:
    def __init__(self, host='localhost', user='postgres', password='123456', database='Performance Management System'):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None, commit=True):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if commit:
                self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            print(f"Error executing query: {error}")
            raise  


    def fetch_all(self, query, params=None):#return all results
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):#return one result
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def excute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
def home(window,pics,pics1,pics2,db):
    window.title("Performance Management System")
    window.geometry("900x600")
    
    label1 = ctk.CTkLabel(window, text="Welcome to \n My Performance Management System!", font=("Arial", 30))
    label1.pack(pady=20)
    label2 = ctk.CTkLabel(window, text="Please select your role below to continue:", font=("Arial", 20))
    label2.pack(pady=20)
    
    button1 = ctk.CTkButton(window, text="Staff Login", command=lambda: staff_login(window,pics), width=140, height=50, font=("Arial", 20))
    button1.pack(pady=60)
    button2 = ctk.CTkButton(window, text="User Login", command=lambda: User_login(window,pics,pics1,pics2,db), width=140, height=50, font=("Arial", 20))
    button2.pack(pady=60)

def staff_login(window,pics):
    for widget in window.winfo_children():
        widget.pack_forget()
    
    back_button = ctk.CTkButton(window, text="Back", command=lambda: log_out(window),width=100,height=30,font=("Arial", 20))
    back_button.pack(pady=20, anchor="nw", side="top", padx=10) 
    
    label = ctk.CTkLabel(window, text="Staff Login", font=("Arial", 30))
    label.pack(pady=20)
    
    label1 = ctk.CTkLabel(window, text="Work ID:", font=("Arial", 20))
    label1.pack(pady=20)
    text1 = ctk.CTkEntry(window,placeholder_text="Enter Work ID", font=("Arial", 20), width=200, height=30)
    text1.pack(pady=10)

    label2 = ctk.CTkLabel(window, text="Password:", font=("Arial", 20))
    label2.pack(pady=20)
    text2 = ctk.CTkEntry(window,placeholder_text="Enter Password", show="*", font=("Arial", 20), width=200, height=30)
    text2.pack(pady=10)

    login_button = ctk.CTkButton(window, text="Login", command=lambda: staff_origin(window, text1.get(), text2.get(),pics),width=100, height=30,font=("Arial", 20))
    login_button.pack(pady=20)
    
def User_login(window,pics,pics1,pics2,db):
    for widget in window.winfo_children():
        widget.pack_forget()

    back_button = ctk.CTkButton(window, text="Back", command=lambda: log_out(window), width=100, height=30, font=("Arial", 20))
    back_button.pack(pady=20, anchor="nw", side="top", padx=10)

    label = ctk.CTkLabel(window, text="User Login", font=("Arial", 30))
    label.pack(pady=20)

    label1 = ctk.CTkLabel(window, text="User ID:", font=("Arial", 20))
    label1.pack(pady=20)
    text1 = ctk.CTkEntry(window, placeholder_text="Enter User ID", font=("Arial", 20), width=200, height=30)
    text1.pack(pady=10)

    label2 = ctk.CTkLabel(window, text="Password:", font=("Arial", 20))
    label2.pack(pady=20)
    text2 = ctk.CTkEntry(window, placeholder_text="Enter Password", show="*", font=("Arial", 20), width=200, height=30)
    text2.pack(pady=10)

    login_button = ctk.CTkButton(window, text="Login", command=lambda: user_origin(window,text1.get(),text2.get(),pics,pics1,pics2,db), width=100, height=30, font=("Arial", 20))
    login_button.pack(pady=20)
    
    login_button = ctk.CTkButton(window, text="Register", command=lambda: user_register(window,db), width=100, height=30, font=("Arial", 20))
    login_button.pack(pady=20)

def staff_origin(window, work_id, password,pics):
    db = DatabaseManager()
    
    staff = db.fetch_one("SELECT * FROM staff WHERE work_id = %s", (work_id,))
    if staff is None:
        messagebox.showerror("Error", "Invalid Work ID!")
    else:
        stored_password = staff[2]
        if password == stored_password:#correct case!!!!!!!!
            success_label = ctk.CTkLabel(window, text="{}, welcome!".format(staff[1]), font=("Arial", 20), text_color="green")
            success_label.pack(pady=10)
            window.after(800, lambda: staff_dashboard(window,work_id, db))
        else:
            messagebox.showerror("Error", "Incorrect password!\nPlease try again!")

def user_register(window, db):
    register_window = tk.Toplevel(window)
    register_window.title("User Registration")
    register_window.geometry("400x600")

    # Title label
    label = ctk.CTkLabel(register_window, text="User Registration", font=("Arial", 20))
    label.pack(pady=10)

    # Name entry
    label4 = ctk.CTkLabel(register_window, text="Name:", font=("Arial", 15))
    label4.pack(pady=5)
    name_entry = ctk.CTkEntry(register_window, placeholder_text="Enter your name", font=("Arial", 15), width=200, height=25)
    name_entry.pack(pady=5)

    # Password entry
    label2 = ctk.CTkLabel(register_window, text="Password:", font=("Arial", 15))
    label2.pack(pady=5)
    password_entry = ctk.CTkEntry(register_window, placeholder_text="Enter Password", show="*", font=("Arial", 15), width=200, height=25)
    password_entry.pack(pady=5)

    # Confirm password entry
    label3 = ctk.CTkLabel(register_window, text="Confirm Password:", font=("Arial", 15))
    label3.pack(pady=5)
    confirm_password_entry = ctk.CTkEntry(register_window, placeholder_text="Confirm Password", show="*", font=("Arial", 15), width=200, height=25)
    confirm_password_entry.pack(pady=5)

    # Gender dropdown menu (using CTkOptionMenu for selection)
    label5 = ctk.CTkLabel(register_window, text="Gender:", font=("Arial", 15))
    label5.pack(pady=5)
    gender_options = ["male", "female"]
    gender_var = tk.StringVar(value=gender_options[0])  # Default value: "male"
    gender_menu = ctk.CTkOptionMenu(register_window, variable=gender_var, values=gender_options, font=("Arial", 15), width=200)
    gender_menu.pack(pady=5)

    # Birthdate entry (Using a placeholder format)
    label6 = ctk.CTkLabel(register_window, text="Birthdate:", font=("Arial", 15))
    label6.pack(pady=5)
    birth_entry = ctk.CTkEntry(register_window, placeholder_text="yyyy-mm-dd", font=("Arial", 15), width=200, height=25)
    birth_entry.pack(pady=5)

    # Country entry
    label7 = ctk.CTkLabel(register_window, text="Country", font=("Arial", 15))
    label7.pack(pady=5)
    country_entry = ctk.CTkEntry(register_window, placeholder_text="Enter your country", font=("Arial", 15), width=200, height=25)
    country_entry.pack(pady=5)

    # Confirm button to register
    confirm_button = ctk.CTkButton(register_window, text="Confirm", command=lambda: register_user(db, name_entry, password_entry, confirm_password_entry, gender_var, birth_entry, country_entry), width=100, height=30, font=("Arial", 20))
    confirm_button.pack(pady=10)
    
    def register_user(db, name_entry, password_entry, confirm_password_entry, gender_var, birth_entry, country_entry):
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        gender = gender_var.get()
        user_name = name_entry.get()
        birthdate = birth_entry.get()
        country = country_entry.get()

        if password != confirm_password:
            show_error_message("Passwords do not match!")
        elif not password or not user_name or not birthdate or not country:
            show_error_message("All fields are required!")
        elif gender not in ["male", "female"]:
            show_error_message("Invalid gender!")
        else:
            try:
                # Check if user already exists
                existing_user = db.fetch_one("SELECT user_name FROM users WHERE user_name = %s", (user_name,))
                if existing_user:
                    show_error_message("Username already exists!")
                else:
                    # Register the user in the database
                    db.execute_query(""" 
                    INSERT INTO users (password, user_name, gender, birthday, country)
                    VALUES (%s, %s, %s, %s, %s) RETURNING user_id
                    """, (password, user_name, gender, birthdate, country))

                    user_id = db.fetch_one("SELECT LASTVAL();")[0]
                    show_success_message(f"Registration successful! Your User ID is {user_id}. \nPlease remember your ID for the next login.")
            except Exception as e:
                show_error_message(f"Error: {str(e)}")

    def show_error_message(message):
        messagebox.showerror("Registration Error", message)

    def show_success_message(message):
        messagebox.showinfo("Registration Success", message)            
def user_origin(window, user_id, password,pics,pics1,pics2,db):
    if user_id == "":
        messagebox.showerror("error","Please enter a user ID.")
        return
    if password == "":
        messagebox.showerror("error","Please enter a password.")
        return
    user = db.fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if user is None:
        messagebox.showerror("Login Error", "No such user found!\nYou can register first!")
         
    else:
        stored_password = user[5] 
        if password == stored_password:
            success_label = ctk.CTkLabel(window, text="{}, welcome!".format(user[1]), font=("Arial", 20), text_color="green")
            success_label.pack(pady=10)
            window.after(800, lambda: user_dashboard(window,user_id, db, pics,pics1,pics2)) 
        else:
            messagebox.showerror("Login Error", "Incorrect password!\nPlease try again!")
 
def edit_dramas(window, display_frame, dramas):
    for widget in display_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget to display the order data
    treeview = ttk.Treeview(display_frame, columns=("drama_id","drama_name","description","duration"), show="headings")

    # Define column headings
    treeview.heading("drama_id", text="Drama ID")
    treeview.heading("drama_name", text="Drama Name")
    treeview.heading("description", text="Description")
    treeview.heading("duration", text="Duration")

    # Define column width
    treeview.column("drama_id", width=50)
    treeview.column("drama_name", width=100)
    treeview.column("description", width=200)
    treeview.column("duration", width=50)

    vertical_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    treeview.pack(fill="both", expand=True)

    for drama in dramas:
        treeview.insert("", "end", values=(drama))
    
    button_frame=ctk.CTkFrame(display_frame)
    button_frame.pack(side="bottom", fill="x", pady=5)

    button = ctk.CTkButton(button_frame, text="Edit Info", command=lambda: edit_drama_info(window,db,treeview))
    button.pack(pady=5,padx=20, side="right")

    button1 = ctk.CTkButton(button_frame, text="Add new", command=lambda: Add_drama(db, treeview, window))
    button1.pack(pady=5,padx=20, side="left")
    
    button2=ctk.CTkButton(button_frame, text="Delete", command=lambda: delete_drama(db, treeview))
    button2.pack(pady=5,padx=20, side="right")

def edit_drama_info(window, db, treeview):
    selected_item = treeview.selection()
    
    if not selected_item:
        messagebox.showerror("Error", "Please select a drama to edit.")
        return

    drama_info = treeview.item(selected_item[0])['values']
    
    if len(drama_info) != 4:
        messagebox.showerror("Error", "Invalid drama data.")
        return
    
    # Extract current data from the selected row
    drama_id, drama_name, description, duration = drama_info
    
    # Create a window to edit the drama info
    edit_drama_info_window = tk.Toplevel(window)
    edit_drama_info_window.title("Edit Drama Info")
    edit_drama_info_window.geometry("300x550")
    
    # Drama name entry
    label1 = ctk.CTkLabel(edit_drama_info_window, text="Drama Name", font=("Arial", 16))
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(edit_drama_info_window, width=200)
    name_entry.insert(0, drama_name)  # Set current name as the default
    name_entry.pack(pady=10)
    
    # Duration entry
    label3 = ctk.CTkLabel(edit_drama_info_window, text="Duration", font=("Arial", 16))
    label3.pack(pady=10)
    duration_entry = ctk.CTkEntry(edit_drama_info_window, width=200)
    duration_entry.insert(0, duration)  # Set current duration as the default
    duration_entry.pack(pady=10)
    
    # Description entry (multiline textbox)
    label2 = ctk.CTkLabel(edit_drama_info_window, text="Description", font=("Arial", 16))
    label2.pack(pady=10)
    description_entry = ctk.CTkTextbox(edit_drama_info_window, width=200, height=100)
    description_entry.insert("1.0", description)  
    description_entry.pack(pady=10)

    button = ctk.CTkButton(edit_drama_info_window, text="Save", 
                           command=lambda: save_drama_info(db, drama_id, name_entry.get(), description_entry.get("1.0", "end-1c"), duration_entry.get(), edit_drama_info_window, treeview))
    button.pack(pady=10)
    button1 = ctk.CTkButton(edit_drama_info_window, text="Close", 
                            command=lambda: edit_drama_info_window.destroy())
    button1.pack(pady=10)

def save_drama_info(db, drama_id, drama_name, description, duration, edit_drama_info_window, treeview):
    if not drama_name:
        messagebox.showerror("Error", "Please enter a name.")
        return
    if not description:
        messagebox.showerror("Error", "Please enter a description.")
        return
    if not duration:
        messagebox.showerror("Error", "Please enter a duration.")
        return
    
    # Check if there are any changes before updating
    if drama_name == treeview.item(treeview.selection()[0])['values'][1] and description == treeview.item(treeview.selection()[0])['values'][2] and duration == treeview.item(treeview.selection()[0])['values'][3]:
        messagebox.showinfo("Success", "No changes made.")
        edit_drama_info_window.destroy()
        return

    # Update the database with the new values
    query = "UPDATE dramas SET drama_name = %s, description = %s, duration = %s WHERE drama_id = %s"
    
    try:
        db.execute_query(query, (drama_name, description, duration, drama_id))
        
        # Update the treeview item to reflect the changes
        selected_item = treeview.selection()[0]
        treeview.item(selected_item, values=(drama_id, drama_name, description, duration))
        
        messagebox.showinfo("Success", "Drama info updated successfully!")
        edit_drama_info_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update drama info: {e}")

def Add_drama(db, treeview, window):
    add_drama_window = tk.Toplevel(window)
    add_drama_window.title("Add Drama")
    add_drama_window.geometry("300x500")  # Increased height for multiline input
    
    label1 = ctk.CTkLabel(add_drama_window, text="Drama Name", font=("Arial", 16))
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(add_drama_window, placeholder_text="Enter drama name", width=200)
    name_entry.pack(pady=10)
    
    label2 = ctk.CTkLabel(add_drama_window, text="Description", font=("Arial", 16))
    label2.pack(pady=10)
    
    # Use CTkTextbox for multiline input
    description_entry = ctk.CTkTextbox(add_drama_window, width=200, height=100)
    description_entry.pack(pady=10)
    
    label3 = ctk.CTkLabel(add_drama_window, text="Duration", font=("Arial", 16))
    label3.pack(pady=10)
    duration_entry = ctk.CTkEntry(add_drama_window, placeholder_text="Enter duration", width=200)
    duration_entry.pack(pady=10)
    
    button = ctk.CTkButton(add_drama_window, text="Add", command=lambda: add_drama(db, name_entry.get(), description_entry.get("1.0", "end-1c"), duration_entry.get(), treeview))
    button.pack(pady=10)
    
    button1 = ctk.CTkButton(add_drama_window, text="Close", command=lambda: add_drama_window.destroy())
    button1.pack(pady=10)
    
    def add_drama(db, name_entry, description_entry, duration_entry, treeview):
        if not name_entry:
            messagebox.showerror("Error", "Please enter a name.")
            return
        if not description_entry:
            messagebox.showerror("Error", "Please enter a description.")
            return
        if not duration_entry:
            messagebox.showerror("Error", "Please enter a duration.")
        
        query = "INSERT INTO dramas (drama_name, description, duration) VALUES (%s, %s, %s)"
        
        try:
            db.execute_query(query, (name_entry, description_entry, duration_entry))
            last_inserted_id = db.cursor.lastrowid
            
            # Insert into the treeview with the updated id
            treeview.insert("", "end", values=(last_inserted_id, name_entry, description_entry, duration_entry))
            messagebox.showinfo("Success", "Drama added successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add drama: {e}")

def delete_drama(db, treeview):
    selected_item = treeview.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this drama?")
        if confirm:
            drama_id = treeview.item(selected_item[0])['values'][0]
            performance_ids = db.fetch_all("SELECT performance_id FROM performances WHERE drama_id = %s", (drama_id,))
    
            query3 = "DELETE FROM tickets WHERE performance_id = %s"
            query4 = "DELETE FROM performance_actors WHERE performance_id = %s"
            query5 = "DELETE FROM schedules WHERE performance_id = %s"
            query1 = "DELETE FROM performances WHERE drama_id = %s"
            query2 = "DELETE FROM dramas WHERE drama_id = %s"
            
            try:
                for performance in performance_ids:
                    performance_id = performance
                    
                    # Deleting related entries in schedules, performance_actors, and tickets for each performance
                    db.execute_query(query5, (performance_id,))
                    db.execute_query(query4, (performance_id,))
                    db.execute_query(query3, (performance_id,))

                # Step 2: Delete the performances and drama
                db.execute_query(query1, (drama_id,))
                db.execute_query(query2, (drama_id,))
                
                # Remove the drama from the treeview
                treeview.delete(selected_item[0])
                
                messagebox.showinfo("Success", "Drama deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete drama: {e}")

def edit_actors(window, display_frame, actors, db):
    for widget in display_frame.winfo_children():
        widget.destroy()
        
    treeview = ttk.Treeview(display_frame, columns=("actor_id", "actor_name", "gender", "birthdate", "biography"), show="headings")

    # Define column headings
    treeview.heading("actor_id", text="Actor ID")
    treeview.heading("actor_name", text="Actor Name")
    treeview.heading("gender", text="Gender")
    treeview.heading("birthdate", text="Birthdate")
    treeview.heading("biography", text="Biography")
    
    treeview.column("actor_id", width=50)
    treeview.column("actor_name", width=100)
    treeview.column("gender", width=50)
    treeview.column("birthdate", width=80)
    treeview.column("biography", width=200)

    vertical_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    treeview.pack(fill="both", expand=True)

    for actor in actors:
        treeview.insert("", "end", values=actor)
    
    button_frame = ctk.CTkFrame(display_frame)
    button_frame.pack(side="bottom", fill="x", pady=5)

    button = ctk.CTkButton(button_frame, text="Edit Info", command=lambda: edit_actor_info(window, db, treeview))
    button.pack(pady=5, padx=20, side="right")

    button1 = ctk.CTkButton(button_frame, text="Add New", command=lambda: Add_actor(db, treeview, window))
    button1.pack(pady=5, padx=20, side="left")
    
    button2 = ctk.CTkButton(button_frame, text="Delete", command=lambda: delete_actor(db, treeview))
    button2.pack(pady=5, padx=20, side="right")


def edit_actor_info(window, db, treeview):
    selected_item = treeview.selection()
    
    if not selected_item:
        messagebox.showerror("Error", "Please select an actor to edit.")
        return

    actor_info = treeview.item(selected_item[0])['values']
    
    if len(actor_info) != 5:
        messagebox.showerror("Error", "Invalid actor data.")
        return
    
    # Extract current data from the selected row
    actor_id, actor_name, gender, birthdate, biography = actor_info
    
    # Create a window to edit the actor info
    edit_actor_info_window = tk.Toplevel(window)
    edit_actor_info_window.title("Edit Actor Info")
    edit_actor_info_window.geometry("300x650")
    
    # Actor name entry
    label1 = ctk.CTkLabel(edit_actor_info_window, text="Actor Name", font=("Arial", 16))
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(edit_actor_info_window, width=200)
    name_entry.insert(0, actor_name)  # Set current name as the default
    name_entry.pack(pady=10)
    
    # Gender entry
    label2 = ctk.CTkLabel(edit_actor_info_window, text="Gender", font=("Arial", 16))
    label2.pack(pady=10)
    gender_entry = ctk.CTkEntry(edit_actor_info_window, width=200)
    gender_entry.insert(0, gender)  # Set current gender as the default
    gender_entry.pack(pady=10)
    
    # Birthdate entry
    label3 = ctk.CTkLabel(edit_actor_info_window, text="Birthdate", font=("Arial", 16))
    label3.pack(pady=10)
    birthdate_entry = ctk.CTkEntry(edit_actor_info_window, width=200)
    birthdate_entry.insert(0, birthdate)  # Set current birthdate as the default
    birthdate_entry.pack(pady=10)
    
    # Biography entry (multiline textbox)
    label4 = ctk.CTkLabel(edit_actor_info_window, text="Biography", font=("Arial", 16))
    label4.pack(pady=10)
    biography_entry = ctk.CTkTextbox(edit_actor_info_window, width=200, height=100)
    biography_entry.insert("1.0", biography)  # Set current biography as the default
    biography_entry.pack(pady=10)

    # Save button
    button = ctk.CTkButton(edit_actor_info_window, text="Save", 
                           command=lambda: save_actor_info(db, actor_id, name_entry.get(), gender_entry.get(), birthdate_entry.get(), biography_entry.get("1.0", "end-1c"), edit_actor_info_window, treeview))
    button.pack(pady=10)
    
    # Close button
    button1 = ctk.CTkButton(edit_actor_info_window, text="Close", 
                            command=lambda: edit_actor_info_window.destroy())
    button1.pack(pady=10)

def save_actor_info(db, actor_id, actor_name, gender, birthdate, biography, edit_actor_info_window, treeview):
    # Input validation
    if not actor_name:
        messagebox.showerror("Error", "Please enter a name.")
        return
    if not biography:
        messagebox.showerror("Error", "Please enter a biography.")
        return
    
    # Check if there are any changes before updating
    selected_item = treeview.selection()[0]
    if actor_name == treeview.item(selected_item)['values'][1] and gender == treeview.item(selected_item)['values'][2] and birthdate == treeview.item(selected_item)['values'][3] and biography == treeview.item(selected_item)['values'][4]:
        messagebox.showinfo("Success", "No changes made.")
        edit_actor_info_window.destroy()
        return

    # Update the database with the new values
    query = "UPDATE actors SET actor_name = %s, gender = %s, birthday = %s, biography = %s WHERE actor_id = %s"
    
    try:
        db.execute_query(query, (actor_name, gender, birthdate, biography, actor_id))
        
        # Update the treeview item to reflect the changes
        treeview.item(selected_item, values=(actor_id, actor_name, gender, birthdate, biography))
        
        messagebox.showinfo("Success", "Actor info updated successfully!")
        edit_actor_info_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update actor info: {e}")

def Add_actor(db, treeview, window):
    add_drama_window = tk.Toplevel(window)
    add_drama_window.title("Add Actor")
    add_drama_window.geometry("300x650")  
    
    label1 = ctk.CTkLabel(add_drama_window, text="Actor Name", font=("Arial", 16))
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(add_drama_window, placeholder_text="Enter actor name", width=200)
    name_entry.pack(pady=10)
    
    label2 = ctk.CTkLabel(add_drama_window, text="Biography", font=("Arial", 16))
    label2.pack(pady=10)
    description_entry = ctk.CTkTextbox(add_drama_window, width=200, height=100)
    description_entry.pack(pady=10)
    
    label3 = ctk.CTkLabel(add_drama_window, text="Gender", font=("Arial", 16))
    label3.pack(pady=10)
    gender_entry = ctk.CTkEntry(add_drama_window, placeholder_text="male/female", width=200)
    gender_entry.pack(pady=10)
    
    label4 = ctk.CTkLabel(add_drama_window, text="Birthdate", font=("Arial", 16))
    label4.pack(pady=10)
    birthdate_entry = ctk.CTkEntry(add_drama_window, placeholder_text="YYYY-MM-DD", width=200)
    birthdate_entry.pack(pady=10)
    
    button = ctk.CTkButton(add_drama_window, text="Add", command=lambda: add_actor(db, name_entry.get(), description_entry.get("1.0", "end-1c"), gender_entry.get(),birthdate_entry.get(), treeview))
    button.pack(pady=10)
    
    button1 = ctk.CTkButton(add_drama_window, text="Close", command=lambda: add_drama_window.destroy())
    button1.pack(pady=10)
    
    def add_actor(db, name_entry, description_entry, gender_entry, birthdate_entry,treeview):
        if not name_entry:
            messagebox.showerror("Error", "Please enter a name.")
            return
        if not description_entry:
            messagebox.showerror("Error", "Please enter a description.")
            return
        
        query = "INSERT INTO actors (actor_name, biography, gender,birthday) VALUES (%s, %s, %s,%s)"
        
        try:
            db.execute_query(query, (name_entry, description_entry, gender_entry,birthdate_entry))
            last_inserted_id = db.cursor.lastrowid
            
            # Insert into the treeview with the updated id
            treeview.insert("", "end", values=(last_inserted_id, name_entry, gender_entry,birthdate_entry,description_entry))
            messagebox.showinfo("Success", "Actor added successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add actor: {e}")


def delete_actor(db, treeview):
    selected_item = treeview.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this actor?")
        if confirm:
            actor_id = treeview.item(selected_item[0])['values'][0]  
            query1 = "DELETE FROM performance_actors WHERE actor_id = %s"
            query2 = "DELETE FROM actors WHERE actor_id = %s"

            try:
                db.execute_query(query1, (actor_id,))
                db.execute_query(query2, (actor_id,))
                treeview.delete(selected_item[0])

                messagebox.showinfo("Success", "Actor deleted successfully!") 
            except Exception as e:
                # Rollback if any error occurs
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete actor: {e}")

def edit_theaters(window, display_frame, theaters, db):
    for widget in display_frame.winfo_children():
        widget.destroy()

    treeview = ttk.Treeview(display_frame, columns=("theater_id", "theater_name", "address", "seats", "contact"), show="headings")

    # Define column headings
    treeview.heading("theater_id", text="Theater ID")
    treeview.heading("theater_name", text="Theater Name")
    treeview.heading("address", text="Address")
    treeview.heading("seats", text="Seats Num")
    treeview.heading("contact", text="Contact Num")
    
    treeview.column("theater_id", width=50)
    treeview.column("theater_name", width=100)
    treeview.column("address", width=200)
    treeview.column("seats", width=50)
    treeview.column("contact", width=100)

    vertical_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    treeview.pack(fill="both", expand=True)

    for theater in theaters:
        treeview.insert("", "end", values=theater)
    
    button_frame = ctk.CTkFrame(display_frame)
    button_frame.pack(side="bottom", fill="x", pady=5)

    button = ctk.CTkButton(button_frame, text="Edit Info", command=lambda: edit_theater_info(window, db, treeview))
    button.pack(pady=5, padx=20, side="right")

    button1 = ctk.CTkButton(button_frame, text="Add New", command=lambda: Add_theater(db, treeview, window))
    button1.pack(pady=5, padx=20, side="left")
    
    button2 = ctk.CTkButton(button_frame, text="Delete", command=lambda: delete_theater(db, treeview))
    button2.pack(pady=5, padx=20, side="right")


def edit_theater_info(window, db, treeview):
    selected_item = treeview.selection()
    
    if not selected_item:
        messagebox.showerror("Error", "Please select a theater to edit.")
        return

    theater_info = treeview.item(selected_item[0])['values']
    
    if len(theater_info) != 5:
        messagebox.showerror("Error", "Invalid theater data.")
        return
    
    theater_id, theater_name, address, seats, contact = theater_info
    
    edit_theater_info_window = tk.Toplevel(window)
    edit_theater_info_window.title("Edit Theater Info")
    edit_theater_info_window.geometry("300x650")

    label1 = ctk.CTkLabel(edit_theater_info_window, text="Theater Name:")
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(edit_theater_info_window, placeholder_text="Theater Name", width=200)
    name_entry.insert(0, theater_name)
    name_entry.pack(pady=10)

    label2 = ctk.CTkLabel(edit_theater_info_window, text="Address:")
    label2.pack(pady=10)
    address_entry = ctk.CTkTextbox(edit_theater_info_window, width=200,height=100)
    address_entry.insert("1.0", address)
    address_entry.pack(pady=10)
    
    label3 = ctk.CTkLabel(edit_theater_info_window, text="Seats:")
    label3.pack(pady=10)
    seats_entry = ctk.CTkEntry(edit_theater_info_window, placeholder_text="Seats", width=200)
    seats_entry.insert(0, seats)
    seats_entry.pack(pady=10)
    
    label4 = ctk.CTkLabel(edit_theater_info_window, text="Contact:")
    label4.pack(pady=10)
    contact_entry = ctk.CTkEntry(edit_theater_info_window, placeholder_text="Contact", width=200)
    contact_entry.insert(0, contact)
    contact_entry.pack(pady=10)

    button = ctk.CTkButton(edit_theater_info_window, text="Save", 
                           command=lambda: save_theater_info(db, theater_id, name_entry.get(), address_entry.get("1.0", "end-1c"), seats_entry.get(), contact_entry.get(), edit_theater_info_window, treeview))
    button.pack(pady=10)
    
    button1 = ctk.CTkButton(edit_theater_info_window, text="Close", 
                            command=lambda: edit_theater_info_window.destroy())
    button1.pack(pady=10)

def save_theater_info(db, theater_id, theater_name, address, seats, contact, edit_theater_info_window, treeview):
    if not theater_name:
        messagebox.showerror("Error", "Please enter a theater name.")
        return
    if not address:
        messagebox.showerror("Error", "Please enter an address.")
        return
    
    selected_item = treeview.selection()[0]
    if theater_name == treeview.item(selected_item)['values'][1] and address == treeview.item(selected_item)['values'][2] and seats == treeview.item(selected_item)['values'][3] and contact == treeview.item(selected_item)['values'][4]:
        messagebox.showinfo("Success", "No changes made.")
        edit_theater_info_window.destroy()
        return

    query = "UPDATE theaters SET theater_name = %s, address = %s, seats = %s, contact_num = %s WHERE theater_id = %s"
    
    try:
        db.execute_query(query, (theater_name, address, seats, contact, theater_id))
        treeview.item(selected_item, values=(theater_id, theater_name, address, seats, contact))
        
        messagebox.showinfo("Success", "Theater info updated successfully!")
        edit_theater_info_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update theater info: {e}")


def Add_theater(db, treeview, window):
    add_theater_window = tk.Toplevel(window)
    add_theater_window.title("Add Theater")
    add_theater_window.geometry("300x650")  
    
    label1 = ctk.CTkLabel(add_theater_window, text="Theater Name:")
    label1.pack(pady=10)
    name_entry = ctk.CTkEntry(add_theater_window, placeholder_text="Theater Name", width=200)
    name_entry.pack(pady=10)
    
    label2 = ctk.CTkLabel(add_theater_window, text="Address:")
    label2.pack(pady=10)
    address_entry = ctk.CTkTextbox(add_theater_window, width=200,height=100)
    address_entry.pack(pady=10)
    
    label3 = ctk.CTkLabel(add_theater_window, text="Seats Num:")
    label3.pack(pady=10)
    seats_entry = ctk.CTkEntry(add_theater_window, placeholder_text="Seats", width=200)
    seats_entry.pack(pady=10)
    
    label4 = ctk.CTkLabel(add_theater_window, text="Contact Num:")
    label4.pack(pady=10)
    contact_entry = ctk.CTkEntry(add_theater_window, placeholder_text="Contact", width=200)
    contact_entry.pack(pady=10)    
    
    button = ctk.CTkButton(add_theater_window, text="Add", command=lambda: add_theater(db, name_entry.get(), address_entry.get("1.0", "end-1c"), seats_entry.get(), contact_entry.get(), treeview))
    button.pack(pady=10)
    
    button1 = ctk.CTkButton(add_theater_window, text="Close", command=lambda: add_theater_window.destroy())
    button1.pack(pady=10)
    
def add_theater(db, name_entry, address_entry, seats_entry, contact_entry, treeview):
    if not name_entry:
        messagebox.showerror("Error", "Please enter a name.")
        return
    if not address_entry:
        messagebox.showerror("Error", "Please enter an address.")
        return
    if not seats_entry:
        messagebox.showerror("Error", "Please enter the number of seats.")
        return
    if not contact_entry:
        messagebox.showerror("Error", "Please enter a contact number.")
        return
    
    query = "INSERT INTO theaters (theater_name, address, seats, contact_num) VALUES (%s, %s, %s, %s)"
    
    try:
        db.execute_query(query, (name_entry, address_entry, seats_entry, contact_entry))
        last_inserted_id = db.cursor.lastrowid
        treeview.insert("", "end", values=(last_inserted_id, name_entry, address_entry, seats_entry, contact_entry))
        messagebox.showinfo("Success", "Theater added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add theater: {e}")

def delete_theater(db, treeview):
    selected_item = treeview.selection()
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this theater?")
        if confirm:
            theater_id = treeview.item(selected_item[0])['values'][0]
            performance_ids = db.fetch_all("SELECT performance_id FROM performances WHERE theater_id = %s", (theater_id,))
            
            query_schedule = "DELETE FROM schedules WHERE theater_id = %s"
            query_ticket = "DELETE FROM tickets WHERE performance_id = %s"
            query_performance_actors = "DELETE FROM performance_actors WHERE performance_id = %s"
            query_performance = "DELETE FROM performances WHERE performance_id = %s"
            query_theater = "DELETE FROM theaters WHERE theater_id = %s"
            
            try:
                db.execute_query(query_schedule, (theater_id,))
                for performance in performance_ids:
                    performance_id = performance[0]
                    db.execute_query(query_ticket, (performance_id,))
                    db.execute_query(query_performance_actors, (performance_id,))
                    db.execute_query(query_performance, (performance_id,))
                db.execute_query(query_theater, (theater_id,))
                treeview.delete(selected_item[0])
                
                messagebox.showinfo("Success", "Theater and associated performances deleted successfully!") 
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete theater: {e}")


def edit_performances(window,display_frame,db):
    for widget in display_frame.winfo_children():
        widget.destroy()
    performances = db.fetch_all("""
                SELECT 
                performances.performance_id,
                dramas.drama_name, 
                theaters.theater_name,
                actors.actor_name, 
                performance_actors.role,
                schedules.start_time,
                schedules.end_time
                FROM performances 
                LEFT JOIN theaters ON performances.theater_id = theaters.theater_id 
                LEFT JOIN dramas ON dramas.drama_id = performances.drama_id
                LEFT JOIN performance_actors ON performance_actors.performance_id = performances.performance_id
                LEFT JOIN actors ON actors.actor_id = performance_actors.actor_id
                LEFT JOIN schedules ON performances.performance_id = schedules.performance_id;
            """)

    treeview = ttk.Treeview(display_frame, columns=("performance_id","drama_name","theater_name","actor","role","start_time","end_time"), show="headings")

    # Define column headings
    treeview.heading("performance_id", text="Performance ID")
    treeview.heading("drama_name", text="Drama Name")
    treeview.heading("theater_name", text="Theater Name")
    treeview.heading("actor", text="Actor")
    treeview.heading("role", text="Role")
    treeview.heading("start_time", text="Start Time")
    treeview.heading("end_time", text="End Time")
    
    treeview.column("performance_id", width=50)
    treeview.column("drama_name", width=80)
    treeview.column("theater_name", width=80)
    treeview.column("actor", width=80)
    treeview.column("role", width=80)
    treeview.column("start_time", width=80)
    treeview.column("end_time", width=80)

    vertical_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    treeview.pack(fill="both", expand=True)

    for performance in performances:
        treeview.insert("", "end", values=performance)
        
    button_frame = ctk.CTkFrame(display_frame)
    button_frame.pack(side="bottom", fill="x", pady=5)

    button = ctk.CTkButton(button_frame, text="Edit Performance Info", command=lambda: edit_performance_info(window, db, treeview))
    button.pack(pady=5, padx=5, side="left")

    button1 = ctk.CTkButton(button_frame, text="Add New Performance", command=lambda: Add_performance(db, treeview, window))
    button1.pack(pady=5, padx=5, side="left")
    
    button2 = ctk.CTkButton(button_frame, text="Delete Performance", command=lambda: delete_performance(db, treeview))
    button2.pack(pady=5, padx=5, side="right")
    
    buutton3 = ctk.CTkButton(button_frame, text="Adjust character", command=lambda: adjust_character(window, db, treeview))
    buutton3.pack(pady=5, padx=5, side="left")


# Edit performance info function
def edit_performance_info(window, db, treeview):
    selected_item = treeview.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a performance to edit.")
        return

    performance_info = treeview.item(selected_item[0])['values']

    if len(performance_info) != 7:
        messagebox.showerror("Error", "Invalid performance data.")
        return

    performance_id, drama_name, theater_name, actor, role, start_time, end_time = performance_info

    edit_performance_info_window = tk.Toplevel(window)
    edit_performance_info_window.title("Edit Performance Info")
    edit_performance_info_window.geometry("300x550")

    # Drama Name
    label2 = ctk.CTkLabel(edit_performance_info_window, text="Drama Name:")
    label2.pack(pady=10)
    drama_entry = ctk.CTkEntry(edit_performance_info_window, placeholder_text="Drama Name", width=200)
    drama_entry.insert(0, drama_name)
    drama_entry.pack(pady=10)
    
    # Theater Name
    label3 = ctk.CTkLabel(edit_performance_info_window, text="Theater Name:")
    label3.pack(pady=10)
    theater_entry = ctk.CTkEntry(edit_performance_info_window, placeholder_text="Theater Name", width=200)
    theater_entry.insert(0, theater_name)
    theater_entry.pack(pady=10)

    # Start Time
    label6 = ctk.CTkLabel(edit_performance_info_window, text="Start Time:")
    label6.pack(pady=10)
    start_time_entry = ctk.CTkEntry(edit_performance_info_window, placeholder_text="Start Time", width=200)
    start_time_entry.insert(0, start_time)
    start_time_entry.pack(pady=10)

    # End Time
    label7 = ctk.CTkLabel(edit_performance_info_window, text="End Time:")
    label7.pack(pady=10)
    end_time_entry = ctk.CTkEntry(edit_performance_info_window, placeholder_text="End Time", width=200)
    end_time_entry.insert(0, end_time)
    end_time_entry.pack(pady=10)

    # Save Button
    save_button = ctk.CTkButton(edit_performance_info_window, text="Save", command=lambda: save_performance_info(treeview, performance_id, drama_entry.get(), theater_entry.get(), start_time_entry.get(), end_time_entry.get(), selected_item, edit_performance_info_window))
    save_button.pack(pady=10)
    
    close_button=ctk.CTkButton(edit_performance_info_window, text="Close", command=lambda:edit_performance_info_window.destroy())
    close_button.pack(pady=10)


def save_performance_info(treeview, performance_id, updated_drama_name, updated_theater_name, updated_start_time, updated_end_time, selected_item, edit_performance_info_window):
    try:
        # Fetch the relevant IDs from the database
        theater_id = db.fetch_one("SELECT theater_id FROM theaters WHERE theater_name=%s", (updated_theater_name,))[0]
        drama_id = db.fetch_one("SELECT drama_id FROM dramas WHERE drama_name=%s", (updated_drama_name,))[0]

        # Update the performance and schedule information
        query_performance = """
        UPDATE performances
        JOIN theaters ON performances.theater_id = theaters.theater_id
        JOIN schedules ON schedules.performance_id = performances.performance_id
        SET performances.theater_id = %s,
            performances.drama_id = %s
        WHERE performances.performance_id = %s
        """
        query_schedule="""UPDATE schedules
        SET start_time = %s,
            end_time = %s
        WHERE performance_id = %s"""
        db.execute_query(query_performance, (theater_id, drama_id, updated_start_time, updated_end_time, performance_id))
        db.execute_query(query_schedule, (updated_start_time, updated_end_time, performance_id))
        # Update the treeview
        treeview.item(selected_item, values=(performance_id, updated_drama_name, updated_theater_name, updated_start_time, updated_end_time))

        messagebox.showinfo("Success", "Performance info updated successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update performance info: {e}")

def Add_performance(db, treeview, window):
    add_performance_window = tk.Toplevel(window)
    add_performance_window.title("Add Performance")
    add_performance_window.geometry("300x600")  

    label2 = ctk.CTkLabel(add_performance_window, text="Drama Name")
    label2.pack(pady=10)
    drama_name_entry = ctk.CTkEntry(add_performance_window, placeholder_text="Drama Name", width=200)
    drama_name_entry.pack(pady=10)
    
    label3 = ctk.CTkLabel(add_performance_window, text="Theater Name")
    label3.pack(pady=10)
    theater_entry= ctk.CTkEntry(add_performance_window, placeholder_text="Theater Name", width=200)
    theater_entry.pack(pady=10)
    
    label5 = ctk.CTkLabel(add_performance_window, text="Start Time")
    label5.pack(pady=10)
    start_time_entry = ctk.CTkEntry(add_performance_window, placeholder_text="Start Time", width=200)
    start_time_entry.pack(pady=10)
    
    label6 = ctk.CTkLabel(add_performance_window, text="End Time")
    label6.pack(pady=10)
    end_time_entry = ctk.CTkEntry(add_performance_window, placeholder_text="End Time", width=200)
    end_time_entry.pack(pady=10)
    
    button = ctk.CTkButton(add_performance_window, text="Add", command=lambda: add_performance(db, drama_name_entry.get(),theater_entry.get(),start_time_entry.get(), end_time_entry.get(), treeview))
    button.pack(pady=10)
    
    button1 = ctk.CTkButton(add_performance_window, text="Close", command=lambda: add_performance_window.destroy())
    button1.pack(pady=10)

def add_performance(db, drama_name, theater_name,start_time, end_time, treeview):
    if not drama_name or not theater_name or not start_time or not end_time:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        drama_id = db.fetch_one("SELECT drama_id FROM dramas WHERE drama_name=%s", (drama_name,))[0]
        theater_id = db.fetch_one("SELECT theater_id FROM theaters WHERE theater_name=%s",(theater_name))[0]

        query = """
        INSERT INTO performances (drama_id, theater_id)
        VALUES (%s, %s)
        """
        db.execute_query(query, (drama_id, theater_id,))
        messagebox.showinfo("Success", "Performance added successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add performance: {e}")


def adjust_character(window, db, treeview):
    window1 = tk.Toplevel(window)
    window1.title("Adjust Character")   
    window1.geometry("300x500") 

    # Performance ID label and entry
    label1 = ctk.CTkLabel(window1, text="Performance ID", font=("Arial", 16))
    label1.pack(pady=10)
    entry1 = ctk.CTkEntry(window1, width=200)
    entry1.pack(pady=10)
    
    # Actor Name label and entry
    label = ctk.CTkLabel(window1, text="Actor Name", font=("Arial", 16))
    label.pack(pady=10)
    entry = ctk.CTkEntry(window1, width=200)
    entry.pack(pady=10)
    
    # Role label and entry
    label3 = ctk.CTkLabel(window1, text="Role", font=("Arial", 16))
    label3.pack(pady=10)
    entry2 = ctk.CTkEntry(window1, width=200)
    entry2.pack(pady=10)
    
    # Confirm button
    button = ctk.CTkButton(window1, text="Confirm", command=lambda: adjust_actor(db, entry1.get(), entry.get(), entry2.get(), treeview))
    button.pack(pady=10)
    
    # Close button
    button2 = ctk.CTkButton(window1, text="Close", command=lambda: window1.destroy())
    button2.pack(pady=10)


def adjust_actor(db, performance_id, actor_name, role, treeview):
    # Fetch all performance ids to check if the performance exists
    performance_ids = [performance[0] for performance in db.fetch_all("SELECT performance_id FROM performances")]
    print(performance_ids)
    if int(performance_id) not in performance_ids:
        messagebox.showerror("Error", "Performance does not exist!")
        return
    
    existing_roles = [role[0] for role in db.fetch_all("SELECT role FROM performance_actors WHERE performance_id=%s", (performance_id,))]
    
    # Check if the role already exists
    if role in existing_roles:
        confirm = messagebox.askyesno("Confirm", "The role exists.\nDo you want to replace it?")
        if confirm:
            db.execute_query("""
                UPDATE performance_actors
                SET actor_id = (SELECT actor_id FROM actors WHERE actor_name = %s)
                WHERE performance_id = %s AND role = %s
            """, (actor_name, performance_id, role))
            messagebox.showinfo("Success", "Actor changed successfully!")
        else:
            return
    else:
        # Check if the actor exists in the actors table
        actor_id = db.fetch_one("SELECT actor_id FROM actors WHERE actor_name = %s", (actor_name,))
        if actor_id is None:
            messagebox.showerror("Error", "Actor not found in the database!")
            return
        
        actor_id = actor_id[0]
        
        db.execute_query("""
            INSERT INTO performance_actors (performance_id, role, actor_id)
            VALUES (%s, %s, %s)
        """, (performance_id, role, actor_id))
        messagebox.showinfo("Success", "Actor added successfully!")
        treeview.refresh()



def delete_performance(db, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a performance to delete.")
        return
    if selected_item:
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this performance?")
        if confirm:
            performance_id = treeview.item(selected_item[0])['values'][0]
            query1 = "DELETE FROM performances WHERE performance_id = %s"
            query2 = "DELETE FROM tickets WHERE performance_id = %s"
            query3 = "DELETE FROM schedules WHERE performance_id = %s"
            query4 = "DELETE FROM performance_actors WHERE performance_id = %s"
            try:
                db.execute_query(query4, (performance_id,))
                db.execute_query(query3, (performance_id,))
                db.execute_query(query2, (performance_id,))
                db.execute_query(query1, (performance_id,))
                treeview.delete(selected_item[0])
                messagebox.showinfo("Success", "Performance deleted successfully!") 
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete performance: {e}")
                
def show_dramas(window, display_frame, dramas, pics, i,user_id):
    for widget in display_frame.winfo_children():
        widget.destroy()
    play1_frame = ctk.CTkFrame(display_frame)
    play1_frame.pack(side="top", fill="x", expand=True, pady=5)

    play2_frame = ctk.CTkFrame(display_frame)
    play2_frame.pack(side="top", fill="x", expand=True, pady=5)
    if i < len(dramas):  
        play1_name = dramas[i][1]
        image = load_image(play1_name, pics)  
        play1 = ctk.CTkLabel(play1_frame, text=play1_name, font=("Arial", 20), image=image, compound="left")
        play1.pack(side="left", padx=10, pady=10)
        play1.image = image
        
        info = ctk.CTkButton(play1_frame, text="Learn more...", command=lambda: detail(window, play1_name,dramas[i]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play1_frame, text="Tickets", command=lambda: select_tickets(window, play1_name,dramas[i],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i + 1 < len(dramas): 
        play2_name = dramas[i + 1][1]
        image = load_image(play2_name, pics) 
        play2 = ctk.CTkLabel(play2_frame, text=play2_name, font=("Arial", 20), image=image, compound="left")
        play2.pack(side="left", padx=10, pady=10)
        play2.image = image
        
        info = ctk.CTkButton(play2_frame, text="Learn more...", command=lambda: detail(window, play2_name, dramas[i+1]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play2_frame, text="Tickets", command=lambda: select_tickets(window, play2_name,dramas[i+1],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i+2<len(dramas):
        next_button = ctk.CTkButton(display_frame, text=">", command=lambda: next_page(window, dramas, pics, display_frame,  i, user_id), width=50, height=30, font=("Arial", 14))
        next_button.pack(side="right", padx=10, pady=10)
    if i>0:  
        last_button = ctk.CTkButton(display_frame, text="<", command=lambda: last_page(window, dramas, pics, display_frame, i, user_id), width=50, height=30, font=("Arial", 14))
        last_button.pack(side="left", padx=10, pady=10)

def show_actors(window, display_frame, actors, pics1, i,user_id):

    for widget in display_frame.winfo_children():
        widget.destroy()
    play1_frame = ctk.CTkFrame(display_frame)
    play1_frame.pack(side="top", fill="x", expand=True, pady=5)

    play2_frame = ctk.CTkFrame(display_frame)
    play2_frame.pack(side="top", fill="x", expand=True, pady=5)
    
    if i < len(actors):  
        actor1_name = actors[i][1]
        image = load_image(actor1_name, pics1)  
        play1 = ctk.CTkLabel(play1_frame, text=actor1_name, font=("Arial", 20), image=image, compound="left")
        play1.pack(side="left", padx=10, pady=10)
        play1.image = image
        
        info = ctk.CTkButton(play1_frame, text="Learn more...", command=lambda: detail_actor(window, actor1_name,actors[i]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play1_frame, text="Tickets", command=lambda: select_tickets_actor(window, actor1_name,actors[i],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i + 1 < len(actors): 
        actor2_name = actors[i + 1][1]
        image = load_image(actor2_name, pics1) 
        play2 = ctk.CTkLabel(play2_frame, text=actor2_name, font=("Arial", 20), image=image, compound="left")
        play2.pack(side="left", padx=10, pady=10)
        play2.image = image
        
        info = ctk.CTkButton(play2_frame, text="Learn more...", command=lambda: detail_actor(window, actor2_name,actors[i+1]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play2_frame, text="Tickets", command=lambda: select_tickets_actor(window, actor2_name,actors[i+1],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i+2<len(actors):
        next_button = ctk.CTkButton(display_frame, text=">", command=lambda: next_page_actor(window, actors, pics1, display_frame,  i, user_id), width=50, height=30, font=("Arial", 14))
        next_button.pack(side="right", padx=10, pady=10)
    if i>0:
        last_button = ctk.CTkButton(display_frame, text="<", command=lambda: last_page_actor(window, actors, pics1, display_frame, i, user_id), width=50, height=30, font=("Arial", 14))
        last_button.pack(side="left", padx=10, pady=10)
        
def show_theaters(window,display_frame, theaters, pics2, i,user_id):
    for widget in display_frame.winfo_children():
        widget.destroy()
    play1_frame = ctk.CTkFrame(display_frame)
    play1_frame.pack(side="top", fill="x", expand=True, pady=5)

    play2_frame = ctk.CTkFrame(display_frame)
    play2_frame.pack(side="top", fill="x", expand=True, pady=5)
    
    if i < len(theaters):  
        theater1_name = theaters[i][1]
        image = load_image(theater1_name, pics2)  
        play1 = ctk.CTkLabel(play1_frame, text=theater1_name, font=("Arial", 20), image=image, compound="left")
        play1.pack(side="left", padx=10, pady=10)
        play1.image = image
        
        info = ctk.CTkButton(play1_frame, text="Learn more...", command=lambda: detail_theater(window, theater1_name,theaters[i]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play1_frame, text="Tickets", command=lambda: select_tickets_theater(window, theater1_name,theaters[i],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i + 1 < len(theaters): 
        theater2_name = theaters[i + 1][1]
        image = load_image(theater2_name, pics2) 
        play2 = ctk.CTkLabel(play2_frame, text=theater2_name, font=("Arial", 20), image=image, compound="left")
        play2.pack(side="left", padx=10, pady=10)
        play2.image = image
        
        info = ctk.CTkButton(play2_frame, text="Learn more...", command=lambda: detail_theater(window, theater2_name,theaters[i+1]), width=50, height=30, font=("Arial", 14))
        info.pack(side="left", padx=10, pady=10)
        
        tickets= ctk.CTkButton(play2_frame, text="Tickets", command=lambda: select_tickets_theater(window, theater2_name,theaters[i+1],db,user_id), width=50, height=30, font=("Arial", 14))
        tickets.pack(side="left", padx=10, pady=10)
        
    if i+2<len(theaters):
        next_button = ctk.CTkButton(display_frame, text=">", command=lambda: next_page_theater(window, theaters, pics2, display_frame,  i, user_id), width=50, height=30, font=("Arial", 14))
        next_button.pack(side="right", padx=10, pady=10)
    if i>0:
        last_button = ctk.CTkButton(display_frame, text="<", command=lambda: last_page_theater(window, theaters, pics2, display_frame, i, user_id), width=50, height=30, font=("Arial", 14))
        last_button.pack(side="left", padx=10, pady=10)
    
    

def select_tickets(window, play_name, current_drama, db, user_id): 
    # Create a new window for buying tickets
    tickets_window = tk.Toplevel(window)
    tickets_window.title(f"Buy Tickets for {play_name}")
    tickets_window.geometry("1000x700")  # Set window size
    
    drama_id = current_drama[0]

    # Create a frame at the top for sorting options
    sort_frame = ctk.CTkFrame(tickets_window)
    sort_frame.pack(fill="x", pady=10)

    # Create sorting column label and dropdown menu
    sort_column_label = ctk.CTkLabel(sort_frame, text="Sort By:", font=("Arial", 15))
    sort_column_label.pack(pady=10, padx=10, side='left')

    sort_column_options = ['Theater', 'Start time', 'End time', 'Class', 'Price']
    sort_column_var = tk.StringVar(value=sort_column_options[0])  # Default is 'Theater'
    
    sort_column_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_column_var, values=sort_column_options, font=("Arial", 15), width=200)
    sort_column_menu.pack(pady=10, padx=10, side='left')

    # Create sorting order label and dropdown menu
    sort_order_label = ctk.CTkLabel(sort_frame, text="Sort Order:", font=("Arial", 15))
    sort_order_label.pack(pady=10, padx=10, side='left')

    sort_order_options = ['Ascending', 'Descending']
    sort_order_var = tk.StringVar(value=sort_order_options[0])  # Default is 'Ascending'

    sort_order_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_order_var, values=sort_order_options, font=("Arial", 15), width=200)
    sort_order_menu.pack(pady=10, padx=10, side='left')
    
    # Create region filter entry field
    region_label = ctk.CTkLabel(sort_frame, text="Region:", font=("Arial", 15))
    region_label.pack(pady=10, padx=10, side='left')
    region_entry = ctk.CTkEntry(sort_frame, width=200, font=("Arial", 15))
    region_entry.pack(pady=10, padx=10, side='left')   

    # Create Confirm button to apply sorting
    confirm_button = ctk.CTkButton(sort_frame, text="Confirm", 
                                   command=lambda: sort_tickets(tickets_window, db, drama_id, sort_column_var.get(), sort_order_var.get(), region_entry.get()), 
                                   width=200, height=30, font=("Arial", 14))
    confirm_button.pack(pady=10, padx=10, side='left')

    treeview = sort_tickets(tickets_window, db, drama_id)
    
    buy_tickets_frame = ctk.CTkFrame(tickets_window)
    buy_tickets_frame.pack(fill='x', pady=10)
    
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", command=lambda: buy_tickets(user_id, tickets_window, buy_tickets_frame, treeview, db, drama_id), width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")

def select_tickets_actor(window, actor_name, current_actor, db, user_id):
    tickets_window = tk.Toplevel(window)
    tickets_window.title(f"Buy Tickets for {actor_name}")
    tickets_window.geometry("1000x700")  
    
    actor_id = current_actor[0]

    # Create a frame at the top for sorting options
    sort_frame = ctk.CTkFrame(tickets_window)
    sort_frame.pack(fill="x", pady=10)

    # Create sorting column label and dropdown menu
    sort_column_label = ctk.CTkLabel(sort_frame, text="Sort By:", font=("Arial", 15))
    sort_column_label.pack(pady=10, padx=10, side='left')

    sort_column_options = ['Drama name','Theater', 'Start time', 'End time', 'Class', 'Price']
    sort_column_var = tk.StringVar(value=sort_column_options[0])  # Default is 'Theater'
    
    sort_column_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_column_var, values=sort_column_options, font=("Arial", 15), width=200)
    sort_column_menu.pack(pady=10, padx=10, side='left')

    # Create sorting order label and dropdown menu
    sort_order_label = ctk.CTkLabel(sort_frame, text="Sort Order:", font=("Arial", 15))
    sort_order_label.pack(pady=10, padx=10, side='left')

    sort_order_options = ['Ascending', 'Descending']
    sort_order_var = tk.StringVar(value=sort_order_options[0])  # Default is 'Ascending'

    sort_order_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_order_var, values=sort_order_options, font=("Arial", 15), width=200)
    sort_order_menu.pack(pady=10, padx=10, side='left')
    
    # Create region filter entry field
    region_label = ctk.CTkLabel(sort_frame, text="Region:", font=("Arial", 15))
    region_label.pack(pady=10, padx=10, side='left')
    region_entry = ctk.CTkEntry(sort_frame, width=200, font=("Arial", 15))
    region_entry.pack(pady=10, padx=10, side='left')   

    # Create Confirm button to apply sorting
    confirm_button = ctk.CTkButton(sort_frame, text="Confirm", 
                                   command=lambda: sort_tickets_actor(tickets_window, db, actor_id, sort_column_var.get(), sort_order_var.get(), region_entry.get()), 
                                   width=200, height=30, font=("Arial", 14))
    confirm_button.pack(pady=10, padx=10, side='left')

    treeview = sort_tickets_actor(tickets_window, db, actor_id)
    
    buy_tickets_frame = ctk.CTkFrame(tickets_window)
    buy_tickets_frame.pack(fill='x', pady=10)
    
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", command=lambda: buy_tickets_actor(user_id, tickets_window, buy_tickets_frame, treeview, db, actor_id), width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")

def select_tickets_theater(window, theater_name,current_theater,db,user_id):
    tickets_window = tk.Toplevel(window)
    tickets_window.title(f"Buy Tickets for {theater_name}")
    tickets_window.geometry("1000x700")  
    
    theater_id = current_theater[0]

    # Create a frame at the top for sorting options
    sort_frame = ctk.CTkFrame(tickets_window)
    sort_frame.pack(fill="x", pady=10)

    # Create sorting column label and dropdown menu
    sort_column_label = ctk.CTkLabel(sort_frame, text="Sort By:", font=("Arial", 15))
    sort_column_label.pack(pady=10, padx=10, side='left')

    sort_column_options = ['Drama name','Theater', 'Start time', 'End time', 'Class', 'Price']
    sort_column_var = tk.StringVar(value=sort_column_options[0])  # Default is 'Theater'
    
    sort_column_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_column_var, values=sort_column_options, font=("Arial", 15), width=200)
    sort_column_menu.pack(pady=10, padx=10, side='left')

    # Create sorting order label and dropdown menu
    sort_order_label = ctk.CTkLabel(sort_frame, text="Sort Order:", font=("Arial", 15))
    sort_order_label.pack(pady=10, padx=10, side='left')

    sort_order_options = ['Ascending', 'Descending']
    sort_order_var = tk.StringVar(value=sort_order_options[0])  # Default is 'Ascending'

    sort_order_menu = ctk.CTkOptionMenu(sort_frame, variable=sort_order_var, values=sort_order_options, font=("Arial", 15), width=200)
    sort_order_menu.pack(pady=10, padx=10, side='left')
      

    # Create Confirm button to apply sorting
    confirm_button = ctk.CTkButton(sort_frame, text="Confirm", 
                                   command=lambda: sort_tickets_theater(tickets_window, db, theater_id, sort_column_var.get(), sort_order_var.get()), 
                                   width=200, height=30, font=("Arial", 14))
    confirm_button.pack(pady=10, padx=10, side='right')

    treeview = sort_tickets_theater(tickets_window, db, theater_id)
    
    buy_tickets_frame = ctk.CTkFrame(tickets_window)
    buy_tickets_frame.pack(fill='x', pady=10)
    
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", command=lambda: buy_tickets_theater(user_id, tickets_window, buy_tickets_frame, treeview, db, theater_id), width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")
    
def buy_tickets(user_id, tickets_window, buy_tickets_frame, treeview, db, drama_id):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a ticket to buy.")
        return
    
    ticket_info = treeview.item(selected_item[0])['values']
    
    # Ensure ticket_info has the correct number of values
    if len(ticket_info) != 7:
        messagebox.showerror("Error", "Invalid ticket data.")
        return

    ticket_id, theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info

    if left_tickets <= 0:
        messagebox.showerror("Error", "Sorry, no tickets available for this show.")
        return

    # Hide the 'Buy it now' button and show the order confirmation
    for widget in buy_tickets_frame.winfo_children():
        widget.destroy()

    # Recreate the 'Buy it now' button with the correct command for confirmation
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", 
                               command=lambda: show_order_confirmation(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class, drama_id),
                               width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")

def buy_tickets_actor(user_id, tickets_window, buy_tickets_frame, treeview, db, actor_id):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a ticket to buy.")
        return
    
    ticket_info = treeview.item(selected_item[0])['values']
    
    if len(ticket_info) != 9:
        messagebox.showerror("Error", "Invalid ticket data.")
        return

    ticket_id,drama_name,role, theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info
    
    if left_tickets <= 0:
        messagebox.showerror("Error", "Sorry, no tickets available for this show.")
        return

    for widget in buy_tickets_frame.winfo_children():
        widget.destroy()

    # Recreate the 'Buy it now' button with the correct command for confirmation
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", 
                               command=lambda: show_order_confirmation_1(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class, actor_id),
                               width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")
    
def buy_tickets_theater(user_id, tickets_window, buy_tickets_frame, treeview, db, theater_id):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a ticket to buy.")
        return
    
    ticket_info = treeview.item(selected_item[0])['values']
    
    if len(ticket_info) != 8:
        messagebox.showerror("Error", "Invalid ticket data.")
        return

    ticket_id,drama_name,theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info
    
    if left_tickets <= 0:
        messagebox.showerror("Error", "Sorry, no tickets available for this show.")
        return

    for widget in buy_tickets_frame.winfo_children():
        widget.destroy()

    # Recreate the 'Buy it now' button with the correct command for confirmation
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", 
                               command=lambda: show_order_confirmation_2(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class,theater_id),
                               width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")
# Function to confirm the order
def confirm_order(user_id, tickets_window, treeview, db, ticket_id, ticket_class):
    print(f"User ID: {user_id}, Ticket ID: {ticket_id}, Ticket Class: {ticket_class}")  # Debug print statement

    try:
        # Fetch orders to check if the user already bought the ticket
        orders = db.fetch_all("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        for order in orders:
            if order[2] == ticket_id:
                messagebox.showerror("Error", "You have already purchased this ticket.")
                return

        # Update the tickets table to reduce the number of available tickets
        db.execute_query(
            """UPDATE tickets
            SET left_tickets = left_tickets - 1
            WHERE ticket_id = %s""",
            (ticket_id,)
        )

        # Generate the seat ID based on ticket class
        seat_id = generate_seat_id(ticket_class)
        db.execute_query(
            """INSERT INTO orders(user_id, ticket_id, seat_id, status)
            VALUES (%s, %s, %s, 'paid')""",
            (user_id, ticket_id, seat_id)
        )
        # Success message
        messagebox.showinfo("Success", f"Successfully purchased one ticket! \nYour seat ID is {seat_id}\nYou can check your order in the <My Orders> page.")
        
        # Close the tickets window
        tickets_window.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while confirming your order: {str(e)}")

# Function to show the order confirmation details
def show_order_confirmation(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class, drama_id):
    try:
        # Hide the 'Buy it now' button and show the order confirmation
        buy_tickets_frame.destroy()
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a ticket to buy.")
            return
        ticket_info = treeview.item(selected_item[0])['values']
        if len(ticket_info) != 7:
            messagebox.showerror("Error", "Invalid ticket data.")
            return

        ticket_id, theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info
        if left_tickets <= 0:
            messagebox.showerror("Error", "Sorry, no tickets available for this show.")
            return

        # Create a frame for the order confirmation details
        order_frame = ctk.CTkFrame(tickets_window, corner_radius=10)
        order_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Title label for confirmation
        title_label = ctk.CTkLabel(order_frame, text="Please confirm your order:", font=("Arial", 18, "bold"))
        title_label.pack(pady=7, padx=10, side='top')

        # Fetch user and drama information from the database
        user_name = db.fetch_one("SELECT user_name FROM users WHERE user_id = %s", (user_id,))
        drama_name = db.fetch_one("SELECT drama_name FROM dramas WHERE drama_id = %s", (drama_id,))
        address = db.fetch_one("SELECT address FROM theaters WHERE theater_name = %s", (theater_name,))
        total_money = price  # Assuming buying 1 ticket

        user_name = user_name[0]
        drama_name = drama_name[0]
        address = address[0]

        # Details to show in the confirmation window
        details = [
            ("User name", user_name),
            ("Drama name", drama_name),
            ("Theater name", theater_name),
            ("Theater address", address),
            ("Start time", start_time),
            ("End time", end_time),
            ("Ticket class", ticket_class),
            ("Amount", 1),
            ("Total money", total_money)
        ]

        details_frame = ctk.CTkScrollableFrame(order_frame, corner_radius=10, bg_color="#f0f0f0")
        details_frame.pack(pady=7, padx=10, fill="both", expand=True)

        # Loop through the details and create labels
        for label_text, value in details:
            detail_label = ctk.CTkLabel(details_frame, text=f"{label_text}: {value}", font=("Arial", 13))
            detail_label.pack(pady=5, padx=10, side='top')

        # Add some space before the button
        button_frame = ctk.CTkFrame(order_frame)
        button_frame.pack(fill='x', pady=6, padx=10)

        # Create the confirm purchase button and the cancel button, placing them in the same row
        confirm_button = ctk.CTkButton(button_frame, text="Confirm Purchase",
                                       command=lambda: confirm_order(user_id, tickets_window, treeview, db, ticket_id, ticket_class),
                                       width=150, height=40, font=("Arial", 14))
        confirm_button.pack(side='left', padx=30)

        cancel_button = ctk.CTkButton(button_frame, text="Cancel Purchase",
                                      command=lambda: cancel_order(user_id, tickets_window, order_frame, treeview, db, drama_id),
                                      width=150, height=40, font=("Arial", 14))
        cancel_button.pack(side='right', padx=30)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def show_order_confirmation_1(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class, actor_id):
    try:
        buy_tickets_frame.destroy()
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a ticket to buy.")
            return
        ticket_info = treeview.item(selected_item[0])['values']
        if len(ticket_info) != 9:
            messagebox.showerror("Error", "Invalid ticket data.")
            return

        ticket_id,drama_name, role,theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info
        if left_tickets <= 0:
            messagebox.showerror("Error", "Sorry, no tickets available for this show.")
            return

        # Create a frame for the order confirmation details
        order_frame = ctk.CTkFrame(tickets_window, corner_radius=10)
        order_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Title label for confirmation
        title_label = ctk.CTkLabel(order_frame, text="Please confirm your order:", font=("Arial", 18, "bold"))
        title_label.pack(pady=7, padx=10, side='top')

        # Fetch user and drama information from the database
        user_name = db.fetch_one("SELECT user_name FROM users WHERE user_id = %s", (user_id,))
        drama_id = db.fetch_one("SELECT drama_id FROM dramas WHERE drama_name = %s", (drama_name,))
        address = db.fetch_one("SELECT address FROM theaters WHERE theater_name = %s", (theater_name,))
        total_money = price  # Assuming buying 1 ticket

        user_name = user_name[0]
        address = address[0]

        # Details to show in the confirmation window
        details = [
            ("User name", user_name),
            ("Drama name", drama_name),
            ("Theater name", theater_name),
            ("Theater address", address),
            ("Start time", start_time),
            ("End time", end_time),
            ("Ticket class", ticket_class),
            ("Amount", 1),
            ("Total money", total_money)
        ]

        details_frame = ctk.CTkScrollableFrame(order_frame, corner_radius=10, bg_color="#f0f0f0")
        details_frame.pack(pady=7, padx=10, fill="both", expand=True)

        # Loop through the details and create labels
        for label_text, value in details:
            detail_label = ctk.CTkLabel(details_frame, text=f"{label_text}: {value}", font=("Arial", 13))
            detail_label.pack(pady=5, padx=10, side='top')

        # Add some space before the button
        button_frame = ctk.CTkFrame(order_frame)
        button_frame.pack(fill='x', pady=6, padx=10)

        # Create the confirm purchase button and the cancel button, placing them in the same row
        confirm_button = ctk.CTkButton(button_frame, text="Confirm Purchase",
                                       command=lambda: confirm_order(user_id, tickets_window, treeview, db, ticket_id, ticket_class),
                                       width=150, height=40, font=("Arial", 14))
        confirm_button.pack(side='left', padx=30)

        cancel_button = ctk.CTkButton(button_frame, text="Cancel Purchase",
                                      command=lambda: cancel_order(user_id, tickets_window, order_frame, treeview, db, drama_id),
                                      width=150, height=40, font=("Arial", 14))
        cancel_button.pack(side='right', padx=30)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
def show_order_confirmation_2(user_id, tickets_window, buy_tickets_frame, treeview, db, ticket_id, ticket_class,theater_id):
    try:
        buy_tickets_frame.destroy()
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a ticket to buy.")
            return
        ticket_info = treeview.item(selected_item[0])['values']
        if len(ticket_info) != 8:
            messagebox.showerror("Error", "Invalid ticket data.")
            return

        ticket_id,drama_name, theater_name, start_time, end_time, ticket_class, price, left_tickets = ticket_info
        if left_tickets <= 0:
            messagebox.showerror("Error", "Sorry, no tickets available for this show.")
            return

        # Create a frame for the order confirmation details
        order_frame = ctk.CTkFrame(tickets_window, corner_radius=10)
        order_frame.pack(pady=20, padx=30, fill="both", expand=True)

        # Title label for confirmation
        title_label = ctk.CTkLabel(order_frame, text="Please confirm your order:", font=("Arial", 18, "bold"))
        title_label.pack(pady=7, padx=10, side='top')

        # Fetch user and drama information from the database
        user_name = db.fetch_one("SELECT user_name FROM users WHERE user_id = %s", (user_id,))
        drama_id = db.fetch_one("SELECT drama_id FROM dramas WHERE drama_name = %s", (drama_name,))
        address = db.fetch_one("SELECT address FROM theaters WHERE theater_name = %s", (theater_name,))
        total_money = price  # Assuming buying 1 ticket

        user_name = user_name[0]
        address = address[0]

        # Details to show in the confirmation window
        details = [
            ("User name", user_name),
            ("Drama name", drama_name),
            ("Theater name", theater_name),
            ("Theater address", address),
            ("Start time", start_time),
            ("End time", end_time),
            ("Ticket class", ticket_class),
            ("Amount", 1),
            ("Total money", total_money)
        ]

        details_frame = ctk.CTkScrollableFrame(order_frame, corner_radius=10, bg_color="#f0f0f0")
        details_frame.pack(pady=7, padx=10, fill="both", expand=True)

        # Loop through the details and create labels
        for label_text, value in details:
            detail_label = ctk.CTkLabel(details_frame, text=f"{label_text}: {value}", font=("Arial", 13))
            detail_label.pack(pady=5, padx=10, side='top')

        # Add some space before the button
        button_frame = ctk.CTkFrame(order_frame)
        button_frame.pack(fill='x', pady=6, padx=10)

        # Create the confirm purchase button and the cancel button, placing them in the same row
        confirm_button = ctk.CTkButton(button_frame, text="Confirm Purchase",
                                       command=lambda: confirm_order(user_id, tickets_window, treeview, db, ticket_id, ticket_class),
                                       width=150, height=40, font=("Arial", 14))
        confirm_button.pack(side='left', padx=30)

        cancel_button = ctk.CTkButton(button_frame, text="Cancel Purchase",
                                      command=lambda: cancel_order(user_id, tickets_window, order_frame, treeview, db, drama_id),
                                      width=150, height=40, font=("Arial", 14))
        cancel_button.pack(side='right', padx=30)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
def cancel_order(user_id, tickets_window, order_frame, treeview, db, drama_id):
    # Close the order confirmation and restore the 'Buy it now' button
    order_frame.destroy()
    buy_tickets_frame = ctk.CTkFrame(tickets_window)
    buy_tickets_frame.pack(fill='x', pady=10)
    buy_button = ctk.CTkButton(buy_tickets_frame, text="Buy it now", command=lambda: buy_tickets(user_id, tickets_window, buy_tickets_frame, treeview, db, drama_id), width=200, height=30, font=("Arial", 14))
    buy_button.pack(pady=10, padx=10, side="top")

def generate_seat_id(ticket_class):
    if ticket_class == 'VIP':
        seat_id = f"V{random.randint(1, 100)}"
    else:
        seat_id = f"{random.choice(['A', 'B', 'C'])}{random.randint(1, 100)}"
    return seat_id

def sort_tickets(tickets_window, db, drama_id, sort_column='theater', sort_order='ascending', region=''):
    # Check if the Treeview already exists, if so, clear its content
    treeview = None
    for widget in tickets_window.winfo_children():
        if isinstance(widget, ttk.Treeview):  # Find the Treeview widget
            treeview = widget
            break  # We only need the first Treeview we find

    if treeview is None:
        treeview = ttk.Treeview(tickets_window, columns=("ticket_id", "theater_name", "start_time", "end_time", "class", "price", "left_tickets"), show="headings")
        treeview.heading("ticket_id", text="Ticket ID")
        treeview.heading("theater_name", text="Theater")
        treeview.heading("start_time", text="Start Time")
        treeview.heading("end_time", text="End Time")
        treeview.heading("class", text="Class")
        treeview.heading("price", text="Price")
        treeview.heading("left_tickets", text="Left Tickets")

        treeview.column("ticket_id", width=30)
        treeview.column("theater_name", width=150)
        treeview.column("start_time", width=150)
        treeview.column("end_time", width=150)
        treeview.column("class", width=80)
        treeview.column("price", width=100)
        treeview.column("left_tickets", width=100)

        scrollbar = ttk.Scrollbar(tickets_window, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        treeview.pack(fill="both", expand=True)

    sort_order_sql = "ASC" if sort_order == 'Ascending' else "DESC"
    
    sort_column_map = {
        'Ticket ID': 'T.ticket_id',
        'Theater': 'H.theater_name',
        'Start time': 'S.start_time',
        'End time': 'S.end_time',
        'Class': 'T.class',
        'Price': 'T.price'
    }

    region_condition = ""
    if region:
        region_condition = f"AND H.address LIKE %s"
        region = f"%{region}%"  # Use SQL LIKE pattern

    query = f"""
        SELECT T.ticket_id, H.theater_name, S.start_time, S.end_time, T.class, T.price, T.left_tickets
        FROM tickets AS T
        JOIN performances AS P ON P.performance_id = T.performance_id
        JOIN Theaters AS H ON P.theater_id = H.theater_id
        JOIN schedules AS S ON P.performance_id = S.performance_id
        WHERE P.drama_id = %s
        {region_condition}
        ORDER BY {sort_column_map.get(sort_column, 'H.theater_name')} {sort_order_sql}
    """

    tickets = db.fetch_all(query, (drama_id, region) if region else (drama_id,))
    for row in treeview.get_children():
        treeview.delete(row)
    for ticket in tickets:
        treeview.insert("", "end", values=ticket)

    return treeview

def sort_tickets_actor(tickets_window, db, actor_id, sort_column='theater', sort_order='ascending', region=''):
    # Check if the Treeview already exists, if so, clear its content
    treeview = None
    for widget in tickets_window.winfo_children():
        if isinstance(widget, ttk.Treeview):  # Find the Treeview widget
            treeview = widget
            break  # We only need the first Treeview we find

    if treeview is None:
        treeview = ttk.Treeview(tickets_window, columns=("ticket_id","drama_name", "role","theater_name", "start_time", "end_time", "class", "price", "left_tickets"), show="headings")
        treeview.heading("ticket_id", text="Ticket ID")
        treeview.heading("drama_name", text="Drama Name")
        treeview.heading("role",text="Role")
        treeview.heading("theater_name", text="Theater")
        treeview.heading("start_time", text="Start Time")
        treeview.heading("end_time", text="End Time")
        treeview.heading("class", text="Class")
        treeview.heading("price", text="Price")
        treeview.heading("left_tickets", text="Left Tickets")

        # Define column widths
        treeview.column("ticket_id", width=30)
        treeview.column("drama_name", width=80)
        treeview.column("role",width=80)
        treeview.column("theater_name", width=130)
        treeview.column("start_time", width=150)
        treeview.column("end_time", width=150)
        treeview.column("class", width=50)
        treeview.column("price", width=80)
        treeview.column("left_tickets", width=80)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tickets_window, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        treeview.pack(fill="both", expand=True)

    # Convert the sort_order to SQL-compliant 'ASC' or 'DESC'
    sort_order_sql = "ASC" if sort_order.lower() == 'ascending' else "DESC"
    
    # Mapping of sort columns to actual SQL columns
    sort_column_map = {
        'Ticket ID': 'T.ticket_id',
        'Drama Name': 'D.drama_name',
        'Role': 'PA.role',
        'Theater': 'H.theater_name',
        'Start Time': 'S.start_time',
        'End Time': 'S.end_time',
        'Class': 'T.class',
        'Price': 'T.price'
    }

    # Handling region filtering
    region_condition = ""
    if region:
        region_condition = f"AND H.address LIKE %s"
        region = f"%{region}%"  # Use SQL LIKE pattern

    # Formulating the SQL query
    query = f"""
        SELECT T.ticket_id, D.drama_name,PA.role,H.theater_name, S.start_time, S.end_time, T.class, T.price, T.left_tickets
        FROM tickets AS T
        JOIN performances AS P ON P.performance_id = T.performance_id
        JOIN theaters AS H ON P.theater_id = H.theater_id
        JOIN schedules AS S ON P.performance_id = S.performance_id
        JOIN dramas AS D ON D.drama_id = P.drama_id
        JOIN performance_actors AS PA ON PA.performance_id = P.performance_id
        JOIN actors AS A ON A.actor_id = PA.actor_id
        WHERE A.actor_id = %s
        {region_condition}
        ORDER BY {sort_column_map.get(sort_column, 'H.theater_name')} {sort_order_sql}
    """

    # Fetch the tickets
    try:
        tickets = db.fetch_all(query, (actor_id, region) if region else (actor_id,))
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching tickets: {e}")
        return

    # Clear the existing rows in the Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert new rows into the Treeview
    for ticket in tickets:
        treeview.insert("", "end", values=ticket)

    return treeview

def sort_tickets_theater(tickets_window, db, theater_id, sort_column='theater', sort_order='ascending'):
    # Check if the Treeview already exists, if so, clear its content
    treeview = None
    for widget in tickets_window.winfo_children():
        if isinstance(widget, ttk.Treeview):  # Find the Treeview widget
            treeview = widget
            break  # We only need the first Treeview we find

    if treeview is None:
        treeview = ttk.Treeview(tickets_window, columns=("ticket_id", "drama_name", "theater_name", "start_time", "end_time", "class", "price", "left_tickets"), show="headings")
        treeview.heading("ticket_id", text="Ticket ID")
        treeview.heading("drama_name", text="Drama Name")
        treeview.heading("theater_name", text="Theater")
        treeview.heading("start_time", text="Start Time")
        treeview.heading("end_time", text="End Time")
        treeview.heading("class", text="Class")
        treeview.heading("price", text="Price")
        treeview.heading("left_tickets", text="Left Tickets")

        # Define column widths
        treeview.column("ticket_id", width=30)
        treeview.column("drama_name", width=80)
        treeview.column("theater_name", width=130)
        treeview.column("start_time", width=150)
        treeview.column("end_time", width=150)
        treeview.column("class", width=50)
        treeview.column("price", width=80)
        treeview.column("left_tickets", width=80)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(tickets_window, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        treeview.pack(fill="both", expand=True)

    # Convert the sort_order to SQL-compliant 'ASC' or 'DESC'
    sort_order_sql = "ASC" if sort_order.lower() == 'ascending' else "DESC"
    
    # Mapping of sort columns to actual SQL columns
    sort_column_map = {
        'Ticket ID': 'T.ticket_id',
        'Drama Name': 'D.drama_name',
        'Theater': 'H.theater_name',
        'Start Time': 'S.start_time',
        'End Time': 'S.end_time',
        'Class': 'T.class',
        'Price': 'T.price'
    }

    # Formulating the SQL query
    query = f"""
        SELECT T.ticket_id, D.drama_name, H.theater_name, S.start_time, S.end_time, T.class, T.price, T.left_tickets
        FROM tickets AS T
        JOIN performances AS P ON P.performance_id = T.performance_id
        JOIN theaters AS H ON P.theater_id = H.theater_id
        JOIN schedules AS S ON P.performance_id = S.performance_id
        JOIN dramas AS D ON D.drama_id = P.drama_id
        WHERE H.theater_id = %s
        ORDER BY {sort_column_map.get(sort_column, 'H.theater_name')} {sort_order_sql}
    """

    # Fetch the tickets
    try:
        tickets = db.fetch_all(query, (theater_id,))
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching tickets: {e}")
        return

    # Clear the existing rows in the Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert new rows into the Treeview
    for ticket in tickets:
        treeview.insert("", "end", values=ticket)

    return treeview

    
def detail(window, play1_name,drama_current):
    detail_window = tk.Toplevel(window)
    detail_window.title(play1_name)
    detail_window.geometry("400x400") 

    description_text = drama_current[2]  

    text_widget = ctk.CTkTextbox(detail_window, font=("Arial", 14), width=350, height=200, wrap="word")
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)
    text_widget.insert("0.0", description_text)  
    text_widget.configure(state="disabled") 

    close_button = ctk.CTkButton(detail_window, text="Close", command=detail_window.destroy, width=100, height=30, font=("Arial", 14))
    close_button.pack(side="bottom", padx=10, pady=10)
def detail_actor(window, actor_name, actor_current):
    detail_window = tk.Toplevel(window)
    detail_window.title(actor_name)
    detail_window.geometry("400x400")
    
    birthdate=actor_current[3]
    gender=actor_current[2]    
    description_text = actor_current[4]  

    text_widget = ctk.CTkTextbox(detail_window, font=("Arial", 14), width=350, height=200, wrap="word")
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)
    text_widget.insert("0.0", f"Birthdate: {birthdate}")
    text_widget.insert("1.0", f"Gender: {gender}\n") 
    text_widget.insert("2.0", f"Biography: {description_text}\n")  
    text_widget.configure(state="disabled") 

    close_button = ctk.CTkButton(detail_window, text="Close", command=detail_window.destroy, width=100, height=30, font=("Arial", 14))
    close_button.pack(side="bottom", padx=10, pady=10)
    
def detail_theater(window, theater_name,current_theater):
    detail_window = tk.Toplevel(window)
    detail_window.title(theater_name)
    detail_window.geometry("400x400")
    
    adress=current_theater[2]  
    contact=current_theater[4]

    text_widget = ctk.CTkTextbox(detail_window, font=("Arial", 14), width=350, height=200, wrap="word")
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)
    text_widget.insert("0.0", f"contact: {contact}\n")
    text_widget.insert("1.0", f"address: {adress}\n")
    text_widget.configure(state="disabled") 

    close_button = ctk.CTkButton(detail_window, text="Close", command=detail_window.destroy, width=100, height=30, font=("Arial", 14))
    close_button.pack(side="bottom", padx=10, pady=10)
def load_image(play_name, pics):
    if play_name in pics:
        return pics[play_name]
    else:
        return pics['Default'] 
def next_page(window, dramas, pics, display_frame,  i, user_id):
    i = i + 2
    show_dramas(window, display_frame, dramas, pics, i,user_id)
        
def next_page_actor(window, actors, pics1, display_frame,i, user_id):
    i = i + 2
    show_actors(window, display_frame, actors, pics1, i,user_id)
    
def next_page_theater(window, theaters, pics2, display_frame,i, user_id):
    i = i + 2
    show_theaters(window, display_frame, theaters, pics2, i,user_id)

def last_page(window, dramas, pics, display_frame, i, user_id):
    i =i- 2
    show_dramas(window,display_frame, dramas, pics, i,user_id)
def last_page_actor(window, actors, pics1, display_frame,i,user_id):
    i =i- 2
    show_actors(window,display_frame, actors, pics1, i,user_id)
    
def last_page_theater(window, theaters, pics2, display_frame,i,user_id):
    i =i- 2
    show_theaters(window,display_frame, theaters, pics2, i,user_id)

def user_dashboard(window, user_id, db, pics,pics1,pics2):
    for widget in window.winfo_children():
        widget.pack_forget()

    frame = ctk.CTkFrame(window)
    frame.pack(fill="x", pady=5)

    back_button = ctk.CTkButton(frame, text="Log Out", command=lambda: log_out(window), width=100, height=30, font=("Arial", 16))
    back_button.pack(side="left", padx=10, pady=10)

    info_button = ctk.CTkButton(frame, text="Personal Info", command=lambda: show_user_info(db, user_id, window), width=150, height=30, font=("Arial", 16))
    info_button.pack(side="right", padx=10)

    container_frame = ctk.CTkFrame(window)
    container_frame.pack(fill="both", expand=True, pady=10)

    search_frame = ctk.CTkFrame(container_frame)
    search_frame.pack(side="left", fill="y", padx=5)

    display_frame = ctk.CTkFrame(container_frame)
    display_frame.pack(side="right", fill="both", expand=True, padx=10)
    
    label = ctk.CTkLabel(search_frame, text="Search:",font=("Arial",16))
    label.pack(pady=30)
    
    actors= db.fetch_all("SELECT * FROM actors")
    theaters=db.fetch_all("SELECT * FROM theaters")

    choose1_button = ctk.CTkButton(search_frame, text="Drama", command=lambda: show_dramas(window, display_frame, dramas, pics, 0,user_id),font=("Arial", 16),width=150,height=50)
    choose1_button.pack(side="top", pady=30, anchor="w", padx=10)

    choose2_button = ctk.CTkButton(search_frame, text="Actor", command=lambda: show_actors(window,display_frame, actors, pics1, 0,user_id),font=("Arial", 16),width=150,height=50)
    choose2_button.pack(side="top", pady=30, anchor="w", padx=10)

    choose3_button = ctk.CTkButton(search_frame, text="Theater", command=lambda: show_theaters(window,display_frame, theaters, pics2, 0,user_id),font=("Arial", 16),width=150,height=50)
    choose3_button.pack(side="top", pady=30, anchor="w", padx=10)

    play1_frame = ctk.CTkFrame(display_frame)
    play1_frame.pack(side="top", fill="x", expand=True, pady=5)

    play2_frame = ctk.CTkFrame(display_frame)
    play2_frame.pack(side="top", fill="x", expand=True, pady=5)

    dramas = db.fetch_all("SELECT * FROM dramas")
    show_dramas(window, display_frame, dramas, pics, 0,user_id)

def staff_dashboard(window,work_id, db,):
    for widget in window.winfo_children():
        widget.pack_forget()

    frame = ctk.CTkFrame(window)
    frame.pack(fill="x", pady=5)

    back_button = ctk.CTkButton(frame, text="Log Out", command=lambda: log_out(window), width=100, height=30, font=("Arial", 16))
    back_button.pack(side="left", padx=10, pady=10)

    container_frame = ctk.CTkFrame(window)
    container_frame.pack(fill="both", expand=True, pady=10)

    search_frame = ctk.CTkFrame(container_frame)
    search_frame.pack(side="left", fill="y", padx=5)

    display_frame = ctk.CTkFrame(container_frame)
    display_frame.pack(side="right", fill="both", expand=True, padx=10)
    
    label = ctk.CTkLabel(search_frame, text="Search:",font=("Arial",16))
    label.pack(pady=30)
    
    dramas = db.fetch_all("SELECT * FROM dramas")
    actors= db.fetch_all("SELECT * FROM actors")
    theaters=db.fetch_all("SELECT * FROM theaters")

    choose1_button = ctk.CTkButton(search_frame, text="Drama", command=lambda: edit_dramas(window, display_frame, dramas),font=("Arial", 16),width=150,height=50)
    choose1_button.pack(side="top", pady=20, anchor="w", padx=10)

    choose2_button = ctk.CTkButton(search_frame, text="Actor", command=lambda: edit_actors(window,display_frame, actors,db),font=("Arial", 16),width=150,height=50)
    choose2_button.pack(side="top", pady=20, anchor="w", padx=10)

    choose3_button = ctk.CTkButton(search_frame, text="Theater", command=lambda: edit_theaters(window,display_frame, theaters,db),font=("Arial", 16),width=150,height=50)
    choose3_button.pack(side="top", pady=20, anchor="w", padx=10)
    
    choose4=ctk.CTkButton(search_frame, text="Performance", command=lambda: edit_performances(window,display_frame,db),font=("Arial", 16),width=150,height=50)
    choose4.pack(side="top", pady=20, anchor="w", padx=10)


    
def picture():
    pics = {}  

    image_path0 = "pics\\default.png"
    img0 = Image.open(image_path0)
    img0 = img0.resize((150, 200), Image.Resampling.LANCZOS)
    img0_tk = ImageTk.PhotoImage(img0)
    pics["Default"] = img0_tk

    image_path1 = "pics\\Hamilton.png" 
    img1 = Image.open(image_path1)
    img1 = img1.resize((150, 200), Image.Resampling.LANCZOS)
    img1_tk = ImageTk.PhotoImage(img1)
    pics["Hamilton"] = img1_tk
    

    image_path2 = "pics\\DearEvanHansen.png" 
    img2 = Image.open(image_path2) 
    img2 = img2.resize((150, 200), Image.Resampling.LANCZOS)
    img2_tk = ImageTk.PhotoImage(img2) 
    pics["Dear Evan Hansen"] = img2_tk 

    image_path3 = "pics\\A Chorus Line.png" 
    img3 = Image.open(image_path3) 
    img3 = img3.resize((150, 200), Image.Resampling.LANCZOS)
    img3_tk = ImageTk.PhotoImage(img3) 
    pics["A Chorus Line"] = img3_tk 

    image_path4 = "pics\\Cats.png" 
    img4 = Image.open(image_path4) 
    img4 = img4.resize((150, 200), Image.Resampling.LANCZOS)
    img4_tk = ImageTk.PhotoImage(img4) 
    pics["Cats"] = img4_tk 

    image_path5 = "pics\\Chicago.png" 
    img5 = Image.open(image_path5) 
    img5 = img5.resize((150, 200), Image.Resampling.LANCZOS)
    img5_tk = ImageTk.PhotoImage(img5) 
    pics["Chicago"] = img5_tk 
    
    image_path6 = "pics\\Les Misérables.png" 
    img6 = Image.open(image_path6) 
    img6 = img6.resize((150, 200), Image.Resampling.LANCZOS)
    img6_tk = ImageTk.PhotoImage(img6) 
    pics["Les Misérables"] = img6_tk 

    image_path7 = "pics\\Mamma Mia!.png" 
    img7 = Image.open(image_path7) 
    img7 = img7.resize((150, 200), Image.Resampling.LANCZOS)
    img7_tk = ImageTk.PhotoImage(img7) 
    pics["Mamma Mia!"] = img7_tk 
    
    image_path8 = "pics\\Rent.png" 
    img8 = Image.open(image_path8) 
    img8 = img8.resize((150, 200), Image.Resampling.LANCZOS)
    img8_tk = ImageTk.PhotoImage(img8) 
    pics["Rent"] = img8_tk 

    image_path9 = "pics\\Rock of Ages.png" 
    img9 = Image.open(image_path9) 
    img9 = img9.resize((150, 200), Image.Resampling.LANCZOS)
    img9_tk = ImageTk.PhotoImage(img9) 
    pics["Rock of Ages"] = img9_tk

    image_path10 = "pics\\The Lion King.png" 
    img10 = Image.open(image_path10) 
    img10 = img10.resize((150, 200), Image.Resampling.LANCZOS)
    img10_tk = ImageTk.PhotoImage(img10) 
    pics["The Lion King"] = img10_tk

    image_path11 = "pics\\The Phantom of the Opera.png" 
    img11 = Image.open(image_path11) 
    img11 = img11.resize((150, 200), Image.Resampling.LANCZOS)
    img11_tk = ImageTk.PhotoImage(img11) 
    pics["The Phantom of the Opera"] = img11_tk
    
    image_path12 = "pics\\The Rocky Horror Picture Show.png" 
    img12 = Image.open(image_path12) 
    img12 = img12.resize((150, 200), Image.Resampling.LANCZOS)
    img12_tk = ImageTk.PhotoImage(img12) 
    pics["The Rocky Horror Picture Show"] = img12_tk
    
    image_path13 = "pics\\West Side Story.png" 
    img13 = Image.open(image_path13) 
    img13 = img13.resize((150, 200), Image.Resampling.LANCZOS)
    img13_tk = ImageTk.PhotoImage(img13) 
    pics["West Side Story"] = img13_tk
    
    image_path14 = "pics\\Wicked.png" 
    img14 = Image.open(image_path14) 
    img14 = img14.resize((150, 200), Image.Resampling.LANCZOS)
    img14_tk = ImageTk.PhotoImage(img14) 
    pics["Wicked"] = img14_tk


    return pics

def picture1():
    pics1 = {}  

    image_path0 = "pics\\default.png"
    img0 = Image.open(image_path0)
    img0 = img0.resize((150, 200), Image.Resampling.LANCZOS)
    img0_tk = ImageTk.PhotoImage(img0)
    pics1["Default"] = img0_tk
    
    image_path1 = "pics1\Lin-Manuel Miranda.png"
    img1 = Image.open(image_path1)
    img1 = img1.resize((150, 200), Image.Resampling.LANCZOS)
    img1_tk = ImageTk.PhotoImage(img1)
    pics1["Lin-Manuel Miranda"] = img1_tk
    
    image_path2 = "pics1\Leslie Odom Jr.png" 
    img2 = Image.open(image_path2) 
    img2 = img2.resize((150, 200), Image.Resampling.LANCZOS)
    img2_tk = ImageTk.PhotoImage(img2) 
    pics1["Leslie Odom Jr."] = img2_tk 
    
    image_path3 = "pics1\Phillipa Soo.png" 
    img3 = Image.open(image_path3) 
    img3 = img3.resize((150, 200), Image.Resampling.LANCZOS)
    img3_tk = ImageTk.PhotoImage(img3) 
    pics1["Phillipa Soo"] = img3_tk 
    
    image_path4 = "pics1\Ben Platt.png" 
    img4 = Image.open(image_path4) 
    img4 = img4.resize((150, 200), Image.Resampling.LANCZOS)
    img4_tk = ImageTk.PhotoImage(img4) 
    pics1["Ben Platt"] = img4_tk 
    
    return pics1

def picture2():
    pics2 = {}  
    image_path0 = "pics\default.png"
    img0 = Image.open(image_path0)
    img0 = img0.resize((150, 200), Image.Resampling.LANCZOS)
    img0_tk = ImageTk.PhotoImage(img0)
    pics2["Default"] = img0_tk
    
    image_path1 = r"pics2\Broadway Theater.png"
    img1 = Image.open(image_path1)
    img1 = img1.resize((150, 200), Image.Resampling.LANCZOS)
    img1_tk = ImageTk.PhotoImage(img1)
    pics2["Broadway Theater"] = img1_tk
    
    image_path2 = r"pics2\National Centre for the Performing Arts.png"
    img2 = Image.open(image_path2) 
    img2 = img2.resize((150, 200), Image.Resampling.LANCZOS)
    img2_tk = ImageTk.PhotoImage(img2) 
    pics2["National Centre for the Performing Arts"] = img2_tk
    
    image_path3 = "pics2\Guangzhou Opera House.png" 
    img3 = Image.open(image_path3) 
    img3 = img3.resize((150, 200), Image.Resampling.LANCZOS)
    img3_tk = ImageTk.PhotoImage(img3) 
    pics2["Guangzhou Opera House"] = img3_tk 
    
    image_path4 = "pics2\Hangzhou Theatre.png" 
    img4 = Image.open(image_path4) 
    img4 = img4.resize((150, 200), Image.Resampling.LANCZOS)
    img4_tk = ImageTk.PhotoImage(img4) 
    pics2["Hangzhou Theatre"] = img4_tk 
    
    image_path5 = "pics2\Beijing Poly Theatre.png" 
    img5 = Image.open(image_path5) 
    img5 = img5.resize((150, 200), Image.Resampling.LANCZOS)
    img5_tk = ImageTk.PhotoImage(img5) 
    pics2["Beijing Poly Theatre"] = img5_tk 
    
    image_path6 = "pics2\Shanghai Grand Theatre.png" 
    img6 = Image.open(image_path6) 
    img6 = img6.resize((150, 200), Image.Resampling.LANCZOS)
    img6_tk = ImageTk.PhotoImage(img6) 
    pics2["Shanghai Grand Theatre"] = img6_tk 

    image_path7 = "pics2\London West End.png" 
    img7 = Image.open(image_path7) 
    img7 = img7.resize((150, 200), Image.Resampling.LANCZOS)
    img7_tk = ImageTk.PhotoImage(img7) 
    pics2["London West End"] = img7_tk 
    return pics2


def log_out(window):
    for widget in window.winfo_children():  
        widget.destroy()
    label1 = ctk.CTkLabel(window, text="Welcome to \n My Performance Management System!", font=("Arial", 30))
    label1.pack(pady=20)
    label2 = ctk.CTkLabel(window, text="Please select your role below to continue:", font=("Arial", 20))
    label2.pack(pady=20)
    
    button1 = ctk.CTkButton(window, text="Staff Login", command=lambda: staff_login(window,pics), width=140, height=50, font=("Arial", 20))
    button1.pack(pady=60)
    button2 = ctk.CTkButton(window, text="User Login", command=lambda: User_login(window,pics,pics1,pics2,db), width=140, height=50, font=("Arial", 20))
    button2.pack(pady=60)

def show_user_info(db, user_id, window):
    # Fetch user information from the database
    user_info = db.fetch_one("SELECT * FROM users WHERE user_id=%s", (user_id,))
    
    # Create a new top-level window to show user information
    info_show = tk.Toplevel(window)
    info_show.title("User Info")
    info_show.geometry("600x350")

    button_frame = ctk.CTkFrame(info_show)
    button_frame.pack(fill="x", pady=5)

    button1 = ctk.CTkButton(button_frame, text="Edit Info", font=("Arial", 15), command=lambda: edit_user_info(db, user_id, info_show))
    button1.pack(side='left', padx=10)  
    
    button2 = ctk.CTkButton(button_frame, text="Edit Password", font=("Arial", 15),command=lambda: edit_password(db, user_id, info_show))
    button2.pack(side='left', padx=10)

    button3 = ctk.CTkButton(button_frame, text="My Order", font=("Arial", 15), command=lambda: My_order(db, user_id, info_show))
    button3.pack(side='right', padx=10)

    # Labels to display user information (each label is packed vertically)
    label1 = ctk.CTkLabel(info_show, text=f"User ID: {user_info[0]}", font=("Arial", 16))
    label1.pack(pady=10)

    label2 = ctk.CTkLabel(info_show, text=f"User Name: {user_info[1]}", font=("Arial", 16))
    label2.pack(pady=10)

    label3 = ctk.CTkLabel(info_show, text=f"Gender: {user_info[2]}", font=("Arial", 16))
    label3.pack(pady=10)
    
    label4 = ctk.CTkLabel(info_show, text=f"Birthdate: {user_info[3]}",font=("Arial", 16))
    label4.pack(pady=10)
    
    label5 = ctk.CTkLabel(info_show, text=f"Country: {user_info[4]}", font=("Arial", 16))
    label5.pack(pady=10)
    
    button=ctk.CTkButton(info_show, text="Close", font=("Arial",16),command=lambda: info_show.destroy())
    button.pack(pady=10)

def edit_user_info(db, user_id, info_show):
    # Create a new window for editing user info
    edit_window = tk.Toplevel(info_show)
    edit_window.title("Edit User Info")
    edit_window.geometry("400x550")

    user_info = db.fetch_one("SELECT * FROM users WHERE user_id=%s", (user_id,))
    
    # Create entry fields for editing
    name_label = ctk.CTkLabel(edit_window, text="User Name",font=("Arial", 16))
    name_label.pack(pady=10)
    name_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=user_info[1])) 
    name_entry.pack(pady=10)
    
    gender_label = ctk.CTkLabel(edit_window, text="User Gender",font=("Arial", 16))
    gender_label.pack(pady=10)
    gender_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=user_info[2]))
    gender_entry.pack(pady=10)
    birthdate_label = ctk.CTkLabel(edit_window, text="User Birthdate",font=("Arial", 16))
    birthdate_label.pack(pady=10)
    birthdate_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=user_info[3]))
    birthdate_entry.pack(pady=10)
    country_label = ctk.CTkLabel(edit_window, text="User Country",font=("Arial", 16))
    country_label.pack(pady=10)
    country_entry = ctk.CTkEntry(edit_window, textvariable=tk.StringVar(value=user_info[4]))
    country_entry.pack(pady=10)
   
    def save_changes():
        new_name = name_entry.get()
        new_gender = gender_entry.get()
        new_birthdate = birthdate_entry.get()
        new_country = country_entry.get()
        
        db.excute_query("UPDATE users SET user_name=%s, gender=%s, birthday=%s, country=%s WHERE user_id=%s", 
                   (new_name, new_gender, new_birthdate, new_country, user_id))
        messagebox.showinfo("Edit User", "User information updated successfully!\n Please reopen the <person info> to see the changes.")
   

    save_button = ctk.CTkButton(edit_window, text="Save Changes", command=save_changes,font=("Arial", 16))
    save_button.pack(pady=20)
    
    button=ctk.CTkButton(edit_window, text="Close", font=("Arial",16),command=lambda: edit_window.destroy())
    button.pack(pady=10)

def edit_password(db, user_id, info_show):
    # Create the edit password window
    edit_window = tk.Toplevel(info_show)
    edit_window.title("Edit Password")
    edit_window.geometry("400x300")
    
    # Fetch the current user's password from the database
    info = db.fetch_one("SELECT * FROM users WHERE user_id=%s", (user_id,))
    current_password = info[5]  # Assuming the password is in the 6th column (index 5)
    
    # Create labels and entries for old and new password
    label = ctk.CTkLabel(edit_window, text="Old Password", font=("Arial", 16))
    label.pack(pady=20)
    old_entry = ctk.CTkEntry(edit_window, show="*")  # Mask the password input
    old_entry.pack()

    label1 = ctk.CTkLabel(edit_window, text="New Password", font=("Arial", 16))
    label1.pack(pady=20)
    new_entry = ctk.CTkEntry(edit_window, show="*")  # Mask the password input
    new_entry.pack()

    # Define the change password logic
    def change_password():
        old_password = old_entry.get()
        new_password = new_entry.get()
        
        if old_password != current_password:
            messagebox.showerror("Error", "Incorrect old password! Please try again.")
            return
        elif old_password == new_password:
            messagebox.showerror("Error", "New password cannot be the same as the current password! Please try again.")
            return
        elif not new_password:  # Check if the new password is empty
            messagebox.showerror("Error", "New password cannot be empty! Please try again.")
            return
        else:
            # Update the password in the database
            db.execute_query("UPDATE users SET password=%s WHERE user_id=%s", (new_password, user_id))
            messagebox.showinfo("Success", "Password changed successfully!")
            edit_window.destroy()  # Close the window after success

    button = ctk.CTkButton(edit_window, text="Change Password", command=change_password, font=("Arial", 16))
    button.pack(pady=5)
    
    button=ctk.CTkButton(edit_window, text="Close", font=("Arial",16),command=lambda: edit_window.destroy())
    button.pack(pady=5)
def My_order(db, user_id, info_show):
    # Create a new top-level window to show the orders
    orders_window = tk.Toplevel(info_show)
    orders_window.title("My Orders")
    orders_window.geometry("1000x400")  # Adjust window size as needed

    # SQL query to fetch all relevant order details
    query = """
    SELECT 
        orders.order_id, 
        orders.seat_id, 
        tickets.price, 
        dramas.drama_name, 
        dramas.duration, 
        schedules.start_time, 
        schedules.end_time, 
        theaters.theater_name, 
        theaters.address
    FROM 
        orders
    RIGHT JOIN tickets ON tickets.ticket_id = orders.ticket_id
    RIGHT JOIN performances ON performances.performance_id = tickets.performance_id
    RIGHT JOIN dramas ON dramas.drama_id = performances.drama_id
    RIGHT JOIN schedules ON schedules.performance_id = performances.performance_id
    RIGHT JOIN theaters ON theaters.theater_id = performances.theater_id
    WHERE 
        orders.user_id = %s
    """
    
    try:
        # Fetch the orders
        orders = db.fetch_all(query, (user_id,))
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching orders: {e}")
        return

    # If there are no orders, display a message and exit the function
    if not orders:
        messagebox.showinfo("No Orders", "Sorry! You don't have any orders yet.")
        return

    # Create a Treeview widget to display the order data
    treeview = ttk.Treeview(orders_window, columns=("order_id", "seat_id", "price", "drama_name", "duration", "start_time", "end_time", "theater_name", "address"), show="headings")

    # Define column headings
    treeview.heading("order_id", text="Order ID")
    treeview.heading("seat_id", text="Seat ID")
    treeview.heading("price", text="Price")
    treeview.heading("drama_name", text="Drama Name")
    treeview.heading("duration", text="Duration")
    treeview.heading("start_time", text="Start Time")
    treeview.heading("end_time", text="End Time")
    treeview.heading("theater_name", text="Theater")
    treeview.heading("address", text="Address")

    # Define column width
    treeview.column("order_id", width=30)
    treeview.column("seat_id", width=30)
    treeview.column("price", width=80)
    treeview.column("drama_name", width=100)
    treeview.column("duration", width=80)
    treeview.column("start_time", width=150)
    treeview.column("end_time", width=150)
    treeview.column("theater_name", width=150)
    treeview.column("address", width=200)

    vertical_scrollbar = ttk.Scrollbar(orders_window, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    horizontal_scrollbar = ttk.Scrollbar(orders_window, orient="horizontal", command=treeview.xview)
    treeview.configure(xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side="bottom", fill="x")

    treeview.pack(fill="both", expand=True)

    for row in treeview.get_children():
        treeview.delete(row)

    for order in orders:
        formatted_order = list(order)
        
        if formatted_order[5]:
            formatted_order[5] = formatted_order[5].strftime('%Y-%m-%d %H:%M:%S')  # Format start_time
        if formatted_order[6]:
            formatted_order[6] = formatted_order[6].strftime('%Y-%m-%d %H:%M:%S')  # Format end_time
        
        treeview.insert("", "end", values=formatted_order)
    
    button_frame = ctk.CTkFrame(orders_window)
    button_frame.pack(pady=10)

    close_button = ctk.CTkButton(button_frame, text="Close", command=orders_window.destroy)
    close_button.pack(pady=5,padx=20, side="right")

    delete_button = ctk.CTkButton(button_frame, text="Delete", command=lambda: delete_order(db, treeview))
    delete_button.pack(pady=5,padx=20, side="left")

def delete_order(db, treeview):
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an order to delete.")
        return

    # Get the order_id from the selected item
    order_id = treeview.item(selected_item)["values"][0]

    # Confirm deletion
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete order {order_id}?")
    if confirm:
        try:
            # Execute the deletion query
            delete_query = "DELETE FROM orders WHERE order_id = %s"
            db.execute_query(delete_query, (order_id,))
            treeview.delete(selected_item)
            messagebox.showinfo("Success", f"Order {order_id} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error deleting order: {e}")

            
if __name__ == "__main__":
    db = DatabaseManager()
    root = tk.Tk()
    pics=picture()
    pics1=picture1()
    pics2=picture2()
    home(root,pics,pics1,pics2,db)
    root.mainloop()