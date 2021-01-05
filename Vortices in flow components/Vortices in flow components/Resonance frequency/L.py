import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
l=0.12
l_value=[]
f_use_1=[]
f_use_2=[]
outData=[]
while l<=0.70:
    l=l+0.01
    l_value.append(l)
for r in l_value:
    length=r
    #length of tube in m

    v_initial_flow=10

    R=0.0125
    #radius of tube in m

    ridge_max=0.0025
    #maximum depth of ridges in m

    ridge_width=0.004
    #width of a ridge in m

    width=0.0025
    #distance between ridges in m

    viscosity= 1.825*(1/(10**5)) #dynamic
    #viscosity of air in kg/m.s

    density=1.2041 #1.1839
    #density of air in kg/m^3

    v_sound= 343.21
    #velocity of sound in m/s at STP

    Volume= ((2/3)*np.pi*(ridge_width/2)*((R+ridge_max)**(2)+R*(R+ridge_max)+R**2))-(R**(2)*np.pi*ridge_width)

    f_use_1.append(((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*1)
    f_use_2.append(((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*2)
    outData.append([((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*1,
                   ((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*2, r])
outData = pd.DataFrame(outData, columns=["f1[Hz]", "f2[Hz]", "L[m]"])
outData.to_excel("Output/L.xlsx")
plt.plot(l_value, f_use_1)
plt.plot(l_value, f_use_2)
plt.xlabel("$L$[m]")
plt.ylabel("$f$[Hz]")
plt.title('Frequency')
plt.show()
