import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests # type: ignore
import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # API Key and Base URL
        self.api_key = "eadf595a1a8743259daec12b7467b8e8"
        self.api_url = f"https://openexchangerates.org/api/latest.json?app_id={self.api_key}"

        # Initialize the total amount in USD
        self.total_usd = 0.0

        # Set up the UI components
        self.setup_ui()

    def setup_ui(self):
        self.create_label_and_entry("Amount", 0)
        self.create_label_and_combobox("Currency", 1, ["USD", "EUR", "GBP", "JPY"])
        self.create_label_and_combobox("Category", 2, ["Rent", "Groceries", "Savings", "Entertainment", "Other"])
        self.create_label_and_combobox("Payment Method", 3, ["Credit Card", "Debit Card", "Paypal", "Cash"])

        self.date_label = ttk.Label(self.root, text="Date")
        self.date_label.grid(row=4, column=0)
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=4, column=1)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, column=0, columnspan=2)

        self.tree = ttk.Treeview(self.root, columns=("Amount", "Currency", "Category", "Payment Method"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Currency", text="Currency")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Payment Method", text="Payment Method")
        self.tree.grid(row=6, column=0, columnspan=2)

        self.total_label = ttk.Label(self.root, text="Total in USD: 0.00", foreground="yellow", background="black")
        self.total_label.grid(row=7, column=0, columnspan=2)

    def create_label_and_entry(self, text, row):
        label = ttk.Label(self.root, text=text)
        label.grid(row=row, column=0)
        entry = ttk.Entry(self.root)
        entry.grid(row=row, column=1)
        setattr(self, f"{text.lower()}_entry", entry)

    def create_label_and_combobox(self, text, row, values):
        label = ttk.Label(self.root, text=text)
        label.grid(row=row, column=0)
        combobox = ttk.Combobox(self.root, values=values)
        combobox.grid(row=row, column=1)
        combobox.current(0)
        setattr(self, f"{text.lower().replace(' ', '_')}_combobox", combobox)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        currency = self.currency_combobox.get()
        category = self.category_combobox.get()
        payment_method = self.payment_method_combobox.get()
        date = self.date_entry.get()

        # Convert the amount to USD
        converted_amount = self.convert_to_usd(amount, currency)
        if converted_amount is None:
            return

        # Add the expense to the treeview
        self.tree.insert("", "end", values=(amount, currency, category, payment_method))

        # Update the total in USD
        self.total_usd += converted_amount
        self.total_label.config(text=f"Total in USD: {self.total_usd:.2f}")

    def convert_to_usd(self, amount, currency):
        if currency == "USD":
            return amount
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            exchange_rate = data["rates"].get(currency)
            if exchange_rate is None:
                messagebox.showerror("Error", f"Currency {currency} not found in the API response.")
                return None
            return amount / exchange_rate
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch exchange rate: {e}")
            return None
        except ValueError:
            messagebox.showerror("Error", "Invalid response format from API.")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
