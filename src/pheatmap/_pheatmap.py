import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from numpy import ndarray
from typing import Union, Sequence, Dict, List
from matplotlib.colors import Colormap
from matplotlib.figure import Figure
from ._heatmap import Heatmap
from ._annotation import ListAnnotationBar
from ._legend import Legend
from ._layout import Layout
from ._utils import HORIZONTAL, VERTICAL, CONTINUOUS, DISCRETE


def none2dict(x: Dict = None) -> Dict:
    """Transform `None` to null `Dict`"""
    if x is None:
        return dict()
    else:
        return x


def check_margin_names(df_margin_names: ndarray, margin_names: Sequence = None,
                       show_margin_names: bool = True, axis: str = "row") -> Union[ndarray, None]:
    """Check row/column names are correct

    Parameters
    ----------
    df_margin_names : ndarray
        the main DataFrame's row/column names
    margin_names : Sequence, optional
        the row/column names provided, by default None
    show_margin_names : bool, optional
        whether show row/column names, by default True
    axis : str, optional
        "row" or "col"? by default "row"

    Returns
    -------
    Union[ndarray, None]

    Raises
    ------
    ValueError
        If provide row/column names and its length is not match the main DataFrame's, will raise
        ValueError
    """
    if not show_margin_names:
        return None
    elif margin_names is None:
        return df_margin_names
    elif len(df_margin_names) == len(margin_names):
        return np.array(margin_names)
    else:
        raise ValueError(f"The length of {axis}names is not match `mat`!")


def create_annotation(
        anno: Union[DataFrame, None], cmaps: Dict[str, Union[str, Colormap, list]],
        show_names: bool, expected_nrows: int, axis="row"
) -> Union[ListAnnotationBar, None]:
    """Instance row/column `ListAnnotationBar`

    Parameters
    ----------
    anno : Union[DataFrame, None]
        the annotation's DataFrame
    cmaps : Dict[str, Union[str, Colormap, list]]
        the colormaps for each AnnotationBar
    show_names : bool
        whether show AnnotationBar's name
    expected_nrows : int
        the number of row/columns of main DataFrame
    axis : str, optional
        "row" or "col" annotation?, by default "row"

    Returns
    -------
    Union[ListAnnotationBar, None]

    Raises
    ------
    ValueError
        If the number of rows of annotation's DataFrame is not match the main DataFrame's row/column
        number, will raise ValueError
    """
    if anno is None:
        return None
    elif anno.shape[0] == expected_nrows:
        axis = VERTICAL if axis == "row" else HORIZONTAL
        cmaps = none2dict(cmaps)
        return ListAnnotationBar(anno=anno, cmaps=cmaps, direction=axis, show_names=show_names)
    else:
        raise ValueError(f"The number of annotation_{axis}'s rows is not match `mat`!")


