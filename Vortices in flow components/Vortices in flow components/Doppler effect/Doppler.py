import matplotlib.pyplot as plt
import math as m
f_value=[]
t_value=[]
t=0
while t<3:
    if 160837196977711168*m.sin(12671 / 2000*t) / (135026116681*m.cos(12671 / 2000* t)*m.cos(12671 / 2000* t) + 50415374800000*m.cos(12671 / 2000 *t) + 4705960000000000)>=0:
        f=1007.1 * 343 / (343 + 12.671 * 0.145*m.cos(12.671*t / 2))
        f_value.append(f)
        t_value.append(t)
    else: # 160837196977711168*m.sin(12671 / 2000*t) / (135026116681*m.cos(12671 / 2000* t)*m.cos(12671 / 2000* t) + 50415374800000*m.cos(12671 / 2000 *t) + 4705960000000000)<0:
        f=1007.1 * 343 / (343 - 12.671 * 0.145*m.cos(12.671*t / 2))
        f_value.append(f)
        t_value.append(t)
    t=t+0.001
plt.plot(t_value, f_value)
plt.xlabel("t(s)")
plt.ylabel("f(Hz)")
plt.title('Doppler')
plt.show()