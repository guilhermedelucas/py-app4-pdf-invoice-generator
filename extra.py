import os.path
import glob
from fpdf import FPDF
from pathlib import Path

TEXT_PATHS = 'texts'
if not os.path.exists(TEXT_PATHS):
    os.makedirs(TEXT_PATHS)

filepaths = glob.glob('texts/*txt')

pdf = FPDF(orientation='P', unit="mm", format="A4")

for filepath in filepaths:
    filename = Path(filepath).stem
    title = filename.title()

    with open(filepath, 'r') as file:
        content = file.read()

    pdf.add_page()
    pdf.set_font(family="Times", size=16, style="B")
    pdf.cell(w=15, h=10, txt=title, ln=True)
    pdf.set_font(family="Times", size=10, style="B")
    pdf.multi_cell(w=180, h=6, txt=content)

pdf.output(f"{TEXT_PATHS}/animals.pdf")