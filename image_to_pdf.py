import streamlit as st
from PIL import Image, ImageOps
import io
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes

st.set_page_config(page_title="Image2PDF Pro 🚀", layout="wide")

# Tabs
image_tab, dark_mode_tab = st.tabs(["📸 Imagens para PDF", "🌙 PDF Dark Mode"])

with image_tab:
    st.title("📸 Image2PDF Pro 🚀")
    st.caption("Transforme múltiplas imagens em um único arquivo PDF, com ferramentas avançadas de edição!")

    st.sidebar.header("⚙️ Configurações")

    pdf_quality = st.sidebar.select_slider("Qualidade do PDF", options=["Baixa", "Média", "Alta"], value="Alta")
    resolution_mapping = {"Baixa": 50, "Média": 100, "Alta": 200}
    resolution = resolution_mapping[pdf_quality]

    margin = st.sidebar.slider("Margem das Imagens no PDF", 0, 50, 10, step=5)

    grayscale = st.sidebar.toggle("Converter imagens para escala de cinza")

    uploaded_files = st.file_uploader(
        "Selecione suas imagens",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
        accept_multiple_files=True
    )

    processed_images = []

    @st.fragment
    def image_editor(file_bytes, idx):
        st.write("---")
        col1, col2 = st.columns([1, 2])

        with col1:
            rotation = st.selectbox("Rotação", [0, 90, 180, 270], key=f"rotation_{idx}")
            flip_horizontal = st.checkbox("Virar horizontalmente", key=f"flip_h_{idx}")
            flip_vertical = st.checkbox("Virar verticalmente", key=f"flip_v_{idx}")

        with col2:
            image = Image.open(io.BytesIO(file_bytes))

            if rotation:
                image = image.rotate(-rotation, expand=True)
            if flip_horizontal:
                image = ImageOps.mirror(image)
            if flip_vertical:
                image = ImageOps.flip(image)
            if grayscale:
                image = ImageOps.grayscale(image).convert("RGB")

            st.image(image, use_column_width=True)

        return image

    if uploaded_files:
        st.header("🖼️ Editor de Imagens")
        for idx, uploaded_file in enumerate(uploaded_files):
            st.subheader(f"📄 {uploaded_file.name}")
            file_bytes = uploaded_file.getvalue()
            img = image_editor(file_bytes, idx)
            processed_images.append(img)

        if st.button("🚀 Gerar PDF"):
            if processed_images:
                pdf_buffer = io.BytesIO()

                images_with_margin = []
                for img in processed_images:
                    bg = Image.new("RGB", (img.width + 2 * margin, img.height + 2 * margin), "white")
                    bg.paste(img, (margin, margin))
                    images_with_margin.append(bg)

                images_with_margin[0].save(
                    pdf_buffer,
                    format="PDF",
                    resolution=resolution,
                    save_all=True,
                    append_images=images_with_margin[1:]
                )

                pdf_buffer.seek(0)
                st.download_button(
                    label="📥 Baixar PDF",
                    data=pdf_buffer,
                    file_name="images_editadas.pdf",
                    mime="application/pdf"
                )

                st.success("PDF gerado com sucesso! 🎉")
            else:
                st.error("Nenhuma imagem válida processada!")

poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin'  # <-- coloque o caminho exato aqui

with dark_mode_tab:
    st.title("🌙 PDF Dark Mode")
    st.caption("Envie um PDF comum para obter uma versão com dark mode ativado!")

    pdf_file = st.file_uploader("Selecione um PDF", type="pdf", key='darkmode_pdf')

    if pdf_file:
        with st.spinner("Convertendo PDF para Dark Mode..."):
            images = convert_from_bytes(pdf_file.getvalue(), dpi=150, poppler_path=poppler_path)

            inverted_images = [ImageOps.invert(img.convert("RGB")) for img in images]

            pdf_buffer = io.BytesIO()
            inverted_images[0].save(
                pdf_buffer,
                format="PDF",
                save_all=True,
                append_images=inverted_images[1:]
            )
            pdf_buffer.seek(0)

            st.download_button(
                label="📥 Baixar PDF Dark Mode",
                data=pdf_buffer,
                file_name="dark_mode.pdf",
                mime="application/pdf"
            )

            st.success("PDF com Dark Mode gerado com sucesso! 🎉")