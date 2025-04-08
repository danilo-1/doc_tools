import io
import streamlit as st
import fitz  # PyMuPDF
def extract_image_from_pdf():
    """
    Extracts an image from a PDF file and saves it as a PNG file.
    """
    st.title("🖼️ Extrair Imagens do PDF")
    pdf_extract = st.file_uploader("Selecione PDF", type="pdf", key="extract")
    if pdf_extract:
        doc = fitz.open(stream=pdf_extract.read(), filetype="pdf")
        for page_index in range(len(doc)):
            for img_index, img in enumerate(doc.get_page_images(page_index)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                st.download_button(f"📥 Baixar imagem {page_index+1}-{img_index+1}", image_bytes, f"imagem_{page_index+1}_{img_index+1}.png")

extract_image_from_pdf()