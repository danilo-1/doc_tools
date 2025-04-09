import whisper
import tempfile
import yt_dlp
from pathlib import Path
import streamlit as st
import requests
import os

# Desativa o "run on save" do Streamlit para ajudar a evitar problemas com o watcher
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"

# Configura a política de loop adequada no Windows
if os.name == 'nt':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Aplica o patch do nest_asyncio para evitar erros de event loop (se necessário)
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    import asyncio
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


def run_app():
    st.header("Modo: Transcrição por áudio/vídeo (Whisper)")
    
    # Seleção de dispositivo para processamento
    proc_option = st.radio(
        "Selecione o dispositivo para transcrição:",
        ["CPU (método mais lento)", "CPU + GPU (Recomendado)"]
    )
    if proc_option == "CPU + GPU (Recomendado)":
        try:
            import torch
            if torch.cuda.is_available():
                num_gpus = torch.cuda.device_count()
                if num_gpus > 1:
                    available_gpus = []
                    for i in range(num_gpus):
                        device_str = f"cuda:{i} - {torch.cuda.get_device_name(i)}"
                        available_gpus.append(device_str)
                    selected_gpu_display = st.selectbox("Selecione a GPU:", options=available_gpus)
                    # Extrai o identificador ("cuda:i") da string selecionada
                    selected_device = selected_gpu_display.split(" - ")[0]
                    st.info(f"GPU selecionada: {selected_gpu_display}")
                else:
                    selected_device = "cuda:0"
                    st.info(f"Utilizando GPU: cuda:0 - {torch.cuda.get_device_name(0)}")
                device = selected_device
            else:
                st.warning("Nenhuma GPU disponível. Usando CPU.")
                device = "cpu"
        except Exception as e:
            st.error("Erro ao verificar a disponibilidade da GPU: " + str(e))
            device = "cpu"
    else:
        device = "cpu"

    # Seleção de como fornecer o áudio
    opcao_input = st.radio(
        "Como deseja fornecer o áudio?",
        ["Upload de Arquivo", "URL de vídeo (YouTube, Vimeo, etc)"]
    )

    audio_bytes = None
    audio_name = None
    tmp_path = None

    if opcao_input == "Upload de Arquivo":
        audio_file = st.file_uploader("Envie um arquivo de áudio ou vídeo", type=["mp3", "mp4", "m4a", "wav", "webm"])
        if audio_file is not None:
            audio_bytes = audio_file.read()
            audio_name = audio_file.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_name).suffix) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            st.write("Arquivo carregado e salvo em:", tmp_path)

    elif opcao_input == "URL de vídeo (YouTube, Vimeo, etc)":
        video_url = st.text_input("Cole a URL do vídeo (YouTube, Vimeo, etc)")
        if video_url:
            try:
                tmp_dir = tempfile.gettempdir()
                output_path = tempfile.mktemp(suffix=".mp3", dir=tmp_dir)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_path,
                    'quiet': False,  # Logs ativados para depuração
                    'noplaylist': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                
                # Verifica se o arquivo convertido (com extensão duplicada) existe
                converted_path = output_path + ".mp3"
                if os.path.exists(converted_path):
                    tmp_path = converted_path
                else:
                    tmp_path = output_path

                audio_name = Path(tmp_path).name
                st.write("Vídeo baixado e convertido. Arquivo salvo em:", tmp_path)
                st.write("Arquivos no diretório temporário:", os.listdir(tmp_dir))
            except Exception as e:
                st.error(f"Erro ao baixar o vídeo: {e}")

    # Botão para solicitar a transcrição
    if tmp_path:
        if st.button("Solicitar a Transcrição"):
            with st.spinner("Transcrevendo com Whisper... isso pode levar um tempinho..."):
                try:
                    model = whisper.load_model("base", device=device)
                    result = model.transcribe(tmp_path)
                    transcribed_text = result["text"]
                    st.success("Transcrição concluída!")
                    st.download_button(
                        label="Baixar Transcrição (.txt)",
                        data=transcribed_text,
                        file_name="transcricao_whisper.txt",
                        mime="text/plain"
                    )
                    with st.expander("Visualizar transcrição"):
                        st.text_area("Conteúdo", transcribed_text, height=300)
                except Exception as e:
                    st.error(f"Erro ao transcrever: {e}")
    else:
        st.info("Envie um arquivo ou cole uma URL para iniciar a transcrição.")

run_app()