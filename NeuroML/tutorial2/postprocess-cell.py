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


celldoc = component_factory("NeuroMLDocument", id="dks577_doc")
celldoc.add("IncludeType", href="dks577.morph.cell")
cell = celldoc.add("Cell", id="dks577", morphology_attr="dks577_morphology")  # type: neuroml.Cell
cell.morphology = None  # since we're using an external morphology
# cell.info(True)

# cell.info(True)
plot_interactive_3D(nml_file=celldoc)
