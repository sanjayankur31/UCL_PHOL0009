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
from pyneuroml.io import read_neuroml2_file
from neuroml.neuro_lex_ids import neuro_lex_ids


class Tutorial2A(object):
    """Class for Tutorial 2A"""

    def __init__(self):
        """TODO: to be defined."""

    celldoc = component_factory(component_type=neuroml.NeuroMLDocument, validate=True, id="dks577_doc",)
    cell_morph = read_neuroml2_file("dks577.neuronexport.morph.cell").morphology[0]
    # create a dummy cell so we can use the cell utilites
    cell = component_factory(component_type="Cell", validate=True, id="dks577", morphology=cell_morph)  # type: neuroml.Cell

    def postprocess(self):
        """Post process the cell to complete the export.

        Refer to dks577.append.hoc for various groups
        """
        # standard default groups
        [soma_group, dendrite_group, axon_group] = self.cell.setup_default_segment_groups(
            default_groups=["soma_group", "dendrite_group", "axon_group"]
        )

        all_group = self.cell.get_segment_group("all")
        # cell already contains group called "soma", copy it
        soma_group_orig = self.cell.get_segment_group("soma")
        for sg in soma_group_orig.members:
            soma_group.add("Member", segments=sg.segments)

        # ["distal_group", "basal_group", "apical_group"]
        distal_group = self.cell.add_segment_group(
            group_id="distal_group", neuro_lex_id=neuro_lex_ids["dend"]
        )
        apical_group = self.cell.add_segment_group(
            group_id="apical_group", neuro_lex_id=neuro_lex_ids["dend"]
        )
        basal_group = self.cell.add_segment_group(
            group_id="basal_group", neuro_lex_id=neuro_lex_ids["dend"]
        )
        # all but not myelin
        allg_ids = [sg.segment_groups for sg in all_group.includes]
        myelin_group = self.cell.add_segment_group(group_id="myelin_group")

        node_group = self.cell.add_segment_group(group_id="node_group")

        for sg in self.cell_morph.segment_groups:
            if sg.id != "dendrite_group" and "dend" in sg.id:
                dendrite_group.add("Include", segment_groups=sg.id)
                if "dend9" in sg.id:
                    # all dend9 are apical
                    apical_group.add("Include", segment_groups=sg.id)

                    # only sections that are more than 550 from soma are distal
                    segments = self.cell.get_all_segments_in_group(sg)
                    first_segment = segments[0]
                    if self.cell.get_distance(first_segment) > 550.0:
                        distal_group.add("Member", segments=first_segment)
            if sg.id == "hill" or sg.id == "iseg" or "node_" in sg.id or "myelin_" in sg.id:
                axon_group.add("Include", segment_groups=sg.id)
            if sg.id != "myelin_group" and "myelin" in sg.id:
                myelin_group.add("Include", segment_groups=sg.id)

            if sg.id != "node_group" and "node" in sg.id:
                node_group.add("Include", segment_groups=sg.id)

        # basal: all dendrites that are not apical
        dendg_ids = [sg.segment_groups for sg in dendrite_group.includes]
        apicalg_ids = [sg.segment_groups for sg in apical_group.includes]
        basal_ids = set(dendg_ids) - set(apicalg_ids)
        for sg in basal_ids:
            basal_group.add("Include", segment_groups=sg)

        active_group = self.cell.add_segment_group(group_id="active_group")
        myeling_ids = [sg.segment_groups for sg in myelin_group.includes]
        active_ids = set(allg_ids) - set(myeling_ids)
        for sg in active_ids:
            active_group.add("Include", segment_groups=sg)

        # biophysics
        ra = "200 ohm_cm"
        global_ra = ra
        rm = "40000 ohm_cm2"
        g_pas = f"{1/4000} S_per_cm2"
        c_m = "0.75 uF_per_cm2"
        v_init = "-70 mV"
        temperature = "23 degC"

        self.cell.set_spike_thresh("0 mV")
        self.cell.set_init_memb_potential(v_init)
        self.cell.set_resistivity(ra)
        self.cell.set_specific_capacitance(c_m)
        self.cell.add_channel_density(
            self.celldoc,
            cd_id="pas",
            ion_channel="pas",
            cond_density=g_pas,
            erev=v_init,
            group_id="all",
            ion="non_specific",
        )

        # different for myelin and node groups
        self.cell.set_specific_capacitance("0.04 uF_per_cm2", group_id=myelin_group.id)
        self.cell.add_channel_density(
            self.celldoc,
            cd_id="pas",
            ion_channel="pas",
            cond_density="0.02 S_per_cm2",
            erev=v_init,
            group_id=node_group.id,
            ion="non_specific",
        )

        # initially 0, then students are asked to increase this value
        self.cell.add_channel_density(self.celldoc, cd_id="na3",
                                      ion_channel="na3", cond_density="0 S_per_cm2",
                                      erev="60 mV", group_id="all", ion="na",
                                      ion_chan_def_file="channels/Na3.channel.nml")

        self.cell.add_channel_density(self.celldoc, cd_id="kd3",
                                      ion_channel="kd3", cond_density="0 S_per_cm2",
                                      erev="-90 mV", group_id="all", ion="k",
                                      ion_chan_def_file="channels/Kd3.channel.nml")

        self.cell.validate(recursive=True)

        # TODO: create default segment groups in morphology
        # TODO: use default segment group colours
        """
        celldoc.add("IncludeType", href="dks577.morph.cell")
        cell.morphology = None  # since we're using an external morphology
        print(cell)
        """

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

    def visualise(self):
        """Visualise in 3D
        :returns: TODO

        """
        segment_dict = {
            "dks577": {
                "cell_color": "Default Groups",
                # "cell_color": "Groups",
                "1321": {
                    "marker_color": "lightgreen",
                    "marker_size": [5.0, 5.0],
                    "marker_type": "sphere",
                },
                "1273": {
                    "marker_color": "seagreen",
                    "marker_size": [5.0, 5.0],
                    "marker_type": "sphere",
                },
                "2511": {
                    "marker_color": "limegreen",
                    "marker_size": [5.0, 5.0],
                    "marker_type": "sphere",
                },
                "9": {
                    "marker_color": "brown",
                    "marker_size": [30.0, 30.0],
                },
                "1315": {
                    "marker_color": "lawngreen",
                    "marker_size": [5.0, 5.0],
                    "marker_type": "sphere",
                },
            }
        }
        plot_interactive_3D(
            nml_file=self.cell,
            upright=True,
            precision=(0, 200),
            highlight_spec=segment_dict,
            plot_type="detailed",
            theme="dark",
        )


if __name__ == "__main__":
    tut = Tutorial2A()
    tut.postprocess()
