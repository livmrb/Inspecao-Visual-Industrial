import os
import shutil

BASE = "dataset/NEU-DET"

DIVISOES = {
    "train": "train",
    "validation": "val"
}

EXTENSOES = (".jpg", ".jpeg", ".png")

for origem, destino in DIVISOES.items():

    pasta_imagens = os.path.join(BASE, origem, "images")
    pasta_labels = os.path.join(BASE, "labels", destino)

    destino_imagens = os.path.join(BASE, "images", destino)
    destino_labels = os.path.join(BASE, "labels", destino)

    os.makedirs(destino_imagens, exist_ok=True)
    os.makedirs(destino_labels, exist_ok=True)

    total = 0

    for raiz, _, arquivos in os.walk(pasta_imagens):
        for arquivo in arquivos:

            if not arquivo.lower().endswith(EXTENSOES):
                continue

            caminho_origem = os.path.join(raiz, arquivo)
            caminho_destino = os.path.join(destino_imagens, arquivo)

            nome_base = os.path.splitext(arquivo)[0]
            caminho_label = os.path.join(
                pasta_labels, nome_base + ".txt"
            )

            if not os.path.isfile(caminho_label):
                print(f"Anotação não encontrada: {arquivo}")
                continue

            shutil.copy2(caminho_origem, caminho_destino)
            total += 1

    print(f"{destino}: {total} imagens organizadas.")

print("Organização finalizada!")