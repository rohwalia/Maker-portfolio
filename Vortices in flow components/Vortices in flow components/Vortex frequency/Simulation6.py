from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.special import lambertw
from sympy import solveset, log, Symbol, S, nsolve
from scipy.optimize import fsolve
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

frequency=0.00645 #(width**2)/(ridge_width+0.000046775)
#ridge frequency in ridge per m

omega=2*np.pi*1.886266
#angular velocity in rad/s

v_1= omega*0
#tangential velocity at near end

v_2= omega*length
#tangential velocity at far end

viscosity= 1.825*(1/(10**5)) #dynamic
#viscosity of air in kg/m.s

density=1.2041 #1.1839
#density of air in kg/m^3

v_sound= 343.21
#velocity of sound in m/s at STP

p_delta= ((v_2**2)-(v_1**2))*(density/2)
#p_delta is pressure difference at ends

L=0
def equations(p):
    v,f=p
    return (((p_delta*2*R*2)/(length*density*f))**(1/2)-v, (1/(0.838*lambertw(0.629*(2*v*R*density)/viscosity)))**2-f)
v,f= fsolve(equations, (0.05, 0.05))
#v=omega*length
def darcy_friction_factor(Re):
    global f_d
    f_d=(1/(0.838*lambertw(0.629*Re)))**2
def velocity_loss (width, v, R, f_d):
    global v_f
    c=(f_d*width)/(8*R)
    v_f=(v-c*v)/(c+1)
outData = []
f=[]
l=[]
v_data=[]
Re_data=[]
v_initial_flow=v
while L<=length:
    Re= (2*v*R*density)/viscosity
    Sr= 0.3585 #0.198*(1-(19.7/Re)) / 0.21
    darcy_friction_factor(Re)
    velocity_loss(width, v, R, f_d)
    v_use=(v+v_f)/2
    v = v_f
    f.append((Sr * v_f) / (frequency))
    l.append(L)
    v_data.append(v)
    Re_data.append(Re*Sr)
    L=L+width
    def velocity_loss_sin(height, blockage_value, ridge_width, density, viscosity):
        global v_f_sin
        global Re
        global Sr
        global f_d
        if x<(ridge_width/2):
            Re = (2 * v * (height[(int(x / x_step))] - blockage_value[(int(x / x_step))]) * density) / viscosity
            Sr=0.3585
            f_d=(1/(0.838*lambertw(0.629*Re)))**2
            c = (f_d * (ridge_width / x_size)) / (8 * (height[(int(x / x_step))] - blockage_value[(int(x / x_step))]))
            v_f_sin=(v-c*v)/(c+1)
        else:
            Re = (2 * v * (height[(int(x / x_step))-int(x_size/2)] - blockage_value[(int(x / x_step))-int(x_size/2)]) * density) / viscosity
            Sr=0.3585
            f_d=(1/(0.838*lambertw(0.629*Re)))**2
            c = (f_d * (ridge_width / x_size)) / (8 * (height[(int(x / x_step))-int(x_size/2)] - blockage_value[(int(x / x_step))-int(x_size/2)]))
            v_f_sin=(v-c*v)/(c+1)
    x_size = 100
    def width_function_up(z, ridge_width, ridge_max, R):
        global function
        function = R + ridge_max * np.sin(z * np.pi / (ridge_width))
    ext = np.linspace(0, ridge_width / 2, int(x_size/2))
    height = []
    for i in ext:
        width_function_up(i, ridge_width, ridge_max, R)
        height.append(function)
    x=0
    v_initial = v
    k = 0.41
    epsilon = 0.0015
    density = 1.2041
    viscosity_kinematic = 1.516 * (1 / (10 ** 5))
    B = ridge_max / (R * 2)
    A = B / 2
    x_step = ridge_width / x_size
    def equationAB(p):
        dA, dB = p
        return (a_11 * dB + a_12 * dA - b_1 * x_step, a_21 * dB + a_22 * dA - b_2 * x_step)
    def equationAV_t(z):
        V_t, A = z
        return (((((1 / A) - 2) / (0.05 + np.log(k * Re_corr) - np.log(abs(V_t / A)))) - (V_t / A)), A - A)
    blockage_value=[]
    while x <= (ridge_width / 2):
        AR = (((height[int(x / x_step)]) ** 2 * np.pi) / (height[int(x / x_step) - 1] ** 2 * np.pi))
        theta = (np.arctan((height[int(x / x_step)] - height[int(x / x_step) - 1]) / (x_step)))
        blockage = B * (height[int(x / x_step)]) * 2
        U_infinite = (v_initial * R ** 2 * np.pi) / (height[int(x / x_step)] * 2 - 2 * blockage)
        Re_corr = (U_infinite * blockage) / (viscosity)
        s = Symbol('s')
        eq = (((1 / A) - 2) / (0.05 + log(k * Re_corr) - log(abs(s / A)))) - (s / A)
        V_t = nsolve(eq, 3, domain=S.Reals, tol=10000000000)
        U_t = V_t * k * U_infinite
        t_max = -(U_t ** 2) * density
        U_B = 2 * (A - V_t) * U_infinite
        C = 5 + (U_B / (2 * U_t)) * (1 - np.cos((np.pi * R) / (blockage / A)))
        h = (1.5 + 0.179 * (V_t / A) + 0.321 * (V_t / A) ** 2) * A
        H = (1 / (1 - h))
        a_11 = (1 / (B * (1 - 2 * B))) * (1 - h + C * V_t + 2 * B * (2 - h + (epsilon / A)))
        a_21 = (1 / (B * (1 - 2 * B)))
        a_12 = C * ((V_t / A) - 2)
        b_1 = (2 / (blockage)) * ((k ** 2 * V_t ** 2) / 1) + ((2 * theta) / (height[int(x / x_step)] * 2)) * (
                    2 - h + (epsilon / A))
        a_22 = (1 / (A * (1 - A)))
        b_2 = (A / (blockage * (1 - A))) * ((10 * t_max) / (density * U_infinite ** 2)) * C + ((0.642 + 0.179 * (
                    2.05 + np.log(k * Re_corr)) + (0.179 - 0.642 * (0.05 + np.log(k * Re_corr))) * (V_t / A)) / ((1.05 + np.log(
            k * Re)) ** 2))
        blockage_value.append(blockage)
        velocity_loss_sin(height, blockage_value, ridge_width, density, viscosity)
        v=v_f_sin
        if x<(4*10**(-5)) and x>(4*10**(-5)):
            f.append((Sr * v_f_sin) / (frequency))
            l.append(L)
            v_data.append(v)
            Re_data.append(Re*Sr)
        if (x / x_step) != 0 and (x / x_step) != (x_size/2):
            v = v / (((height[(int(x / x_step))] - blockage_value[(int(x / x_step))]) ** 2) / (
                        (height[(int(x / x_step)) - 1] - blockage_value[(int(x / x_step) - 1)]) ** 2))
        dA, dB = fsolve(equationAB, (0.025, 0.025))
        A = A + dA
        B = B + dB
        L = L + x_step
        x = x + x_step
    height_down = height[::-1]
    v_down_value = []
    blockage_value_inverse = blockage_value[::-1]
    while x <= (ridge_width):
        velocity_loss_sin(height_down, blockage_value_inverse, ridge_width, density, viscosity)
        v = v_f_sin
        if x<(ridge_width+4*10**(-5)) and x>(ridge_width-4*10**(-5)):
            f.append((Sr * v_f_sin) / (frequency))
            l.append(L)
            v_data.append(v)
            Re_data.append(Re*Sr)
            outData.append([L, (Sr * v_f_sin) / (frequency), v_f_sin])
        if int(x / x_step) != (x_size/2) and int(x / x_step) != x_size:
            v = v / (((height_down[(int(x / x_step)) - int(x_size/2)] - blockage_value_inverse[(int(x / x_step)) - int(x_size/2)]) ** 2) / (
                    (height_down[(int(x / x_step)) - int(x_size/2)-1] - blockage_value_inverse[(int(x / x_step) - int(x_size/2)-1)]) ** 2))
        L = L + x_step
        x = x + x_step

