import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import solveset, log, Symbol, S, nsolve
x=0
R=0.0125
ridge_max=0.0025
ridge_width=0.004
x_step=ridge_width/100
def width_function_up(z, ridge_width, ridge_max, R):
    global function
    function = R + ridge_max * np.sin(z * np.pi / (ridge_width)) #((z/(ridge_width/100))*ridge_max/50)
ext = np.linspace(0, ridge_width/2, 50)
height = []
for i in ext:
    width_function_up(i, ridge_width, ridge_max, R)
    height.append(function)
print(height)
v=12
v_initial=v
v_ur=v
v_real=v
k=0.41
epsilon=0.0015
density=1.2041
viscosity=1.516*(1/(10**5)) #kinematic
#C=5.1
#t_max=0
B=ridge_max/(R*2)
A=B/2
x_value=[]
A_value = []
B_value = []
V_t_value = []
blockage_value= []
U_infinite_value= []
v_value=[]
v_ur_value=[]
v_real_value=[]
wall=[]
real_blockage_value=[]
def equationAB(p):
    dA, dB = p
    return (a_11 * dB + a_12 * dA - b_1 * x_step, a_21 * dB + a_22 * dA - b_2 * x_step)
def equationAV_t(z):
    V_t, A=z
    return (((((1/A)-2)/(0.05+np.log(k*Re)-np.log(abs(V_t/A))))-(V_t/A)), A-A)
while x<=(ridge_width/2):
    AR = (R+ridge_max)/R
    theta = (np.arctan((height[int(x / x_step)]-height[int(x / x_step) - 1])/(x_step)))
    blockage=B*(height[int(x/x_step)])*2
    real_blockage=blockage/A
    U_infinite=(v_initial*R**2*np.pi)/(height[int(x/x_step)]*2-2*blockage)
    Re=(U_infinite*blockage)/(viscosity)
    s = Symbol('s')
    eq = (((1 / A) - 2) / (0.05 + log(k * Re) - log(abs(s / A)))) - (s / A)
    V_t = nsolve(eq, 3, domain=S.Reals, tol=100000000)
    #V_t, A= fsolve(equationAV_t, (0.05, 0.05))
    U_t = V_t * k * U_infinite
    t_max = -(U_t ** 2) * density
    U_B = 2 * (A - V_t) * U_infinite
    C = 5 + (U_B / (2 * U_t)) * (1 - np.cos((np.pi * R) / (blockage / A)))
    h=(1.5+0.179*(V_t/A)+0.321*(V_t/A)**2)*A
    H=(1/(1-h))
    a_11= (1/(B*(1-2*B)))*(1-h+C*V_t+2*B*(2-h+(epsilon/A)))
    a_21= (1/(B*(1-2*B)))
    a_12= C*((V_t/A)-2)
    b_1=(2/(blockage))*((k**2*V_t**2)/1)+((2*theta)/(height[int(x/x_step)]*2))*(2-h+(epsilon/A))
    a_22= (1/(A*(1-A)))
    b_2=(A/(blockage*(1-A)))*((10*t_max)/(density*U_infinite**2))*C+((0.642+0.179*(2.05+np.log(k*Re))+(0.179-0.642*(0.05+np.log(k*Re)))*(V_t/A))/((1.05+np.log(k*Re))**2))
    x_value.append(x)
    v_value.append(v)
    v_ur_value.append(v_ur)
    v_real_value.append(v_real)
    B_value.append(B)
    A_value.append(A)
    V_t_value.append(V_t)
    U_infinite_value.append(U_infinite)
    blockage_value.append(blockage)
    real_blockage_value.append(real_blockage)
    wall.append(height[(int(x/x_step))]-blockage_value[(int(x/x_step))]+0.0025)
    if (x/x_step) != 0 and (x/x_step) != 50:
        v=v/(((height[(int(x/x_step))]-blockage_value[(int(x/x_step))])**2)/((height[(int(x/x_step))-1]-blockage_value[(int(x/x_step)-1)])**2))
        v_real=v/(((height[(int(x/x_step))]-real_blockage_value[(int(x/x_step))])**2)/((height[(int(x/x_step))-1]-real_blockage_value[(int(x/x_step)-1)])**2))
        v_ur=v_ur/(((height[(int(x/x_step))])**2)/((height[(int(x/x_step))-1])**2))
    dA, dB = fsolve(equationAB, (0.025, 0.025))
    A=A+dA
    B=B+dB
    x = x + x_step
#blockage_value.remove(blockage_value[0])
#v_value.remove(v_value[0])
#x_value.remove(x_value[0])
#B_value.remove(B_value[0])
#wall.remove(wall[0])
print(sum(v_value)/len(v_value))
print(sum(v_ur_value)/len(v_ur_value))
""""
plt.plot(x_value, blockage_value)
plt.title('Blockage')
#plt.show()
plt.plot(x_value, v_value)
plt.plot(x_value, v_ur_value)
plt.title('v')
#plt.show()
plt.plot(x_value, B_value)
plt.title('B')
#plt.show()
plt.plot(x_value, A_value)
plt.title('A')
#plt.show()
plt.plot(x_value, U_infinite_value)
plt.title('U_infinite')
#plt.show()
plt.plot(x_value, V_t_value)
plt.title('V_t')
#plt.show()
plt.plot(x_value, wall)
plt.plot(x_value, height)
plt.title('Wall')
#plt.show()
"""""

height_down=height[::-1]
v_down_value=[]
blockage_value_inverse=blockage_value[::-1]
real_blockage_value_inverse=real_blockage_value[::-1]
while x<=(ridge_width):
    x_value.append(x)
    v_value.append(v)
    v_ur_value.append(v_ur)
    v_real_value.append(v_real)
    if int(x / x_step) != 50 and int(x / x_step) != 100:
        v = v / (((height_down[(int(x / x_step))-50] - blockage_value_inverse[(int(x / x_step))-50]) ** 2) / (
                    (height_down[(int(x / x_step)) - 51] - blockage_value_inverse[(int(x / x_step) - 51)]) ** 2))
        v_real=v / (((height_down[(int(x / x_step))-50] - real_blockage_value_inverse[(int(x / x_step))-50]) ** 2) / (
                    (height_down[(int(x / x_step)) - 51] - real_blockage_value_inverse[(int(x / x_step) - 51)]) ** 2))
        v_ur = v_ur / (((height_down[(int(x / x_step))-50]) ** 2) / ((height_down[(int(x / x_step)) - 51]) ** 2))
    x = x + x_step
v_certain=[]
zip_object = zip(v_ur_value, v_value)
for v_ur_value_i, v_value_i in zip_object:
    v_certain.append((v_ur_value_i-v_value_i)+v_initial)
print(sum(v_certain)/len(v_certain))
plt.plot(x_value, v_certain)
#plt.plot(x_value, v_real_value)
plt.plot(x_value, v_ur_value)
plt.xlabel('x(m)')
plt.ylabel('v(m/s)')
plt.title('Flow over corrugation')
plt.show()