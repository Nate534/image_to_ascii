from enum import Enum

class Method(Enum):
    PCA="pca"
    EDGE="edge"
    CNN="cnn"

class Filter(Enum):
    LUMINANCE=0
    AVERAGE=1
    LIGHTNESS=2

    
    