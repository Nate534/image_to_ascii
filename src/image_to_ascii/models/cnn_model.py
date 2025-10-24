"""
cnn_model.py
Defines a small CNN for ASCII image conversion.
Compatible with cnn_converter.py and CLI.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from .ascii_symbols import chars


class ASCIIConvNet(nn.Module):
    def __init__(self, num_classes: int = len(chars)):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 2 * 2, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.fc2(x), dim=1)


# Helper functions


def create_model():
    return ASCIIConvNet()


def train_model(save_path: str = None):
    model = ASCIIConvNet()
    if save_path:
        torch.save(model.state_dict(), save_path)
    return model


def load_model(model_path=None):
    """
    Returns a CNN model instance.
    Currently, this is a placeholder that returns an untrained model.
    """
    model = ASCIIConvNet()

    if model_path is not None:
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model
