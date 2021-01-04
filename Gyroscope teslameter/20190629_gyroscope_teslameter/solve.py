import numpy as np
import pandas as pd
from helper.helpers import calc_du, buildSparseConnMat, buildConnMat
from config import params
import os
from scipy.sparse.linalg import bicg
import time
from math import sqrt

t= time.clock()

R= params.resistivity/params.thickness
dirs = [(1,0),(-1,0),(0,1), (0,-1)]
eqIndToConn= []
eqIndToRHS= []

indToEqInd = {}
eqIndToInd = []
indToP = {}

#setup ind conversion functions
nEqns = 0

print("%.2fs Computing Connections"%(time.clock()-t))
for ix, x in enumerate(params.xArray):
    for iy, y in enumerate(params.xArray):
        ind = ix+params.nX*iy
        p= np.array((x,y))
        indToP[ind] = p
        r = sqrt(np.dot(p, p))
        if r<params.R:
            indToEqInd[ind]= nEqns
            eqIndToInd.append(ind)
            nEqns+=1

for ix, x in enumerate(params.xArray):
    for iy, y in enumerate(params.xArray):
        ind = ix+ params.nX* iy
        if ind not in indToEqInd:
            continue
        eqInd = indToEqInd[ind]

        currConn = {}
        p= np.array((x,y))
        rhsVal= 0
        weightSum = 0
        for d_ix, d_iy in dirs:
            ixOther = ix+d_ix
            iyOther = iy+d_iy
            if ixOther<0 or ixOther>= params.nX or iyOther<0 or iyOther>= params.nX:
                continue
            indOther = ix+d_ix + params.nX*(iy+d_iy)
            if indOther not in indToEqInd:
                continue
            eqIndOther = indToEqInd[indOther]
            currConn[eqIndOther] = 1/R
            weightSum-= 1/R
            pOther = p+np.array((d_ix,d_iy))*params.dX
            rhsVal-= calc_du(params.e_add_f, pOther, p, params.nStep_for_du) / R

        currConn[eqInd] = weightSum
        eqIndToConn.append(currConn)
        eqIndToRHS.append(rhsVal)

print("%.2fs Building connection Matrix"%(time.clock()-t))
#connMat = buildConnMat(eqIndToConn)
connMat = buildSparseConnMat(eqIndToConn)
print("%.2fs Solving Equation System"%(time.clock()-t))
#res= np.linalg.solve(connMat, eqIndToRHS)
res,_ = bicg(connMat,eqIndToRHS)
res = res-np.min(res)
print("%.2fs Writing to File"%(time.clock()-t))

if not os.path.exists(params.outDirPath):
    os.makedirs(params.outDirPath)

data = []
for eqInd, pot in enumerate(res):
   p= indToP[eqIndToInd[eqInd]]
   data.append((p[0],p[1],pot))
data = pd.DataFrame(data, columns=["x","y","pot"])
data.to_excel(params.solPath)

print("%.2fs Finished"%(time.clock()-t))