# logic.py

import random

# Fungsi untuk preprocess input pelajar
def preprocess_question(question):
    return question.strip().lower()

# Fungsi dummy untuk jana jawapan AI
def generate_answer(question, style="Formal"):
    processed_q = preprocess_question(question)
    
    # Contoh jawapan berdasarkan gaya
    if style == "Santai":
        return f"Ok adik, senang je. Ini jawapannya: {random.choice(dummy_answers)}"
    elif style == "Tegas":
        return f"Jawapan: {random.choice(dummy_answers)}"
    elif style == "Formal":
        return f"Ini adalah jawapan kepada soalan anda: {random.choice(dummy_answers)}"
    else:
        return "Gaya jawapan tidak dikenali."

# Dummy dataset - nanti akan diganti dengan model AI sebenar
dummy_answers = [
    "Fotosintesis ialah proses tumbuhan hasilkan makanan guna cahaya matahari.",
    "Tenaga kinetik bergantung kepada jisim dan kelajuan objek.",
    "Sel ialah unit asas kehidupan dalam semua organisma."
]

# Fungsi simpan interaksi (optional untuk masa depan)
def save_interaction(question, answer, style, filepath="data/interaksi_log.csv"):
    import csv
    import os

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([question, answer, style])
