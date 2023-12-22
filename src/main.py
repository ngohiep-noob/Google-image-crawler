from src.utils import read_index
from src.env import index_path
from src.dataset import Vietnam46AttrDataset
from src.model import FeatureExtractor
from src.utils import read_index
from src.retriever import Retriever
from src.manager import Manager
from src.env import index_path, device


index = read_index(str(index_path))
print(f"Index loaded! Shape: {index.ntotal}")

extractor = FeatureExtractor().to(device)
print("Model loaded!")

view_ds = Vietnam46AttrDataset(transform=None)
print("Dataset loaded!")


retriever = Retriever(view_ds, index, extractor)
manager = Manager(view_ds, index, extractor)
