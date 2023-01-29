import time
import logging
import numpy as np

import faiss

from src.const.global_map import RESOURCE_MAP
from src.utils.load_method.load_utils import register_load_method


utils_logger = logging.getLogger("utils_logger")


def get_index(index_name: str):
    index = RESOURCE_MAP[f"{index_name}_index"]
    return index


def write_faiss_index(index_name: str) -> None:
    index = get_index(index_name)
    faiss.write_index(index, RESOURCE_MAP[f"{index_name}_index"]["args"]["index_file"])


@register_load_method
def load_faiss_index(index_file: str) -> None:
    print(f"Loading Faiss index {index_file} ...")
    t1 = time.time()
    index = faiss.read_index(index_file)
    t2 = time.time()
    utils_logger.info(f"Faiss index {index_file} loading success in {t2 - t1}s.")

    return index


def add_to_faiss_index(arr: np.array, idx: int, index_name: str):
    index = get_index(index_name)

    index_idx = np.array([idx])
    index.remove_ids(index_idx)
    utils_logger.info("Post %s: Add to index %s: Remove old vector" % (idx, index_name))

    index.add_with_ids(arr, index_idx)
    utils_logger.info(
        "ID %s: Add to index %s: array shape %s" % (idx, index_name, arr.shape)
    )
    write_faiss_index(index_name)


def search_faiss_index(arr: np.array, index_name: str, top_k: int = 10):
    index = get_index(index_name)

    dists, ids = index.search(arr, k=top_k)

    return dists[0], ids[0]
