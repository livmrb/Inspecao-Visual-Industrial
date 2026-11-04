import cv2
from pathlib import Path

pasta_imagens = Path("dataset/NEU-DET/images/val")
caminho_saida = "dataset/video_teste_neu_det.mp4"

imagens = sorted(pasta_imagens.glob("*.jpg"))

if not imagens:
    print("Nenhuma imagem encontrada!")
    exit()

primeira_imagem = cv2.imread(str(imagens[0]))

altura, largura = primeira_imagem.shape[:2]

# Vídeo com 10 quadros por segundo
fps = 10

codec = cv2.VideoWriter_fourcc(*"mp4v")

video = cv2.VideoWriter(
    caminho_saida,
    codec,
    fps,
    (largura, altura)
)

if not video.isOpened():
    print("Erro ao criar o vídeo!")
    exit()

for caminho in imagens:
    imagem = cv2.imread(str(caminho))

    if imagem is None:
        continue

    imagem = cv2.resize(imagem, (largura, altura))
    video.write(imagem)

video.release()

print("\nVídeo criado com sucesso!")
print(f"Local: {caminho_saida}")
print(f"Quantidade de imagens: {len(imagens)}")
print(f"FPS: {fps}")
print(f"Duração aproximada: {len(imagens) / fps:.1f} segundos")