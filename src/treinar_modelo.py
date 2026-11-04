from ultralytics import YOLO

# Carregar o modelo YOLOv8 Nano pré-treinado
model = YOLO("yolov8n.pt")

# Iniciar o treinamento
resultados = model.train(
    data="dataset/NEU-DET/data.yaml",
    epochs=20,
    imgsz=320,
    batch=4,
    device="cpu",
    workers=0,
    project="runs/detect",
    name="neu_det"
)

print("Treinamento finalizado!")