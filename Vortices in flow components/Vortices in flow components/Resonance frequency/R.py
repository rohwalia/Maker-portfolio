import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
r=0.01
R_value=[]
f_use_1=[]
f_use_2=[]
outData=[]
while r<=0.045:
    r=r+0.001
    R_value.append(r)
for x in R_value:
    length=0.57
    #length of tube in m

    v_initial_flow=10

    R= x
    #radius of tube in m

    ridge_max=0.003
    #maximum depth of ridges in m

    ridge_width=0.003
    #width of a ridge in m

    width=0.002
    #distance between ridges in m

    viscosity= 1.825*(1/(10**5)) #dynamic
    #viscosity of air in kg/m.s

    density=1.2041 #1.1839
    #density of air in kg/m^3

    v_sound= 340
    #velocity of sound in m/s at STP

    Volume= ((R+ridge_max)**2*np.pi-R**2*np.pi)*ridge_max*ridge_width

    f_use_1.append(((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*1)
    f_use_2.append(((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*2)
    outData.append([((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*1,
                   ((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*2, x])
outData = pd.DataFrame(outData, columns=["f1[Hz]", "f2[Hz]", "R[m]"])
outData.to_excel("Output/R.xlsx")
plt.plot(R_value, f_use_1)
plt.plot(R_value, f_use_2)
plt.xlabel("$R$[m]")
plt.ylabel("$f$[Hz]")
plt.title('Frequency')
plt.show()