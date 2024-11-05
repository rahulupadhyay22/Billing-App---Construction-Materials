# Billing App - Construction Materials

Welcome to the **Billing App - Construction Materials**! This Python application allows users to generate bills for construction materials efficiently. It features a user-friendly graphical interface and integrates PDF generation, database storage, and QR code payment options.

## Features

- **User-Friendly GUI**: Built using Tkinter for an interactive experience.
- **PDF Generation**: Generate clean and professional PDF bills with customer and item details.
- **Database Storage**: Save bill details in an SQLite database for record-keeping.
- **QR Code Integration**: Includes a QR code for online payment using UPI.
- **Invoice Management**: Organizes invoices by month for easy retrieval.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Required Python libraries:
  - `fpdf`
  - `qrcode`
  - `tkinter` (comes with Python standard library)
  - `sqlite3` (comes with Python standard library)

You can install the required libraries using pip:

```bash
pip install fpdf qrcode[pil]
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/billing-app.git
   cd billing-app
   ```

2. **Run the application**:

   ```bash
   python billing_app.py
   ```

## Usage

1. **Input Customer Details**: Enter the customer's name, address, and phone number.
2. **Add Items**: Fill in the item name, price, quantity, unit (kg/tons), and any weighting rate. Click the "Add Item" button to include it in the bill.
3. **Generate Bill**: Once all items are added, click the "Generate Bill" button to create the PDF invoice and save the data to the database. You will be prompted to open the generated PDF.
4. **Payment Details**: A QR code will be included in the PDF for easy online payments via UPI.

## Database Structure

The application uses an SQLite database to store the bill records. The database includes the following fields:

| Field Name      | Data Type      |
|------------------|----------------|
| id               | INTEGER        |
| name             | TEXT           |
| address          | TEXT           |
| phone            | TEXT           |
| item_name        | TEXT           |
| item_price       | REAL           |
| quantity         | REAL           |
| unit             | TEXT           |
| weighting_rate   | REAL           |
| total_amount     | REAL           |
| date             | TEXT           |

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **FPDF** for PDF generation
- **qrcode** for QR code generation
- **SQLite** for database management
- **Tkinter** for creating the GUI

---

Thank you for using the **Billing App - Construction Materials**! If you have any questions or feedback, feel free to reach out.
