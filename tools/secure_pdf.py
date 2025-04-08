import io
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
def convert_secure_pdf():
    """
    Encrypt a PDF file with a password.
    
    Args:
        input_pdf_path (str): Path to the input PDF file.
        password (str): Password to encrypt the PDF file.
        
    Returns:
        str: Path to the encrypted PDF file.
    """
    st.title("🔒 Proteger PDF")
    pdf_protect = st.file_uploader("Selecione PDF", type="pdf", key="protect")
    password = st.text_input("Digite a senha", type="password")

    if pdf_protect and password:
        reader = PdfReader(pdf_protect)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        st.download_button("📥 Baixar PDF protegido", output, "protegido.pdf")
    
convert_secure_pdf()