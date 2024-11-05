import sqlite3
from fpdf import FPDF
import os
import datetime

# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('billing_app.db')
cursor = conn.cursor()

# Create a table to store bill details if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone TEXT,
    item_name TEXT,
    item_price REAL,
    quantity REAL,
    unit TEXT,
    weighting_rate REAL,
    total_amount REAL,
    date TEXT
)
''')
conn.commit()

# Create a table to store customer details if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    address TEXT,
    phone TEXT
)
''')
conn.commit()

def save_customer_details(name, address, phone):
    """Save customer details to the database"""
    cursor.execute('''
        INSERT OR IGNORE INTO customers (name, address, phone)
        VALUES (?, ?, ?)
    ''', (name, address, phone))
    conn.commit()

def get_customer_details(name):
    """Retrieve customer details from the database"""
    cursor.execute('''
        SELECT address, phone FROM customers WHERE name = ?
    ''', (name,))
    return cursor.fetchone()

class PDF(FPDF):
    def header(self):
        """Header with Business Name and Date"""
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Business Name: Shree Guru Construction Materials", 0, 1, "C")
        self.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "C")
        self.ln(10)

    def footer(self):
        """Footer with page number"""
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf_bill(customer_data, items):
    """Generate a simple and clean PDF bill."""
    pdf = PDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "XYZ Construction Materials", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "R")
    pdf.ln(10)

    # Customer Details
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Customer Details", 0, 1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Name: {customer_data['name']}", 0, 1)
    pdf.cell(0, 10, f"Address: {customer_data['address']}", 0, 1)
    pdf.cell(0, 10, f"Phone: {customer_data['phone']}", 0, 1)
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Item", 1)
    pdf.cell(30, 10, "Price (INR)", 1)
    pdf.cell(30, 10, "Quantity", 1)
    pdf.cell(30, 10, "Unit", 1)
    pdf.cell(40, 10, "Total (INR)", 1, 1)

    # Table Content
    pdf.set_font("Arial", "", 12)
    total_amount = 0
    for item in items:
        item_total = (item['item_price'] * item['quantity'])
        pdf.cell(50, 10, item['item_name'], 1)
        pdf.cell(30, 10, f"{item['item_price']:.2f}", 1)
        pdf.cell(30, 10, f"{item['quantity']:.2f}", 1)
        pdf.cell(30, 10, item['unit'], 1)
        pdf.cell(40, 10, f"{item_total:.2f}", 1, 1)
        total_amount += item_total

    # Total Amount Section
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total Amount: {total_amount:.2f} INR", 0, 1, "R")

    # Footer Note
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "Thank you for your business!", 0, 1, "C")

    # Save the PDF
    pdf_name = f"Invoice_{customer_data['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(pdf_name)
    return pdf_name


def save_to_database(data):
    """Save bill details to the database"""
    cursor.execute('''
        INSERT INTO bills (name, address, phone, item_name, item_price, quantity, unit, weighting_rate, total_amount, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['address'], data['phone'], data['item_name'], data['item_price'], 
          data['quantity'], data['unit'], data['weighting_rate'], data['total_amount'], 
          datetime.datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    print("Bill saved to database.")

def get_user_input():
    """Collect user input for the bill"""
    name = input("Enter Customer Name: ")
    address = input("Enter Address: ")
    phone = input("Enter Phone Number: ")
    item_name = input("Enter Item Name: ")
    item_price = float(input("Enter Item Price (INR): "))
    quantity = float(input("Enter Quantity (e.g., 1.5, 2.0): "))
    unit = input("Enter Unit (tons/kg): ")
    weighting_rate = float(input("Enter Weighting Rate (INR): "))

    total_amount = (item_price * quantity) + weighting_rate

    # Prepare data dictionary
    data = {
        'name': name,
        'address': address,
        'phone': phone,
        'item_name': item_name,
        'item_price': item_price,
        'quantity': quantity,
        'unit': unit,
        'weighting_rate': weighting_rate,
        'total_amount': total_amount
    }
    return data

def main():
    while True:
        print("\n--- Billing App for Construction Materials ---")
        print("1. Generate New Bill")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            bill_data = get_user_input()
            generate_pdf_bill(bill_data)
            save_to_database(bill_data)
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
