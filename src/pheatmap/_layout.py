import numpy as np
import matplotlib.pyplot as plt
from typing import List, Sequence, Union
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpecFromSubplotSpec, SubplotSpec, GridSpecBase


class Layout:
    def __init__(
        self,
        center_width: float, center_height: float,
        left_width: float, top_height: float,
        right_width: float, bottom_height: float,
        sub_left_width: Sequence[float], sub_top_height: Sequence[float],
        sub_right_width: Sequence[float], sub_bottom_height: Sequence[float],
        wspace: float, hspace: float,
        sub_left_wspace: float, sub_top_hspace: float,
        sub_right_wspace: float, sub_bottom_hspace: float,
        width: float = None, height: float = None
    ) -> None:
        """_summary_

        Parameters
        ----------
        center_width : float
            the center region's relative width
        center_height : float
            the center region's relative height
        left_width : float
            the left region's relative width
        top_height : float
            the top region's relative height
        right_width : float
            the right region's relative width
        bottom_height : float
            the bottom region's relative height
        sub_left_width : Sequence[float]
            the sub region's ratio in the left region
        sub_top_height : Sequence[float]
            the sub region's ratio in the top region
        sub_right_width : Sequence[float]
            the sub region's ratio in the right region
        sub_bottom_height : Sequence[float]
            the sub region's ratio in the bottom region
        wspace : float
            the space between regions at width direction
        hspace : float
            the space between regions at height direction
        sub_left_wspace : float
            the space between left sub regions at width direction
        sub_top_hspace : float
            the space between top sub regions at height direction
        sub_right_wspace : float
            the space between right sub regions at width direction
        sub_bottom_hspace : float
            the space between bottom sub regions at height direction
        width : float, optional
            the real width of whole figure, by default None, use the sum of regions' relative width
        height : float, optional
            the real height of whole figure, by default None, use the sum of regions' relative height
        """
        self.width = center_width + left_width + right_width if width is None else width
        self.height = center_height + top_height + bottom_height if height is None else height

        self.center_w, self.center_h = center_width, center_height
        self.left_w, self.top_h = left_width, top_height
        self.right_w, self.bottom_h = right_width, bottom_height

        self.sub_left_w, self.sub_top_h = sub_left_width, sub_top_height
        self.sub_right_w, self.sub_bottom_h = sub_right_width, sub_bottom_height

        self.wspace, self.hspace = wspace, hspace
        self.sub_left_wspace, self.sub_top_hspace = sub_left_wspace, sub_top_hspace
        self.sub_right_wspace, self.sub_bottom_hspace = sub_right_wspace, sub_bottom_hspace

        self.fig, self.gs = self._create_gridspec()
        self.left_gs = self._create_subgridspec(
            self.gs[1, 0], None, self.sub_left_wspace, [1], self.sub_left_w)
        self.right_gs = self._create_subgridspec(
            self.gs[1, 2], None, self.sub_right_wspace, [1], self.sub_right_w)
        self.top_gs = self._create_subgridspec(
            self.gs[0, 1], self.sub_top_hspace, None, self.sub_top_h, [1])
        self.bottom_gs = self._create_subgridspec(
            self.gs[2, 1], self.sub_bottom_hspace, None, self.sub_bottom_h, [1])

    def _create_gridspec(self):
        fig = plt.figure(figsize=(self.width, self.height))
        gs = fig.add_gridspec(
            nrows=3, ncols=3,
            hspace=self.hspace, wspace=self.wspace,
            height_ratios=[self.top_h, self.center_h, self.bottom_h],
            width_ratios=[self.left_w, self.center_w, self.right_w]
        )
        return fig, gs

    def _create_subgridspec(
        self, sps: SubplotSpec, hspace: float, wspace: float,
        h_ratios: Sequence, w_ratios: Sequence
    ) -> GridSpecFromSubplotSpec:
        """Create the sub `GridSpec`

        Parameters
        ----------
        sps : SubplotSpec
            the `SubplotSpec` generated from main `GridSpec`
        hspace : float
            the space between `SubplotSpec`s from the sub `GridSpec` at height direction 
        wspace : float
            the space between `SubplotSpec`s from the sub `GridSpec` at width direction
        h_ratios : Sequence
            the ratios of heights of `SubplotSpec`s  from the sub `GridSpec`
        w_ratios : Sequence
            the ratios of widths of `SubplotSpec`s  from the sub `GridSpec`

        Returns
        -------
        GridSpecFromSubplotSpec
        """
        gs_sps = sps.subgridspec(
            nrows=len(h_ratios), ncols=len(w_ratios),
            hspace=hspace, wspace=wspace,
            height_ratios=h_ratios, width_ratios=w_ratios
        )
        return gs_sps

    def create_axes(
        self, sps: Union[GridSpecBase, SubplotSpec], axis: int = 0
    ) -> Union[Axes, List[Axes]]:
        """Create List Axes or single from `GridSpec` or `SubplotSpec` 

        Parameters
        ----------
        sps : Union[GridSpecBase, SubplotSpec]
        axis : int, optional
            create Axes along which axis, by default 0, along the row

        Returns
        -------
        Union[Axes, List[Axes]]
        """
        if isinstance(sps, SubplotSpec):
            return self.fig.add_subplot(sps)
        if isinstance(sps, GridSpecBase):
            axes = []
            if axis == 0:
                for i in range(sps.nrows):
                    axes.append(self.fig.add_subplot(sps[i, 0]))
                return axes
            elif axis == 1:
                for i in range(sps.ncols):
                    axes.append(self.fig.add_subplot(sps[0, i]))
                return axes
            else:
                raise KeyError("'axis' must be '0' or '1'!")


if __name__ == '__main__':
    width, height = 16, 20
    bar_width = 1 / 20
    legend_bar_width = 1.5 * bar_width

    bar_wspace = 0.3
    legend_bar_wspace = 1

    n_leftbars = 3
    n_rightbars = 3
    n_topbars = 1
    n_bottombars = 1

    left_width = bar_width * width * n_leftbars + \
        bar_wspace * (bar_width * width) * (n_leftbars - 1)
    right_width = legend_bar_width * width * n_rightbars + \
        legend_bar_wspace * (legend_bar_width * width) * (n_rightbars - 1)
    top_height = (bar_width * width) * n_topbars + bar_wspace * \
        (bar_width * width) * (n_topbars - 1)
    bottom_height = (bar_width * width) * n_bottombars + bar_wspace * \
        (bar_width * width) * (n_bottombars - 1)

    center_width = width - left_width - right_width
    center_heigh = height - top_height - bottom_height

    layout = Layout(
        center_width=center_width, center_height=center_heigh,
        left_width=left_width, top_height=top_height,
        right_width=right_width, bottom_height=bottom_height,
        sub_left_width=[1] * n_leftbars, sub_top_height=[1] * n_topbars,
        sub_right_width=[1] * n_rightbars, sub_bottom_height=[1] * n_bottombars,
        wspace=0.1, hspace=0.1,
        sub_left_wspace=bar_wspace, sub_top_hspace=bar_wspace,
        sub_right_wspace=legend_bar_wspace, sub_bottom_hspace=bar_wspace,
        width=width, height=height
    )
    layout.create_axes(layout.gs[1, 1])
    layout.create_axes(layout.left_gs, axis=1)
    layout.create_axes(layout.right_gs, axis=1)
    layout.create_axes(layout.top_gs, axis=0)
    layout.create_axes(layout.bottom_gs, axis=0)
    plt.savefig("tmp.pdf")
