import numpy as np
from PIL import Image
import glob
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
files = glob.glob('saved-data/images-gradient/*')
tensor = []
tensor_gradient = []
tensor_filter = []
for f in files:
    RGB = []
    dct = {}
    im = Image.open(f, "r")
    width, height = im.size
    factor = 0.1
    reduce_resolution = (int(width*factor), int(height*factor))
    im = im.resize(reduce_resolution)
    width, height = im.size
    #print(width)
    #print(height)
    dct["RGB_%s" %f] = []
    for i in range(width):
        #print("row finished:", i)
        for j in range(height):
            coordinate = (i,j)
            #https://www.kite.com/python/answers/how-to-find-the-rgb-value-of-a-pixel-in-python
            pixel_values = im.convert("RGB").getpixel(coordinate)
            dct["RGB_%s" %f].append([i,j, pixel_values])
            #print(dct["RGB_%s" %f])
    RGB.append(dct["RGB_%s" %f])
    RGB = RGB[0]
    RGB = [RGB[x:x+height] for x in range(0, len(RGB),height)]
    RGB = np.array(RGB)
    tensor.append(RGB.tolist())
    #print(RGB)
    #decrease resolution of images later on: https://deeplearning.lipingyang.org/2017/02/15/converting-tiff-to-jpeg-in-python/

    """print(RGB[7,4])
    print("R-value:", RGB[7,4, 2][0])
    print(len(RGB))"""

    def gradient(index_x,index_y):
        global R_mag, G_mag, B_mag

        """R_value = RGB[index_x, index_y, 0]
        G_value = RGB[index_x, index_y, 1]
        B_value = RGB[index_x, index_y, 2]"""

        R_gradient_x = RGB[index_x+1, index_y, 2][0] - RGB[index_x, index_y, 2][0]
        R_gradient_y = RGB[index_x, index_y+1, 2][0] - RGB[index_x, index_y, 2][0]
        R_vector = np.array([R_gradient_x, R_gradient_y])
        R_mag = np.sqrt(R_vector.dot(R_vector))
        G_gradient_x = RGB[index_x + 1, index_y, 2][1] - RGB[index_x, index_y, 2][1]
        G_gradient_y = RGB[index_x, index_y + 1, 2][1] - RGB[index_x, index_y, 2][1]
        G_vector = np.array([G_gradient_x, G_gradient_y])
        G_mag = np.sqrt(G_vector.dot(G_vector))
        B_gradient_x = RGB[index_x + 1, index_y, 2][2] - RGB[index_x, index_y, 2][2]
        B_gradient_y = RGB[index_x, index_y + 1, 2][2] - RGB[index_x, index_y, 2][2]
        B_vector = np.array([B_gradient_x, B_gradient_y])
        B_mag = np.sqrt(B_vector.dot(B_vector))
    gradient_values = []
    for i in range(width):
        for j in range(height):
            if j == height-1:
                pass
            elif i == width-1:
                pass
            else:
                gradient(i,j)
                #print([i,j, R_mag, G_mag, B_mag])
                gradient_values.append([i,j, R_mag, G_mag, B_mag])
    height = height - 1
    width = width - 1
    #print(gradient_values)
    gradient_values = np.array(gradient_values)
    tensor_gradient.append(gradient_values.tolist())

    threshold = 10
    gradient_filter = []
    for i in gradient_values:
        if i[2] >threshold and i[3] >threshold and i[4] >threshold:
            gradient_filter.append([i[0], i[1], 1])
        else:
            gradient_filter.append([i[0], i[1], 0])
    #print(gradient_filter)
    #gradient_filter = [gradient_filter[x:x + height] for x in range(0, len(gradient_filter), height)]
    gradient_filter = np.array(gradient_filter)
    tensor_filter.append(gradient_filter.tolist())
    """plt.scatter(gradient_filter[:,0], gradient_filter[:,1], c=gradient_filter[:,2], cmap='Blues',vmin=0, vmax=max(gradient_filter[:,2]))
    plt.colorbar()
    plt.show()"""
tensor = np.array(tensor)
tensor_gradient = np.array(tensor_gradient)
tensor_filter = np.array(tensor_filter)
#print(tensor_filter)
width = tensor_filter[0, -1, 0] + 1
height = tensor_filter[0, -1, 1] + 1
#print(tensor_filter[0])
tensor_average = []
for i in range(int(width)):
    for j in range(int(height)):
        #print((height*i+j))
        Average = sum(item[(int(height)*i+j)][2] for item in tensor_filter)/len(files)
        if Average >= 0.5:
            tensor_average.append([i, j , 1])
        else:
            tensor_average.append([i, j, 0])
