import os
from PyPDF2 import PdfReader

dataset_folder = "./dataset"
pdf_files = [f for f in os.listdir(dataset_folder) if f.lower().endswith(".pdf")]

scan_count = 0
text_count = 0

for i, pdf_file in enumerate(pdf_files):
    if i % 10 == 0:
        print(f"Processing {i+1}/{len(pdf_files)}: {pdf_file}")
    pdf_path = os.path.join(dataset_folder, pdf_file)
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        if text.strip():
            text_count += 1
        else:
            scan_count += 1
    except Exception as e:
        print(f"Error reading {pdf_file}: {e}")
        scan_count += 1

print(f"Tổng số file PDF: {len(pdf_files)}")
print(f"Số file PDF text: {text_count}")
print(f"Số file PDF scan: {scan_count}")