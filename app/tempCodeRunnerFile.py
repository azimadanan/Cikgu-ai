# app/main.py

import streamlit as st
import datetime
import os
import csv
import pdfplumber
import docx

# ---------- CONFIG & HEADER ----------
st.set_page_config(page_title="Cikgu-ai", layout="centered")
st.title("📘 Cikgu-ai")
st.subheader("AI Pendidikan Gaya Guru Malaysia 🇲🇾")

# ---------- PILIH GAYA GURU ----------
style = st.selectbox(
    "Pilih gaya jawapan guru:",
    ("Santai", "Tegas", "Formal")
)

# ---------- INPUT SOALAN ----------
question = st.text_input("Soalan anda:", placeholder="Contoh: Apakah itu fotosintesis?")

# ---------- FUNGSI JAWAPAN (SIMULASI) ----------
def generate_dummy_answer(q, style):
    if style == "Santai":
        return f"Ok adik, senang je. Fotosintesis tu proses tumbuhan buat makanan guna cahaya matahari. 🌞"
    elif style == "Tegas":
        return f"Jawapan: Fotosintesis ialah proses sintesis makanan dalam tumbuhan melalui cahaya matahari. Ini asas penting."
    else:  # Formal
        return f"Fotosintesis merupakan satu proses di mana tumbuhan hijau menghasilkan makanan menggunakan cahaya matahari, air dan karbon dioksida."

# ---------- FUNGSI LOG INTERAKSI ----------
def log_interaction(question, answer):
    os.makedirs("data/logs", exist_ok=True)
    with open("data/logs/interactions.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        timestamp = datetime.datetime.now().isoformat()
        writer.writerow([timestamp, question, answer])

# ---------- BUTANG HANTAR ----------
if st.button("📝 Hantar"):
    if not question.strip() and not uploaded_file:
        st.warning("Sila taip soalan atau muat naik fail.")
    else:
        final_question = question
        if uploaded_file:
            final_question = extract_text_from_file(uploaded_file)
            st.info("Soalan daripada fail berjaya dibaca.")

        answer = generate_dummy_answer(final_question, style)
        st.success(answer)
        log_interaction(final_question, answer, style)
