import unittest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
from pheatmap._heatmap import Heatmap


class testHeatmap(unittest.TestCase):
    def setUp(self) -> None:
        self.nrows = 10
        self.ncols = 20
        self.mat = np.linspace(-1, 1, self.nrows * self.ncols).reshape(self.nrows, self.ncols)
        self.rownames = np.arange(self.nrows)
        self.colnames = np.arange(self.ncols)

    def test_attribute_cmap(self):
        cmaps = ["bwr", ["b", "w", "r"], plt.colormaps["Blues"], 1234]
        for cmap in cmaps:
            with self.subTest(cmap=cmap):
                if not isinstance(cmap, (str, list, Colormap)):
                    with self.assertRaises(TypeError):
                        Heatmap(self.mat, cmap=cmap)
                else:
                    self.assertIsInstance(Heatmap(self.mat, cmap=cmap).cmap, Colormap)

    def test_attribute_norm(self):
        vmin_vmaxs = [(-1, -0.5), (-0.5, 0.5), (0, 0.5), (0.5, 1)]
        for vmin, vmax in vmin_vmaxs:
            with self.subTest(vmin=vmin, vmax=vmax):
                ht = Heatmap(self.mat, cmap="bwr", vmin=vmin, vmax=vmax)
                self.assertEqual(ht.norm.vmin, vmin)
                self.assertEqual(ht.norm.vmax, vmax)
    
    def test_attribute_nrows_ncols(self):
        ht = Heatmap(self.mat, cmap="bwr")
        self.assertEqual(ht.nrows, self.nrows)
        self.assertEqual(ht.ncols, self.ncols)

    def test_attribute_rownames(self):
        rownames_cases = [
            self.rownames, 
            np.array(["CNS"[i % 3] for i in np.arange(self.nrows)]),
            np.arange(self.nrows - 5),
            np.arange(self.nrows + 10)
        ]
        for rownames in rownames_cases:
            with self.subTest(rownames=rownames):
                if len(rownames) != self.nrows:
                    with self.assertRaises(ValueError):
                        Heatmap(self.mat, cmap="bwr", rownames=rownames)
                else:
                    ht = Heatmap(self.mat, cmap="bwr", rownames=rownames)
                    np.testing.assert_array_equal(ht.rownames, rownames)
    
    def test_attribute_colnames(self):
        colnames_cases = [
            self.colnames, 
            np.array(["CNS"[i % 3] for i in np.arange(self.ncols)]),
            np.arange(self.ncols - 5),
            np.arange(self.ncols + 10)
        ]
        for colnames in colnames_cases:
            with self.subTest(colnames=colnames):
                if len(colnames) != self.ncols:
                    with self.assertRaises(ValueError):
                        Heatmap(self.mat, cmap="bwr", colnames=colnames)
                else:
                    ht = Heatmap(self.mat, cmap="bwr", colnames=colnames)
                    np.testing.assert_array_equal(ht.colnames, colnames)

    def test_attribute_sides(self):
        sides = {
            "null": {"labeltop": False, "labelbottom": False, "labelleft": False, "labelright": False},
            "null_row": {"labeltop": True, "labelbottom": False, "labelleft": False, "labelright": False},
            "null_col": {"labeltop": False, "labelbottom": False, "labelleft": True, "labelright": False},
            ("left", "top"): {"labeltop": True, "labelbottom": False, "labelleft": True, "labelright": False}, 
            ("right", "bottom"): {"labeltop": False, "labelbottom": True, "labelleft": False, "labelright": True}, 
            ("left", "bottom"): {"labeltop": False, "labelbottom": True, "labelleft": True, "labelright": False}, 
            ("right", "top"): {"labeltop": True, "labelbottom": False, "labelleft": False, "labelright": True}, 
            ("r", "t"): None,
            ("left", "b"): None
        }
        for kside, vside in sides.items():
            if vside is not None:
                if kside == "null":
                    with self.subTest(msg="Not provide rownames and colnames"):
                        self.assertEqual(Heatmap(self.mat, cmap="bwr").sides, vside)
                elif kside == "null_row":
                    with self.subTest(msg="Not provide rownames"):
                        self.assertEqual(Heatmap(self.mat, cmap="bwr", colnames=self.colnames).sides, vside)
                elif kside == "null_col":
                    with self.subTest(msg="Not provide colnames"):
                        self.assertEqual(Heatmap(self.mat, cmap="bwr", rownames=self.rownames).sides, vside)
                else:
                    with self.subTest(rownames_side=kside[0], colnames_side=kside[1]):
                        ht = Heatmap(
                            self.mat, cmap="bwr", rownames=self.rownames, colnames=self.colnames,
                            rownames_side=kside[0], colnames_side=kside[1]
                        )
                        self.assertEqual(ht.sides, vside)
            else:
                with self.subTest(rownames_side=kside[0], colnames_side=kside[1]):
                    with self.assertRaises(KeyError):
                        Heatmap(
                            self.mat, cmap="bwr", rownames=self.rownames, colnames=self.colnames,
                            rownames_side=kside[0], colnames_side=kside[1]
                        )
