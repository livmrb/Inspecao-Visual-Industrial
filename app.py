import streamlit as st

st.set_page_config(
    page_title="Inspeção Visual Industrial",
    page_icon="🔍",
    layout="wide"
)

st.title("Sistema de Inspeção Visual Industrial")

st.write(
    "Bem-vindo ao sistema de detecção de defeitos "
    "em produtos utilizando Inteligência Artificial."
)

st.subheader("Envie uma imagem para inspeção")

imagem = st.file_uploader(
    "Selecione uma imagem",
    type=["jpg", "jpeg", "png"]
)

if imagem is not None:
    st.image(imagem, caption="Imagem enviada", use_container_width=True)