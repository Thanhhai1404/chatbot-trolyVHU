import pdfplumber
import sys

# Đảm bảo encoding UTF-8 cho output
sys.stdout.reconfigure(encoding='utf-8')

pdf = pdfplumber.open('Thong tin tuyen sinh VHU 1.pdf')

for i, page in enumerate(pdf.pages):
    print(f"{'='*60}")
    print(f"PAGE {i+1}")
    print(f"{'='*60}")
    print(page.extract_text())
    print("\n")

pdf.close()
