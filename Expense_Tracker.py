import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests  # type: ignore
import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        
        self.api_key = "eadf595a1a8743259daec12b7467b8e8"  
        self.api_url = f"https://openexchangerates.org/api/latest.json?"


        
        self.setup_ui()

        
        self.total_usd = 0.0

    def setup_ui(self):
        self.amount_label = ttk.Label(self.root, text="Amount")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        self.currency_label = ttk.Label(self.root, text="Currency")
        self.currency_label.grid(row=1, column=0)
        self.currency_combobox = ttk.Combobox(self.root, values=["USD", "EUR", "GBP", "JPY"])
        self.currency_combobox.grid(row=1, column=1)
        self.currency_combobox.current(0)

        self.category_label = ttk.Label(self.root, text="Category")
        self.category_label.grid(row=2, column=0)
        self.category_combobox = ttk.Combobox(self.root, values=["Rent", "Groceries", "Savings", "Entertainment", "Other"])
        self.category_combobox.grid(row=2, column=1)
        self.category_combobox.current(0)

        self.payment_label = ttk.Label(self.root, text="Payment Method")
        self.payment_label.grid(row=3, column=0)
        self.payment_combobox = ttk.Combobox(self.root, values=["Credit Card", "Debit Card", "Paypal", "Cash"])
        self.payment_combobox.grid(row=3, column=1)
        self.payment_combobox.current(0)

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

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return
        
        currency = self.currency_combobox.get()
        category = self.category_combobox.get()
        payment_method = self.payment_combobox.get()
        date = self.date_entry.get()

        
        converted_amount = self.convert_to_usd(amount, currency)

        if converted_amount is None:
            return

        
        self.tree.insert("", "end", values=(amount, currency, category, payment_method))

        
        self.total_usd += converted_amount
        self.total_label.config(text=f"Total in USD: {self.total_usd:.2f}")

    def convert_to_usd(self, amount, currency):
        if currency == "USD":
            return amount
        try:
            response = requests.get(f"{self.api_url}app_id={self.api_key}")
            response.raise_for_status() 
            data = response.json()
            
            if 'rates' not in data or currency not in data['rates']:
                messagebox.showerror("Error", f"Currency {currency} not found in the API response.")
                return None

            exchange_rate = data["rates"][currency]
            usd_rate = data["rates"]["USD"]
            converted_amount = amount / exchange_rate * usd_rate
            return converted_amount
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
