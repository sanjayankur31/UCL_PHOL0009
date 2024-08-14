#!/usr/bin/env python3
"""
Convert the kd3 channel

File: NeuroML/tutorial2/convert_kd3.py

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

ENDCOMMENT


COMMENT

Kd3h5.mod

Potassium channel, Hodgkin-Huxley style kinetics
Kinetic rates based roughly on Sah et al. and Hamill et al. (1991)

Use with na3h5.mod

Author: Zach Mainen, Salk Institute, 1994, zach@salk.edu

    """
)

kd3_doc = component_factory(neuroml.NeuroMLDocument, id="kd3")
annotation_str = create_annotation(
    xml_header=False,
    subject="kd3",
    title="Potassium channel",
    description="Potassium channel with Hodgkin-Huxley style kinetics",
    annotation_style="miriam",
    authors={"Zack Mainen"},
    contributors={"Padraig Gleeson", "Volker Steuber", "Ankur Sinha"},
    sources={"https://modeldb.science/8210": "ModelDB"}
)
# print(annotation_str)

ion_channel = kd3_doc.add("IonChannelHH", id="kd3", conductance="10 pS",
                          species="K")
annotation = ion_channel.add("Annotation", __ANY__=annotation_str)

disable_build_time_validation()

# it isn't HHExpLinearRate, so I need to make a new one

newHHrate = kd3_doc.add(neuroml.ComponentType, name="HHNearlyExpLinearRate",
                        extends="baseHHRate", description="A HHExpLinearRate, but not quite")

# required to have correct dimensions, since the numerator in the equations in
# the mod file does not have a scale to divide the voltage difference by
newHHrate.add(neuroml.Constant, name="VOLT_SCALE", dimension="voltage",
              value="1 mV")
newHHrate.add(neuroml.Parameter, name="scale", dimension="voltage")
newHHrate.add(neuroml.Parameter, name="midpoint", dimension="voltage")
newHHrate.add(neuroml.Parameter, name="rate", dimension="per_time")
dynamics = newHHrate.add(neuroml.Dynamics)
dynamics.add(neuroml.DerivedVariable, name="x", dimension="voltage",
             value="(v - midpoint)")
dynamics.add(neuroml.DerivedVariable, name="xnodim", dimension="none",
             value="x / VOLT_SCALE")
cdv = dynamics.add(neuroml.ConditionalDerivedVariable, name="r",
                   dimension="per_time", exposure="r")
cdv.add(neuroml.Case, condition="xnodim .neq. 0", value="rate * xnodim/(1 - exp(0 - x/scale))")
cdv.add(neuroml.Case, value="rate")

# standard rate, luckily vshift is 0
gate_n = ion_channel.add("GateHHUndetermined", type="gateHHrates", id="n", instances=1, validate=False)
q10 = gate_n.add("Q10Settings", type="q10ExpTemp", experimental_temp="16 degC",
                 q10_factor="3")
gate_n.add("HHRate", hint="forward_rate", type="HHNearlyExpLinearRate", scale="9 mV",
           midpoint="20 mV", rate="0.02 per_ms")
gate_n.add("HHRate", hint="reverse_rate", type="HHNearlyExpLinearRate", scale="-9 mV",
           midpoint="20 mV", rate="-0.002 per_ms")

enable_build_time_validation()

kd3_doc.validate(True)
print(kd3_doc)
write_neuroml2_file(kd3_doc, "channels/Kd3.channel.nml", validate=True)
