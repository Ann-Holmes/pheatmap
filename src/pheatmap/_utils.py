import matplotlib.pyplot as plt
from numpy import ndarray
from typing import Union
from matplotlib.colors import Normalize, Colormap, ListedColormap, LinearSegmentedColormap

CONTINUOUS = "continuous"
DISCRETE = "discrete"
HORIZONTAL = "horizontal"
VERTICAL = "vertical "

def get_norm(values: ndarray, vmin: float, vmax: float) -> Normalize:
    """Get `Normalize` by the provided `vmin` and `vmax`

    Parameters
    ----------
    values : ndarray
        values are used to normalize
    vmin : float
        the minemum value visualized
    vmax : float
        the maximum value visualized
    Returns
    -------
    Normalize
    """
    vmin = vmin if vmin is not None else values.min()
    vmax = vmax if vmax is not None else values.max()
    return Normalize(vmin=vmin, vmax=vmax)


def cycle_cmap(cmap: Colormap, num: int) -> Colormap:
    """When the number of discrete colors are not enough for categories, cycle the colors of cmap 
    to meet the number of categories.

    Parameters
    ----------
    cmap : Colormap
        Colormap of categories
    num : int
        the number of categories

    Returns
    -------
    Colormap
    """
    colors = cmap.colors * (num // cmap.N) + cmap.colors[:(num % cmap.N)]
    return ListedColormap(colors)


def get_cmap(cmap: Union[Colormap, str, list], cmap_type: str = CONTINUOUS) -> Colormap:
    """Transform different color expresion types to Colormap

    Parameters
    ----------
    cmap : Union[Colormap, str, list]
        the raw color expression
    cmap_type : str, optional
        cmap is used for bar type, by default CONTINUOUS

    Returns
    -------
    Colormap
    """
    if isinstance(cmap, str):
        cmap =  plt.colormaps[cmap]
    elif isinstance(cmap, list):
        if cmap_type == CONTINUOUS:
            cmap = LinearSegmentedColormap.from_list("from_list", colors=cmap)
        else:
            cmap = ListedColormap(colors=cmap)
    elif isinstance(cmap, Colormap):
        pass
    else:
        raise TypeError("'cmap' must be `Colormap` type!")
    
    if (cmap_type == CONTINUOUS) and (not isinstance(cmap, LinearSegmentedColormap)):
        raise TypeError(f"'cmap' must be 'LinearSegmentedColormap' for {CONTINUOUS}!")
    elif (cmap_type == DISCRETE) and (not isinstance(cmap, ListedColormap)):
        raise TypeError(f"'cmap' must be 'ListedColormap' for {DISCRETE}")
    else:
        return cmap
