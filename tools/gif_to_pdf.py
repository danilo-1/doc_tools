import io
from PIL import Image, ImageSequence
import streamlit as st
def convert_gif_to_pdf():
    """
    Convert a GIF file to a PDF file.
    """
    st.title("🎞️ GIF para PDF")
    gif_file = st.file_uploader("Selecione GIF", type="gif")
    if gif_file:
        gif = Image.open(gif_file)
        frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(gif)]
        pdf_buffer = io.BytesIO()
        frames[0].save(pdf_buffer, format="PDF", save_all=True, append_images=frames[1:])
        pdf_buffer.seek(0)
        st.download_button("📥 Baixar PDF", pdf_buffer, "gif_para_pdf.pdf")

convert_gif_to_pdf()