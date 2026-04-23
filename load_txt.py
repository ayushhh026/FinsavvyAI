from memory import add_txt_knowledge

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

file_path = "data/data_ingestion2.txt"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text)

for chunk in chunks:
    add_txt_knowledge(
        chunk,
        source="custom_notes"
    )
print("ADDING:", chunk[:80])
print("✅ TXT knowledge loaded")
