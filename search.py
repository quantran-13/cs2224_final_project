import json
import pandas as pd

from PIL import Image

import torch
import clip
import faiss

from src.encode_image import encode_image


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

test_case = df.iloc[0].to_dict()

image = Image.open(f"./data/oxbuild_images-v1/{test_case['image_name']}")
image_features = encode_image(image, model, preprocess, device)

dists, ids = index.search(image_features, k=10)

print([id_mapping[_] for _ in ids[0]])
print(test_case["good"])


def total_metrics(train_embs, train_labels, test_embs, test_labels, top_k=5):
    topk_correct = 0
    mapk = []
    for emb, label in zip(test_embs, test_labels):
        dists = cdist(np.expand_dims(emb, axis=0), train_embs, metric="euclidean")[0]
        min_dist_indexes = dists.argsort()[:top_k]
        pred_labels = train_labels[min_dist_indexes]
        mapk.append(map_per_image(str(label), list(map(str, pred_labels))))

        if label in pred_labels:
            topk_correct += 1

    topk_value = topk_correct / test_embs.shape[0]
    mapk = np.mean(mapk)
    print(">>> Top{} acc: {:.4f}".format(top_k, topk_value))
    print(">>> Map@{}: {:.4f}".format(top_k, mapk))

    return topk_value, mapk
