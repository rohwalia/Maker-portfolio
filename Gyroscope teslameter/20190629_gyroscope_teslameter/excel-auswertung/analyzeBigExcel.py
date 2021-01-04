import pandas as pd
from lib.analyzeData import analyzeData
import matplotlib.pyplot as plt
import os


outFolderPath = "out"
excelName = "Retry2"
sheetNames = ["Tabelle1"]

for sheetName in sheetNames:
    data = pd.read_excel("%s.xlsx"%excelName, sheetName)
    for i in range(3):
        ts, pts, omegas, avOmegas = analyzeData(data,"t%d"%i, "pt%d"%i)
        plt.plot(ts, avOmegas)
        plt.plot(ts, omegas)
        plt.xlabel("t[s]")
        plt.ylabel("$\omega$[rad/s]")
        plt.show()
        outData = []
        for t,pt, omega, avOmega in zip(ts,pts,omegas,avOmegas):
            outData.append([t,pt,omega,avOmega])
        outData = pd.DataFrame(outData, columns=["t","pt","omega","avOmega"])
        outDirPath = "%s/%s"%(outFolderPath, excelName)
        if not os.path.exists(outDirPath):
            os.makedirs(outDirPath)
        outPath = "%s/%s_%d.xlsx"%(outDirPath, sheetName, i)
        outData.to_excel(outPath)