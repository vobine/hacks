import numpy as np
from numpy import random

class CometData:
    """"""
    def __init__ (self, shape, threshold = 0.9):
        """Create an array of time series."""
        self.shape = shape
        self.threshold = threshold

        raw = random.uniform (size=shape)
        self.data = np.cumprod (1 - 2 * (raw > threshold), axis=1)
