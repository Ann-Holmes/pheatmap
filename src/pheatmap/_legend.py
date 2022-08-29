import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Sequence, Dict
from matplotlib.colors import Colormap, Normalize, BoundaryNorm
from matplotlib.axes import Axes
from ._utils import CONTINUOUS, DISCRETE


class Legend:
    def __init__(
        self, cmap: Colormap, norm: Normalize,
        tick_locs: Sequence, tick_labels: Sequence,
        name: str = None, tick_labels_params: Dict = dict(size=8),
        title_params: Dict = dict(size=10),
        bartype: str = CONTINUOUS
    ) -> None:
        """_summary_

        Parameters
        ----------
        cmap : Colormap
            the colormap which is the same as its owner
        norm : Normalize
            the Normalize which is the same as its owner
        tick_locs : Sequence, optional
            the tick locations
        tick_labels : Sequence, optional
            the tick labels, which must be match with tick locations
        name : str, optional
            the legend name get from its owner, by default None, don't show it
        tick_labels_params : Dict, optional
            modify tick labels' style, by default dict(size=8)
        title_params : Dict, optional
            modify title's style, by default dict(size=10)
        bartype : str, optional
            the legend bar type(CONTINUOUS or DISCRETE), by default CONTINUOUS
        """
        self.ticks = np.array(tick_locs)
        self.labels = np.array(tick_labels)
        self.tick_labels_params = tick_labels_params
        self.title_params = title_params
        self.cmap = cmap
        self.norm = self._scale_norm(norm)
        self.name = name if name else ""
        self.bartype = bartype
        self.cbar = None
    
    def _scale_norm(self, norm):
        """Scale the continuous norm by the tick_locs"""
        if isinstance(norm, BoundaryNorm):
            return norm
        else:
            if self.ticks.min() < norm.vmin:
                vmin = self.ticks.min()
            else:
                vmin = norm.vmin
            if self.ticks.max() > norm.vmax:
                vmax = self.ticks.max()
            else:
                vmax = norm.vmax
            return Normalize(vmin, vmax)

    def draw(self, ax: Axes) -> None:
        self.cbar = mpl.colorbar.Colorbar(
            ax, mpl.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
            orientation="vertical", drawedges=False, filled=True
        )
        ax.set_yticks(self.ticks, self.labels, **self.tick_labels_params)
        ax.invert_yaxis()
        ax.set_title(self.name, loc="left", **self.title_params)
        ax.spines[:].set_visible(False)
        ax.tick_params(
            axis="both", pad=0, top=False, bottom=False, left=False, right=False,
            labeltop=False, labelbottom=False, labelleft=False, labelright=True
        )
        if self.bartype == CONTINUOUS:
            ax.tick_params(axis="y", pad=2, direction="in", color="#DADADA", left=True, right=True)
        elif self.bartype == DISCRETE:
            pass
        else:
            raise KeyError(f"'bartype' must be {[CONTINUOUS, DISCRETE]}!")
