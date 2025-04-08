import streamlit as st
from PIL import Image
import io

def convert_images_to_pdf():
    st.title("📸 Image to PDF 🚀")
    st.caption("Transforme múltiplas imagens em PDF, com ferramentas avançadas!")

    uploaded_files = st.file_uploader(
        "Selecione imagens", type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"], accept_multiple_files=True
    )

    if uploaded_files:
        imgs = [Image.open(file) for file in uploaded_files]
        pdf_buffer = io.BytesIO()
        imgs[0].save(pdf_buffer, format="PDF", save_all=True, append_images=imgs[1:])
        pdf_buffer.seek(0)
        st.download_button("📥 Baixar PDF", pdf_buffer, "images.pdf")

convert_images_to_pdf()