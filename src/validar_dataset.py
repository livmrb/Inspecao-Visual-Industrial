from pathlib import Path

BASE = Path("dataset/NEU-DET/labels")
DIVISOES = ["train", "val"]
NUM_CLASSES = 6

for divisao in DIVISOES:
    pasta = BASE / divisao

    total_caixas = 0
    erros = []

    for arquivo in pasta.glob("*.txt"):
        with open(arquivo, "r", encoding="utf-8") as f:
            for numero, linha in enumerate(f, start=1):
                partes = linha.split()

                if len(partes) != 5:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: formato inválido"
                    )
                    continue

                try:
                    classe = int(partes[0])
                    x, y, largura, altura = map(float, partes[1:])
                except ValueError:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: valor inválido"
                    )
                    continue

                if not 0 <= classe < NUM_CLASSES:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: classe inválida"
                    )

                if not all(0 <= v <= 1 for v in [x, y, largura, altura]):
                    erros.append(
                        f"{arquivo.name}, linha {numero}: coordenada fora do intervalo"
                    )

                if largura <= 0 or altura <= 0:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: caixa sem dimensão válida"
                    )

                if x - largura / 2 < 0 or x + largura / 2 > 1:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: caixa ultrapassa a largura"
                    )

                if y - altura / 2 < 0 or y + altura / 2 > 1:
                    erros.append(
                        f"{arquivo.name}, linha {numero}: caixa ultrapassa a altura"
                    )

                total_caixas += 1

    print(f"\n--- {divisao.upper()} ---")
    print(f"Caixas analisadas: {total_caixas}")
    print(f"Problemas encontrados: {len(erros)}")

    for erro in erros[:20]:
        print(erro)

    if not erros:
        print("Todas as anotações passaram na validação!")