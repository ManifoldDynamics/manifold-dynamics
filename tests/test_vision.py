import pytest
import torch
import numpy as np
from unittest.mock import MagicMock, patch
from manifold.vision.topo_clip_encoder import TopoCLIP
from manifold.vision.topo_clip_data import TopoClipDataset
from manifold.core.io import ManifoldTensor

@pytest.fixture
def mock_tokenizer():
    with patch('manifold.vision.topo_clip_data.DistilBertTokenizer') as mock:
        instance = mock.from_pretrained.return_value
        # Mock the callable return of tokenizer
        instance.return_value = MagicMock(
            input_ids=torch.randint(0, 100, (1, 32)),
            attention_mask=torch.ones((1, 32))
        )
        yield mock

def test_topo_clip_model():
    # Mock the BERT model inside TopoCLIP
    with patch('manifold.vision.topo_clip_encoder.DistilBertModel') as mock_bert:
        mock_instance = mock_bert.from_pretrained.return_value
        mock_instance.config.dim = 768 # Standard BERT dim

        # Mock forward pass
        # output is tuple/object with last_hidden_state
        mock_output = MagicMock()
        mock_output.last_hidden_state = torch.randn(2, 32, 768)
        # Support both object access and tuple unpacking if needed (though code uses .last_hidden_state)
        mock_instance.return_value = mock_output

        # Now instantiate
        model = TopoCLIP()

        # Mock inputs
        batch_size = 2
        terrain = torch.randn(batch_size, 7, 256, 256)
        text_ids = torch.randint(0, 1000, (batch_size, 32))
        mask = torch.ones((batch_size, 32))

        terrain_emb, text_emb = model(terrain, text_ids, mask)

        assert terrain_emb.shape == (batch_size, 512)
        assert text_emb.shape == (batch_size, 512)

def test_topo_clip_dataset(tmp_path, mock_tokenizer):
    # create dummy MFT
    path = tmp_path / "dummy.mft"
    rows, cols = 512, 512
    t = ManifoldTensor(rows=rows, cols=cols, gsd=10.0)
    t.elevation = np.random.rand(rows, cols).astype(np.float32)
    t.derived = np.random.rand(6, rows, cols).astype(np.float32)
    t.save(str(path))

    texts = ["a", "b"]
    dataset = TopoClipDataset(str(path), text_data=texts)

    assert len(dataset) > 0
    item = dataset[0]
    # item is terrain, text_ids, attention_mask
    assert len(item) == 3
    assert item[0].shape == (7, 256, 256)
