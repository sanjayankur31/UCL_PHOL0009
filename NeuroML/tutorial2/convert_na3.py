#!/usr/bin/env python3
"""
Enter one line description here.

File:

Copyright 2024 Ankur Sinha
Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com>
"""


import textwrap
import neuroml
from neuroml import disable_build_time_validation, enable_build_time_validation
from neuroml.utils import component_factory
from pyneuroml.annotations import create_annotation
from pyneuroml.io import write_neuroml2_file


comment = textwrap.dedent(
    """
UCL, Department of Physiology, C123 Tutorial
This original code has been taken from:
http://senselab.med.yale.edu/modeldb/ShowModel.asp?model=8210
Padraig Gleeson, Volker Steuber, 2005-2007

na3h5.mod

Sodium channel, Hodgkin-Huxley style kinetics.  

Kinetics were fit to data from Huguenard et al. (1988) and Hamill et
al. (1991)

qi is not well constrained by the data, since there are no points
between -80 and -55.  So this was fixed at 5 while the thi1,thi2,Rg,Rd
were optimized using a simplex least square proc

voltage dependencies are shifted approximately +5mV from the best
fit to give higher threshold

use with kd3h5.mod

Author: Zach Mainen, Salk Institute, 1994, zach@salk.edu

    """
)
na3_doc = component_factory(neuroml.NeuroMLDocument, id="na3")
annotation_str = create_annotation(
    xml_header=False,
    subject="Na3",
    title="Sodium channel",
    description="Sodium channel with Hodgkin-Huxley style kinetics",
    annotation_style="miriam",
    authors={"Zack Mainen"},
    contributors={"Padraig Gleeson", "Volker Steuber", "Ankur Sinha"},
    sources={"https://modeldb.science/8210": "ModelDB"}
)
# print(annotation_str)

ion_channel = na3_doc.add("IonChannelHH", id="na3", conductance="10 pS",
                          species="Na")
annotation = ion_channel.add("Annotation", __ANY__=annotation_str)

disable_build_time_validation()

# standard rate, luckily vshift is 0
gate_m = ion_channel.add("GateHHUndetermined", type="gateHHrates", id="m", instances=3, validate=False)
q10 = gate_m.add("Q10Settings", type="q10ExpTemp", experimental_temp="23 degC",
                 q10_factor="2.3")
gate_m.add("HHRate", hint="forward_rate", type="HHExpLinearRate", scale="9 mV", midpoint="-35 mV", rate="0.182 per_ms")
gate_m.add("HHRate", hint="reverse_rate", type="HHExpLinearRate", scale="-9 mV",
           midpoint="-35 mV", rate="0.124 per_ms")

gate_h = ion_channel.add("GateHHUndetermined", type="gateHHratesInf", id="h", instances=1, validate=False)
gate_h.add(q10)
gate_h.add("HHRate", hint="forward_rate", type="HHExpLinearRate", scale="5 mV",
           midpoint="-50 mV", rate="0.124 per_ms")
gate_h.add("HHRate", hint="reverse_rate", type="HHExpLinearRate", scale="-5 mV",
           midpoint="-75 mV", rate="0.0091 per_ms")
gate_h.add("HHVariable", hint="steady_state", type="HHSigmoidVariable",
           midpoint="-65 mV", rate="1", scale="-6.2 mV")

enable_build_time_validation()

na3_doc.validate(True)
print(na3_doc)
write_neuroml2_file(na3_doc, "channels/Na3.channel.nml", validate=True)
