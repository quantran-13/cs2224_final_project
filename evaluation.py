import json
import pandas as pd

from PIL import Image

import torch
import clip
import faiss

from src.encode_image import encode_image


def AP_at_k(predict_result: list[str], groundtruth: list[str], k: int):
    ap = 0
    topk_correct = 0
    N = min(k, len(groundtruth))
    for id, _ in enumerate(predict_result[:N], start=1):
        if _ in groundtruth:
            topk_correct += 1
            ap += topk_correct / id

    return ap / N


# check device
device = "cuda" if torch.cuda.is_available() else "cpu"

# load model and image preprocessing
model, preprocess = clip.load("./resources/ViT-B-32.pt", device=device, jit=False)


index = faiss.read_index("./resources/oxford5k_clip_index")


with open("./data/id_image.json", "r") as f:
    data = json.load(f)

id_mapping = {_[0]: _[1] for _ in data}
id_mapping_reverse = {_[1]: _[0] for _ in data}
df = pd.read_csv("./data/data.csv")



ap_10s, ap_20s, ap_50s, ap_100s = [], [], [], [] 
for id, row in df.iterrows():
    row = row.to_dict()

    image = Image.open(f"./data/oxbuild_images-v1/{row['image_name']}")
    image_features = encode_image(image, model, preprocess, device)

    dists, ids = index.search(image_features, k=100)

    list_result = [id_mapping[_].split(".")[0] for _ in ids[0]]
    list_good = row["good"][1:-1].replace("'", "").split(", ")

    ap_10 = AP_at_k(list_result, list_good, k=10)
    ap_20 = AP_at_k(list_result, list_good, k=20)
    ap_50 = AP_at_k(list_result, list_good, k=50)
    ap_100 = AP_at_k(list_result, list_good, k=100)
    ap_10s.append(ap_10)
    ap_20s.append(ap_20)
    ap_50s.append(ap_50)
    ap_100s.append(ap_100)


map_10 = sum(ap_10s)/len(ap_10s)
map_20 = sum(ap_20s)/len(ap_20s)
map_50 = sum(ap_50s)/len(ap_50s)
map_100 = sum(ap_100s)/len(ap_100s)

print("MAP@10 = ", map_10 * 100)
print("MAP@20 = ", map_20 * 100)
print("MAP@50 = ", map_50 * 100)
print("MAP@100 = ", map_100 * 100)