import tkinter as tk
from tkinter import messagebox
import sqlite3

class BMI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BMI Calculator")

        # Creating labels and entry fields for age, height, and weight
        self.label_age = tk.Label(self.root, text="Age:")
        self.label_age.pack()
        self.entry_age = tk.Entry(self.root)
        self.entry_age.pack()

        self.label_height = tk.Label(self.root, text="Height (cm):")
        self.label_height.pack()
        self.entry_height = tk.Entry(self.root)
        self.entry_height.pack()

        self.label_weight = tk.Label(self.root, text="Weight (kg):")
        self.label_weight.pack()
        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.pack()

        self.button_calculate = tk.Button(self.root, text="Calculate", command=self.calculate_bmi)
        self.button_calculate.pack()

        self.button_show_history = tk.Button(self.root, text="Show History", command=self.show_history)
        self.button_show_history.pack()

        # Connect to the SQLite database
        self.conn = sqlite3.connect("bmi_history.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create a table for BMI history if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                height INTEGER,
                weight INTEGER,
                bmi REAL
            )
        ''')
        self.conn.commit()

    def calculate_bmi(self):
        try:
            age = int(self.entry_age.get())
            height = int(self.entry_height.get())
            weight = int(self.entry_weight.get())

            # Calculate BMI
            height_in_meters = height / 100
            bmi = weight / (height_in_meters ** 2)

            # Display BMI category
            self.display_bmi_category(bmi)

            # Save data to the database
            self.save_to_database(age, height, weight, bmi)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for age, height, and weight.")

    def display_bmi_category(self, bmi):
        if bmi <= 16:
            category = "Severe Thinness"
        elif 16 < bmi <= 17:
            category = "Mild Thinness"
        elif 17 < bmi <= 18.5:
            category = "Moderate Thinness"
        elif 18.5 < bmi <= 25:
            category = "Normal"
        elif 25 < bmi <= 30:
            category = "Overweight"
        elif 30 <= bmi <= 35:
            category = "Obese Class I"
        elif 35 <= bmi <= 40:
            category = "Obese Class II"
        else:
            category = "Obese Class III"

        messagebox.showinfo("BMI Category", category)

    def save_to_database(self, age, height, weight, bmi):
        # Save data to the database
        self.cursor.execute("INSERT INTO bmi_data (age, height, weight, bmi) VALUES (?, ?, ?, ?)", (age, height, weight, bmi))
        self.conn.commit()

    def show_history(self):
        # Fetch data from the database
        self.cursor.execute("SELECT age, height, weight, bmi FROM bmi_data")
        data = self.cursor.fetchall()

        # Display past BMI entries in a new window
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")

        for entry in data:
            entry_text = f"Age: {entry[0]}, Height: {entry[1]} cm, Weight: {entry[2]} kg, BMI: {entry[3]:.2f}"
            tk.Label(history_window, text=entry_text).pack()

    def run(self):
        self.root.mainloop()

    def __del__(self):
        # Close the database connection when the instance is deleted
        self.conn.close()

if __name__ == "__main__":
    game = BMI()
    game.run()
