import numpy as np
import cv2 as cv, os
from PIL import Image, ImageStat
import matplotlib.pyplot as plt, numpy as np
from pdf2image import convert_from_path
from os import listdir, getcwd
from os.path import isfile, join

def pdfToImg(name):
    path = getcwd() + r'/pdfs/{}'.format(name)
    pages = convert_from_path(path, 500)
    for page in pages:
        page.save(getcwd() + r'/Images/{}.jpg'.format(os.path.splitext(name)[0]), 'JPEG')

from os import getcwd


def plotPixels(im, pixelsOrdenados):
    width, heith = im.size
    x = []
    y = []
    for point in pixelsOrdenados:
        
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

def saveCounteurs(contours, im, fileName):
    path = getcwd() + r'/Contours/{}'.format(fileName)
    for c in range (0, len(contours)):
        cv.drawContours(im, contours, c, (0,255,0), 3)
        cv.imwrite(path + '{}.jpg'.format(c), im)

def saveList(lista, name):
    f = open(getcwd() + r'/Outputs/{}.txt'.format(os.path.splitext(name)[0]), 'w')
    f.write('{\n')
    for item in lista:
        f.write('[{}, {}], '.format(item[0], item[1]))
    f.write('\n}')
    f.close()


def main(onlyfiles = None):
    mypath = getcwd() + r'/pdfs/'
    if(onlyfiles == None):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    else:
        onlyfiles = [onlyfiles]  
    print(onlyfiles)  
    #mypath = getcwd() + r'/Minimal/'
    for file in onlyfiles:
        pdfToImg(file)
        getContour(file)
        

def getContour(fileName):
    print(fileName)
    path = getcwd() + r'/Images/{}.jpg'.format(os.path.splitext(fileName)[0])
    im = cv.imread(path)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    saveCounteurs(contours, im, os.path.splitext(fileName)[0])
    imagem = Image.open(path)
    #plotPixels(imagem, contours[1])


main()
##https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html