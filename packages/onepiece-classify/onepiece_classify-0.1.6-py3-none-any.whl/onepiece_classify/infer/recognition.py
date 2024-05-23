import os
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import torch
from PIL import Image

from onepiece_classify.models import image_recog
from onepiece_classify.transforms import get_test_transforms
from onepiece_classify.utils import downloader

from .base import BaseInference


class ImageRecognition(BaseInference):
    def __init__(self, device: str, model_path=None):

        path_to_save = str(self._get_cache_dir()) + "/model.pth"
        if model_path is None:
            downloader(path_to_save)
            self.model_path = path_to_save
        else:
            self.model_path = Path(model_path)
            if not self.model_path.exists():
                raise FileNotFoundError("Model does not exist, check your model location and read README for more information")

        self.device = device
        self.class_dict = {
            0: "Ace",
            1: "Akainu",
            2: "Brook",
            3: "Chopper",
            4: "Crocodile",
            5: "Franky",
            6: "Jinbei",
            7: "Kurohige",
            8: "Law",
            9: "Luffy",
            10: "Mihawk",
            11: "Nami",
            12: "Rayleigh",
            13: "Robin",
            14: "Sanji",
            15: "Shanks",
            16: "Usopp",
            17: "Zoro",
        }
        self.nclass = len(self.class_dict)
        self.model = self._build_model()

    def _build_model(self):
        # load model
        state_dict = torch.load(self.model_path, map_location=self.device)
        model_backbone = image_recog(self.nclass)
        model_backbone.load_state_dict(state_dict)
        return model_backbone
    
    def _get_cache_dir(self):
        if sys.platform.startswith("win"):
            cache_dir = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "OnepieceClassifyCache"
        else:
            cache_dir = Path.home() / ".cache" / "OnepieceClassifyCache"

        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def pre_process(
        self, image: Optional[str | np.ndarray | Image.Image]
    ) -> torch.Tensor:
        trans = get_test_transforms()

        if isinstance(image, str):
            img = Image.open(image).convert("RGB")
            img = trans(img).unsqueeze(0)

        elif isinstance(image, Image.Image):
            img = image.convert("RGB")
            img = trans(img).unsqueeze(0)

        elif isinstance(image, np.ndarray):
            img = image.astype(np.uint8)
            img = Image.fromarray(img).convert("RGB")
            img = trans(img).unsqueeze(0)

        else:
            print("Image type not recognized")

        return img.to(self.device)

    def forward(self, image_tensor: torch.Tensor) -> torch.Tensor:
        self.model.eval()

        result = self.model(image_tensor)
        return result

    def post_process(self, output: torch.Tensor) -> Tuple[str, float]:
        logits_prob = torch.softmax(output, dim=1).squeeze()
        class_idx = int(torch.argmax(logits_prob))

        class_names = self.class_dict[class_idx]
        confidence = logits_prob[class_idx]
        return (class_names, float(confidence))

    def predict(
        self, image: Optional[str | np.ndarray | Image.Image]
    ) -> Dict[str, str]:
        tensor_img = self.pre_process(image=image)
        logits = self.forward(tensor_img)
        class_names, confidence = self.post_process(logits)

        return {"class_names": class_names, "confidence": f"{confidence:.4f}"}
