import fitz  # PDF reader
from memory import add_ca_book
import os
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
name=input("Enter the name of the pdf to convert with .pdf ")
# 🔹 Load your CA PDF
file_path = f"data/{name}.pdf"
if os.path.exists(file_path):
    pdf = fitz.open(file_path)
    print("PDF loaded successfully ✅")
else:
    print("File not found ❌")

for page_num, page in enumerate(pdf):
    text = page.get_text()

    chunks = chunk_text(text)

    for chunk in chunks:
        add_ca_book(
            chunk,
            source=f"income_tax_book_page_{page_num+1}"
        )

print("✅ CA book loaded")

### pdfs:- https://www.icai.org/post/intermediate-nset