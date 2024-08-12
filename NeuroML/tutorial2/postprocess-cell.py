#!/usr/bin/env python3
"""
Complete the cell conversion by adding biophysics.

File: postprocess-cell.py

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import neuroml
from neuroml.utils import component_factory
from pyneuroml.plot.PlotMorphologyVispy import plot_interactive_3D


# TODO: create default segment groups in morphology
# TODO: use default segment group colours
celldoc = component_factory("NeuroMLDocument", id="dks577_doc")
celldoc.add("IncludeType", href="dks577.morph.cell")
cell = celldoc.add("Cell", id="dks577", morphology_attr="dks577_morphology")  # type: neuroml.Cell
cell.morphology = None  # since we're using an external morphology
print(cell)

# Inputs with approximate segments in NeuroML:
# IClamp at dend6[11](0.25) -> Seg6_dend6_11 (1321)
# MyExpSyn 0 at dend6[11](0.25) -> Seg6_dend6_11 (1321)
# MyExpSyn 1 at dend6[9](0) -> Seg0_dend6_9 (1273)
# MyExpSyn 2 at dend9[7](0.625) -> Seg45_dend9_7 (2511)
# MyExpSyn 3 at soma(0.5) -> Seg8_soma (9)
# MyExpSyn 4 at dend6[11](0) -> Seg0_dend6_11 (1315)
# MyExpSyn 5 at soma(0.5) -> Seg8_soma (9)

# cell.info(True)

# cell.info(True)
segment_dict = {
    "dks577": {
        "cell_color": "lightseagreen",
        "1321":
        {
            "marker_color": "blue",
            "marker_size": [16., 16.],
        },
        "1273":
        {
            "marker_color": "red",
            "marker_size": [16., 16.],
        },
        "2511":
        {
            "marker_color": "green",
            "marker_size": [16., 16.],
        },
        "9":
        {
            "marker_color": "brown",
            "marker_size": [30., 30.],
        },
        "1315":
        {
            "marker_color": "yellow",
            "marker_size": [16., 16.],
        }
    }
}
plot_interactive_3D(nml_file=celldoc, axes_pos="origin", upright=True,
                    precision=(0, 200), highlight_spec=segment_dict,
                    plot_type="detailed", theme="dark")
