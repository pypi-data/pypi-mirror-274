from pathlib import Path

from torch.utils.data import DataLoader
from torchvision import datasets

from onepiece_classify.transforms import (
    get_test_transforms,
    get_train_transforms,
    get_valid_transforms,
)


class OnepieceImageDataLoader:
    def __init__(self, root_path: str, batch_size: int = 32, num_workers: int = 0):
        self.root_path: Path = Path(root_path)
        self.train_path: Path = self.root_path.joinpath("train")
        self.valid_path: Path = self.root_path.joinpath("val")
        self.test_path: Path = self.root_path.joinpath("test")

        self.batch_size = batch_size
        self.num_workers = num_workers

        self.trainset = self._build_dataset(mode="train")
        self.validset = self._build_dataset(mode="valid")
        self.testset = self._build_dataset(mode="test")

        self.train_loader = self._build_dataloader(mode="train", shuffle=True)
        self.valid_loader = self._build_dataloader(mode="valid", shuffle=False)
        self.test_loader = self._build_dataloader(mode="test", shuffle=False)

    def _build_dataset(self, mode="train") -> datasets.ImageFolder:
        dset = None
        if mode == "train":
            trans = get_train_transforms()
            path = self.train_path
        elif mode == "valid":
            trans = get_valid_transforms()
            path = self.valid_path
        elif mode == "test":
            trans = get_test_transforms()
            path = self.test_path
        else:
            trans = get_test_transforms()
            path = self.test_path

        dset = datasets.ImageFolder(str(path), transform=trans)
        return dset

    def _build_dataloader(
        self, mode: str = "train", shuffle: bool = True
    ) -> DataLoader:
        if mode == "train":
            dset = self.trainset
        elif mode == "valid":
            dset = self.validset
        elif mode == "test":
            dset = self.testset
        else:
            dset = self.testset

        loader = DataLoader(
            dset, batch_size=self.batch_size, shuffle=shuffle, pin_memory=True
        )

        return loader
