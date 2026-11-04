# Inspeção Visual Industrial com YOLO + Streamlit

## Sobre o projeto

Este projeto tem como objetivo desenvolver um sistema de inspeção visual industrial utilizando técnicas de Visão Computacional e Inteligência Artificial para identificar defeitos em produtos.

A solução utilizará modelos YOLO para detecção de objetos e anomalias, integrados a uma interface web desenvolvida com Streamlit.

O sistema permitirá o envio de imagens e vídeos para análise, a visualização dos resultados de detecção e a apresentação de indicadores sobre a qualidade dos produtos inspecionados.

## Objetivos

- Detectar defeitos em produtos por meio de imagens e vídeos.
- Utilizar modelos YOLO para identificação e localização de anomalias.
- Exibir os resultados por meio de uma interface interativa.
- Apresentar estatísticas de produtos conformes e não conformes.
- Permitir a exportação dos resultados e relatórios.

## Tecnologias utilizadas

- Python 3.11.9
- YOLO (Ultralytics)
- OpenCV
- Streamlit
- PyTorch
- Pandas
- Plotly
- ReportLab

## Estrutura do projeto

```text
Inspecao-Visual-Industrial/
│
├── dataset/          # Imagens e anotações
├── models/           # Modelos treinados
├── src/              # Código-fonte
├── reports/          # Relatórios gerados
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
├── README.md         # Documentação
└── .gitignore        # Arquivos ignorados pelo Git
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

### 6. Executar a aplicação

```bash
streamlit run app.py
```

A aplicação poderá ser acessada pelo navegador no endereço:

http://localhost:8501

## Equipe

- Alexandre Toscano
- Arthur Cavalcante
- João Pedro Alexandre
- Lívia Barbosa
- Pedro Holanda

## Disciplina

Tópicos Especiais em TI