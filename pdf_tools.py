import streamlit as st


st.set_page_config(page_title="Image2PDF Pro 🚀", layout="centered")

side = st.sidebar

pages = {
    "Tools to PDF": [
        st.Page("tools/image_to_pdf.py", title="Image2PDF Pro 🚀", icon="📄"),
        st.Page("tools/pdf_darkmode.py", title="darkmode", icon="🌙"),
        st.Page("tools/secure_pdf.py", title="Secure PDF", icon="🔒"),
        st.Page("tools/merge_split_pdf.py", title="Merge/Split PDF", icon="🔀"),
        st.Page("tools/ocr_docling.py", title="OCR Docling", icon="🖼️"),
        st.Page("tools/gif_to_pdf.py", title="GIF to PDF", icon="🎞️"),
        st.Page("tools/extract_image.py", title="Extract Images", icon="🖼️"),
        st.Page("tools/pdf_to_html.py", title="PDF to HTML", icon="🌐"),
    ],
    "Captions of videos": [
        st.Page("tools/captions_vtt.py", title="Legenda (.vtt)", icon="📝"),
        st.Page("tools/audio_video_whisper.py", title="Áudio/Vídeo (Whisper)", icon="🎤"),
    ],
}
pg = st.navigation(pages)
pg.run()

# # Existing tabs (Image to PDF & Dark Mode)
# with image_tab:
#     from tools.image_to_pdf import convert_images_to_pdf
#     convert_images_to_pdf()

# with dark_mode_tab:
#     from tools.pdf_darkmode import convert_pdf_to_dark_mode
#     convert_pdf_to_dark_mode()

# # Protect PDF
# with protect_tab:
#     from tools.secure_pdf import convert_secure_pdf
#     convert_secure_pdf()

# # Merge/Split PDF
# with merge_split_tab:
#     from tools.divide_merge_pdf import divide_or_merge_pdf
#     divide_or_merge_pdf()

# # OCR Docling
# with ocr_tab:
#     from tools.ocr_docling import ocr_docling
#     ocr_docling()

# # GIF para PDF
# with gif_tab:
#     from tools.gif_to_pdf import convert_gif_to_pdf
#     convert_gif_to_pdf()

# # Extract images from PDF
# with extract_images_tab:
#     from tools.extract_image import extract_image_from_pdf
#     extract_image_from_pdf()

# # PDF to HTML
# with pdf_html_tab:
#     from tools.pdf_to_html import convert_pdf_to_html
#     convert_pdf_to_html()

# # VTT Extractor
# with vtt_extrator:
#     import streamlit as st
#     import requests

#     st.title("Extrator de Texto de Legenda (.vtt)")

#     st.markdown("""
#     Cole o link direto do arquivo `.vtt` (por exemplo, copiado do console do navegador).
#     O aplicativo vai extrair automaticamente o texto falado e disponibilizar para download.
#     """)

#     vtt_url = st.text_input("URL da legenda (.vtt)", placeholder="Cole aqui o link direto do Firebase")

#     idiomas_visuais = {
#         "Português (Brasil)": "pt-BR",
#         "Inglês (EUA)": "en-US",
#         "Espanhol": "es"
#     }
#     st.selectbox("Idioma da legenda (visual)", list(idiomas_visuais.keys()))


#     def extract_spoken_text(vtt_data):
#         lines = vtt_data.splitlines()
#         text_lines = []
#         for line in lines:
#             if "-->" in line or line.strip() == "" or line.strip().isdigit():
#                 continue
#             text_lines.append(line.strip())
#         return "\n".join(text_lines)

#     if vtt_url:
#         try:
#             response = requests.get(vtt_url)
#             response.raise_for_status()
#             vtt_content = response.content.decode("utf-8")
#             spoken_text = extract_spoken_text(vtt_content)

#             st.success("Texto extraído com sucesso!")
#             st.download_button(
#                 title="Baixar Texto Extraído (.txt)",
#                 data=spoken_text,
#                 file_name="legenda_extraida.txt",
#                 mime="text/plain"
#             )

#             with st.expander("Visualizar texto extraído"):
#                 st.text_area("Conteúdo", spoken_text, height=300)
#         except Exception as e:
#             st.error(f"Erro ao baixar ou processar o arquivo: {e}")
#     else:
#         st.info("Cole o link da legenda para iniciar o processo.")
