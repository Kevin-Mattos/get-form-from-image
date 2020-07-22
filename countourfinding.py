import numpy as np
import cv2 as cv, os
from PIL import Image, ImageStat
import matplotlib.pyplot as plt, numpy as np


from os import getcwd


def plotPixels(im, pixelsOrdenados):
    width, heith = im.size
    x = []
    y = []
    for point in pixelsOrdenados:
        print(point[0])
        x.append(np.abs(point[0,0]))
        y.append(np.abs(point[0,1] - heith))

    x = np.array(x)
    y = np.array(y)
    normalPlot(x,y)

def normalPlot(x,y):

    #f2 = interp1d(x, y, )
    #plt.plot(f2(x))
    plt.plot(x, y)    
    plt.grid()
    plt.show()
def saveCounteurs():
    for c in range (0, len(contours)):
        cv.drawContours(im, contours, c, (0,255,0), 3)
        cv.imwrite('teste{}.jpg'.format(c), im)

path = getcwd() + r'/Images/maozinha.PNG'
im = cv.imread(path)
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


saveCounteurs()

imagem = Image.open(path)
plotPixels(imagem, contours[1])


##https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html