from torch.utils.data import Dataset

from PIL import Image
from src.utils import get_created_time

from src.env import data_path


def scan_image_list():
    imlist = dict()
    landmark_paths = list(data_path.iterdir())

    landmark_paths.sort(key=get_created_time)

    for lm_path in landmark_paths:
        landmark_name = lm_path.name
        imlist[landmark_name] = []

        file_paths = list(lm_path.iterdir())
        file_paths.sort(key=get_created_time)

        for file in file_paths:
            if file.suffix in [".jpg", ".jpeg", ".png"]:
                imlist[landmark_name].append(file.name)
    return imlist


class Vietnam46AttrDataset(Dataset):
    def __init__(self, transform=None):
        self.imlist = scan_image_list()
        self.landmarks = list(self.imlist.keys())
        self.lengths = [len(value) for value in self.imlist.values()]
        self.image_loc = self._load_data()
        self.transform = transform

    def reload(self):
        self.imlist = scan_image_list()
        self.landmarks = list(self.imlist.keys())
        self.lengths = [len(value) for value in self.imlist.values()]
        self.image_loc = self._load_data()

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
        return img, str(img_path)

    def _load_data(self):
        images_loc = []
        for landmark in self.landmarks:
            for filename in self.imlist[landmark]:
                image_path = data_path / landmark / filename
                images_loc.append(image_path)
        return images_loc
