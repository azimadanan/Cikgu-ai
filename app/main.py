# app/main.py

import streamlit as st
import datetime
import os
import csv
import pdfplumber
import docx

from logic import load_dataset, cari_jawapan

# ---------- CONFIG ----------
st.set_page_config(page_title="Cikgu-ai", layout="centered")
st.title("📘 Cikgu-ai")
st.subheader("AI Pendidikan Gaya Guru Malaysia 🇲🇾")

# ---------- PILIH GAYA GURU ----------
style = st.selectbox("Pilih gaya jawapan guru:", ("Santai", "Tegas", "Formal"))

# ---------- FUNGSI BACA FAIL ----------
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = ""
    return text.strip()

# ---------- FUNGSI SIMPAN LOG ----------
def simpan_log(soalan, gaya, jawapan):
    os.makedirs("data/logs", exist_ok=True)
    with open("data/logs/interactions.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), soalan, gaya, jawapan])

# ---------- INPUT SOALAN ----------
question = st.text_input("Soalan anda:", placeholder="Contoh: Apakah itu elektromagnet?")
uploaded_file = st.file_uploader("Atau muat naik fail (PDF/Word):", type=["pdf", "docx"])

# ---------- LOAD DATASET SEKALI ----------
df_dataset = load_dataset()

# ---------- BUTANG HANTAR ----------
if st.button("📝 Hantar"):
    final_question = question.strip()

    if uploaded_file:
        final_question = extract_text_from_file(uploaded_file)
        st.info("Soalan daripada fail berjaya dibaca.")

    if not final_question:
        st.warning("Sila taip soalan atau muat naik fail.")
    else:
        answer = cari_jawapan(final_question, style, df_dataset)
        st.success(answer)
        simpan_log(final_question, style, answer)



