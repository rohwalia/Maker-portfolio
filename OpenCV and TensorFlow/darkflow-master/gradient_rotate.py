from gradient_optimal import tensor_average
import numpy as np
from PIL import Image, ImageOps
import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
files = glob.glob('saved-data/images-example/*')
#print(files)
tensor = []
tensor_export = []
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
            dct["RGB_%s" %f].append([i,j, pixel_values, os.path.splitext(os.path.basename(os.path.normpath(f)))[0]])
            #print(dct["RGB_%s" %f])
    RGB.append(dct["RGB_%s" %f])
    RGB = RGB[0]
    RGB_export = RGB
    RGB = [RGB[x:x+height] for x in range(0, len(RGB),height)]
    RGB = np.array(RGB)
    tensor.append(RGB.tolist())
    RGB_export = np.array(RGB_export)
    tensor_export.append(RGB_export.tolist())
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
    plt.scatter(gradient_filter[:,0], gradient_filter[:,1], c=gradient_filter[:,2], cmap='Blues',vmin=0, vmax=max(gradient_filter[:,2]))
    plt.colorbar()
    plt.show()

tensor = np.array(tensor)
tensor_export = np.array(tensor_export)
#print(tensor_export)
tensor_gradient = np.array(tensor_gradient)
tensor_filter = np.array(tensor_filter)
#print(tensor_filter)
width = tensor_filter[0, -1, 0] + 1
height = tensor_filter[0, -1, 1] + 1
matrix_result = []
matrix_result_inverse = []
#print(len(tensor_filter))
for place in range(len(tensor_filter)):
    for i in range(int(width)):
        for j in range(int(height)):
            matrix_result.append([i, j, tensor_filter[place][(int(height)*i+j)][2] * tensor_average[(int(height)*i+j)][2]])
            matrix_result_inverse.append([i, j, tensor_filter[place][(int(height)*int(abs(height-i))+j)][2] * tensor_average[(int(height)*i+j)][2]])
matrix_result = [matrix_result[x:x+int(height*width)] for x in range(0, len(matrix_result),int(height*width))]
matrix_result = np.array(matrix_result)
matrix_result_inverse = [matrix_result_inverse[x:x+int(height*width)] for x in range(0, len(matrix_result_inverse),int(height*width))]
matrix_result_inverse = np.array(matrix_result_inverse)
print(matrix_result)
print("ok")
print(matrix_result_inverse)
for place in range(len(matrix_result)):
    """plt.scatter(matrix_result[place][:,0], matrix_result[place][:,1], c=matrix_result[place][:,2], cmap='Blues',vmin=0, vmax=max(matrix_result[place][:,2]))
    plt.colorbar()
    plt.show()
    plt.scatter(matrix_result_inverse[place][:, 0], matrix_result_inverse[place][:, 1], c=matrix_result_inverse[place][:, 2], cmap='Blues',vmin=0, vmax=max(matrix_result_inverse[place][:, 2]))
    plt.colorbar()
    plt.show()"""
    denominator = 0
    numerator = 0
    denominator_inverse = 0
    numerator_inverse = 0
    for element in matrix_result[place]:
        if element[1] < int(height*0.29):
            if element[0] < int(width*0.5):
                numerator = numerator + element[2]
            else:
                denominator = denominator + element[2]
    for element in matrix_result_inverse[place]:
        if element[1] < int(height*0.29):
            if element[0] < int(width*0.5):
                numerator_inverse = numerator_inverse + element[2]
            else:
                denominator_inverse = denominator_inverse + element[2]
    fraction = numerator/denominator
    fraction_inverse = numerator_inverse/denominator_inverse
    print(fraction)
    print(fraction_inverse)
    if fraction_inverse < fraction:
        im = Image.open(files[place])
        im_mirror = ImageOps.mirror(im)
        im_mirror.save('saved-data/images-example/%s.png' % os.path.splitext(os.path.basename(os.path.normpath(files[place])))[0])
    else:
        im = Image.open(files[place])
        im.save('saved-data/images-example/%s.png' % os.path.splitext(os.path.basename(os.path.normpath(files[place])))[0])
f = open("saved-data/tensor.txt", "w")
for picture in tensor_export:
    for element in picture:
        element = element.tolist()
        np.savetxt(f, element, delimiter=" ", fmt="%s")
f.close()
f = open("saved-data/tensor.txt", "r")
tensor_import = np.loadtxt(f, comments="#", delimiter="\n", unpack=True, dtype = object).tolist()
tensor_import = [tensor_import[x:x + int(4)] for x in range(0, len(tensor_import), int(4))]
tensor_import = [tensor_import[x:x + int((width+1)*(height+1))] for x in range(0, len(tensor_import), int((width+1)*(height+1)))]
tensor_import = np.array(tensor_import)
#print(tensor_import)
f.close()



"""print(tensor_export[0])
for place in range(len(tensor_export)):
    with pd.ExcelWriter("saved-data/tensor.xls") as writer:
        for element in place:
            d1 = pd.DataFrame(tensor_export[place][:,1])
        d1.to_excel(writer, sheet_name='Sheet_name_%d' % place)"""
"""""
for i in range(width):
    for j in range(height):
        Average = sum(item[(i*j)-1][2] for item in tensor_filter)/len(files)
        if Average >= 0.5:
            tensor_average.append([i, j , 1])
        else:
            tensor_average.append([i, j, 0])
tensor_average = np.array(tensor_average)"""

