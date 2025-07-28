
import streamlit as st
from fpdf import FPDF
from translations import translations

lang = st.selectbox("🌐 Choose Language", list(translations.keys()), index=0)
T = translations[lang]

st.image("images/clinic_logo.png", width=300)
st.title(T["title"])

degree = st.selectbox(T["hearing_loss"], ["Mild", "Moderate", "Severe", "Profound"])
style = st.selectbox(T["style"], ["BTE", "RIC", "CIC"])
tech = st.radio(T["tech"], ["Yes", "No"])
phone = st.radio(T["phone"], ["Android", "iPhone"])
budget = st.selectbox(T["budget"], ["Low", "Medium", "High"])
age = st.slider(T["age"], 18, 100, 60)

if st.button(T["recommend"]):
    recommendation = f"Based on your inputs, we recommend a {style} hearing aid."
    if tech == "Yes" and phone == "Android":
        recommendation += " Consider Phonak or Signia BCT for Android compatibility."
    st.subheader(T["result"])
    st.write(recommendation)

    data = {
        T["hearing_loss"]: degree,
        T["style"]: style,
        T["tech"]: tech,
        T["phone"]: phone,
        T["budget"]: budget,
        T["age"]: age,
        T["result"]: recommendation
    }

    class PDF(FPDF):
        def header(self):
            try:
                self.image("images/clinic_logo.png", x=10, y=8, w=50)
                self.ln(20)
            except:
                self.ln(10)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for k, v in data.items():
        pdf.multi_cell(0, 10, f"{k}: {v}")
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    st.download_button(label=T["download"], data=pdf_bytes, file_name="recommendation.pdf", mime="application/pdf")
