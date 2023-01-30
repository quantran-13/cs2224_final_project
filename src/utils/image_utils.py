import io
import base64
import codecs
import numpy as np

from PIL import Image


def base64_to_image(byte64_str: str, grayscale: bool = False) -> Image.Image:
    bytearr = codecs.decode(
        codecs.encode(byte64_str, encoding="ascii"), encoding="base64"
    )

    if grayscale:
        return Image.open(io.BytesIO(bytearr)).convert("L")

    return Image.open(io.BytesIO(bytearr)).convert("RGB")


def image_to_base64(image0: np.ndarray, grayscale: bool = False) -> str:
    """
    Convert numpy image to base64 encode

    Args:
        image0 (np.ndarray): _description_

    Returns:
        str: _description_
    """

    if grayscale:
        image = Image.fromarray(image0, "L")
    else:
        image = Image.fromarray(image0, "RGB")

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")

    return base64.b64encode(buffered.getvalue()).decode()


def read_image(path: str) -> np.ndarray:
    """
    Read image to RGB order.

    Args:
        path (str): path to image file location.

    Returns:
        numpy.adarray
    """

    image = Image.open(path).convert("RGB")

    # numpy array format (H, W, C=3), channel order RGB
    return np.asarray(image)
