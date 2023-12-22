from pathlib import Path
import torch

data_path = Path("landmark_images")
annotation_path = Path("annotation")
index_path = Path("index") / "Vietnam46Attr_full.resnet50_IP.bin"

device = "cuda" if torch.cuda.is_available() else "cpu"
