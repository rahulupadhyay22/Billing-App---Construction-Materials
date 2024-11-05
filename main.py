import sqlite3
from fpdf import FPDF
import os
import datetime
import tkinter as tk
from tkinter import messagebox
import webbrowser
import qrcode

class PDF(FPDF):
    """Custom PDF class inheriting from FPDF."""
    pass

# Database setup
conn = sqlite3.connect('python projects/billingapp/billing_app.db')
cursor = conn.cursor()

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

def generate_pdf_bill(customer_data, items):
    """Generate a simple and clean PDF bill."""
    pdf = PDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 25)
    pdf.cell(0, 10, "Shree Guru Construction Materials", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", 0, 1, "R")
    pdf.set_draw_color(0, 0, 0)  # Set the color for the line (black)
    pdf.set_line_width(0.5)  # Set the line width
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw the line from left to right margin
    pdf.ln(10)

    # Customer Details in Table Format
    pdf.set_font("Arial", "I", 18)
    pdf.cell(0, 10, "Customer Details:", 0, 1)
    pdf.set_font("Arial", "B", 12)

    # Define column widths
    col_widths = [40, 150]

    # Define customer details
    customer_details = [
        ("Name:", customer_data['name']),
        ("Address:", customer_data['address']),
        ("Phone:", customer_data['phone'])
    ]

    # Draw the table
    for label, value in customer_details:
        pdf.cell(col_widths[0], 10, label, 1)
        pdf.cell(col_widths[1], 10, value, 1, 1)
    pdf.ln(10)
    
    pdf.set_font("Arial", "I", 18)
    pdf.cell(0, 10, "Item's Details:", 0, 1)
    pdf.set_font("Arial", "", 12)

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
    pdf.set_draw_color(0, 0, 0)  # Set the color for the line (black)
    pdf.set_line_width(0.5)  # Set the line width
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw the line from left to right margin
    pdf.ln(5)
    
    # QR Code and UPI ID Section
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Online Payment Details:", 0, 1)

    # UPI ID
    upi_id = "6300927946@pthdfc"
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"UPI ID: {upi_id}", 0, 1)
    
    # Generate QR Code
    qr_data = f"upi://pay?pa={upi_id}&pn=Shree%20Guru%20Construction%20Materials&cu=INR"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    
    # Save QR Code as an image file
    qr_img_path = "qr_code.png"
    qr_img.save(qr_img_path)
    
    # Insert QR Code into PDF
    pdf.image(qr_img_path, x=pdf.get_x(), y=pdf.get_y(), w=50)
    
    # Remove the QR Code image file after inserting into PDF
    os.remove(qr_img_path)
    
    
    # Footer Note
    pdf.ln(60)  # Adjust the space as needed to fit the QR code
    pdf.set_font("Arial", "B", 15)
    pdf.cell(0, 10, "Thank you for your business!", 0, 1, "C")
    pdf.set_draw_color(0, 0, 0)  # Set the color for the line (black)
    pdf.set_line_width(0.5)  # Set the line width
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Draw the line from left to right margin
    pdf.ln(5)
    
    # Create invoice directory if it doesn't exist
    invoice_dir = "python projects/billingapp/invoices"
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)

    # Create month-based directory
    month_dir = os.path.join(invoice_dir, datetime.datetime.now().strftime('%Y-%m'))
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)

    # Save the PDF in the month-based directory
    pdf_name = os.path.join(month_dir, f"Invoice_{customer_data['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
    pdf.output(pdf_name)
    return pdf_name

def save_to_database(customer_data, items):
    """Save bill details to the database."""
    for item in items:
        cursor.execute('''
            INSERT INTO bills (name, address, phone, item_name, item_price, quantity, unit, weighting_rate, total_amount, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer_data['name'], customer_data['address'], customer_data['phone'],
              item['item_name'], item['item_price'], item['quantity'], item['unit'],
              item['weighting_rate'], (item['item_price'] * item['quantity']) + item['weighting_rate'],
              datetime.datetime.now().strftime('%Y-%m-%d')))
    conn.commit()

def add_item():
    """Add item details to the list."""
    item_name = entry_item_name.get()
    item_price = float(entry_item_price.get())
    quantity = float(entry_quantity.get())
    unit = entry_unit.get()
    weighting_rate = float(entry_weighting_rate.get())

    item = {
        'item_name': item_name,
        'item_price': item_price,
        'quantity': quantity,
        'unit': unit,
        'weighting_rate': weighting_rate
    }
    
    items.append(item)
    update_item_list()
    
    # Clear entry fields
    entry_item_name.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_unit.delete(0, tk.END)
    entry_weighting_rate.delete(0, tk.END)

def update_item_list():
    """Update the displayed item list."""
    item_list.delete(0, tk.END)  # Clear current list
    total_amount = 0
    for item in items:
        item_list.insert(tk.END, f"{item['item_name']} - {item['quantity']} {item['unit']} @ {item['item_price']} INR")
        total_amount += (item['item_price'] * item['quantity']) + item['weighting_rate']
    total_label.config(text=f"Total Amount: {total_amount:.2f} INR")

def submit_bill():
    """Handle submission of bill data."""
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()

    customer_data = {
        'name': name,
        'address': address,
        'phone': phone
    }

    if not items:
        messagebox.showwarning("No Items", "Please add at least one item before generating the bill.")
        return

    pdf_name = generate_pdf_bill(customer_data, items)
    save_to_database(customer_data, items)

    # Ask user if they want to open the generated PDF
    if messagebox.askyesno("PDF Generated", "The bill has been generated. Do you want to open it?"):
        webbrowser.open(pdf_name)

# Tkinter GUI Setup
app = tk.Tk()
app.title("Billing App - Construction Materials")
app.geometry("500x600")

# Customer Details 
tk.Label(app, text="Customer Name").pack()
entry_name = tk.Entry(app)
entry_name.pack()

tk.Label(app, text="Address").pack()
entry_address = tk.Entry(app)
entry_address.pack()

tk.Label(app, text="Phone").pack()
entry_phone = tk.Entry(app)
entry_phone.pack()

# Item Details
tk.Label(app, text="Item Name").pack()
entry_item_name = tk.Entry(app)
entry_item_name.pack()

tk.Label(app, text="Item Price (INR)").pack()
entry_item_price = tk.Entry(app)
entry_item_price.pack()

tk.Label(app, text="Quantity").pack()
entry_quantity = tk.Entry(app)
entry_quantity.pack()

tk.Label(app, text="Unit (kg/tons)").pack()
entry_unit = tk.Entry(app)
entry_unit.pack()

tk.Label(app, text="Weighting Rate (INR)").pack()
entry_weighting_rate = tk.Entry(app)
entry_weighting_rate.pack()

# Add Item Button
tk.Button(app, text="Add Item", command=add_item).pack()

# List of Added Items
items = []
item_list = tk.Listbox(app, width=70, height=10)
item_list.pack()

total_label = tk.Label(app, text="Total Amount: 0.00 INR")
total_label.pack()

# Submit Button
tk.Button(app, text="Generate Bill", command=submit_bill).pack()

app.mainloop()

