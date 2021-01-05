from scipy.special import lambertw
import numpy as np
length=0.445
#length of tube in m

R=0.0125
#radius of tube in m

ridge_max=0.0025
#maximum depth of ridges in m

ridge_width=0.004
#width of a ridge in m

width=0.0025
#distance between ridges in m


omega=2*np.pi*1.886
#angular velocity in rad/s

v_1= omega*0
#tangential velocity at near end

v_2= omega*length
#tangential velocity at far end

viscosity= 1.825*(1/(10**5))
#viscosity of air in kg/m.s

density=1.2041 #1.1839
#density of air in kg/m^3

v_sound= 343.21
#velocity of sound in m/s at STP

p_delta= ((v_2**2)-(v_1**2))*(density/2)
#p_delta is pressure difference at ends

from scipy.optimize import fsolve
def equations(p):
    v,f=p
    return (((p_delta*2*R*2)/(length*density*f))**(1/2)-v,
            (1/(0.838*lambertw(0.629*(2*v*R*density)/viscosity)))**2-f)
v,f= fsolve(equations, (0.05, 0.05))
print(equations((v,f)))
print(v)
print(f)
#v=omega*length

"""def equations2(p):
    v_2,f_2=p
    return (((p_delta*2*R*2)/(length*density*f_2))**(1/2)-v_2, 64/((2*v_2*R*density)/viscosity)-f_2)#(0.25/(m.log((0.5/3.7)+(5.74/(2*v_2*R*(density/viscosity))**0.9)))**2)-f_2)
v_2,f_2= fsolve(equations2, (0.01, 0.01))
print(equations2((v_2,f_2)))"""

"""j=0
omega=[]
v_data=[]
def graph(i):
    global v_2
    global f_2
    length = 1.08
    R = 0.019
    omega = 2 * np.pi * i
    v_1 = omega * 0
    v_2 = omega * length
    viscosity = 1.825 * (1 / (10 ** 5))
    density = 1.22
    p_delta = ((v_2 ** 2) - (v_1 ** 2)) * (density / 2)
    # p_delta is pressure difference at ends

    def equations2(p):
        v_2, f_2 = p
        return (((p_delta * 2 * R * 2) / (length * density * f_2)) ** (1 / 2) - v_2,
                64 / ((2 * v_2 * R * density) / viscosity) - f_2)
v_2, f_2 = fsolve(equations2, (0.05, 0.05))
while j<10:
    omega.append(j)
    j=j+0.1
for i in omega:
    graph(i)
    v_data.append(v_2)
import matplotlib.pyplot as plt
plt.plot(omega, v_data)
plt.xlabel("$Frequenz$[Hz]")
plt.ylabel("$v$[m/s]")
plt.title('Dreh')
plt.show()"""
