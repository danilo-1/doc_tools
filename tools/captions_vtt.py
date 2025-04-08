import os


import streamlit as st
import requests




def extract_spoken_text(vtt_data):
    lines = vtt_data.splitlines()
    text_lines = []
    for line in lines:
        if "-->" in line or line.strip() == "" or line.strip().isdigit():
            continue
        text_lines.append(line.strip())
    return "\n".join(text_lines)

def captions_vtt_extractor():
    st.header("Modo: Extração de legenda (.vtt)")
    vtt_url = st.text_input("URL da legenda (.vtt)", placeholder="Cole aqui o link direto do Firebase")
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

captions_vtt_extractor()