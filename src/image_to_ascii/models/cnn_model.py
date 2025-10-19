"""
cnn_model.py
Defines a small CNN for ASCII image conversion.
Compatible with cnn_converter.py and CLI.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from ..ascii_symbols import chars

# ---------------- CNN Definition ---------------- #

class ASCIIConvNet(nn.Module):
    def __init__(self, num_classes: int = len(chars)):
        super().__init__()
        # 1x8x8 input grayscale patch → 2 conv layers → pooling → fc
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 2 * 2, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.fc2(x), dim=1)

# ---------------- Helper Functions ---------------- #

def create_model():
    """Return a fresh, untrained CNN model."""
    return ASCIIConvNet()

def train_model(save_path: str = None):
    """
    Placeholder training function.
    Returns an untrained model (for now).
    Save to disk if save_path is provided.
    """
    model = ASCIIConvNet()
    if save_path:
        torch.save(model.state_dict(), save_path)
    return model

def load_model(model_path: str = None):
    """
    Loads CNN weights if model_path exists.
    Otherwise, returns a fresh untrained model.
    """
    model = ASCIIConvNet()
    if model_path and os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()
    return model
