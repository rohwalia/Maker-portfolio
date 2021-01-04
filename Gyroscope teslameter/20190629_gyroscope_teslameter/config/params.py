import numpy as np
from helper.helpers import loadBField
#nX=1000
nX= 200
R= 0.042
#R=0.055
nStep_for_du= 10

# sigma is the resistivity (in units of Ohms*meter) (to get the resistance of a small path,
# divide by the cross section area and multiple by the length of the path)
resistivity = 2.65*10**(-8)
thickness = 0.004
#omega= 37
#resistivity= 1.68*10**(-8)
#thickness = 0.000035
omega= 60

#Bz=40*0.001
#Bz= 100*0.001
"""
x0 = 0.015-0.015/2
x1 = 0.015+0.015/2
"""
"""
x0 = 0.0155 - 0.015/2
x1 = 0.0155 + 0.015/2
"""

"""
y0=-0.02/2
y1=0.02/2
"""
outDirPath = "out"
solPath = "%s/sol.xlsx"%outDirPath

dX= 2*R/nX
xArray = np.linspace(-R+dX/2, R-dX/2, nX)

Bz_f = loadBField("in/60mT_pattern_2.xlsx",0.0275+0.035, 0.045, 0.005)

"""
def Bz_f(x):
    if x[0]>=x0 and x[0]<x1:
        if x[1]>=y0 and x[1]<y1:
            return Bz
    return 0
"""
def e_add_f(x):
    return omega * Bz_f(x) * x

def f_per_dA_add_after_f(x, j):
    return np.array((j[1],-j[0]))*thickness* Bz_f(x)