import os
import logging

from PIL import Image

import clip
import torch


utils_logger = logging.getLogger("utils_logger")


class CLIPModel:
    def __init__(self, model_weights: str):
        utils_logger.info("Loading CLIP model...")

        if not os.path.exists(model_weights):
            raise FileNotFoundError(
                f"{model_weights} should be in resource folder. If not, please download if first and committed."
            )

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model, preprocess = clip.load(model_weights, device=device, jit=False)
        utils_logger.info(
            "Using CLIP pretrained {} and running on {}".format(model_weights, device)
        )

        self.model = model
        self.preprocess = preprocess
        self.device = device

    def encode_image(self, image: Image.Image, norm: bool = False) -> torch.Tensor:
        image = (
            self.preprocess(image).unsqueeze(0).to(self.device)
        )  # torch.Size([1, 3, 224, 224])

        with torch.no_grad():
            image_features = self.model.encode_image(image)  # torch.Size([1, 512])
            if norm:
                image_features /= image_features.norm(dim=-1, keepdim=True)
            image_features = image_features.float()

        return image_features

    def batch_encode_images(
        self,
        image_list: list[Image.Image],
        norm: bool = False,
    ) -> torch.Tensor:
        image_inputs = [self.preprocess(image).to(self.device) for image in image_list]
        image_inputs = torch.stack(image_inputs)  # (N,3,224,224)

        with torch.no_grad():
            all_image_features = self.model.encode_image(image_inputs)
            all_image_features = all_image_features.float()

        del image_inputs
        return all_image_features


def load_clip_model(model_weights: str) -> CLIPModel:
    try:
        model = CLIPModel(model_weights=model_weights)
        return model
    except FileNotFoundError as E:
        raise FileNotFoundError(
            f"{E}. Please check again where the model stored and config file."
        )
