import io
import streamlit as st
import docx

def ocr_docling():
    st.title("📝 OCR com Docling")
    img_ocr = st.file_uploader("Envie a imagem para OCR", type=["jpg", "png", "jpeg"])
    if img_ocr:
        st.image(img_ocr)
        text = "Texto extraído da imagem via OCR (Simulação)."
        doc = docx.Document()
        doc.add_paragraph(text)
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        st.download_button("📥 Baixar DOCX", output, "ocr_resultado.docx")

ocr_docling()