import json


clip_models = {
    # "RN50",
    # "RN101",
    # "RN50x4",
    # "RN50x16",
    # "RN50x64",
    "ViT-B-32": 512,
    # "ViT-B/16",
    # "ViT-L/14",
    # "ViT-L/14@336px",
}


indexes = ["oxford5k_clip"]


with open("./data/id_image.json", "r") as f:
    data = json.load(f)

id_mapping = {_[0]: _[1] for _ in data}
id_mapping_reverse = {_[1]: _[0] for _ in data}
