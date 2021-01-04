from config import params
import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt
import math
from helper.helpers import calc_du
import time

# resolution (for scalar and vector plots)
# scalar resolution is also used for computations
# nXS = 1000
nXS = 200
nXV = 90

t = time.clock()

print("%.2fs Loading potential"%(time.clock()-t))
data = pd.read_excel(params.solPath)

points = []
potVals = []
for _, row in data.iterrows():
    points.append((row["x"],row["y"]))
    potVals.append(row["pot"])

print("%.2fs Interpolating potential"%(time.clock()-t))
potF = LinearNDInterpolator(points, potVals)


print("%.2fs Computing current densities and others"%(time.clock()-t))
dirs = [(1,0),(-1,0),(0,1), (0,-1)]

jxVec, jyVec, ex_add_vec, ey_add_vec, fx_per_dA_add_after_vec, fy_per_dA_add_after_vec = [], [], [], [], [], []

for x, y in points:
    p= np.array((x,y))
    j= np.zeros(2)
    e_add= np.zeros(2)
    weight= np.zeros(2)
    for d_ix, d_iy in dirs:
        d_i = np.array((d_ix, d_iy))
        pOther = p + d_i * params.dX
        sp0= -(potF(pOther)-potF(p))/(params.dX*params.resistivity)
        sp1= calc_du(params.e_add_f, p, pOther, params.nStep_for_du) / params.dX
        sp0+= sp1/params.resistivity
        if not math.isnan(sp0):
            j+= sp0*d_i
            e_add+= sp1*d_i
            weight+=(abs(d_ix),abs(d_iy))
    j/=weight
    e_add/=weight
    f_per_dA_add_after= params.f_per_dA_add_after_f(p, j)

    jxVec.append(j[0])
    jyVec.append(j[1])
    ex_add_vec.append(e_add[0])
    ey_add_vec.append(e_add[1])
    fx_per_dA_add_after_vec.append(f_per_dA_add_after[0])
    fy_per_dA_add_after_vec.append(f_per_dA_add_after[1])

print("%.2fs Interpolating current densities and others"%(time.clock()-t))
jxF = LinearNDInterpolator(points, jxVec)
jyF = LinearNDInterpolator(points, jyVec)
ex_addF = LinearNDInterpolator(points, ex_add_vec)
ey_addF = LinearNDInterpolator(points, ey_add_vec)
fx_per_dA_add_afterF = LinearNDInterpolator(points, fx_per_dA_add_after_vec)
fy_per_dA_add_afterF = LinearNDInterpolator(points, fy_per_dA_add_after_vec)


print("%.2fs Computing quantities to plot"%(time.clock()-t))
xSArray = np.linspace(-params.R, params.R, nXS)
ySArray = np.linspace(-params.R, params.R, nXS)
xSMg, ySMg = np.meshgrid(xSArray, ySArray)

potMat = potF(xSMg, ySMg)
jMat = np.sqrt(jxF(xSMg,ySMg)**2+ jyF(xSMg,ySMg)**2)
fx_per_dA_add_after_fineMat= fx_per_dA_add_afterF(xSMg, ySMg)
fy_per_dA_add_after_fineMat= fy_per_dA_add_afterF(xSMg, ySMg)
rMat = np.sqrt(xSMg**2+ySMg**2)
dP_per_dA_add_fineMat = (-ySMg * fx_per_dA_add_after_fineMat + xSMg * fy_per_dA_add_after_fineMat) * params.omega
dP_per_dA_add_fineMat= np.nan_to_num(dP_per_dA_add_fineMat, 0)

xVArray = np.linspace(-params.R, params.R, nXV)
yVArray = np.linspace(-params.R, params.R, nXV)

xVMg, yVMg = np.meshgrid(xVArray, yVArray)

jxMat = jxF(xVMg,yVMg)
jyMat = jyF(xVMg,yVMg)

jxDirMat = jxMat/np.sqrt(jxMat**2+ jyMat**2)
jyDirMat = jyMat/np.sqrt(jxMat**2+ jyMat**2)

fx_per_dA_add_after = fx_per_dA_add_afterF(xVMg, yVMg)
fy_per_dA_add_after = fy_per_dA_add_afterF(xVMg, yVMg)
f_per_dA_after_fine = np.sqrt(fx_per_dA_add_after_fineMat**2+ fy_per_dA_add_after_fineMat**2)
fx_per_dA_add_after_dir = fx_per_dA_add_after/np.sqrt(fx_per_dA_add_after**2+ fy_per_dA_add_after**2)
fy_per_dA_add_after_dir = fy_per_dA_add_after/np.sqrt(fx_per_dA_add_after**2+ fy_per_dA_add_after**2)

ex_add_mat= ex_addF(xVMg,yVMg)
ey_add_mat= ey_addF(xVMg,yVMg)
e_add_mat_coarse= np.sqrt(ex_add_mat**2+ ey_add_mat**2)
ex_add_dir_mat = ex_add_mat/e_add_mat_coarse
ey_add_dir_mat = ey_add_mat/e_add_mat_coarse
e_add_mat = np.sqrt(ex_addF(xSMg,ySMg)**2+ ey_addF(xSMg,ySMg)**2)

print("%.2fs Compute deceleration powers"%(time.clock()-t))
# compute the decelaration power by summing up the power lost through heat at the resistors
dXS = xSArray[1]-xSArray[0]
dP0Mat = jMat**2*params.thickness*params.resistivity*dXS**2
dP0Mat=np.nan_to_num(dP0Mat,0)
pDecelaration0 = dP0Mat.sum()
print(pDecelaration0)
pDecelaration1 = dP_per_dA_add_fineMat.sum()*dXS**2
print(pDecelaration1)
print(pDecelaration1/pDecelaration0)

print("%.2fs Do Plots"%(time.clock()-t))
fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.pcolormesh(xSMg, ySMg, potMat, cmap= plt.get_cmap('gist_rainbow'))
plt.colorbar()
plt.show()

fig, ax = plt.subplots()
ax.set_aspect('equal')
# Einheit der Stromdichte soll Ampere/cm^2 sein
plt.pcolormesh(xSMg, ySMg, jMat/100**2, cmap= plt.get_cmap('gist_rainbow'))
plt.colorbar()
plt.quiver(xVMg, yVMg, jxDirMat, jyDirMat, scale_units="xy", scale= nXV/(2*params.R))
plt.show()

fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.pcolormesh(xSMg, ySMg, f_per_dA_after_fine, cmap= plt.get_cmap('gist_rainbow'))
plt.colorbar()
plt.quiver(xVMg, yVMg, fx_per_dA_add_after_dir, fy_per_dA_add_after_dir, scale_units="xy", scale= nXV/(2*params.R))
plt.show()

fig, ax = plt.subplots()
ax.set_aspect('equal')
plt.pcolormesh(xSMg, ySMg, e_add_mat, cmap= plt.get_cmap('gist_rainbow'))
plt.colorbar()
plt.quiver(xVMg, yVMg, ex_add_dir_mat, ey_add_dir_mat, scale_units="xy", scale= nXV/(2*params.R))
plt.show()