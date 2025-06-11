# logic.py

import random
import pandas as pd
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

    import pandas as pd

def load_dataset():
    return pd.read_csv("dataset/processed_prompts.csv")

def cari_jawapan(soalan, gaya, df):
    result = df[(df['soalan'].str.lower() == soalan.lower()) & (df['gaya'].str.lower() == gaya.lower())]
    if not result.empty:
        return result.iloc[0]['jawapan']
    else:
        return "Maaf, cikgu-ai belum ada jawapan untuk soalan itu lagi. Cuba tanya soalan lain 😊"

from rapidfuzz import process

def cari_soalan_terdekat(soalan_input, df):
    soalan_list = df['soalan'].tolist()
    match, score, index = process.extractOne(soalan_input, soalan_list)
    if score > 70:
        row = df.iloc[index]
        return row['jawapan']
    else:
        return "Maaf, saya tidak dapat jumpa jawapan yang hampir dengan soalan tersebut."

