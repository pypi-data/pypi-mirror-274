import torch.nn as nn
from torchvision import models


class ImageRecogModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.num_classes = num_classes

    def build_backbone(self):
        model = models.mobilenet_v3_large(weights="DEFAULT")

        for param in model.parameters():
            param.requires_grad = False

        in_features = model.classifier[0].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.2), nn.Linear(in_features, out_features=self.num_classes)
        )

        return model

    def forward(self, x):
        model = self.build_backbone()
        x = model(x)
        return x


def image_recog(num_classes):
    net = ImageRecogModel(num_classes).build_backbone()
    return net
