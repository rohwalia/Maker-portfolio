from math import pi, isnan
from collections import deque


def analyzeData(data, tName, ptName):
    ts = []
    pts = []
    omegas = []
    for _, row in data.iterrows():
        pt = row[ptName]
        t = row[tName]
        if (not isnan(pt)) and (not isnan(t)):
            omega = 2 * pi / (4 * pt)
            pts.append(pt)
            ts.append(t)
            omegas.append(omega)


    avOmegas = []
    currOmegas = deque()
    currOmegaSum = 0
    for omega in omegas:
        currOmegaSum += omega
        currOmegas.append(omega)
        if len(currOmegas) > 4:
            currOmegaSum -= currOmegas.popleft()
        if len(currOmegas) == 4:
            avOmegas.append(currOmegaSum / 4)
        else:
            avOmegas.append(omega)

    return ts, pts, omegas, avOmegas