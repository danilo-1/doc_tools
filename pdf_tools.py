import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageOps
import io
from PyPDF2 import PdfReader, PdfWriter
import docx
from pdf2image import convert_from_bytes
import fitz  # PyMuPDF
import base64

st.set_page_config(page_title="Image2PDF Pro 🚀", layout="centered")

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
    vtt_extrator
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
        "📝 Extrator de Legenda(VTT)",
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

with vtt_extrator:
    import streamlit as st
    import requests

    st.title("Extrator de Texto de Legenda (.vtt)")

    st.markdown("""
    Cole o link direto do arquivo `.vtt` (por exemplo, copiado do console do navegador).
    O aplicativo vai extrair automaticamente o texto falado e disponibilizar para download.
    """)

    vtt_url = st.text_input("URL da legenda (.vtt)", placeholder="Cole aqui o link direto do Firebase")

    idiomas_visuais = {
        "Português (Brasil)": "pt-BR",
        "Inglês (EUA)": "en-US",
        "Espanhol": "es"
    }
    st.selectbox("Idioma da legenda (visual)", list(idiomas_visuais.keys()))


    def extract_spoken_text(vtt_data):
        lines = vtt_data.splitlines()
        text_lines = []
        for line in lines:
            if "-->" in line or line.strip() == "" or line.strip().isdigit():
                continue
            text_lines.append(line.strip())
        return "\n".join(text_lines)

    if vtt_url:
        try:
            response = requests.get(vtt_url)
            response.raise_for_status()
            vtt_content = response.content.decode("utf-8")
            spoken_text = extract_spoken_text(vtt_content)

            st.success("Texto extraído com sucesso!")
            st.download_button(
                label="Baixar Texto Extraído (.txt)",
                data=spoken_text,
                file_name="legenda_extraida.txt",
                mime="text/plain"
            )

            with st.expander("Visualizar texto extraído"):
                st.text_area("Conteúdo", spoken_text, height=300)
        except Exception as e:
            st.error(f"Erro ao baixar ou processar o arquivo: {e}")
    else:
        st.info("Cole o link da legenda para iniciar o processo.")
