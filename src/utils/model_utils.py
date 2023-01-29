import os
import random
import numpy as np

import torch


def seed_everything(seed: int, train: bool = False) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    if train:
        # for faster training, but not deterministic
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.fastest = True
