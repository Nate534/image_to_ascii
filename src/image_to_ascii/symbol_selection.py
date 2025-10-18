"""
Symbol selection using the default PCA implementation.

This module imports and uses the PCA converter from the implementations directory.
"""

from .implementations.pca_converter import select_symbol

__all__ = ['select_symbol']