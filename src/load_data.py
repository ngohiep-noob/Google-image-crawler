from src.utils import load_dict
from src.env import annotation_path
from PIL import Image

ground_truth = load_dict(annotation_path / "ground_truth.pkl")

query_loc = load_dict(annotation_path / "query_loc.pkl")

imlist = load_dict(annotation_path / "imlist.pkl")


def get_query(query_idx):
    img_path = query_loc[query_idx]
    img = Image.open(img_path)
    landmark = img_path.parent.name
    return img, landmark
