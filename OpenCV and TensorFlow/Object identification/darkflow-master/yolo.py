import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import glob
import os
import shutil
import subprocess
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')
from wand.image import Image
from PIL import Image
#subprocess.call("convert -list format | grep PNG")
def system_call(args, cwd="."):
    print("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass
def fix_image_files(root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for dir in dirs:
            system_call("mogrify *.png", "{}".format(os.path.join(path, dir)))
fix_image_files("saved-data")
options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.45,
    "gpu": 1.0,
    'dataset': 'saved-data/images-original',
    'annotation': 'annotation.txt'
}
tfnet = TFNet(options)
g = open('annotation.txt', "w")
files = glob.glob('saved-data/images-original/*')
print("running")
"""
shutil.rmtree("saved-data/images-yolo")
os.mkdir("saved-data/images-yolo")
shutil.rmtree("saved-data/images-yolo-cropped")
os.mkdir("saved-data/images-yolo-cropped")
shutil.rmtree("saved-data/images-yolo-resized")
os.mkdir("saved-data/images-yolo-resized")
"""
for f in files:
    img = cv2.imread(f, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# use YOLO to predict the image
    result = tfnet.return_predict(img)
    #print(result)
    g.write(f+"\n")
    count = 0
    for j in range(0, len(result)):
        j =j - count
        if result[j]["label"] != "bicycle":
            result.pop(j)
            count = count + 1
    for i in range(0, len(result)):
        if result[i]["label"] == "bicycle" and result[i]["confidence"]>0.45:
            tl = (result[i]['topleft']['x'], result[i]['topleft']['y'])
            br = (result[i]['bottomright']['x'], result[i]['bottomright']['y'])
            label = result[i]['label']
            img = cv2.rectangle(img, tl, br, (0, 255, 0), 7)
            img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
            plt.imshow(img)
            img2 = Image.open(f)
            area = (result[i]['topleft']['x'], result[i]['topleft']['y'], result[i]['bottomright']['x'], result[i]['bottomright']['y'])
            img2 = img2.crop(area)
            newsize = (864, 576)
            img3 = img2.resize(newsize)
        else:
            break
        g.write(str(result[i]))
    print(result)
    if len(result) != 0:
        #plt.savefig('saved-data/images-yolo/'+os.path.split(f)[1])
        #img2.save('saved-data/images-yolo-cropped/' + os.path.split(f)[1])
        img3.save('saved-data/images-yolo-resized/' + os.path.split(f)[1])
    #plt.show()
g.close()
