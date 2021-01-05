import numpy as np
import pandas as pd
import math as m
from scipy.special import lambertw
import matplotlib.pyplot as plt
o=0
omega_resonance=[]
omega_value=[]
while o<=20:
    omega=2*np.pi*o
    #angular velocity in rad/s

    length=0.222
    #length of tube in m

    R=0.0125
    #radius of tube in m

    ridge_max=0.0025
    #maximum depth of ridges in m

    ridge_width=0.0065
    #width of a ridge in m

    width=0.0065
    #distance between ridges in m

    frequency=(width**2)/(width+0.000046775)
    #ridge frequency in ridge per m

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
        v_use_wall=v_use * (1+1.33*(F)**0.5)* ((1-(R/0.015))**(1/2.34))
    from scipy.optimize import fsolve
    def equations(p):
        v,f=p
        return (((p_delta*2*R*2)/(length*density*f))**(1/2)-v, (1/(0.838*lambertw(0.629*(2*v*R*density)/viscosity)))**2-f)
    v,f= fsolve(equations, (0.05, 0.05))
    #print(equations((v,f)))
    f = []
    while L<=length:
        Re= (2*v*R*density)/viscosity
        Sr= 0.3585 #0.198*(1-(19.7/Re)) / 0.21
        darcy_friction_factor(Re)
        velocity_loss(width, v, R, f_d)
        v_use=(v+v_f)/2
        v_wall(v_use, Re)
        v = v_f
        f.append((Sr*v_use_wall)/(frequency))
        L=L+width
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
            Sr=0.3585 #0.198*(1-(19.7/Re)) / 0.21
            f_d=(1/(0.838*lambertw(0.629*Re)))**2
            v_f_sin=v-(((width/6)*f_d)/(2*2*(height[t])))
        def v_wall_sin(v_f_sin, Re):
            global v_use_wall
            F = 0.316 * (1 / Re) ** (0.25)
            v_use_wall = (v_f_sin * (1 + 1.33 * (F) ** 0.5)) * ((1-((height[t]/2)/0.015))**(1/2.34))
        L_ursprung=L
        t=0
        while L<=L_ursprung+ridge_width:
            velocity_loss_sin(height, t, width, density, viscosity)
            v_wall_sin(v_f_sin, Re)
            L = L + (ridge_width / 6)
            t = t + 1
            v=v_f_sin
            f.append((Sr*v_use_wall) / (frequency))
    p=0
    f_r=[]
    while p*(v_sound/(2*(length+1.2*R)))<=max(f):
        f_r_o=(v_sound/(2*(length+1.2*R)))*p
        p=p+1
        f_r.append(f_r_o)
    f_r_s=[]
    for i in f_r:
        if i<=max(f) and i>=min(f):
            f_r_s.append(i)
            omega_resonance.append(i)
        """else:
            omega_resonance.append(0)"""
    for i in f_r_s:
        if len(f_r_s) != 0:
            omega_value.append(o)
        """else:
            omega_value.append(0)"""
    o=o+0.01
print(omega_value)
print(omega_resonance)
plt.plot(omega_value, omega_resonance, 'x')
plt.show()
omega_range=[]
for i in omega_resonance:
    if i !=0:
        omega_range.append(omega_value[omega_resonance.index(i)])
print(omega_range)
omega_range = list(dict.fromkeys(omega_range))
print(omega_range)