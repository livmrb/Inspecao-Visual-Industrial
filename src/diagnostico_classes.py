from pathlib import Path
from collections import Counter

BASE = Path("dataset/NEU-DET/labels")

CLASSES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches"
]

for divisao in ["train", "val"]:
    contador = Counter()

    pasta = BASE / divisao

    for arquivo in pasta.glob("*.txt"):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.split()

                if partes:
                    indice = int(partes[0])
                    contador[CLASSES[indice]] += 1

    print(f"\n--- {divisao.upper()} ---")

    for classe in CLASSES:
        print(f"{classe}: {contador[classe]}")

    print(f"Total de defeitos: {sum(contador.values())}")