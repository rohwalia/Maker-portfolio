from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as m
from scipy.special import lambertw
length=(0.580/1)
#length of tube in m

R=0.0125
#radius of tube in m

ridge_max=0.003
#maximum depth of ridges in m

ridge_width=0.0035
#width of a ridge in m

width=0.0025
#distance between ridges in m

frequency=(width**2)/(width)
#ridge frequency in ridge per m

frequency_ridge = (ridge_width**2)/(ridge_width)

omega=2*np.pi*1.16
#angular velocity in rad/s

v_1= omega*0
#tangential velocity at near end

v_2= omega*length
#tangential velocity at far end

viscosity= 1.825*(1/(10**5))
#viscosity of air in kg/m.s

density=1.1839
#density of air in kg/m^3

v_sound= 346
#velocity of sound in m/s at STP

p_delta= ((v_2**2)-(v_1**2))*(density/2)
#p_delta is pressure difference at ends

L=0
def darcy_friction_factor(Re):
    global f_d
    f_d=(1/(0.838*lambertw(0.629*Re)))**2
def velocity_loss (width, v, R, f_d):
    global v_f
    v_f=v-((width*f_d)/(2*2*R))
def v_wall (v_use, Re):
    global v_use_wall
    F= 0.316*(1/Re)**(0.25)
    v_use_wall=v_use * (1+1.33*(F)**0.5) * ((1-(R/0.015))**(1/7))
outData = []
f=[]
l=[]
v_data=[]
Re_data=[]
from solvingv_panzer import v
while L<=length:
    Re= (2*v*R*density)/viscosity
    Sr= 0.1551 #0.198*(1-(19.7/Re)) / 0.21
    darcy_friction_factor(Re)
    velocity_loss(width, v, R, f_d)
    v_use=(v+v_f)/2
    v_wall(v_use, Re)
    v = v_f
    f.append((Sr*v_use_wall)/(frequency))
    l.append(L)
    v_data.append(v)
    Re_data.append(Re)
    L=L+width
    outData.append([L, (Sr*v_use_wall)/(frequency), v])
    def width_function (z, ridge_width, ridge_max, R):
        global function
        function= R+ridge_max*np.sin(z*m.pi/(ridge_width))
    ext=np.linspace(0, ridge_width, 7)
    height=[]
    for i in ext:
        width_function(i, ridge_width, ridge_max,R)
        height.append(function)
    def velocity_loss_sin(height, t, width, density, viscosity):
        global v_f_sin
        global Re
        global Sr
        global f_d
        Re = (2 * v * height[t] * density) / viscosity
        Sr=0.1551 #0.198*(1-(19.7/Re)) / 0.21
        f_d=(1/(0.838*lambertw(0.629*Re)))**2
        v_f_sin=v-(((ridge_width/6)*f_d)/(2*2*(height[t])))
    def v_wall_sin(v_f_sin, Re):
        global v_use_wall
        F = 0.316 * (1 / Re) ** (0.25)
        v_use_wall = (v_f_sin * (1 + 1.33 * (F) ** 0.5)) * ((1-(R/0.015))**(1/7))
    L_ursprung=L
    t=0
    while L<=L_ursprung+ridge_width:
        velocity_loss_sin(height, t, ridge_width, density, viscosity)
        L = L + (ridge_width / 6)
        t = t + 1
        v_wall_sin(v_f_sin, Re)
        v=v_f_sin
        f.append((Sr*v_use_wall) / (frequency_ridge))
        l.append(L)
        v_data.append(v)
        Re_data.append(Re)
        outData.append([L, (Sr*v_use_wall) / (frequency_ridge), v_f_sin])
outData = pd.DataFrame(outData, columns=["L[m]", "f[Hz]", "v[m/s]"])
outData.to_excel("Output/Frequenzen3.xlsx")
plt.plot(l, f)
plt.xlabel("$L$[m]")
plt.ylabel("$f$[Hz]")
plt.title('Frequencies')
plt.show()
plt.plot(l, v_data)
plt.xlabel("$L$[m]")
plt.ylabel("$v$[m/s]")
plt.title('Velocities')
plt.show()
plt.plot(l, Re_data)
plt.xlabel("$L$[m]")
plt.ylabel("Re")
plt.title('Reynolds Number')
plt.show()
print(f)
print(v_data)
print(sum(f)/len(f))
p=0
f_r=[]
while p*(v_sound/(2*(length+1.2*R)))<=max(f):
    f_r_o=(v_sound/(2*(length+1.2*R)))*p
    p=p+1
    f_r.append(f_r_o)
f_r_s=[]
for i in f_r:
    if i<=max(f) and i>=min(f):
        print(i)
        f_r_s.append(i)
print(f_r_s)

def closest(value, f_r_s):
    global id
    value = np.asarray(value)
    id = (np.abs(value - f_r_s)).argmin()

f_amp=[]
for i in f_r_s:
    closest(f, i)
    for i in [id , id+7, id-7]:
        f_amp.append(f[i].real)

print(f_amp)