import io
from PIL import Image, ImageOps
from pdf2image import convert_from_bytes
import streamlit as st

def convert_pdf_to_dark_mode():
    """
    Convert a PDF file to dark mode by inverting the colors.
    
    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to save the output dark mode PDF file.
    """

    st.title("🌙 PDF Dark Mode")
    pdf_file = st.file_uploader("Selecione PDF", type="pdf", key="darkmode")

    if pdf_file:
        images = convert_from_bytes(pdf_file.getvalue(), dpi=150)
        inverted_images = [ImageOps.invert(img.convert("RGB")) for img in images]
        pdf_buffer = io.BytesIO()
        inverted_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=inverted_images[1:])
        pdf_buffer.seek(0)
        st.download_button("📥 Baixar PDF Dark Mode", pdf_buffer, "dark_mode.pdf")

convert_pdf_to_dark_mode()