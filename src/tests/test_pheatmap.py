import unittest
import numpy as np
import pandas as pd
import os
from pheatmap import pheatmap


class test_pheatmap(unittest.TestCase):
    def setUp(self) -> None:
        self.nrows, self.ncols = 10, 10
        self.mat = np.linspace(-1, 1, self.nrows * self.ncols).reshape(self.nrows, self.ncols)
        self.rownames = ["abcdefghig"[i % 10] for i in np.arange(self.nrows)]
        self.colnames = ["xyz"[i % 3] for i in np.arange(self.ncols)]

        self.mat = pd.DataFrame(self.mat, index=self.rownames, columns=self.colnames)

        self.anno_row = pd.DataFrame(dict(
            anno1=np.linspace(0, 10, self.nrows),
            anno2=["CNS"[i % 3] for i in np.arange(self.nrows)]
        ))
        self.anno_col = pd.DataFrame(dict(
            anno3=np.linspace(0, 20, self.ncols),
            anno4=["ABC"[i % 3] for i in np.arange(self.ncols)]
        ))

        self.anno_row_cmaps = {"anno1": "Blues", "anno2": "Set1"}
        self.anno_col_cmaps = {"anno3": "Purples", "anno4": "Set3"}

    def test_all(self):
        fig = pheatmap(
            self.mat, annotation_row=self.anno_row, annotation_col=self.anno_col,
            annotation_row_cmaps=self.anno_row_cmaps, annotation_col_cmaps=self.anno_col_cmaps
        )
        fig.savefig("pheatmap.png")
        fig.savefig("pheatmap.pdf")

    def tearDown(self) -> None:
        for file in ["pheatmap.png", "pheatmap.pdf"]:
            if os.path.exists(file):
                os.remove(file)