def pheatmap(
    mat: DataFrame,
    cmap: Union[str, Colormap, list] = "bwr",
    vmin: float = None, vmax: float = None,
    name: str = None, rownames: ndarray = None, colnames: ndarray = None,
    rownames_side: str = "left", colnames_side: str = "bottom",
    show_rownames: bool = True, show_colnames: bool = True,
    rownames_style: dict = dict(rotation=0, size=6), 
    colnames_style: dict = dict(rotation=0, size=6),
    edgecolor: str = "none", edgewidth: float = 1,
    annotation_row: DataFrame = None, annotation_col: DataFrame = None,
    annotation_row_cmaps: Dict[str, Union[str, Colormap, list]] = None,
    annotation_col_cmaps: Dict[str, Union[str, Colormap, list]] = None,
    show_annotation_row_names: bool = True, show_annotation_col_names: bool = True,
    legend_tick_locs: Dict[str, Sequence] = None, legend_tick_labels: Dict[str, Sequence] = None,
    legend_tick_labels_params: Dict = dict(size=6),
    legend_titles: Dict[str, bool] = None, legend_title_params: Dict = dict(size=6),
    width: float = 8, height: float = 6, wspace: float = 0.1, hspace: float = 0.1,
    annotation_bar_width: float = 0.03, legend_bar_width: float = 1.5 * 0.03,
    annotation_bar_space: float = 0.2, legend_bar_space: float = 1
) -> Figure:
    """Plot heatmap with annotation bars

    Parameters
    ----------
    mat : DataFrame
        the main heatmap DataFrame
    cmap : Union[str, Colormap, list], optional
        the colormap of heatmap, by default "bwr"
    vmin : float, optional
        the minemum value scaled. by default None, use the minemum value of `mat`
    vmax : float, optional
        the maximum value scaled. by default None, use the maximum value of `mat`
    name : str, optional
        the name of heatmap, by default None, use "heatmap" as the name of heatmap
    rownames : ndarray, optional
        the row names provided, by default None, use the row names of main heatmap DataFrame
    colnames : ndarray, optional
        the column names provided, by default None, use the column names of main heatmap DataFrame
    rownames_side : str, optional
        show row names on which side("left" or "right")? by default "left"
    colnames_side : str, optional
        show column names on which side("top" or "bottom")? by default "bottom"
    show_rownames : bool, optional
        whether show row names? by default True
    show_colnames : bool, optional
        whether show column names? by default True
    rownames_style : dict, optional
        modify row names' style, such as, fontsize, fontstyle, etc. See more information on 
        [`matplotlib.text.Text`](https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text).
        by default dict(rotation=0, size=6)
    colnames_style : dict, optional
        see `rownames_style`, by default dict(rotation=0, size=6)
    edgecolor : str, optional
        the color of heatmap's cell edge, by default "none", no edge. 
        !Note: If provide `None`, will use the `rcParams["patch.edgecolor"]`, it default as "black".
    edgewidth : float, optional
        the width of heatmap's cell edge, by default 1
    annotation_row : DataFrame, optional
        DataFrame used to create row Annotationbar, by default None
    annotation_col : DataFrame, optional
        DataFrame used to create column Annotationbar, by default None
    annotation_row_cmaps : Dict[str, Union[str, Colormap, list]], optional
        Colormaps for each Annotationbar, keys are the DataFrame's columns, by default None, use
        "viridis" for continuous and "tab20" for discrete
    annotation_col_cmaps : Dict[str, Union[str, Colormap, list]], optional
        see `annotation_row_cmaps`, by default None
    show_annotation_row_names : bool, optional
        whether show row Annotationbar's name, by default True
    show_annotation_col_names : bool, optional
        whether show column Annotationbar's name, by default True
    legend_tick_locs : Dict[str, Sequence], optional
        modify the tick locations of legend, keys are the name of heatmap or the column names of
        annotation DataFrame, by default None
    legend_tick_labels : Dict[str, Sequence], optional
        modify the tick labels of legend, keys are the name of heatmap or the column names of
        annotation DataFrame. The length of each legend tick labels must be matched with its tick
        locations. by default None
    legend_tick_labels_params : Dict, optional
        modify the each legend tick labels' style. Keys are the name of heatmap or the column names
        of annotation DataFrame. More informations see `rownames_style`. by default dict(size=6)
    legend_titles : Dict[str, bool], optional
        modify the each legend title. Others are the same as `legend_tick_labels_params`.
        by default None
    legend_title_params : Dict, optional
        modify the each legend title's style. Others are the same as `legend_tick_labels_params`.
        by default dict(size=6)
    width : float, optional
        the whole figure width, by default 8
    height : float, optional
        the whole figure height, by default 6
    wspace : float, optional
        the space of whole figure at the width direction, by default 0.1. It's the fraction of the
        average length of width's axises
    hspace : float, optional
        see wspace, by default 0.1
    annotation_bar_width : float, optional
        the width of Annotationbar, by default 0.03. It's the fraction of the whole figure width
    legend_bar_width : float, optional
        the width of legend bar, by default 1.5*0.03. It's the fraction of the whole figure width.
        And it's better, set it as 1.5 * annotation_bar_width.
    annotation_bar_space : float, optional
        the space between Annotationbars, by default 0.2. It's the fraction of the real
        Annotationbar width.
    legend_bar_space : float, optional
        the space between legend bars, by default 1. It's the fraction of the real legend bar width

    Returns
    -------
    Figure
    """
    # Heatmap
    # Check arguments
    rownames = check_margin_names(mat.index.to_numpy(), rownames, show_rownames, axis="row")
    colnames = check_margin_names(mat.columns.to_numpy(), colnames, show_colnames, axis="col")
    mat = mat.to_numpy()
    name = name if name is not None else "heatmap"

    # Instance class
    heatmap = Heatmap(
        mat=mat, cmap=cmap, vmin=vmin, vmax=vmax, name=name,
        rownames=rownames, colnames=colnames,
        rownames_side=rownames_side, colnames_side=colnames_side,
        rownames_style=rownames_style, colnames_style=colnames_style,
        edgecolor=edgecolor, edgewidth=edgewidth
    )

    # Row/Column Annotations
    row_annotationbars = create_annotation(
        anno=annotation_row, cmaps=annotation_row_cmaps, show_names=show_annotation_row_names,
        expected_nrows=heatmap.nrows, axis="row"
    )
    col_annotationbars = create_annotation(
        anno=annotation_col, cmaps=annotation_col_cmaps, show_names=show_annotation_col_names,
        expected_nrows=heatmap.ncols, axis="col"
    )

    # Legends
    legends = []
    legend_tick_locs = none2dict(legend_tick_locs)
    legend_tick_labels = none2dict(legend_tick_labels)
    legend_tick_labels_params = none2dict(legend_tick_labels_params)
    legend_titles = none2dict(legend_titles)
    legend_title_params = none2dict(legend_title_params)

    # Heatmap's legend
    legends.append(Legend(
        cmap=heatmap.cmap, norm=heatmap.norm, name=legend_titles.pop(heatmap.name, heatmap.name),
        tick_locs=legend_tick_locs.pop(
            heatmap.name, np.linspace(heatmap.mat.min(), heatmap.mat.max(), 5)),
        tick_labels=legend_tick_labels.pop(
            heatmap.name, np.linspace(heatmap.mat.min(), heatmap.mat.max(), 5)),
        tick_labels_params=legend_tick_labels_params,
        title_params=legend_title_params,
        bartype=CONTINUOUS
    ))

    # AnnotationBars legends
    if row_annotationbars is not None:
        for anno_bar in row_annotationbars.annotationbars:
            if anno_bar.bartype == CONTINUOUS:
                tick_locs = legend_tick_locs.pop(
                    anno_bar.name, np.linspace(anno_bar.values.min(), anno_bar.values.max(), 5))
                tick_labels = legend_tick_labels.pop(
                    anno_bar.name, np.linspace(anno_bar.values.min(), anno_bar.values.max(), 5))
            else:
                tick_locs = legend_tick_locs.pop(
                    anno_bar.name, list(anno_bar.values_mapper.values()))
                tick_labels = legend_tick_labels.pop(
                    anno_bar.name, list(anno_bar.values_mapper.keys()))

            legends.append(Legend(
                cmap=anno_bar.cmap, norm=anno_bar.norm, name=anno_bar.name,
                tick_locs=tick_locs, tick_labels=tick_labels,
                tick_labels_params=legend_tick_labels_params,
                title_params=legend_title_params,
                bartype=anno_bar.bartype
            ))
    if col_annotationbars is not None:
        for anno_bar in col_annotationbars.annotationbars:
            if anno_bar.bartype == CONTINUOUS:
                tick_locs = legend_tick_locs.pop(
                    anno_bar.name, np.linspace(anno_bar.values.min(), anno_bar.values.max(), 5))
                tick_labels = legend_tick_labels.pop(
                    anno_bar.name, np.linspace(anno_bar.values.min(), anno_bar.values.max(), 5))
            else:
                tick_locs = legend_tick_locs.pop(
                    anno_bar.name, list(anno_bar.values_mapper.values()))
                tick_labels = legend_tick_labels.pop(
                    anno_bar.name, list(anno_bar.values_mapper.keys()))

            legends.append(Legend(
                cmap=anno_bar.cmap, norm=anno_bar.norm, name=anno_bar.name,
                tick_locs=tick_locs, tick_labels=tick_labels,
                tick_labels_params=legend_tick_labels_params,
                title_params=legend_title_params,
                bartype=anno_bar.bartype
            ))

    # Layout
    # width, height = width, height
    # bar_width = 1 / 20
    # legend_bar_width = 1.5 * bar_width

    # annotation_bar_space = 0.3
    # legend_bar_space = 0.3

    n_leftbars = len(row_annotationbars.annotationbars) if row_annotationbars is not None else 1
    n_rightbars = len(legends) if len(legends) > 0 else 1
    n_topbars = len(col_annotationbars.annotationbars) if col_annotationbars is not None else 1
    n_bottombars = 1

    left_width = annotation_bar_width * width * n_leftbars + \
        annotation_bar_space * (annotation_bar_width * width) * (n_leftbars - 1)
    right_width = legend_bar_width * width * n_rightbars + \
        legend_bar_space * (legend_bar_width * width) * (n_rightbars - 1)
    top_height = (annotation_bar_width * width) * n_topbars + annotation_bar_space * \
        (annotation_bar_width * width) * (n_topbars - 1)
    bottom_height = (annotation_bar_width * width) * n_bottombars + annotation_bar_space * \
        (annotation_bar_width * width) * (n_bottombars - 1)

    center_width = width - left_width - right_width
    center_height = height - top_height - bottom_height
    layout = Layout(
        center_width=center_width, center_height=center_height,
        left_width=left_width, top_height=top_height,
        right_width=right_width, bottom_height=bottom_height,
        sub_left_width=[1] * n_leftbars, sub_top_height=[1] * n_topbars,
        sub_right_width=[1] * n_rightbars, sub_bottom_height=[1] * n_bottombars,
        wspace=wspace, hspace=hspace,
        sub_left_wspace=annotation_bar_space, sub_top_hspace=annotation_bar_space,
        sub_right_wspace=legend_bar_space, sub_bottom_hspace=annotation_bar_space,
        width=width, height=height
    )

    # Draw plots
    # Heatmap
    ht_ax = layout.create_axes(layout.gs[1, 1])
    heatmap.draw(ht_ax)

    # Annotation Bars
    if row_annotationbars is not None:
        row_annobars_axes = layout.create_axes(layout.left_gs, axis=1)
        for ax, annobar in zip(row_annobars_axes, row_annotationbars.annotationbars):
            annobar.draw(ax)
    if col_annotationbars is not None:
        col_annobars_axes = layout.create_axes(layout.top_gs, axis=0)
        for ax, annobar in zip(col_annobars_axes, col_annotationbars.annotationbars):
            annobar.draw(ax)
    if len(legends) > 0:
        legend_bars_axes = layout.create_axes(layout.right_gs, axis=1)
        for ax, legend in zip(legend_bars_axes, legends):
            legend.draw(ax)

    return layout.fig


if __name__ == '__main__':
    # mat = pd.DataFrame(
    #     dict(a=np.arange(1000), b=np.arange(1000, 2000), c=np.arange(2000, 3000)),
    #     index=["zyxwvutsrq"[i % 10] for i in np.arange(1000)]
    # ).T
    nrows = 30
    mat = pd.DataFrame(np.arange(nrows * 1000).reshape(-1, 1000))
    anno_row = pd.DataFrame(
        dict(anno1=np.arange(nrows), anno2=["CNS"[i % 3] for i in np.arange(nrows)])
    )
    anno_col = pd.DataFrame(
        dict(anno2=np.arange(1000), anno3=["abcdefghigk"[i % 10] for i in np.arange(1000)])
    )
    fig = pheatmap(
        mat,
        annotation_row=anno_row,
        annotation_col=anno_col,
        show_colnames=False,
        # rownames_side="right", colnames_side="bottom",
        # wspace=0.3, legend_bar_space=1.5
    )
    fig.savefig("pheatmap.png")
