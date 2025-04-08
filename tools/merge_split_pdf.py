import io
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
def merge_split_pdf():
    """
    Divide or merge a PDF file based on the specified action.
    """
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

merge_split_pdf()