from torch.utils.data import Dataset
from src.load_data import imlist
from PIL import Image

from src.env import data_path


class Vietnam46AttrDataset(Dataset):
    def __init__(self, transform=None):
        self.imlist = imlist
        self.landmarks = list(imlist.keys())
        self.lengths = [len(value) for value in imlist.values()]
        self.image_loc = self._load_data()
        self.transform = transform

    def __len__(self):
        return sum(self.lengths)

    def _get_filepath(self, idx):
        return self.image_loc[idx]

    def __getitem__(self, index):
        img_path = self._get_filepath(index)
        img = Image.open(img_path)
        img = img.convert("RGB")

        if self.transform:
            img = self.transform(img)
        return img, img_path

    def _load_data(self):
        images_loc = []
        for landmark in self.landmarks:
            for filename in self.imlist[landmark]:
                image_path = data_path / landmark / filename
                images_loc.append(image_path)
        return images_loc
