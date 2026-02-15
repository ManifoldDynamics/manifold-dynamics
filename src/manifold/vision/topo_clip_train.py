import torch
import torch.optim as optim
import torch.nn.functional as F
import sys
import os
import argparse
from torch.utils.data import DataLoader
from .topo_clip_encoder import TopoCLIP
from .topo_clip_loss import InfoNCELoss
from .topo_clip_data import TopoClipDataset # Import the actual Dataset

# --- FINAL MOCK TEXT DATA (Matches structure used in data loader) ---
# In production, this list would be replaced by scraped, real-world data labels.
MOCK_TEXTS = [
    "A highly exposed summit with high wind risk",
    "A quiet, concave hollow perfect for cover",
    "Flat terrain suitable for landing zone",
    "Rugged, chaotic boulder field with sharp edges"
]

# --- TRAINING LOOP (Uses real data) ---
def train_topo_clip(mft_path, epochs=5, learning_rate=1e-4):
    print("--- TOPOCLIP TRAINING SIMULATION STARTED ---")
    
    if not os.path.exists(mft_path):
        print(f"ERROR: MFT file not found at {mft_path}. Please run ingest.py first.")
        return

    # 1. Initialization
    model = TopoCLIP()
    criterion = InfoNCELoss(temperature=0.07)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Use GPU if available (Essential for large data)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    print(f"Model running on device: {device}")
    
    # 2. Data Setup (Loads real MFT tensor and creates training batches)
    topo_dataset = TopoClipDataset(mft_path, MOCK_TEXTS)
    data_loader = DataLoader(topo_dataset, batch_size=4, shuffle=True, num_workers=0)
    
    print(f"Loaded {len(topo_dataset)} training patches from {mft_path}.")
    
    # 3. Training Loop Iteration
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for terrain_data, text_ids, attention_mask in data_loader:
            optimizer.zero_grad() # Reset gradients
            
            # Move data to GPU/device
            terrain_data = terrain_data.to(device)
            text_ids = text_ids.to(device)
            attention_mask = attention_mask.to(device)
            
            # Forward Pass
            terrain_embeddings, text_embeddings = model(
                terrain_data, text_ids, attention_mask
            )
            
            # Calculate Loss (InfoNCE)
            loss = criterion(terrain_embeddings, text_embeddings)
            
            # Backward Pass & Optimization
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # 4. Reporting
        avg_loss = total_loss / len(data_loader)
        print(f"Epoch [{epoch+1}/{epochs}] | Avg Loss: {avg_loss:.4f}")
        
    print("--- FULL SEMANTIC ENGINE ARCHITECTURE COMPLETE. ---")

def main():
    parser = argparse.ArgumentParser(description="Train TopoCLIP Model")
    parser.add_argument("input", nargs='?', default="data/processed/smokies.mft", help="Path to input MFT file")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    args = parser.parse_args()

    train_topo_clip(args.input, epochs=args.epochs, learning_rate=args.lr)

if __name__ == "__main__":
    main()
