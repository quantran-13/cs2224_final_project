from src.const.global_map import RESOURCE_MAP
from src.utils.image_utils import base64_to_image
from src.utils.faiss_utils import search_faiss_index


def search_image_func(
    base64_image: str,
    index_name: str,
    top_results: int,
) -> list[float]:
    image = base64_to_image(base64_image)

    image_features = RESOURCE_MAP["clip_model"].encode_image(image=image)
    image_features = image_features.cpu().numpy()

    dists, ids = search_faiss_index(
        arr=image_features, index_name=index_name, top_k=top_results
    )

    return dists, ids
