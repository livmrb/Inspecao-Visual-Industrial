import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time
import io
import tempfile
import os
import cv2
import pandas as pd
import subprocess

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Inspeção Visual Industrial",
    page_icon="🔍",
    layout="wide"
)


# ==========================================
# CAMINHO DO FFMPEG
# ==========================================

CAMINHO_FFMPEG = os.path.join(
    os.environ["LOCALAPPDATA"],
    "Microsoft",
    "WinGet",
    "Packages",
    "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe",
    "ffmpeg-9.0.2-full_build",
    "bin",
    "ffmpeg.exe"
)


# ==========================================
# CARREGAMENTO DO MODELO
# ==========================================

@st.cache_resource
def carregar_modelo():

    caminho = "runs/detect/runs/detect/neu_det/weights/best.pt"

    return YOLO(caminho)


# ==========================================
# CONVERSÃO PARA H.264
# ==========================================

def converter_video_h264(caminho_entrada, caminho_saida):

    if not os.path.exists(CAMINHO_FFMPEG):

        raise FileNotFoundError(
            "FFmpeg não encontrado no caminho configurado."
        )

    comando = [
        CAMINHO_FFMPEG,
        "-y",
        "-i", caminho_entrada,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-an",
        caminho_saida
    ]

    try:

        subprocess.run(
            comando,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as erro:

        detalhes = (
            erro.stderr[-2000:]
            if erro.stderr
            else str(erro)
        )

        raise RuntimeError(
            f"Erro ao converter o vídeo para H.264:\n{detalhes}"
        )

    if (
        not os.path.exists(caminho_saida)
        or os.path.getsize(caminho_saida) == 0
    ):

        raise RuntimeError(
            "O FFmpeg não conseguiu gerar o vídeo convertido."
        )


# ==========================================
# GERAÇÃO DO PDF
# ==========================================

def gerar_pdf(nome_arquivo, status, quantidade, tempo, dados):

    buffer = io.BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    estilos = getSampleStyleSheet()

    conteudo = []

    conteudo.append(
        Paragraph(
            "Relatório de Inspeção Visual Industrial",
            estilos["Title"]
        )
    )

    conteudo.append(Spacer(1, 20))

    conteudo.append(
        Paragraph(
            f"<b>Arquivo:</b> {nome_arquivo}",
            estilos["Normal"]
        )
    )

    conteudo.append(
        Paragraph(
            f"<b>Resultado:</b> {status}",
            estilos["Normal"]
        )
    )

    conteudo.append(
        Paragraph(
            f"<b>Defeitos detectados:</b> {quantidade}",
            estilos["Normal"]
        )
    )

    conteudo.append(
        Paragraph(
            f"<b>Tempo de processamento:</b> {tempo:.3f} segundos",
            estilos["Normal"]
        )
    )

    conteudo.append(Spacer(1, 20))

    conteudo.append(
        Paragraph(
            "Detalhamento das detecções",
            estilos["Heading2"]
        )
    )

    conteudo.append(Spacer(1, 10))

    tabela_dados = [
        ["Defeito", "Confiança / Quantidade"]
    ]

    for item in dados:

        tabela_dados.append([
            item["Defeito"],
            item["Confiança"]
        ])

    if not dados:

        tabela_dados.append([
            "Nenhum defeito detectado",
            "-"
        ])

    tabela = Table(
        tabela_dados,
        colWidths=[250, 150]
    )

    tabela.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#263B55")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ])
    )

    conteudo.append(tabela)

    documento.build(conteudo)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# PROCESSAMENTO DO VÍDEO COM YOLO
# ==========================================

