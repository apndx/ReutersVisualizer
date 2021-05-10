import matplotlib.pyplot as plt
import numpy as np

class Freq_colormap_color_func(object):
    """Color func created from matplotlib colormap.

    Parameters
    ----------
    colormap : string or matplotlib colormap
    word_dict : sorted dictionary that has word frequencies from smallest to largest

    Example
    -------
    >>> WordCloud(color_func=colormap_color_func('magma', 'word_dict'))

    """
    def __init__(self, colormap, word_dict):
        self.colormap = plt.cm.get_cmap(colormap)
        self.freq_max = list(word_dict.values())[-1]
        self.word_dict = word_dict
        

    def __call__(self, word, **kwargs):
        freq = self.word_dict.get(word)/self.freq_max
        r, g, b, _ = np.maximum(0, 255 * np.array(self.colormap(
            freq)))
        return "rgb({:.0f}, {:.0f}, {:.0f})".format(r, g, b)
