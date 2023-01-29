import json
from tqdm import tqdm

from PIL import Image

import torch
import clip
import faiss

from src.encode_image import encode_image

# check device
device = "cuda" if torch.cuda.is_available() else "cpu"

# load model and image preprocessing
model, preprocess = clip.load("./resources/ViT-B-32.pt", device=device, jit=False)

# read dataframe
with open("./data/id_image.json", "r") as f:
    data = json.load(f)


# Create Index
index = faiss.IndexFlatL2(512)  # build the index
index = faiss.IndexIDMap(index)
print(index.ntotal)
print(index.is_trained)


fea_indexes = []
error_indexes = []
for idx, name in tqdm(data):
    try:
        image = Image.open(f"./data/oxbuild_images-v1/{name}")
        image_features = encode_image(image, model, preprocess, device)

        index.add_with_ids(image_features, [idx])
        fea_indexes.append(idx)
    except Exception:
        error_indexes.append(idx)
        continue
print(index.ntotal)

faiss.write_index(index, "./resources/oxford5k_clip_index")
