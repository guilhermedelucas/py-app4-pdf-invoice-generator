import os.path
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

PDF_PATH = 'pdfs'
if not os.path.exists(PDF_PATH):
    os.makedirs(PDF_PATH)

LINE_HEIGHT = 10
CELL_HEIGHT = 7

filepaths = glob.glob('invoices/*xlsx')


def get_cell_with(column_name):
    if column_name == 'product_name':
        return 60
    elif column_name == 'price_per_unit' or column_name == 'total_price':
        return 30
    return 35


for filepath in filepaths:
    pdf = FPDF(orientation='P', unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font(family="Times", size=16, style="B")

    filename = Path(filepath).stem
    invoice_nr, date = filename.split('-')
    pdf.cell(w=15, h=LINE_HEIGHT, txt=f"Invoice nr, {invoice_nr}")
    pdf.ln(8)
    # pdf.set_font(family="Times", size=14, style="B")
    pdf.cell(w=15, h=LINE_HEIGHT, txt=f"Date {date}", ln=True)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    total_sum = df['total_price'].sum()
    columns = df.columns

    # Generate the table header
    pdf.set_font(family="Times", size=10, style="B")
    for column in columns:
        cell_width = get_cell_with(column)
        column_title = str(column).replace('_', ' ').title()
        pdf.cell(w=cell_width, h=CELL_HEIGHT, txt=str(column).replace('_', ' ').title(), border=1)

    pdf.ln(CELL_HEIGHT)
    pdf.set_font(family="Times", size=10, style="")

    for index, row in df.iterrows():  # iterate rows
        for column in columns:  # loop all the columns of the row (df.columns only return the column name)
            cell_value = row[column]
            cell_width = get_cell_with(column)
            pdf.cell(w=cell_width, h=CELL_HEIGHT, txt=str(cell_value), border=1)
        # Move to the next line after each row
        pdf.ln(CELL_HEIGHT)

    # Generate the last row, to display the total on the last column
    for column in columns:
        cell_width = get_cell_with(column)
        if column == 'total_price':
            pdf.cell(w=cell_width, h=CELL_HEIGHT, txt=str(total_sum), border=1)
        else:
            pdf.cell(w=cell_width, h=CELL_HEIGHT, txt="", border=1)

    pdf.ln(LINE_HEIGHT)
    pdf.ln(LINE_HEIGHT)

    # Add total sum sentence
    pdf.set_font(family="Times", size=12, style="B")
    pdf.cell(w=15, h=LINE_HEIGHT, txt=f"The total due amount is {total_sum} Euros.", ln=True)
    # Add company name and logo
    pdf.cell(w=48, h=LINE_HEIGHT, txt="Show me the money INC.")
    pdf.image('pythonhow.png', w=10)

    pdf.output(f"{PDF_PATH}/{filename}.pdf")