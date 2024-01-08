import torch
import torch.nn as nn
import torchvision.models as models
import numpy as np


class MobileNetV3Extractor(nn.Module):
    def __init__(self):
        super(MobileNetV3Extractor, self).__init__()
        self.model = torch.hub.load(
            "pytorch/vision:v0.10.0", "mobilenet_v3_large", pretrained=True
        )
        self.model.eval()
        self.model.classifier[-1].register_forward_hook(self.output_hook)

    def output_hook(self, module, input, output):
        self.feature = input[0]

    def forward(self, x):
        self.model(x)
        return self.feature


class InceptionV3Extractor(nn.Module):
    def __init__(self):
        super(InceptionV3Extractor, self).__init__()
        self.model = torch.hub.load(
            "pytorch/vision:v0.10.0", "inception_v3", pretrained=True
        )
        self.model.eval()
        self.model.Mixed_7c.register_forward_hook(self.output_hook)

    def output_hook(self, module, input, output):
        self.mixed_7c_output = output

    def forward(self, x):
        assert x.shape[1:] == (
            3,
            299,
            299,
        ), "Expected input shape to be: (N,3,299,299)" + ", but got {}".format(x.shape)
        x = x * 2 - 1  # Normalize to [-1, 1]

        # Trigger output hook
        self.model(x)

        # Output: N x 2048 x 1 x 1
        activations = self.mixed_7c_output
        activations = nn.functional.adaptive_avg_pool2d(activations, (1, 1))
        activations = activations.view(x.shape[0], 2048)
        return activations


def get_model(model_name="resnet50"):
    model = None
    feature_size = None
    match model_name:
        case "resnet50":
            model = models.resnet50(weights="IMAGENET1K_V2")
            modules = list(model.children())[:-1]
            model = nn.Sequential(*modules)
            feature_size = 2048
        case "resnet101":
            model = models.resnet101(weights="IMAGENET1K_V2")
            modules = list(model.children())[:-1]
            model = nn.Sequential(*modules)
            feature_size = 2048
        case "inceptionv3":
            model = InceptionV3Extractor()
            feature_size = 2048
        case "mobilenetv3":
            model = MobileNetV3Extractor()
            feature_size = 1280
        case _:
            raise ValueError("Model not found")

    model = model.eval()
    return model, feature_size


class FeatureExtractor(torch.nn.Module):
    def __init__(self, model_name="resnet50"):
        super().__init__()
        self.model, self.feature_size = get_model(model_name=model_name)

    def forward(self, batch):
        # Pass the image through the Resnet50 model and get the feature maps of the input image
        with torch.no_grad():
            feature = self.model(batch)
            feature = torch.flatten(feature, start_dim=1)

        np_feature = feature.cpu().detach().numpy()

        # Return features to numpy array
        return np_feature / np.linalg.norm(np_feature, axis=1, keepdims=True)
