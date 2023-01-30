from src.const.global_map import RESOURCE_MAP
import src.const.const_map as CONST_MAP
from src.utils.image_utils import base64_to_image
from src.utils.faiss_utils import search_faiss_index
from src.utils.image_utils import read_image, image_to_base64
from src.render_image import (
    _label_content_start,
    _label_content_li_start,
    _label_content_li_nested,
    _label_content_li_end,
    _label_content_end,
)


def search_image_func(
    base64_image: str,
    index_name: str,
    top_results: int,
) -> tuple[list[float], ...]:
    image = base64_to_image(base64_image)

    # image.save("test.jpg")

    image_features = RESOURCE_MAP["clip_model"].encode_image(image=image)
    image_features = image_features.cpu().numpy()

    dists, ids = search_faiss_index(
        arr=image_features, index_name=index_name, top_k=top_results
    )

    return dists.tolist(), ids.tolist()


def search_image_func_return_image(
    base64_image: str,
    index_name: str,
    top_results: int,
) -> str:
    dists, ids = search_image_func(
        base64_image=base64_image,
        index_name=index_name,
        top_results=top_results,
    )

    label_card = _label_content_start
    for d, i in zip(dists, ids):
        idx = CONST_MAP.id_mapping[i]

        image = read_image(f"data/oxbuild_images-v1/{idx}")
        image_base64 = image_to_base64(image)

        label_card += _label_content_li_start.format(image_base64)
        label_card += _label_content_li_nested.format(idx, d)
        label_card += _label_content_li_end

    label_card += _label_content_end

    return label_card
