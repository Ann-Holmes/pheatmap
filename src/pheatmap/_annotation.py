import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray, number
from pandas import DataFrame, Series
from typing import Union, Dict, Tuple, List
from matplotlib.colors import Colormap, Normalize, BoundaryNorm
from matplotlib.axes import Axes
from ._utils import get_norm, get_cmap, cycle_cmap, CONTINUOUS, DISCRETE, HORIZONTAL, VERTICAL


def _object2categrey(anno: DataFrame) -> DataFrame:
    """Transform columns without `category` or `numpy.number` type to `category`"""
    need_transform_columns = anno.select_dtypes(exclude=[np.number, "category"]).columns
    return anno.apply(lambda x: x.astype("category") if x.name in need_transform_columns else x,
                      axis=0)


def _get_bartype(values: Series) -> str:
    if values.dtype in ["int", "float"]:
        return CONTINUOUS
    else:
        return DISCRETE


def _transform_discrete_values(values: Series) -> Tuple[ndarray, Dict[str, number]]:
    """Deal with discrete values, transform categories to numbers and create mapper for categories 
    and their numbers

    Parameters
    ----------
    values : Series
        categories
    Returns
    -------
    Tuple[ndarray, Dict[str, number]]
        return transformed numeric values and categories-numbers mapper
    """
    values_order = values.dtype.categories.to_list()
    values_mapper = {k: v for v, k in enumerate(values_order)}
    values = values.map(values_mapper)
    return values, values_mapper


class AnnotationBar:
    def __init__(
        self,
        values: ndarray, cmap: Union[str, Colormap, List],
        values_mapper: Dict[str, number] = None,
        name: str = None, vmin: float = None, vmax: float = None,
        bartype: str = CONTINUOUS, direction: str = HORIZONTAL,
        tick_labels_params: Dict = dict(size=6)
    ) -> None:
        """single AnnotationBar

        Parameters
        ----------
        values : ndarray
            values are used to draw annotation bar
        cmap : Union[str, Colormap, List]
            colormap for annotation bar
        values_mapper : Dict[str, number], optional
            values_mapper is used to create legend for DISCRETE values, by default None
        name : str, optional
            AnnotationBar name, show it on the bar side and its legend, by default None
        vmin : float, optional
            the minemum value scaled. `None` means use the minemum value of values. by default None
        vmax : float, optional
            the maximum value scaled. `None` means use the maximum value of values. by default None
        bartype : str, optional
            bar values are CONTINUOUS or DISCRETE, by default CONTINUOUS
        direction : str, optional
            visualize bar as HORIZONTAL or VERTICAL, by default HORIZONTAL
        """
        self.name = name
        self.direction = direction
        self.bartype = self._check_bartype(bartype)
        self.name_attrs = self._get_name_attrs()

        self.values = self._check_direction(values)
        self.values_mapper = values_mapper
        self.cmap = get_cmap(cmap, self.bartype)
        self.norm = self._get_norm(vmin, vmax)
        self.tick_labels_params = tick_labels_params

    def _check_bartype(self, bartype: str) -> str:
        """Validate `bar_type`"""
        if bartype in [CONTINUOUS, DISCRETE]:
            return bartype
        else:
            raise KeyError(f"`bar_type` have to be chose from {[CONTINUOUS, DISCRETE]}!")

    def _check_direction(self, values: ndarray) -> ndarray:
        """Validate `direction` and reshape `values`"""
        if self.direction == HORIZONTAL:
            return values.reshape(1, -1)
        elif self.direction == VERTICAL:
            return values.reshape(-1, 1)
        else:
            raise KeyError(f"`direction` have to be chose from {[HORIZONTAL, VERTICAL]}!")

    def _get_norm(self, vmin: float, vmax: float) -> Normalize:
        """`Normalize` for CONTINUOUS and `BoundaryNorm` for DISCRETE

        Parameters
        ----------
        vmin : float
            the minemum value scaled
        vmax : float
            the maximum value scaled

        Returns
        -------
        Normalize
        """
        if self.bartype == CONTINUOUS:
            return get_norm(self.values, vmin, vmax)
        else:
            num_colors = len(self.values_mapper)
            # Update cmap
            self.cmap = cycle_cmap(self.cmap, num_colors)
            bounds = np.arange(-0.5, num_colors)
            return BoundaryNorm(bounds, num_colors)

    def _get_name_attrs(self) -> Dict:
        """Config name's attrs used in visualized

        Returns
        -------
        Dict
            Get more information, see: 
            [matplotlib.axes.Axes.tick_params](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html)
        """
        side_dict = {"labeltop": False, "labelbottom": False,
                     "labelleft": False, "labelright": False}
        if self.direction == HORIZONTAL:
            side_dict["labelright"] = bool(self.name)
            side_dict["labelrotation"] = 0
        else:
            side_dict["labelbottom"] = bool(self.name)
            side_dict["labelrotation"] = 90
        return side_dict

    def draw(self, ax: Axes) -> None:
        ax.imshow(self.values, norm=self.norm, cmap=self.cmap, aspect="auto")
        ax.tick_params(
            axis="both", pad=0, top=False, bottom=False, left=False, right=False,
            **self.name_attrs
        )
        if self.direction == HORIZONTAL:
            ax.set_yticks([0], [self.name], **self.tick_labels_params)
        elif self.direction == VERTICAL:
            ax.set_xticks([0], [self.name], **self.tick_labels_params)
        else:
            raise KeyError("`direction` have to be chose from ['horizontal', 'vertical']!")
        ax.spines[:].set_visible(False)
        ax.grid(False)


class ListAnnotationBar:
    def __init__(
        self, anno: DataFrame, cmaps: Dict[str, Union[str, Colormap, List]],
        direction: str = HORIZONTAL, show_names: bool = True,
        tick_labels_params: Dict = dict(size=6)
    ) -> None:
        """Contain multiple Annotationbars

        Parameters
        ----------
        anno : DataFrame
            DataFrame used to create Annotationbar
        cmaps : Dict[str, Union[str, Colormap, List]]
            Colormaps for each Annotationbar, keys are the DataFrame's columns
        direction : str, optional
            visualize bar as HORIZONTAL or VERTICAL, by default HORIZONTAL
        show_names : bool, optional
            show AnnotationBar name or not, by default True
        tick_labels_params: Dict
        """
        anno = _object2categrey(anno)

        self.cmaps = cmaps
        self.direction = direction
        self.show_names = show_names
        self.tick_labels_params = tick_labels_params
        self.annotationbars = self._get_annotation_bars(anno)

    def _get_annotation_bars(self, anno: DataFrame) -> List[AnnotationBar]:
        """Create AnnotationBars along columns

        Parameters
        ----------
        anno : DataFrame
            DataFrame used to create Annotationbar

        Returns
        -------
        List[AnnotationBar]
        """
        annotationbars = []
        for name, values in anno.items():
            bartype = _get_bartype(values)
            if bartype == CONTINUOUS:
                cmap = self.cmaps.pop(name, "viridis")
                values_mapper = None
            else:
                values, values_mapper = _transform_discrete_values(values)
                cmap = self.cmaps.pop(name, "tab20")
            name = name if self.show_names else None
            tmp_annobar = AnnotationBar(
                values=values.to_numpy(), cmap=cmap, values_mapper=values_mapper,
                name=name, vmin=None, vmax=None, bartype=bartype, direction=self.direction,
                tick_labels_params=self.tick_labels_params
            )
            annotationbars.append(tmp_annobar)
        return annotationbars

    def draw(self, axes: List[Axes]) -> None:
        for annobar, ax in zip(self.annotationbars, axes):
            annobar.draw(ax)
