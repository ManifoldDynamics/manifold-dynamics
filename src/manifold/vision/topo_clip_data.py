import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
from transformers import DistilBertTokenizer
from manifold.core.io import ManifoldTensor
import os
import sys

# Mock Text Labels (Used in __getitem__ for pairing)
MOCK_TEXTS = [
    "A highly exposed summit with high wind risk",
    "A quiet, concave hollow perfect for cover",
    "Flat terrain suitable for landing zone",
    "Rugged, chaotic boulder field with sharp edges"
]

class TopoClipDataset(Dataset):
    """
    PyTorch Dataset class for loading Manifold Tensor data and paired text.
    It slices the massive MFT tensor into smaller training patches.
    """
    def __init__(self, mft_filepath, text_data=MOCK_TEXTS, patch_size=256):
        print(f"Loading full tensor from {mft_filepath}...")
        self.tensor = ManifoldTensor.load(mft_filepath)
        self.patch_size = patch_size
        self.text_data = text_data
        
        # Combine Elevation (1, R, C) and Derived (6, R, C) into one 7-channel array
        self.full_feature_map = np.concatenate(
            (self.tensor.elevation[np.newaxis, :], self.tensor.derived), axis=0
        )
        
        self.num_rows, self.num_cols = self.tensor.elevation.shape
        
        # Define total items to yield (simulates 100 random samples per text label)
        self.num_samples = len(self.text_data) * 100
        
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # --- 1. SAMPLE RANDOM MAP PATCH ---
        # Ensure the patch stays within the bounds of the massive map
        r_start = np.random.randint(0, self.num_rows - self.patch_size)
        c_start = np.random.randint(0, self.num_cols - self.patch_size)
        
        # Slice the 7-channel tensor (Channels, H, W)
        map_patch = self.full_feature_map[:, 
                                          r_start : r_start + self.patch_size, 
                                          c_start : c_start + self.patch_size]
        
        # Convert to PyTorch tensor
        terrain_tensor = torch.from_numpy(map_patch).float()

        # --- 2. SELECT PAIRED TEXT ---
        # Cycle through the text labels based on the index
        text = self.text_data[idx % len(self.text_data)]
        
        # Encode the text
        encoded_text = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=128,
            return_tensors='pt'
        )
        
        # Squeeze removes the batch dimension created by the tokenizer
        input_ids = encoded_text.input_ids.squeeze(0)
        attention_mask = encoded_text.attention_mask.squeeze(0)
        
        return terrain_tensor, input_ids, attention_mask

# --- MODULE TESTER (Optional) ---
if __name__ == '__main__':
    # Add a check here if needed, but the main script handles the core logic.
    pass