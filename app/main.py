# app/main.py

import streamlit as st
import datetime, csv, os
import pdfplumber
import docx
import pandas as pd

from logic import load_dataset, cari_jawapan
from logic import extract_text_from_file, flag_last_interaction, get_weakness_report

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

# ─── LOG INTERAKSI (UC01 + UC04) ──────────────────────────────────────────────
def log_interaction(question, concept, style, answer,
                    is_correct=True, is_flagged=False,
                    log_path="data/logs/interactions.csv"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().isoformat(),
            question,
            concept,
            style,            
            answer,
            is_correct,
            is_flagged
        ])

# ─── TAB: Chat vs Dashboard ─────────────────────────────────────────────────
tab_chat, tab_guru = st.tabs(["💬 Chat", "📊 Laporan Guru"])

with tab_chat:
    question = st.text_input("Soalan anda:", placeholder="Contoh: Apakah itu elektromagnet?")
    uploaded_file = st.file_uploader("Atau muat naik fail (PDF/Word):", type=["pdf", "docx"])

# ---------- LOAD DATASET SEKALI ----------
df_dataset = load_dataset()

# ---------- BUTANG HANTAR ----------
    if st.button("📝 Hantar"):  # UC01 + UC02
        final = question.strip()
        if uploaded_file:
            final = extract_text_from_file(uploaded_file)
            st.info("Teks berjaya diekstrak daripada fail.")
        if not final:
            st.warning("Sila taip soalan atau muat naik fail.")
        else:
            ans = cari_jawapan(final, style, df_dataset)
            # fallback kepada soalan terdekat
            if not ans:
                from logic import cari_soalan_terdekat
                ans = cari_soalan_terdekat(final, df_dataset)
            st.success(ans)
            # simpan log (concept set kepada "Elektrik")
            log_interaction(final, "Elektrik", style, ans)

            # UC04: butang flag untuk guru
            if st.session_state.get("role") == "guru":
               if st.button("🚩 Tandakan Salah"):
                    flag_last_interaction()
                    st.warning("Jawapan telah ditandakan.")

with tab_guru:  
    st.header("📊 Laporan Kelemahan Konsep")
    report = get_weakness_report()
    if report.empty:
        st.info("Tiada data salah untuk dipaparkan.")
    else:
        st.bar_chart(report)
        st.dataframe(report.reset_index(name="Bil. Salah"))





