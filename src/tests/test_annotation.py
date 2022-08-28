import unittest
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize, BoundaryNorm, LinearSegmentedColormap, ListedColormap
from pheatmap._annotation import AnnotationBar, _object2categrey, _get_bartype, _transform_discrete_values
from pheatmap._utils import HORIZONTAL, VERTICAL, CONTINUOUS, DISCRETE


class testAnnotationBar(unittest.TestCase):
    def setUp(self) -> None:
        self.values = np.arange(10)

    def test_attribute_bartype_cmap_norm(self):
        bartype_cases = {
            CONTINUOUS: [np.arange(100), "bwr", None, Normalize, LinearSegmentedColormap], 
            CONTINUOUS: [np.arange(100), "Set1", None, Normalize, LinearSegmentedColormap], 
            DISCRETE: [np.random.randint(0, 3, 100), "Set1", {"abc"[i]: i for i in np.arange(0, 3)}, BoundaryNorm, ListedColormap], 
            DISCRETE: [np.random.randint(0, 3, 100), "bwr", {"abc"[i]: i for i in np.arange(0, 3)}, BoundaryNorm, None], 
            "Others": [None, None, None, None, None]
        }
        for bartype, (values, cmap, values_mapper, norm, cmap_type) in bartype_cases.items():
            with self.subTest(bartype=bartype, values=values, cmap=cmap, values_mapper=values_mapper, cmap_type=cmap_type):
                if bartype in [CONTINUOUS, DISCRETE]:
                    if cmap_type is not None:
                        annobar = AnnotationBar(values, cmap=cmap, values_mapper=values_mapper, bartype=bartype)
                        self.assertEqual(annobar.bartype, bartype)
                        self.assertIsInstance(annobar.norm, norm)
                        self.assertIsInstance(annobar.cmap, cmap_type)
                    else:
                        with self.assertRaises(TypeError):
                            AnnotationBar(values, cmap=cmap, values_mapper=values_mapper, bartype=bartype)
                else:
                    with self.assertRaises(KeyError):
                        AnnotationBar(self.values, cmap="bwr", bartype=bartype)

    def test_attribute_name_attrs(self):
        name_cases = {
            (None, HORIZONTAL): {"labeltop": False, "labelbottom": False, "labelleft": False, "labelright": False, "labelrotation": 0}, 
            (None, VERTICAL): {"labeltop": False, "labelbottom": False, "labelleft": False, "labelright": False, "labelrotation": 90}, 
            ("a", HORIZONTAL): {"labeltop": False, "labelbottom": False, "labelleft": False, "labelright": True, "labelrotation": 0},
            ("a", VERTICAL): {"labeltop": False, "labelbottom": True, "labelleft": False, "labelright": False, "labelrotation": 90},
            (1, HORIZONTAL): {"labeltop": False, "labelbottom": False, "labelleft": False, "labelright": True, "labelrotation": 0},
            (1, VERTICAL): {"labeltop": False, "labelbottom": True, "labelleft": False, "labelright": False, "labelrotation": 90}
        }
        for (name, direction), name_attr in name_cases.items():
            with self.subTest(name=name, direction=direction, name_attr=name_attr):
                annobar = AnnotationBar(values=self.values, cmap="bwr", name=name, direction=direction)
                self.assertEqual(annobar.name_attrs, name_attr)
    
    def test_attribute_values(self):
        n_values = 10
        values_cases = {
            (HORIZONTAL, (1, n_values)): np.arange(n_values),
            (VERTICAL, (n_values, 1)): np.arange(n_values),
            ("Others", None): np.arange(n_values)
        }
        for (direction, values_shape), values in values_cases.items():
            with self.subTest(direction=direction, values=values):
                if direction in [HORIZONTAL, VERTICAL]:
                    annobar = AnnotationBar(values=values, cmap="bwr", values_mapper=None, direction=direction)
                    self.assertEqual(annobar.values.shape, values_shape)
                else:
                    with self.assertRaises(KeyError):
                        AnnotationBar(values=values, cmap="bwr", values_mapper=None, direction=direction)


class test_help_funcs(unittest.TestCase):
    def setUp(self) -> None:
        self.anno = pd.DataFrame(dict(anno1=np.arange(10), anno2=["abc"[i % 3] for i in np.arange(10)]))
        self.bartypes = [CONTINUOUS, DISCRETE]
    
    def test__object2categrey(self):
        anno = self.anno.copy()
        anno["anno2"] = anno["anno2"].astype("category")
        pd.testing.assert_frame_equal(_object2categrey(self.anno), anno)
    
    def test__get_bartype(self):
        anno = _object2categrey(self.anno)
        for i in range(2):
            with self.subTest(bartype=self.bartypes[i]):
                self.assertEqual(_get_bartype(anno.iloc[:, i]), self.bartypes[i])
    
    def test__transform_discrete_values(self):
        anno = _object2categrey(self.anno).iloc[:, 1]
        anno_transformed = [pd.Series([0, 1, 2, 0, 1, 2, 0, 1, 2, 0], name="anno2").astype("category"), {"a": 0, "b": 1, "c": 2}]
        values, values_mapper = _transform_discrete_values(anno)
        pd.testing.assert_series_equal(values, anno_transformed[0])
        self.assertEqual(values_mapper, anno_transformed[1])