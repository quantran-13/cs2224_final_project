from PIL import Image

import torch

from src.const.global_map import RESOURCE_MAP
from src.utils.image_utils import base64_to_image


def encode_image(image: Image.Image, model, preprocess, device):
    # pre-process image
    image = preprocess(image).unsqueeze(0).to(device)  # torch.Size([1, 3, 224, 224])
    with torch.no_grad():
        image_features = model.encode_image(image)  # torch.Size([1, 512])

    return image_features


def encode_image_func(base64_image: str) -> list[float]:
    image = base64_to_image(base64_image)

    image_features = RESOURCE_MAP["clip_model"].encode_image(image=image)

    return image_features.cpu().squeeze().tolist()  # 512