outData = pd.DataFrame(outData, columns=["L[m]", "f[Hz]", "v[m/s]"])
#outData.to_excel("Output/Frequenzen6.xlsx")
window_size = 10
numbers_series = pd.Series(f)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
f = moving_averages_list[window_size - 1:]
numbers_series = pd.Series(l)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
l = moving_averages_list[window_size - 1:]
numbers_series = pd.Series(v_data)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
v_data = moving_averages_list[window_size - 1:]
numbers_series = pd.Series(Re_data)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()
moving_averages_list = moving_averages.tolist()
Re_data = moving_averages_list[window_size - 1:]
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


sampleRate = 44100
frequency = 440
length_audio = 3
frequencies=[]

for i in f[::14]:
    i = i.real
    t = np.linspace(0, length_audio, sampleRate * length_audio)  # length of file
    y = np.sin(i * 2 * np.pi * t)  #  has frequency of f_value
    frequencies.append(y)
    #wavfile.write('Output/Sine1.wav', sampleRate, np.array(frequencies).T)

p=0
Volume= ((2/3)*np.pi*(ridge_width/2)*((R+ridge_max)**(2)+R*(R+ridge_max)+R**2))-(R**(2)*np.pi*ridge_width)
f_r=[]
while p*((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))<=max(f):
    f_r_o=((1/((1+(Volume/(R**(2)*np.pi*(width+ridge_width))))**(1/2)))-(v_initial_flow/v_sound)**(2))*(v_sound/(2*(length+1.2*R)))*p
    p=p+1
    f_r.append(f_r_o)
f_r_s=[]
for i in f_r:
    if i<=max(f) and i>=min(f):
        f_r_s.append(i)
print('1st Harmonic:')
print(f_r_s)
f_r_s_2=[]
for i in f_r:
    if 2*i<=max(f) and 2*i>=min(f):
        f_r_s_2.append(i)
print('2nd Harmonic:')
print(f_r_s_2)
sampleRate = 44100
frequency = 440
length_audio = 3
frequencies_2=[]

for i in f_r_s:
    i=i.real
    t = np.linspace(0, length_audio, sampleRate * length_audio)  # length of file
    y = np.sin(i * 2 * np.pi * t)  #  has frequency of f_value
    frequencies_2.append(y)
    #wavfile.write('Output/Sine2.wav', sampleRate, np.array(frequencies_2).T)
k=0
def closest(value, f_r_s, x):
    global id
    value = np.asarray(value)
    id = np.argpartition((np.abs(value - f_r_s)), x)[x]
f_amp=[]
k_list=[]
for i in f_r_s:
    while k<=6:
        closest(f, i, k)
        k_list.append(id)
        k=k+1
    for i in k_list:
        f_amp.append(f[i].real)

print(f_amp)
sampleRate = 44100
frequency = 440
length_audio = 3
frequencies_3=[]

for i in f_amp:
    i=i.real
    t = np.linspace(0, length_audio, sampleRate * length_audio)  # length of file
    y = np.sin(i * 2 * np.pi * t)  #  has frequency of f_value
    frequencies_3.append(y)
    #wavfile.write('Output/Sine3.wav', sampleRate, np.array(frequencies_3).T)