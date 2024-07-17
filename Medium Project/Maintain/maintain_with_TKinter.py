import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import os
import csv

class CSV:
    csv_File = os.path.join(os.path.dirname(__file__), "data.csv")
    col = ["date", "amount", "catagory", "description"]

    @classmethod
    def init_csv(cls):
        try:
            pd.read_csv(cls.csv_File)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.col)
            df.to_csv(cls.csv_File, index=False)

    @classmethod
    def add_items(cls, date, amount, catagory, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "catagory": catagory,
            "description": description,
        }
        with open(cls.csv_File, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.col)
            writer.writerow(new_entry)
        messagebox.showinfo("Success", "Successfully added!")

    @classmethod
    def history(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_File)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        between_start_and_end = (df["date"] >= start_date) & (df["date"] <= end_date)
        filter_df = df.loc[between_start_and_end]

        if filter_df.empty:
            return "No Transaction Found"
        else:
            details = f"Transaction start {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:\n"
            details += filter_df.to_string(index=False, formatters={"date": lambda x: x.strftime("%d-%m-%Y")}) + "\n"
            total_save = filter_df[filter_df["catagory"] == "Deposit"]["amount"].sum()
            total_cost = filter_df[filter_df["catagory"] == "Cost"]["amount"].sum()
            details += "\nShort Details:\n"
            details += f"Total Deposit: {total_save:.2f}\n"
            details += f"Total Cost: {total_cost:.2f}\n"
            details += f"Present Amount: {total_save - total_cost:.2f}\n"
            return details


catagorys = {
    "D": "Deposit", "C": "Cost"
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Manager")
        self.geometry("600x400")
        
        self.initUI()
        CSV.init_csv()

    def initUI(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill="both")
        
        self.tab_add = ttk.Frame(self.tabs)
        self.tab_history = ttk.Frame(self.tabs)
        
        self.tabs.add(self.tab_add, text="Add Entry")
        self.tabs.add(self.tab_history, text="View History")
        
        self.create_add_tab()
        self.create_history_tab()

    def create_add_tab(self):
        tk.Label(self.tab_add, text="Date (dd-mm-yyyy)").grid(row=0, column=0, padx=10, pady=10)
        self.entry_date = tk.Entry(self.tab_add)
        self.entry_date.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.tab_add, text="Amount").grid(row=1, column=0, padx=10, pady=10)
        self.entry_amount = tk.Entry(self.tab_add)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.tab_add, text="Category (D for Deposit, C for Cost)").grid(row=2, column=0, padx=10, pady=10)
        self.entry_category = tk.Entry(self.tab_add)
        self.entry_category.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.tab_add, text="Description").grid(row=3, column=0, padx=10, pady=10)
        self.entry_description = tk.Entry(self.tab_add)
        self.entry_description.grid(row=3, column=1, padx=10, pady=10)
        
        self.add_button = ttk.Button(self.tab_add, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)

    def add_entry(self):
        date = self.entry_date.get() or datetime.today().strftime("%d-%m-%Y")
        amount = self.entry_amount.get()
        category = self.entry_category.get().upper()
        description = self.entry_description.get()
        
        if category not in catagorys:
            messagebox.showerror("Error", "Invalid category")
            return
        
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount cannot be less than zero")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        CSV.add_items(date, amount, catagorys[category], description)
        self.entry_date.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)

    def create_history_tab(self):
        tk.Label(self.tab_history, text="Start Date (dd-mm-yyyy)").grid(row=0, column=0, padx=10, pady=10)
        self.entry_start_date = tk.Entry(self.tab_history)
        self.entry_start_date.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.tab_history, text="End Date (dd-mm-yyyy)").grid(row=1, column=0, padx=10, pady=10)
        self.entry_end_date = tk.Entry(self.tab_history)
        self.entry_end_date.grid(row=1, column=1, padx=10, pady=10)
        
        self.view_button = ttk.Button(self.tab_history, text="View History", command=self.view_history)
        self.view_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.history_text = tk.Text(self.tab_history, wrap="word")
        self.history_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.tab_history.rowconfigure(3, weight=1)
        self.tab_history.columnconfigure(1, weight=1)

    def view_history(self):
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        
        if not start_date or not end_date:
            messagebox.showerror("Error", "Please enter both start and end dates")
            return
        
        history = CSV.history(start_date, end_date)
        self.history_text.delete("1.0", tk.END)
        self.history_text.insert(tk.END, history)

if __name__ == "__main__":
    app = App()
    app.mainloop()
