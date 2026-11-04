import os
import xml.etree.ElementTree as ET

DATASET_DIR = "dataset/NEU-DET"

CLASSES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches"
]

DIVISOES = {
    "train": "train",
    "validation": "val"
}


def converter_anotacoes(pasta_original, pasta_destino):
    pasta_xml = os.path.join(
        DATASET_DIR, pasta_original, "annotations"
    )

    pasta_labels = os.path.join(
        DATASET_DIR, "labels", pasta_destino
    )

    os.makedirs(pasta_labels, exist_ok=True)

    total = 0

    for arquivo in os.listdir(pasta_xml):
        if not arquivo.lower().endswith(".xml"):
            continue

        caminho_xml = os.path.join(pasta_xml, arquivo)

        arvore = ET.parse(caminho_xml)
        raiz = arvore.getroot()

        largura = int(raiz.find("size/width").text)
        altura = int(raiz.find("size/height").text)

        linhas = []

        for objeto in raiz.findall("object"):
            nome_classe = objeto.find("name").text.strip()

            if nome_classe not in CLASSES:
                print(f"Classe desconhecida: {nome_classe}")
                continue

            indice = CLASSES.index(nome_classe)

            caixa = objeto.find("bndbox")

            xmin = float(caixa.find("xmin").text)
            ymin = float(caixa.find("ymin").text)
            xmax = float(caixa.find("xmax").text)
            ymax = float(caixa.find("ymax").text)

            x_centro = ((xmin + xmax) / 2) / largura
            y_centro = ((ymin + ymax) / 2) / altura

            largura_caixa = (xmax - xmin) / largura
            altura_caixa = (ymax - ymin) / altura

            linhas.append(
                f"{indice} {x_centro:.6f} {y_centro:.6f} "
                f"{largura_caixa:.6f} {altura_caixa:.6f}"
            )

        nome_txt = os.path.splitext(arquivo)[0] + ".txt"

        caminho_txt = os.path.join(pasta_labels, nome_txt)

        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))

        total += 1

    print(f"{pasta_original}: {total} anotações convertidas.")


if __name__ == "__main__":
    for origem, destino in DIVISOES.items():
        converter_anotacoes(origem, destino)

    print("Conversão finalizada!")