tensor_average = np.array(tensor_average)
#print(tensor_average)
"""plt.scatter(tensor_average[:,0], tensor_average[:,1], c=tensor_average[:,2], cmap='Blues',vmin=0, vmax=max(tensor_average[:,2]))
plt.colorbar()
plt.show()"""


"""print("Max R_mag:", max(gradient_values[:,2]))
print("Max G_mag:", max(gradient_values[:,3]))
print("Max B_mag:", max(gradient_values[:,4]))"""
#Plottet die Änderung für jeden Pixel im Bild für alle drei RGB-Werte getrennt
"""plt.title("R")
plt.scatter(gradient_values[:,0], gradient_values[:,1], c=gradient_values[:,2], cmap='Reds',vmin=0, vmax=max(gradient_values[:,2]))
plt.colorbar()
plt.show()
plt.title("G")
plt.scatter(gradient_values[:,0], gradient_values[:,1], c=gradient_values[:,3], cmap='Greens',vmin=0, vmax=max(gradient_values[:,3]))
plt.colorbar()
plt.show()"""

"""plt.title("B")
plt.scatter(gradient_values[:,0], gradient_values[:,1], c=gradient_values[:,4], cmap='Blues',vmin=0, vmax=max(gradient_values[:,4]))
plt.colorbar()
plt.show()"""
#Filteret alle Datenpunkte heraus die eine zu wenige Änderung aufweisen bei den B-Werten
"""gradient_filter = []
for i in gradient_values:
    if i[4] >100:
        gradient_filter.append(i.tolist())
print(gradient_filter)
gradient_filter = np.array(gradient_filter)"""

"""plt.title("B_filter")
plt.scatter(gradient_filter[:,0], gradient_filter[:,1], c=gradient_filter[:,4], cmap='Blues',vmin=0, vmax=max(gradient_filter[:,4]))
plt.colorbar()
plt.show()"""
#Das mit den Ellipsen hat nicht funktioniert, weil der Mittelpunkt der Ellipse ja nich im Ursprung ist, sondern irgendwo dazwischen.
#Der Code schaut ob ein Pixel in der gleichen Höhe liegt und löst ein Gleichungsystem für die Formel der Ellipse. Falls diese Ellipse nicht vertikal oder
#nicht rundlich genug ist, dann wird sie herausgefiltert. Zusätzlich wird geschaut ob die Ellipse durch möglichs viele Punkte gegangen ist.
#Am Ende werden dann alle Ellipsen gezeichnet, die aber vom Ursprung ausgehen und nicht vom tatsächlichen Mittelpunkt der Ellipse.
"""def ellipse_solve(p):
    a, b = p
    return (a ** 2 * x1 ** 2 + b ** 2 * y1 ** 2 - a ** 2 * b ** 2, a ** 2 * x2 ** 2 + b ** 2 * y2 ** 2 - a ** 2 * b ** 2)
tolerance = 1
ellipse_dimensions = []
for i in gradient_filter:
    for j in gradient_filter:
        if j[1] == i[1]:
            point_meet = []
            x1 = i[0]
            y1 = i[1]
            x2 = j[0]
            y2 = j[1]
            a,b = fsolve(ellipse_solve, (10, 10))
            ellipse = lambda x: np.sqrt((1-(x**2/b**2))*a**2)
            for k in gradient_filter:
                if k[1] >= ellipse(k[0])-tolerance and k[1] <= ellipse(k[0])+tolerance or k[1] >= -ellipse(k[0])-tolerance and k[1] <= -ellipse(k[0])+tolerance:
                    point_meet.append(k)
            if len(point_meet) > 5:
                ellipse_dimensions.append((a,b))
print(ellipse_dimensions)
x = np.linspace(-width, width, 1000)
y = np.linspace(-height, height, 1000)
x, y = np.meshgrid(x,y)
#print(ellipse_dimensions[0][0])
for i in ellipse_dimensions:
    epsilon = np.sqrt(i[0] ** 2 - i[1] ** 2) / i[0]
    print(epsilon)
    if abs(i[0])>abs(i[1]) and epsilon>0.5:
        F = i[0] ** 2 * x ** 2 + i[1] ** 2 * y ** 2 - i[0] ** 2 * i[1] ** 2
        plt.contour(x,y,F,[0])
#plt.title("B_filter")
plt.scatter(gradient_filter[:,0], gradient_filter[:,1], c=gradient_filter[:,4], cmap='Blues',vmin=0, vmax=max(gradient_filter[:,4]))
#plt.colorbar()
plt.show()"""