def processar_video(caminho_entrada, caminho_saida, confianca):

    captura = cv2.VideoCapture(caminho_entrada)

    if not captura.isOpened():

        raise ValueError(
            "Não foi possível abrir o vídeo enviado."
        )

    fps = captura.get(cv2.CAP_PROP_FPS)

    largura = int(
        captura.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    altura = int(
        captura.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    total_quadros = int(
        captura.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    if fps <= 0 or largura <= 0 or altura <= 0:

        captura.release()

        raise ValueError(
            "O vídeo possui informações inválidas."
        )

    quatrocc = cv2.VideoWriter_fourcc(*"mp4v")

    escritor = cv2.VideoWriter(
        caminho_saida,
        quatrocc,
        fps,
        (largura, altura)
    )

    if not escritor.isOpened():

        captura.release()

        raise ValueError(
            "Não foi possível criar o vídeo processado."
        )

    total_deteccoes = 0

    deteccoes_por_classe = {}

    confiancas = []

    quadros_processados = 0

    progresso = st.progress(0)

    mensagem = st.empty()

    inicio = time.perf_counter()

    try:

        while True:

            sucesso, quadro = captura.read()

            if not sucesso:
                break

            resultado = modelo.predict(
                source=quadro,
                conf=confianca,
                imgsz=320,
                verbose=False
            )[0]

            quadro_anotado = resultado.plot()

            escritor.write(quadro_anotado)

            quantidade = len(resultado.boxes)

            total_deteccoes += quantidade

            for caixa in resultado.boxes:

                classe = int(caixa.cls[0])

                nome_classe = modelo.names[classe]

                valor_confianca = float(caixa.conf[0])

                deteccoes_por_classe[nome_classe] = (
                    deteccoes_por_classe.get(nome_classe, 0) + 1
                )

                confiancas.append(valor_confianca)

            quadros_processados += 1

            if total_quadros > 0:

                progresso.progress(
                    min(
                        quadros_processados / total_quadros,
                        1.0
                    )
                )

            mensagem.write(
                f"Processando quadro {quadros_processados} "
                f"de {total_quadros}..."
            )

    finally:

        captura.release()

        escritor.release()

    tempo_total = time.perf_counter() - inicio

    progresso.empty()

    mensagem.empty()

    if (
        not os.path.exists(caminho_saida)
        or os.path.getsize(caminho_saida) == 0
    ):

        raise RuntimeError(
            "O vídeo processado não foi gerado corretamente."
        )

    media_confianca = (
        sum(confiancas) / len(confiancas)
        if confiancas
        else 0
    )

    return {
        "quadros": quadros_processados,
        "deteccoes": total_deteccoes,
        "classes": deteccoes_por_classe,
        "confiancas": confiancas,
        "media_confianca": media_confianca,
        "tempo": tempo_total
    }


# ==========================================
# INTERFACE PRINCIPAL
# ==========================================

st.title("Inspeção Visual Industrial")

st.write(
    "Sistema de identificação automática de defeitos "
    "em superfícies metálicas utilizando YOLOv8."
)

modelo = carregar_modelo()


# ==========================================
# CONFIGURAÇÕES LATERAIS
# ==========================================

st.sidebar.header("Configurações")

confianca = st.sidebar.slider(
    "Confiança mínima",
    min_value=0.10,
    max_value=0.90,
    value=0.27,
    step=0.01
)

st.sidebar.write("Modelo: YOLOv8 Nano")

st.sidebar.write("Material: Superfícies metálicas")


# ==========================================
# UPLOAD DE ARQUIVOS
# ==========================================

arquivo = st.file_uploader(
    "Envie uma imagem ou vídeo para inspeção",
    type=["jpg", "jpeg", "png", "mp4"]
)


# ==========================================
# PROCESSAMENTO DE IMAGEM
# ==========================================

if arquivo is not None and arquivo.type.startswith("image/"):

    imagem = Image.open(arquivo).convert("RGB")

    inicio = time.perf_counter()

    resultado = modelo.predict(
        source=imagem,
        conf=confianca,
        imgsz=320,
        verbose=False
    )[0]

    tempo = time.perf_counter() - inicio

    imagem_processada = resultado.plot()

    quantidade = len(resultado.boxes)

    status = (
        "Não conforme"
        if quantidade > 0
        else "Sem defeitos detectados"
    )

    dados = []

    for caixa in resultado.boxes:

        classe = int(caixa.cls[0])

        valor = float(caixa.conf[0])

        dados.append({
            "Defeito": modelo.names[classe],
            "Confiança": f"{valor:.2%}"
        })

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Imagem original")

        st.image(
            imagem,
            use_container_width=True
        )

    with col2:

        st.subheader("Resultado da inspeção")

        st.image(
            imagem_processada,
            use_container_width=True
        )

    st.divider()

    st.subheader("Indicadores da inspeção")

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        "Defeitos detectados",
        quantidade
    )

    kpi2.metric(
        "Tempo de processamento",
        f"{tempo:.3f} s"
    )

    kpi3.metric(
        "Resultado",
        status
    )

    st.subheader("Defeitos identificados")

    df = pd.DataFrame(
        dados,
        columns=["Defeito", "Confiança"]
    )

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.success(
            "Nenhum defeito foi detectado."
        )

    csv = df.to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    ).encode("utf-8-sig")

    pdf = gerar_pdf(
        arquivo.name,
        status,
        quantidade,
        tempo,
        dados
    )

    st.divider()

    st.subheader("Exportar relatório")

    col_csv, col_pdf = st.columns(2)

    with col_csv:

        st.download_button(
            "Baixar relatório CSV",
            data=csv,
            file_name="relatorio_inspecao.csv",
            mime="text/csv"
        )

    with col_pdf:

        st.download_button(
            "Baixar relatório PDF",
            data=pdf,
            file_name="relatorio_inspecao.pdf",
            mime="application/pdf"
        )


# ==========================================
# PROCESSAMENTO DE VÍDEO
# ==========================================

elif arquivo is not None and arquivo.name.lower().endswith(".mp4"):

    st.subheader("Inspeção de vídeo")

    # Identificador para manter os resultados
    # associados ao arquivo enviado.

    chave = f"{arquivo.name}_{arquivo.size}"

    chave_video = f"video_processado_{chave}"

    chave_resultados = f"resultados_video_{chave}"

    chave_original = f"video_original_{chave}"

    # ======================================
    # CONVERTER VÍDEO ORIGINAL PARA PRÉVIA
    # ======================================

    if chave_original not in st.session_state:

        try:

            with tempfile.TemporaryDirectory() as pasta_preview:

                caminho_original = os.path.join(
                    pasta_preview,
                    "video_original.mp4"
                )

                caminho_preview = os.path.join(
                    pasta_preview,
                    "video_original_h264.mp4"
                )

                with open(caminho_original, "wb") as f:

                    f.write(arquivo.getbuffer())

                converter_video_h264(
                    caminho_original,
                    caminho_preview
                )

                with open(caminho_preview, "rb") as f:

                    st.session_state[chave_original] = f.read()

        except Exception as erro:

            st.error(
                f"Erro ao preparar o vídeo original: {erro}"
            )

    # ======================================
    # BOTÃO DE INSPEÇÃO
    # ======================================

    if st.button("Iniciar inspeção do vídeo"):

        with tempfile.TemporaryDirectory() as pasta_temp:

            caminho_entrada = os.path.join(
                pasta_temp,
                "entrada.mp4"
            )

            caminho_intermediario = os.path.join(
                pasta_temp,
                "resultado_mp4v.mp4"
            )

            caminho_saida = os.path.join(
                pasta_temp,
                "resultado_h264.mp4"
            )

            with open(caminho_entrada, "wb") as f:

                f.write(arquivo.getbuffer())

            try:

                with st.spinner("Executando inspeção com YOLO..."):

                    resultados_video = processar_video(
                        caminho_entrada,
                        caminho_intermediario,
                        confianca
                    )

                with st.spinner("Convertendo vídeo para H.264..."):

                    converter_video_h264(
                        caminho_intermediario,
                        caminho_saida
                    )

                with open(caminho_saida, "rb") as f:

                    st.session_state[chave_video] = f.read()

                st.session_state[chave_resultados] = resultados_video

                st.success(
                    "Processamento do vídeo concluído!"
                )

            except Exception as erro:

                st.error(
                    f"Erro ao processar vídeo: {erro}"
                )

    # ======================================
    # EXIBIÇÃO DOS DOIS VÍDEOS LADO A LADO
    # ======================================

    if chave_video in st.session_state:

        col_original, col_processado = st.columns(2)

        with col_original:

            st.subheader("Vídeo original")

            if chave_original in st.session_state:

                st.video(
                    st.session_state[chave_original],
                    format="video/mp4",
                    width=350
                )

        with col_processado:

            st.subheader("Vídeo processado")

            st.video(
                st.session_state[chave_video],
                format="video/mp4",
                width=350
            )

        # ==================================
        # INDICADORES
        # ==================================

        resultados_video = st.session_state[chave_resultados]

        quantidade = resultados_video["deteccoes"]

        status = (
            "Não conforme"
            if quantidade > 0
            else "Sem defeitos detectados"
        )

        st.divider()

        st.subheader("Indicadores da inspeção")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric(
            "Detecções nos quadros",
            quantidade
        )

        kpi2.metric(
            "Quadros processados",
            resultados_video["quadros"]
        )

        kpi3.metric(
            "Confiança média",
            f'{resultados_video["media_confianca"]:.2%}'
        )

        kpi4.metric(
            "Tempo de processamento",
            f'{resultados_video["tempo"]:.2f} s'
        )

        st.write(
            f"**Resultado geral:** {status}"
        )

        # ==================================
        # TABELA DE DEFEITOS
        # ==================================

        dados = []

        for classe, total in resultados_video["classes"].items():

            dados.append({
                "Defeito": classe,
                "Quantidade de detecções": total
            })

        st.subheader("Defeitos identificados no vídeo")

        df_video = pd.DataFrame(
            dados,
            columns=[
                "Defeito",
                "Quantidade de detecções"
            ]
        )

        st.dataframe(
            df_video,
            use_container_width=True
        )

        # ==================================
        # RELATÓRIOS
        # ==================================

        dados_pdf = [
            {
                "Defeito": item["Defeito"],
                "Confiança": str(
                    item["Quantidade de detecções"]
                )
            }
            for item in dados
        ]

        csv = df_video.to_csv(
            index=False,
            sep=";",
            encoding="utf-8-sig"
        ).encode("utf-8-sig")

        pdf = gerar_pdf(
            arquivo.name,
            status,
            quantidade,
            resultados_video["tempo"],
            dados_pdf
        )

        st.divider()

        st.subheader("Exportar resultados")

        st.download_button(
            "Baixar vídeo processado",
            data=st.session_state[chave_video],
            file_name="video_inspecionado.mp4",
            mime="video/mp4"
        )

        col_csv, col_pdf = st.columns(2)

        with col_csv:

            st.download_button(
                "Baixar relatório CSV",
                data=csv,
                file_name="relatorio_video.csv",
                mime="text/csv"
            )

        with col_pdf:

            st.download_button(
                "Baixar relatório PDF",
                data=pdf,
                file_name="relatorio_video.pdf",
                mime="application/pdf"
            )

    else:

        st.info(
            "Clique em 'Iniciar inspeção do vídeo' "
            "para executar a análise e comparar os resultados."
        )

        if chave_original in st.session_state:

            st.caption("Prévia do vídeo original")

            st.video(
                st.session_state[chave_original],
                format="video/mp4",
                width=350
            )