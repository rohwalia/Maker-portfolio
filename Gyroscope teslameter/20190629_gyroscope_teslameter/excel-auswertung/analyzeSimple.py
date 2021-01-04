import pandas as pd
from math import isnan, pi
import matplotlib.pyplot as plt
from collections import deque


data = pd.read_excel("Retry.xlsx")

ts = []
omegas = []
for _, row in data.iterrows():
    pulseTime = row["Pulse time"]
    if not isnan(pulseTime):
        t = row["Time"]
        omega = 2*pi/(4*pulseTime)
        ts.append(t)
        omegas.append(omega)

avOmegas = []
currOmegas = deque()
currOmegaSum = 0
for omega in omegas:
    currOmegaSum+=omega
    currOmegas.append(omega)
    if len(currOmegas)>4:
        currOmegaSum -= currOmegas.popleft()
    if len(currOmegas)==4:
        avOmegas.append(currOmegaSum/4)
    else:
        avOmegas.append(omega)

plt.plot(ts,avOmegas)
plt.plot(ts,omegas)
plt.xlabel("t[s]")
plt.ylabel("$\omega$[rad/s]")
plt.show()