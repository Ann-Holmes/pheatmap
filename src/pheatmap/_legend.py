import warnings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Sequence, Dict, Tuple
from numpy import ndarray
from matplotlib.colors import Colormap, Normalize, BoundaryNorm
from matplotlib.axes import Axes
from _utils import CONTINUOUS, DISCRETE


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
        self.ticks = tick_locs
        self.labels = tick_labels
        self.tick_labels_params = tick_labels_params
        self.title_params = title_params
        self.cmap = cmap
        self.norm = norm
        self.name = name if name else ""
        self.bartype = bartype
        self.cbar = None

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


if __name__ == '__main__':
    fig, axes = plt.subplots(ncols=2, figsize=(2, 8), tight_layout=True)
    # Continuous
    cmap = plt.colormaps["bwr"]
    norm = Normalize(-1, 1)
    tick_locs = [-1, -0.5, 0, 0.5, 1]
    tick_labels = [-1, -0.5, 0, 0.5, 1]

    legend = Legend(tick_locs=tick_locs, tick_labels=tick_labels,
                    cmap=cmap, norm=norm, name="continuous")
    legend.draw(axes[0])

    # Discrete
    cmap = plt.colormaps["Set1"]
    norm = BoundaryNorm(np.arange(-0.5, 5), 5)
    tick_locs = np.arange(5)
    tick_labels = ["abcdefgh"[i] for i in tick_locs]
    legend = Legend(tick_locs=tick_locs, tick_labels=tick_labels,
                    cmap=cmap, norm=norm, name="discrete", bartype=DISCRETE)
    legend.draw(axes[1])

    plt.savefig("tmp.pdf")
