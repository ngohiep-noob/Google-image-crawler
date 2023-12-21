from src.model import FeatureExtractor
from src.dataset import Vietnam46AttrDataset
from torchvision import transforms
import torch
from src.utils import read_index
from src.env import index_path

device = "cuda" if torch.cuda.is_available() else "cpu"

transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


class Retriever:
    def __init__(self):
        self.index = read_index(str(index_path / "Vietnam46Attr.resnet50_IP.bin"))
        print(f"Index loaded! Shape: {self.index.ntotal}")
        self.extractor = FeatureExtractor().to(device)
        print("Model loaded!")
        self.view_ds = Vietnam46AttrDataset(transform=None)
        print("Dataset loaded!")

    def get_view(self, idx):
        return self.view_ds[idx]

    def retrieve(self, query_img, k):
        img = transform(query_img)
        img = img.unsqueeze(0).to(device)

        feat = self.extractor(img)
        distance, indices = self.index.search(feat, k)

        return indices[0].tolist(), distance[0].tolist()
