import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageOps
import io
from PyPDF2 import PdfReader, PdfWriter
import docx
from pdf2image import convert_from_bytes
import fitz  # PyMuPDF
import base64

st.set_page_config(page_title="Image2PDF Pro 🚀", layout="wide")

# Tabs
(
    image_tab,
    dark_mode_tab,
    protect_tab,
    merge_split_tab,
    ocr_tab,
    gif_tab,
    extract_images_tab,
    pdf_html_tab,
) = st.tabs(
    [
        "📸 Imagens para PDF",
        "🌙 PDF Dark Mode",
        "🔒 Proteger PDF",
        "📚 Mesclar/Dividir PDF",
        "📝 OCR (Docling)",
        "🎞️ GIF para PDF",
        "🖼️ Extrair Imagens",
        "🌐 PDF para HTML",
    ]
)

# Existing tabs (Image to PDF & Dark Mode)
with image_tab:
    st.title("📸 Image2PDF Pro 🚀")
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

with dark_mode_tab:
    st.title("🌙 PDF Dark Mode")
    pdf_file = st.file_uploader("Selecione PDF", type="pdf", key="darkmode")

    if pdf_file:
        images = convert_from_bytes(pdf_file.getvalue(), dpi=150)
        inverted_images = [ImageOps.invert(img.convert("RGB")) for img in images]
        pdf_buffer = io.BytesIO()
        inverted_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=inverted_images[1:])
        pdf_buffer.seek(0)
        st.download_button("📥 Baixar PDF Dark Mode", pdf_buffer, "dark_mode.pdf")

# New Features

# Protect PDF
with protect_tab:
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

# Merge/Split PDF
with merge_split_tab:
    st.title("📚 Mesclar/Dividir PDF")
    mode = st.radio("Escolha uma ação", ["Mesclar", "Dividir"])

    if mode == "Mesclar":
        pdfs = st.file_uploader("Selecione PDFs", type="pdf", accept_multiple_files=True, key="merge")
        if pdfs:
            merger = PdfWriter()
            for pdf in pdfs:
                reader = PdfReader(pdf)
                for page in reader.pages:
                    merger.add_page(page)
            output = io.BytesIO()
            merger.write(output)
            output.seek(0)
            st.download_button("📥 Baixar PDF mesclado", output, "mesclado.pdf")

    if mode == "Dividir":
        pdf = st.file_uploader("Selecione PDF", type="pdf", key="split")
        if pdf:
            reader = PdfReader(pdf)
            for i, page in enumerate(reader.pages):
                output = io.BytesIO()
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(output)
                output.seek(0)
                st.download_button(f"📥 Baixar página {i+1}", output, f"pagina_{i+1}.pdf")

# OCR Docling
with ocr_tab:
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

# GIF para PDF
with gif_tab:
    st.title("🎞️ GIF para PDF")
    gif_file = st.file_uploader("Selecione GIF", type="gif")
    if gif_file:
        gif = Image.open(gif_file)
        frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(gif)]
        pdf_buffer = io.BytesIO()
        frames[0].save(pdf_buffer, format="PDF", save_all=True, append_images=frames[1:])
        pdf_buffer.seek(0)
        st.download_button("📥 Baixar PDF", pdf_buffer, "gif_para_pdf.pdf")

# Extract images from PDF
with extract_images_tab:
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

# PDF to HTML
with pdf_html_tab:
    st.title("🌐 PDF para HTML")
    pdf_html = st.file_uploader("Selecione PDF", type="pdf", key="html")
    if pdf_html:
        code_html = f"<!DOCTYPE html><html><embed src='data:application/pdf;base64,{base64.b64encode(pdf_html.getvalue()).decode()}' width='100%' height='800px'/></html>"
        st.html(code_html)
        st.download_button("📥 Baixar HTML", code_html.encode(), "pdf_view.html")
