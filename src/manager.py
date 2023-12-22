from src.utils import serialize_str, deserialize_str, write_index
from src.env import data_path, index_path, device
from PIL import Image
from src.dataset import Vietnam46AttrDataset
from src.utils import transform
import torch
from faiss import IndexFlatL2, IndexFlatIP


def images_to_batch(images: list[Image.Image]):
    batch = []
    for image in images:
        batch.append(transform(image))

    return torch.stack(batch)


class Manager:
    def __init__(
        self,
        view_ds: Vietnam46AttrDataset,
        index: IndexFlatL2 | IndexFlatIP,
        extractor: torch.nn.Module,
    ):
        self.view_ds = view_ds
        self.index = index
        self.extractor = extractor

    def get_landmark_list(self):
        name_list = []
        for folder in data_path.iterdir():
            if folder.is_dir():
                name_list.append(deserialize_str(folder.name))

        return name_list

    def images_in_landmark(self, landmark_name: str):
        lm_folder = data_path / serialize_str(landmark_name)

        if not lm_folder.exists():
            raise Exception("Landmark does not exist!")

        image_paths = list(lm_folder.iterdir())

        images = []
        for image_path in image_paths:
            images.append(Image.open(image_path))

        return images

    def create_landmark(
        self,
        name: str,
    ):
        # create a new folder
        lm_folder = data_path / serialize_str(name)

        if lm_folder.exists():
            raise Exception("Landmark already exists")

        lm_folder.mkdir()

    def save_index(self):
        write_index(index=self.index, index_path=str(index_path))

    def add_images_to_landmark(self, landmark_name: str, images: list[Image.Image]):
        lm_folder = data_path / serialize_str(landmark_name)

        if not lm_folder.exists():
            raise Exception("Landmark does not exist!, Please create it first")

        if len(images) > 10:
            raise Exception("Cannot add more than 10 images at once")
        n_existing_imgs = len(list(lm_folder.iterdir()))
        new_indices = range(n_existing_imgs, n_existing_imgs + len(images))

        # save images to disk
        for image, idx in zip(images, new_indices):
            image.save(lm_folder / f"{idx}.jpg")

        # reload dataset
        self.view_ds.reload()

        # add images to index
        batch = images_to_batch(images).to(device)

        features = self.extractor(batch)

        self.index.add(features)

        # save index
        self.save_index()
        print(f"Added {len(images)} images to index")
