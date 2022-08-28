import numpy as np
import matplotlib.pyplot as plt
from typing import Union, List
from numpy import ndarray
from matplotlib.colors import Colormap
from matplotlib.axes import Axes
from ._utils import get_norm, get_cmap


class Heatmap:
    def __init__(
        self, mat: ndarray,
        cmap: Union[str, Colormap, list], vmin: float = None, vmax: float = None,
        name: str = None, rownames: ndarray = None, colnames: ndarray = None,
        rownames_side: str = "left", colnames_side: str = "top",
        rownames_style: dict = dict(rotation=0), colnames_style: dict = dict(rotation=0),
        edgecolor: str = "none", edgewidth: float = 1
    ) -> None:
        """Heatmap

        Parameters
        ----------
        mat : ndarray
            the matrix used to plot heatmap
        cmap : Union[str, Colormap, list]
            colormap for the matrix
        vmin : float, optional
            the minemum value scaled. by default None, use the minemum value of matrix. 
        vmax : float, optional
            the maximum value scaled. by default None, use the maximum value of matrix.
        name : str, optional
            heatmap name, show it on its legend. by default None, don't show the name
        rownames : ndarray, optional
            row names of heatmap. by default None, don't show the row names
        colnames : ndarray, optional
            column names of heatmap. by default None, don't show the column names
        rownames_side : str, optional
            show row names on which side("left" or "right")? by default "left"
        colnames_side : str, optional
            show column names on which side("top" or "bottom")?, by default "top"
        rownames_style : dict, optional
            modify row names' style, such as, fontsize, fontstyle, etc. See more information on 
            [`matplotlib.text.Text`](https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text).
            by default dict(rotation=0)
        colnames_style : dict, optional
            See `rownames_style`, by default dict(rotation=0)
        edgecolor : str, optional
            the color of heatmap's cell edge, by default "none", no edge. 
            !Note: If provide `None`, will use the `rcParams["patch.edgecolor"]`, 
            it default as "black". 
        edgewidth : float, optional
            the width of heatmap's cell edge, by default 1
        """
        self.mat = mat
        self.name = name

        self.cmap = get_cmap(cmap)
        self.norm = get_norm(self.mat, vmin, vmax)

        self.nrows, self.ncols = self._get_nrows_ncols()
        self.rownames = self._check_names(axis="row", names=rownames)
        self.colnames = self._check_names(axis="col", names=colnames)
        self.sides = self._parse_name_side(rownames_side, colnames_side)

        self.rownames_style, self.colnames_style = rownames_style, colnames_style
        self.edgecolor = edgecolor
        self.edgewidth = edgewidth

    def _get_nrows_ncols(self):
        return self.mat.shape

    def _parse_name_side(self, rownames_side: str, colnames_side: str) -> dict:
        """Parse the row/column names' side

        Parameters
        ----------
        rownames_side : str
            show row names on which side("left" or "right")? by default "left"
        colnames_side : str
            show column names on which side("top" or "bottom")?, by default "top"

        Returns
        -------
        dict
            used in `tick_params`, will change row/column names side

        Raises
        ------
        KeyError
            If the rownames_side/colnames_side provided are not correct, will raise KeyError
        """
        side_dict = {"labeltop": False, "labelbottom": False,
                     "labelleft": False, "labelright": False}

        # Check row/colnames_side options
        rownames_side_options = ["left", "right"]
        colnames_side_options = ["top", "bottom"]
        if rownames_side not in rownames_side_options:
            raise KeyError(
                f"The rownames_side, '{rownames_side}' is not one of {rownames_side_options}")
        if colnames_side not in colnames_side_options:
            raise KeyError(
                f"The colnames_side, '{colnames_side}' is not one of {colnames_side_options}")

        side_dict[f"label{rownames_side}"] = all([rownames_side, self.rownames is not None])
        side_dict[f"label{colnames_side}"] = all([colnames_side, self.colnames is not None])
        return side_dict

    def _check_names(self, axis: str, names: ndarray) -> ndarray:
        """Check the row/column names provided are correct

        Parameters
        ----------
        axis : str
            "row" or "col"?
        names : ndarray
            the row/column names provided

        Returns
        -------
        ndarray

        Raises
        ------
        ValueError
            If the row/column names provided are not correct will raise KeyError
        """
        num = self.nrows if axis == "row" else self.ncols
        if names is None:
            return names
        elif len(names) != num:
            raise ValueError(
                f"The length of {axis}names is not equal to the number of heatmap matrix!")
        else:
            return names

    def draw(self, ax: Axes) -> None:
        ax.imshow(self.mat, norm=self.norm, cmap=self.cmap, aspect="auto")

        # Set row/colnames and their font style(rotation, family, size, etc)
        ax.set_xticks(np.arange(self.ncols), labels=self.colnames,
                      minor=False, **self.colnames_style)
        ax.set_yticks(np.arange(self.nrows), labels=self.rownames,
                      minor=False, **self.rownames_style)

        # Set ticks and ticklabels location and if show them
        ax.tick_params(
            axis="both", which="major", pad=0, top=False, bottom=False, left=False, right=False,
            **self.sides
        )

        # Configure edges color and width
        if self.edgecolor:
            ax.set_xticks(np.arange(-0.5, self.ncols), minor=True)
            ax.set_yticks(np.arange(-0.5, self.nrows), minor=True)
            ax.tick_params(axis="both", which="minor", pad=0,
                           top=False, bottom=False, left=False, right=False)
            # For whole Axes
            ax.spines[:].set_color(self.edgecolor)
            ax.spines[:].set_linewidth(self.edgewidth)
            # For every cells
            ax.grid(True, axis="both", which="minor",
                    color=self.edgecolor, linewidth=self.edgewidth)
        else:
            ax.spines[:].set_visible(False)
            ax.grid(False, axis="both", which="both")


if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(4, 4))
    mat = np.arange(200).reshape(10, 20)
    # cmap = ["red", "white", "blue"]
    ht = Heatmap(
        mat, cmap="bwr",
        colnames=np.arange(mat.shape[1]),
        colnames_side="top",
        colnames_style=dict(rotation=90, color="blue", fontstyle="normal", fontsize=3),
        edgecolor="g")
    ht.draw(ax)
    plt.savefig("tmp.pdf")
