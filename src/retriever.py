from src.env import device
from src.utils import transform


class Retriever:
    def __init__(
        self,
        view_ds,
        index,
        extractor,
    ):
        self.index = index
        self.extractor = extractor
        self.view_ds = view_ds

    def get_view(self, idx):
        return self.view_ds[idx]

    def retrieve(self, query_img, k):
        img = transform(query_img)
        img = img.unsqueeze(0).to(device)

        feat = self.extractor(img)
        distance, indices = self.index.search(feat, k)

        return indices[0].tolist(), distance[0].tolist()
