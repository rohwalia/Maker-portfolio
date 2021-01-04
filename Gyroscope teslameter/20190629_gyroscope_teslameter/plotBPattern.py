import numpy as np
import matplotlib.pyplot as plt
from helper.helpers import loadBField

bF = loadBField("in/60mT_pattern.xlsx", 0.025,0.045, 0.005)

xs = np.linspace(-0.05,0.05,1000)
ys = np.linspace(-0.05, 0.05, 1000)

xs, ys = np.meshgrid(xs,ys)

bs = bF(xs,ys)

fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.pcolormesh(xs, ys, bs, cmap= plt.get_cmap('gist_rainbow'))
plt.colorbar()
plt.show()