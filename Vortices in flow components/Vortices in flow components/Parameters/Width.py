import numpy as np
import pandas as pd
import math as m
from scipy.special import lambertw
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
w=0.002
w_value=[]
w_use2=[]
w_use=[]
while w<=0.01:
    w=w+0.001
    w_value.append(w)
omega_value = []
omega_value2 =[]
outData = []
outData2 =[]
for r in w_value:
    o = 0
    omega_current = []
    omega_current2=[]
    while o <= 50:
        length = 0.2
        # length of tube in m

        R = 0.0125
        # radius of tube in m

        ridge_max = 0.0025
        # maximum depth of ridges in m

        ridge_width = r
        # width of a ridge in m

        width = 0.002
        # distance between ridges in m

        frequency = 0.00645  # (width**2)/(ridge_width+0.000046775)
        # ridge frequency in ridge per m

        omega = 2 * np.pi * o
        # angular velocity in rad/s

        v_1 = omega * 0
        # tangential velocity at near end

        v_2 = omega * length
        # tangential velocity at far end

        viscosity = 1.825 * (1 / (10 ** 5))  # dynamic
        # viscosity of air in kg/m.s

        density = 1.2041  # 1.1839
        # density of air in kg/m^3

        v_sound = 340
        # velocity of sound in m/s at STP

        p_delta = ((v_2 ** 2) - (v_1 ** 2)) * (density / 2)
        # p_delta is pressure difference at ends

        L = 0


        def equations(p):
            v, f = p
            return (((p_delta * 2 * R * 2) / (length * density * f)) ** (1 / 2) - v,
                    (1 / (0.838 * lambertw(0.629 * (2 * v * R * density) / viscosity))) ** 2 - f)


        v, f = fsolve(equations, (0.05, 0.05))


        # v=omega*length
        def darcy_friction_factor(Re):
            global f_d
            f_d = (1 / (0.838 * lambertw(0.629 * Re))) ** 2


        def velocity_loss(width, v, R, f_d):
            global v_f
            c = (f_d * width) / (8 * R)
            v_f = v  # (v - c * v) / (c + 1)


        f = []
        l = []
        v_data = []
        Re_data = []
        v_initial_flow = v
        while L <= length:
            Re = (2 * v * R * density) / viscosity
            Sr = 0.3585  # 0.198*(1-(19.7/Re)) / 0.21
            darcy_friction_factor(Re)
            velocity_loss(width, v, R, f_d)
            v_use = (v + v_f) / 2
            v = v_f
            f.append((Sr * v_f) / (frequency))
            l.append(L)
            v_data.append(v)
            Re_data.append(Re * Sr)
            L = L + width


            def velocity_loss_sin(height, blockage_value, ridge_width, density, viscosity):
                global v_f_sin
                global Re
                global Sr
                global f_d
                if x < (ridge_width / 2):
                    Re = (2 * v * R * density) / viscosity
                    Sr = 0.3585
                    f_d = (1 / (0.838 * lambertw(0.629 * Re))) ** 2
                    c = (f_d * (ridge_width / x_size)) / (
                            8 * R)
                    v_f_sin = v  # (v - c * v) / (c + 1)
                else:
                    Re = (2 * v * R * density) / viscosity
                    Sr = 0.3585
                    f_d = (1 / (0.838 * lambertw(0.629 * Re))) ** 2
                    c = (f_d * (ridge_width / x_size)) / (8 * R)
                    v_f_sin = v  # (v - c * v) / (c + 1)


            x_size = 100


            def width_function_up(z, ridge_width, ridge_max, R):
                global function
                function = R + ridge_max * np.sin(z * np.pi / (ridge_width))


            ext = np.linspace(0, ridge_width / 2, int(x_size / 2))
            height = []
            for i in ext:
                width_function_up(i, ridge_width, ridge_max, R)
                height.append(function)
            x = 0
            """v_initial = v
            k = 0.41
            epsilon = 0.0015
            density = 1.2041
            viscosity_kinematic = 1.516 * (1 / (10 ** 5))
            B = ridge_max / (R * 2)
            A = B / 2"""
            x_step = ridge_width / x_size

            """""
            def equationAB(p):
                dA, dB = p
                return (a_11 * dB + a_12 * dA - b_1 * x_step, a_21 * dB + a_22 * dA - b_2 * x_step)


            def equationAV_t(z):
                V_t, A = z
                return (((((1 / A) - 2) / (0.05 + np.log(k * Re_corr) - np.log(abs(V_t / A)))) - (V_t / A)), A - A)
            """

            blockage_value = []
            while x <= (ridge_width / 2):
                blockage = 0
                """AR = (((height[int(x / x_step)]) ** 2 * np.pi) / (height[int(x / x_step) - 1] ** 2 * np.pi))
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
                b_2 = (A / (blockage * (1 - A))) * ((10 * t_max) / (density * U_infinite ** 2)) * C + (
                            (0.642 + 0.179 * (
                                    2.05 + np.log(k * Re_corr)) + (0.179 - 0.642 * (0.05 + np.log(k * Re_corr))) * (
                                         V_t / A)) / ((1.05 + np.log(
                        k * Re)) ** 2))"""
                blockage_value.append(blockage)
                velocity_loss_sin(height, blockage_value, ridge_width, density, viscosity)
                v = v_f_sin
                if x < (4 * 10 ** (-5)) and x > (4 * 10 ** (-5)):
                    f.append((Sr * v_f_sin) / (frequency))
                    l.append(L)
                    v_data.append(v)
                    Re_data.append(Re * Sr)
                #if (x / x_step) != 0 and (x / x_step) != (x_size / 2):
                    #v = v / 1
                """dA, dB = fsolve(equationAB, (0.025, 0.025))
                A = A + dA.real
                B = B + dB.real"""
                L = L + x_step
                x = x + x_step
            height_down = height[::-1]
            v_down_value = []
            blockage_value_inverse = blockage_value[::-1]
            while x <= (ridge_width):
                velocity_loss_sin(height_down, blockage_value_inverse, ridge_width, density, viscosity)
                v = v_f_sin
                if x < (ridge_width + 4 * 10 ** (-5)) and x > (ridge_width - 4 * 10 ** (-5)):
                    f.append((Sr * v_f_sin) / (frequency))
                    l.append(L)
                    v_data.append(v)
                    Re_data.append(Re * Sr)
                #if int(x / x_step) != (x_size / 2) and int(x / x_step) != x_size:
                    #v = v / 1
                L = L + x_step
                x = x + x_step
        Volume = ((2 / 3) * np.pi * (ridge_width / 2) * ((R + ridge_max) ** (2) + R * (R + ridge_max) + R ** 2)) - (
                R ** (2) * np.pi * ridge_width)
        p = 1
        f_r = []
        f_r_o = ((1 / ((1 + (Volume / (R ** (2) * np.pi * (width + ridge_width)))) ** (1 / 2))) - (
                v_initial_flow / v_sound) ** (2)) * (v_sound / (2 * (length + 1.2 * R))) * p
        f_r.append(f_r_o)
        for i in f_r:
            if abs(max(f) - i) < 10 and abs(min(f) - i) < 10:
                # if 0.94*(v_sound / (2 * (length + 1.2 * R))) <= max(f) and 0.94*(v_sound / (2 * (length + 1.2 * R))) >= min(f) and abs(0.94*(v_sound / (2 * (length + 1.2 * R)))-max(f))<=2:
                omega_value.append(o)
                w_use.append(r)
                omega_current.append(o)
                outData.append([r, o])
        """if 0.94*(v_sound / (2 * (length + 1.2 * R))) <= max(f) and 0.94*(v_sound / (2 * (length + 1.2 * R))) >= min(f) and abs(0.94*(v_sound / (2 * (length + 1.2 * R)))-min(f))<=2:
            omega_value_max.append(o)
            l_use_max.append(x)
            omega_current_max.append(o)"""
        for i in f_r:
            if abs(max(f) - 2 * i) < 10 and abs(min(f) - 2 * i) < 10:
                omega_value2.append(o)
                w_use2.append(r)
                omega_current2.append(o)
                outData2.append([r, o])
        if len(omega_current) != 0 and len(omega_current2) != 0:
            break
        o = o + 0.01
outData = pd.DataFrame(outData, columns=["W[m]", "f[Hz]"])
outData2 = pd.DataFrame(outData2, columns=["W[m]", "f[Hz]"])
outData.to_excel("Output/Width.xlsx")
outData2.to_excel("Output/Width2.xlsx")
print(omega_value)
print(w_use)
plt.plot(w_use, omega_value)
plt.plot(w_use2, omega_value2)
plt.title('Width')
plt.show()