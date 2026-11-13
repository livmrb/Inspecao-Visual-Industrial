# Inspeção Visual Industrial com YOLO + Streamlit

## Sobre o projeto

O projeto consiste no desenvolvimento de um sistema de inspeção visual industrial utilizando Visão Computacional e Inteligência Artificial para identificar defeitos em superfícies metálicas.

A solução utiliza o modelo YOLOv8 Nano, treinado com o dataset NEU-DET, integrado a uma aplicação web desenvolvida com Streamlit.

O sistema permite enviar imagens e vídeos para análise, localizar defeitos por meio de caixas delimitadoras (*bounding boxes*), visualizar os resultados e gerar relatórios de inspeção.

## Objetivos

- Detectar e localizar defeitos em superfícies metálicas.
- Aplicar técnicas de Deep Learning e Visão Computacional.
- Disponibilizar uma interface interativa para inspeção de imagens e vídeos.
- Apresentar indicadores sobre os defeitos identificados.
- Classificar os resultados das inspeções como conformes ou não conformes.
- Permitir a exportação dos resultados em CSV e PDF.

## Dataset

Foi utilizado o dataset **NEU-DET (Northeastern University Surface Defect Database)**, composto por imagens de superfícies metálicas com seis categorias de defeitos.

O conjunto utilizado possui:
- 1.440 imagens para treinamento.
- 360 imagens para validação.
- 6 classes de defeitos.

### Classes identificadas

| Classe | Descrição |
|---|---|
| crazing | Fissuras |
| inclusion | Inclusões |
| patches | Manchas |
| pitted_surface | Superfície com pequenos furos |
| rolled-in_scale | Incrustações de carepa |
| scratches | Arranhões |

As anotações originais foram convertidas do formato Pascal VOC (XML) para o formato YOLO (TXT).

## Tecnologias utilizadas

- Python 3.11.9
- YOLOv8 Nano (Ultralytics)
- PyTorch
- OpenCV
- Streamlit
- Pandas
- Plotly
- ReportLab
- Pillow
- FFmpeg

## Funcionalidades implementadas

### Inspeção de imagens

- Envio de imagens nos formatos JPG, JPEG e PNG.
- Identificação automática de defeitos.
- Localização dos defeitos por meio de caixas delimitadoras.
- Exibição da confiança de cada detecção.
- Comparação visual entre imagem original e imagem processada.

### Inspeção de vídeos

- Envio de vídeos no formato MP4.
- Processamento dos quadros do vídeo utilizando YOLO.
- Identificação e localização dos defeitos ao longo dos quadros.
- Comparação entre vídeo original e vídeo processado.
- Exportação do vídeo com as detecções.

### Indicadores e relatórios

- Quantidade de defeitos detectados.
- Número de quadros processados.
- Confiança média das detecções.
- Tempo de processamento.
- Quantidade de detecções por classe.
- Exportação dos resultados em CSV e PDF.

### Configurações

- Seleção do limiar mínimo de confiança.
- Utilização do modelo YOLOv8 Nano treinado com o NEU-DET.

## Resultados do treinamento

O modelo foi treinado utilizando os seguintes parâmetros:

| Parâmetro | Configuração |
|---|---|
| Arquitetura | YOLOv8 Nano |
| Épocas | 20 |
| Tamanho da imagem | 320 × 320 |
| Batch size | 4 |
| Dispositivo | GPU AMD Radeon RX 9060 XT (ROCm 6.4) |
| Dataset | NEU-DET |

Ambiente: Ultralytics 8.4.211, PyTorch 2.9.1 (ROCm 6.4), Python 3.11.

### Métricas gerais de validação

Avaliação no conjunto de validação (360 imagens, 854 defeitos anotados):

| Métrica | Resultado |
|---|---:|
| Precisão (Precision) | 0,760 |
| Revocação (Recall) | 0,604 |
| mAP@50 | 0,691 |
| mAP@50-95 | 0,351 |

Tempo de inferência: aproximadamente 1,8 ms por imagem (GPU).

### Métricas por classe

| Classe | Imagens | Instâncias | Precisão | Revocação | mAP@50 | mAP@50-95 |
|---|---:|---:|---:|---:|---:|---:|
| crazing | 60 | 162 | 1,000 | 0,015 | 0,442 | 0,163 |
| inclusion | 71 | 159 | 0,732 | 0,773 | 0,808 | 0,430 |
| patches | 73 | 193 | 0,811 | 0,860 | 0,918 | 0,574 |
| pitted_surface | 60 | 87 | 0,890 | 0,667 | 0,780 | 0,397 |
| rolled-in_scale | 60 | 132 | 0,607 | 0,439 | 0,480 | 0,225 |
| scratches | 60 | 121 | 0,518 | 0,868 | 0,721 | 0,320 |

### Análise

- As classes `patches` e `inclusion` apresentaram os melhores resultados.
- A classe `crazing` é o principal ponto fraco. (revocação de 0,015)
- A classe `rolled-in_scale` também apresenta desempenho abaixo da média.

## Estrutura do projeto

```text
Inspecao-Visual-Industrial/
│
├── dataset/
│   └── NEU-DET/
│       ├── images/
│       │   ├── train/
│       │   └── val/
│       ├── labels/
│       │   ├── train/
│       │   └── val/
│       ├── train/
│       ├── validation/
│       └── data.yaml
│
├── models/
│
├── src/
│   ├── converter_dataset.py
│   ├── organizar_dataset.py
│   ├── criar_video_teste.py
│   ├── diagnostico_classes.py
│   ├── testar_modelo.py
│   ├── treinar_modelo.py
│   └── validar_dataset.py
│
├── reports/
│
├── runs/
│   └── # Resultados e pesos do treinamento (não versionados)
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalação e configuração

### 1. Clonar o repositório

```bash
git clone https://github.com/livmrb/Inspecao-Visual-Industrial.git
```

### 2. Entrar na pasta do projeto

```bash
cd Inspecao-Visual-Industrial
```

### 3. Criar o ambiente virtual

```bash
py -3.11 -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Disponibilizar os pesos do modelo

O arquivo `best.pt` contém os pesos do modelo treinado e não é versionado no GitHub.

Para executar a aplicação sem treinar novamente, disponibilize o arquivo `best.pt` na seguinte localização:

```text
runs/detect/runs/detect/neu_det/weights/best.pt
```

Caso não tenha os pesos, é possível treinar novamente utilizando o script:

```bash
python src/treinar_modelo.py
```

### 7. Configurar o FFmpeg

O FFmpeg é utilizado para converter os vídeos para o formato H.264, garantindo compatibilidade com o player da aplicação.

Instale o FFmpeg e confira se o caminho configurado na variável `CAMINHO_FFMPEG`, no arquivo `app.py`, corresponde ao local de instalação na máquina utilizada.

### 8. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação poderá ser acessada pelo navegador no endereço:

http://localhost:8501

## Scripts auxiliares

| Script | Finalidade |
|---|---|
| converter_dataset.py | Conversão das anotações XML para o formato YOLO |
| organizar_dataset.py | Organização das imagens para treinamento e validação |
| validar_dataset.py | Verificação da integridade das imagens e anotações |
| diagnostico_classes.py | Análise da distribuição das classes |
| treinar_modelo.py | Treinamento do modelo YOLO |
| testar_modelo.py | Testes de inferência do modelo |
| criar_video_teste.py | Geração de vídeo para testes da aplicação |

## Equipe

- Alexandre Toscano
- Arthur Cavalcante
- João Pedro Alexandre
- Lívia Barbosa
- Pedro Holanda

## Disciplina

Tópicos Especiais em TI