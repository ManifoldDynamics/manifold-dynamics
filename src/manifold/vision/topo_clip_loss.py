import torch
import torch.nn as nn
import torch.nn.functional as F

class InfoNCELoss(nn.Module):
    """
    Implements the symmetric cross-entropy loss used for Contrastive Learning (CLIP).
    This function measures the similarity between paired map and text embeddings.
    """
    def __init__(self, temperature=0.07):
        super().__init__()
        self.temperature = temperature
        # CrossEntropyLoss is the mathematical core of InfoNCE
        self.cross_entropy_loss = nn.CrossEntropyLoss()

    def forward(self, map_embeddings, text_embeddings):
        """
        Calculates the InfoNCE Loss between a batch of N map and N text embeddings.

        Args:
            map_embeddings (torch.Tensor): Output from TerrainEncoder (N, D)
            text_embeddings (torch.Tensor): Output from TextEncoder (N, D)
        """
        
        # 1. Calculate Cosine Similarity Matrix (N x N)
        # S[i, j] = Similarity between Map[i] and Text[j]
        # We normalize the vectors first (essential for cosine similarity)
        map_norm = F.normalize(map_embeddings, p=2, dim=1)
        text_norm = F.normalize(text_embeddings, p=2, dim=1)
        
        # S = (Map @ Text.T) / temperature
        similarity_matrix = (map_norm @ text_norm.T) / self.temperature
        
        # 2. Create Ground Truth Labels
        # The correct pair is always on the diagonal (i == j).
        # Labels should be a vector [0, 1, 2, 3, ..., N-1]
        labels = torch.arange(len(similarity_matrix)).long().to(similarity_matrix.device)
        
        # 3. Calculate Symmetric Loss
        
        # Loss A: Map-to-Text (How well does Map[i] match its Text label[i]?)
        loss_a = self.cross_entropy_loss(similarity_matrix, labels)
        
        # Loss B: Text-to-Map (How well does Text[i] match its Map label[i]?)
        # We need to transpose the similarity matrix here
        loss_b = self.cross_entropy_loss(similarity_matrix.T, labels)
        
        # Final Loss: Average of the two directional losses (Symmetric Cross-Entropy)
        total_loss = (loss_a + loss_b) / 2
        
        return total_loss

if __name__ == '__main__':
    print("Verifying InfoNCE Loss...")
    
    # Mock data: 4 samples, 512 dimensions
    N, D = 4, 512
    # In a perfect world, M[i] == T[i]
    mock_map = torch.randn(N, D)
    mock_text = mock_map.clone() + torch.randn(N, D) * 0.1 # Add slight noise
    
    # Run Loss
    loss_fn = InfoNCELoss(temperature=0.1)
    loss = loss_fn(mock_map, mock_text)
    
    print(f"Loss value (should be low if data is similar): {loss.item():.4f}")
    assert loss.item() < 3.0 # A small loss indicates the architecture is mathematically sound.
    print("InfoNCE Loss Verification: PASSED.")