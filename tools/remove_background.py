import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("🪄 Removedor de Fundo de Logos e Imagens")

uploaded_file = st.file_uploader("Envie sua logo ou imagem (PNG, JPG, etc)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.subheader("Prévia da imagem original")
    original = Image.open(uploaded_file).convert("RGBA")
    st.image(original, use_container_width =True)

    st.subheader("Imagem com fundo removido")
    result = remove(original)
    st.image(result, use_container_width =True)

    # Converter resultado para download
    buffered = io.BytesIO()
    result.save(buffered, format="PNG")
    st.download_button(
        label="📥 Baixar imagem com fundo transparente",
        data=buffered.getvalue(),
        file_name="imagem_sem_fundo.png",
        mime="image/png"
    )
else:
    st.info("Envie uma imagem para começar.")