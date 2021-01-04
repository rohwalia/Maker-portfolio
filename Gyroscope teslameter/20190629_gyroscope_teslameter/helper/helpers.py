import numpy as np
from scipy.sparse import csc_matrix, csr_matrix
from scipy.interpolate import LinearNDInterpolator
import pandas as pd


# energy per charge that the field give to charge in field e_f (field does not have to be of electrostatic orgin)
def calc_du(e_f, p0, p1, nStep):
    dStep = (p1 - p0) / nStep
    du=0
    p= p0 + dStep / 2
    for i in range(nStep):
        du+=np.dot(e_f(p),dStep)
        p+=dStep
    return du

def buildConnMat(conns):
    n= len(conns)
    mat = []
    for conn in conns:
        row = []
        for i in range(n):
            row.append(conn.get(i,0))
        mat.append(row)
    return mat

def buildSparseConnMat(conns):
    n= len(conns)
    data, row_inds, column_inds = [], [], []
    for row_ind, conn in enumerate(conns):
        for column_ind, val in conn.items():
            row_inds.append(row_ind)
            column_inds.append(column_ind)
            data.append(val)
    return csc_matrix((data,(row_inds,column_inds)),shape=(n,n))

def loadBField(bPatternPath, x0,y0,dx):
    data = pd.read_excel(bPatternPath)
    points, bs = [], []
    for ix, (_, row) in enumerate(data.iterrows()):
        for iy, bVal in enumerate(row):
            x = x0 - ix * dx
            y = y0 - iy * dx
            points.append((x, y))
            bs.append(bVal/1000)
    return LinearNDInterpolator(points, bs, fill_value= 0)