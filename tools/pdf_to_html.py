import base64
import streamlit as st

def convert_pdf_to_html():
    """
    Convert a PDF file to HTML.
    """
    st.title("🌐 PDF para HTML")
    pdf_html = st.file_uploader("Selecione PDF", type="pdf", key="html")
    if pdf_html:
        code_html = f"<!DOCTYPE html><html><embed src='data:application/pdf;base64,{base64.b64encode(pdf_html.getvalue()).decode()}' width='100%' height='800px'/></html>"
        st.html(code_html)
        st.download_button("📥 Baixar HTML", code_html.encode(), "pdf_view.html")

convert_pdf_to_html()