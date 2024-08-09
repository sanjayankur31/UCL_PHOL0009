COMMENT

UCL, Department of Physiology, C123 Tutorial

Example of an exponentially decaying synaptic mechanism

Padraig Gleeson, Volker Steuber, 2005-2007

ENDCOMMENT



NEURON {
	POINT_PROCESS MyExpSyn
	RANGE tau, e, i, gmax, onset
	NONSPECIFIC_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	onset = 0 (ms)
	tau = 2 (ms) <1e-9,1e9>
	e = 0	(mV)
	gmax = 0.001 (uS)
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
}

INITIAL {
	g=0
}

FUNCTION myexp(x) {
	if (x < -100) {
		myexp = 0
	} else {
		myexp = exp(x)
	}
}

FUNCTION cond(x) {
	if (x < onset) {
		cond = 0
	} else {
		cond = myexp(-(x - onset)/tau)
	}
}
	
BREAKPOINT {
	g = gmax*cond(t)
	i = g*(v - e)
}


