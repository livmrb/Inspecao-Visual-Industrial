from ultralytics import YOLO
from pathlib import Path

modelo = YOLO(
    "runs/detect/runs/detect/neu_det/weights/best.pt"
)

pasta_imagens = Path("dataset/NEU-DET/images/val")
pasta_labels = Path("dataset/NEU-DET/labels/val")

imagens = sorted(pasta_imagens.glob("*.jpg"))[:5]

resultados = modelo.predict(
    source=[str(imagem) for imagem in imagens],
    conf=0.10,
    imgsz=320,
    save=False
)


def calcular_iou(caixa1, caixa2):
    x1 = max(caixa1[0], caixa2[0])
    y1 = max(caixa1[1], caixa2[1])
    x2 = min(caixa1[2], caixa2[2])
    y2 = min(caixa1[3], caixa2[3])

    intersecao = max(0, x2 - x1) * max(0, y2 - y1)

    area1 = (caixa1[2] - caixa1[0]) * (caixa1[3] - caixa1[1])
    area2 = (caixa2[2] - caixa2[0]) * (caixa2[3] - caixa2[1])

    uniao = area1 + area2 - intersecao

    return intersecao / uniao if uniao > 0 else 0


for resultado in resultados:
    nome = Path(resultado.path).name
    arquivo_label = pasta_labels / (Path(nome).stem + ".txt")

    altura, largura = resultado.orig_shape

    reais = []

    with open(arquivo_label, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.split()

            classe = int(partes[0])
            xc, yc, w, h = map(float, partes[1:5])

            reais.append({
                "classe": classe,
                "caixa": [
                    (xc - w / 2) * largura,
                    (yc - h / 2) * altura,
                    (xc + w / 2) * largura,
                    (yc + h / 2) * altura
                ]
            })

    previstas = []

    for caixa in resultado.boxes:
        previstas.append({
            "classe": int(caixa.cls[0]),
            "confianca": float(caixa.conf[0]),
            "caixa": caixa.xyxy[0].tolist()
        })

    previstas.sort(key=lambda x: x["confianca"], reverse=True)

    usadas = set()
    verdadeiros_positivos = 0
    falsos_positivos = 0

    for previsao in previstas:
        melhor_iou = 0
        melhor_indice = None

        for indice, real in enumerate(reais):
            if indice in usadas:
                continue

            if previsao["classe"] != real["classe"]:
                continue

            iou = calcular_iou(
                previsao["caixa"],
                real["caixa"]
            )

            if iou > melhor_iou:
                melhor_iou = iou
                melhor_indice = indice

        if melhor_indice is not None and melhor_iou >= 0.5:
            verdadeiros_positivos += 1
            usadas.add(melhor_indice)
        else:
            falsos_positivos += 1

    falsos_negativos = len(reais) - verdadeiros_positivos

    print(f"\nImagem: {nome}")
    print(f"Verdadeiros positivos: {verdadeiros_positivos}")
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")

print("\nDiagnóstico concluído!")