import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title('Expense Tracker')

        self.categories = []   # Initialize an empty list to store expense categories
        self.expenses = []     # Initialize an empty list to store expenses
        
        # Load categories from a JSON file
        self.load_categories()

        # Create category manager frame
        self.category_manager_frame = ttk.LabelFrame(root, text='Category Manager')
        self.category_manager_frame.grid(row=0, column=0, padx=18, pady=19)

        # Create category manager widgets
        self.category_label = ttk.Label(self.category_manager_frame, text='Category:')
        self.category_label.grid(row=0, column=0)

        self.category_entry = ttk.Entry(self.category_manager_frame)
        self.category_entry.grid(row=0, column=1)

        self.add_category_button = ttk.Button(self.category_manager_frame, text='Add Category', command=self.add_category)
        self.add_category_button.grid(row=0, column=2)

        self.category_listbox = tk.Listbox(self.category_manager_frame, height=10, width=25)
        self.category_listbox.grid(row=1, column=0, columnspan=3)
        self.update_category_list()

        # Create expense tracker frame
        self.expense_tracker_frame = ttk.LabelFrame(root, text='Expense Tracker')
        self.expense_tracker_frame.grid(row=0, column=1, padx=20, pady=20)

        # Create expense tracker widgets
        self.date_label = ttk.Label(self.expense_tracker_frame, text='Date:')
        self.date_label.grid(row=0, column=0)

        # Create Combobox for month
        self.month_var = tk.StringVar()
        self.month_combobox = ttk.Combobox(self.expense_tracker_frame, textvariable=self.month_var, values=[str(i) for i in range(1, 13)], width=3)
        self.month_combobox.grid(row=0, column=1, columnspan=1)

        # Create Combobox for day
        self.day_var = tk.StringVar()
        self.day_combobox = ttk.Combobox(self.expense_tracker_frame, textvariable=self.day_var, values=[str(i) for i in range(1, 32)], width=3, )
        self.day_combobox.grid(row=0, column=2, columnspan=1)

        # Create Combobox for year
        current_year = datetime.now().year
        self.year_var = tk.StringVar()
        self.year_combobox = ttk.Combobox(self.expense_tracker_frame, textvariable=self.year_var, values=[str(i) for i in range(current_year - 50, current_year + 6)], width=4)
        self.year_combobox.grid(row=0, column=3, columnspan=1)

        self.category_label = ttk.Label(self.expense_tracker_frame, text='Category:')
        self.category_label.grid(row=1, column=0)

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.expense_tracker_frame, textvariable=self.category_var, values=self.categories)
        self.category_dropdown.grid(row=1, column=1)

        self.amount_label = ttk.Label(self.expense_tracker_frame, text='Amount:')
        self.amount_label.grid(row=2, column=0)

        self.amount_entry = ttk.Entry(self.expense_tracker_frame)
        self.amount_entry.grid(row=2, column=1)

        self.add_expense_button = ttk.Button(self.expense_tracker_frame, text='Add Expense', command=self.add_expense)
        self.add_expense_button.grid(row=3, column=0, columnspan=2)

        self.expense_listbox = tk.Listbox(self.expense_tracker_frame, height=10, width=30)
        self.expense_listbox.grid(row=0, column=4, rowspan=4)

# Function to add a new category
    def add_category(self):
        category = self.category_entry.get()
        if category and category not in self.categories:
            self.categories.append(category)
            self.category_listbox.insert(tk.END, category)
            self.category_entry.delete(0, tk.END)
            self.save_categories()
            self.update_category_dropdown()

 # Function to add a new expense
    def add_expense(self):
        month = self.month_var.get()
        day = self.day_var.get()
        year = self.year_var.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()

        if month and day and year and category and amount:
            date = f"{month}/{day}/{year}"
            expense = {'date': date, 'category': category, 'amount': amount}
            self.expenses.append(expense)
            self.expense_listbox.insert(tk.END, f"{date} - {category} - {amount}")
            self.clear_expense_entries()
            self.save_expenses()

# Function to save expenses to a JSON file
    def save_expenses(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file)

    # Function to clear the expense entry fields
    def clear_expense_entries(self):
        self.month_var.set('')
        self.day_var.set('')
        self.year_var.set('')
        self.category_var.set('')
        self.amount_entry.delete(0, tk.END)

    # Function to load categories from a JSON file
    def load_categories(self):
        try:
            with open('categories.json', 'r') as file:
                self.categories = json.load(file)
        except FileNotFoundError:
            pass

   # Function to save categories to a JSON file
    def save_categories(self):
        with open('categories.json', 'w') as file:
            json.dump(self.categories, file)

    # Function to update the category list in the Category Manager
    def update_category_list(self):
        self.category_listbox.delete(0, tk.END)
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

 # Function to update the category dropdown in the Expense Tracker
    def update_category_dropdown(self):
        self.category_dropdown['values'] = self.categories

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()