import torch
import torch.nn as nn
from transformers import DistilBertModel, DistilBertConfig
import numpy as np

# --- 1. TERRAIN ENCODER (Swin Transformer Placeholder) ---
# Goal: Convert the 7-channel MFT tensor (H, W, 7) into a fixed-size vector (Embedding).
class TerrainEncoder(nn.Module):
    def __init__(self, in_channels=7, embedding_dim=512):
        super().__init__()
        # In a full deployment, this would be a large Swin Transformer.
        # For the alpha architecture, we use a simple ConvNet stack as a fast proxy.
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)) # Downsample to a single point
        )
        self.projection = nn.Linear(128, embedding_dim)

    def forward(self, x):
        # Input shape must be (Batch, Channels, Height, Width)
        x = self.encoder(x)
        x = torch.flatten(x, 1)
        # Output shape: (Batch, Embedding_Dim)
        return self.projection(x)

# --- 2. TEXT ENCODER (DistilBERT) ---
# Goal: Convert a sentence ("exposed peak") into a fixed-size vector (Embedding).
class TextEncoder(nn.Module):
    def __init__(self, embedding_dim=512, model_name='distilbert-base-uncased'):
        super().__init__()
        # Load the base transformer model
        self.distilbert = DistilBertModel.from_pretrained(model_name)
        # Add a linear layer to match the required embedding size (512)
        self.projection = nn.Linear(self.distilbert.config.dim, embedding_dim)
        
    def forward(self, input_ids, attention_mask):
        # Get the hidden states
        outputs = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        # Use the CLS token output (first token) for sentence representation
        cls_token = outputs.last_hidden_state[:, 0, :] 
        return self.projection(cls_token)

# --- 3. THE UNIFIED TOPOCLIP MODEL ---
class TopoCLIP(nn.Module):
    def __init__(self, embedding_dim=512):
        super().__init__()
        self.terrain_encoder = TerrainEncoder(embedding_dim=embedding_dim)
        self.text_encoder = TextEncoder(embedding_dim=embedding_dim)

    def forward(self, terrain_tensor, input_ids, attention_mask):
        # Encoders project data into the same 512-dimensional latent space
        terrain_embedding = self.terrain_encoder(terrain_tensor)
        text_embedding = self.text_encoder(input_ids, attention_mask)
        return terrain_embedding, text_embedding

# --- MODULE TESTER (Verification) ---
if __name__ == '__main__':
    print("Verifying TopoCLIP Architecture...")
    
    # 1. Instantiate Model
    model = TopoCLIP()
    
    # 2. Mock Terrain Data (Batch=4, Channels=7, Height=1024, Width=1024)
    # The MFT tensor must be converted to (Batch, Channel, H, W) format for PyTorch
    mock_terrain_data = torch.randn(4, 7, 1024, 1024)
    
    # 3. Mock Text Data
    mock_text_ids = torch.randint(0, 1000, (4, 128)) # 4 sentences, 128 tokens long
    mock_attention_mask = torch.ones(4, 128)
    
    # 4. Run Forward Pass
    terrain_vec, text_vec = model(mock_terrain_data, mock_text_ids, mock_attention_mask)
    
    # Verification Print
    print(f"Terrain Output Shape: {terrain_vec.shape}")
    print(f"Text Output Shape:    {text_vec.shape}")
    assert terrain_vec.shape == torch.Size([4, 512])
    assert text_vec.shape == torch.Size([4, 512])
    print("Architecture Verification: PASSED. Encoders output matching 512-dim vectors.")