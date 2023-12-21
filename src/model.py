import torch
import torch.nn as nn
import torchvision.models as models
import numpy as np


class FeatureExtractor(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.resnet50(weights="IMAGENET1K_V2")
        # Get the layers of the model
        self.modules = list(self.model.children())[:-1]
        self.model = nn.Sequential(*self.modules)
        self.model = self.model.eval()
        self.feature_size = 2048  # the length of the feature vector

    def forward(self, batch):
        # Pass the image through the Resnet50 model and get the feature maps of the input image
        with torch.no_grad():
            feature = self.model(batch)
            feature = torch.flatten(feature, start_dim=1)

        np_feature = feature.cpu().detach().numpy()

        # Return features to numpy array
        return np_feature / np.linalg.norm(np_feature, axis=1, keepdims=True)
