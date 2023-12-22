import faiss
import pickle
from torchvision import transforms


def create_index(shape, metrics):
    if metrics == "L2":
        index = faiss.IndexFlatL2(shape)
    elif metrics == "IP":
        index = faiss.IndexFlatIP(shape)
    else:
        raise ValueError("metrics must be either L2 or IP")
    return index


def write_index(index, index_path):
    faiss.write_index(index, index_path)


def read_index(index_path):
    index = faiss.read_index(index_path)
    return index


def load_dict(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)


def save_dict(dict, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(dict, f)


def serialize_str(name):
    return name.lower().replace(" ", "_")


def deserialize_str(name):
    return name.replace("_", " ").title()


def get_created_time(path):
    return path.stat().st_mtime


transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)
