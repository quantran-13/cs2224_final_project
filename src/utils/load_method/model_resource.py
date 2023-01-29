import time
import logging

from src.utils.load_method.load_utils import register_load_method
from src.models.clip_model import load_clip_model as load_model


utils_logger = logging.getLogger("utils_logger")


@register_load_method
def load_clip_model(model_weights: str):
    print("Loading CLIP model...")
    t1 = time.time()
    model = load_model(model_weights)
    t2 = time.time()
    utils_logger.info(f"CLIP model loading success in {t2 - t1}s.")

    return model
