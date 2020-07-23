import numpy as np
import cv2 as cv, os
from PIL import Image, ImageStat
import matplotlib.pyplot as plt, numpy as np
from pdf2image import convert_from_path
from os import listdir, getcwd
from os.path import isfile, join
import shutil
from os import getcwd
from PIL import Image
import PIL.ImageOps  

def pdfToImg(fileName):
    path = getcwd() + r'/pdfs/{}'.format(fileName)
    pages = convert_from_path(path, 500)
    for page in pages:
        filePath = getcwd() + r'/Images/{}.jpg'.format(removeFileFormat(fileName)) 
        page.save(filePath, 'JPEG')
        
        
def invertColor(fileName):
    fileName = getcwd() + r'/Images/{}.jpg'.format(removeFileFormat(fileName)) 
    print(fileName)
    image = Image.open(fileName)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(fileName)




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

def saveList(lista, fileName):
    f = open(getcwd() + r'/Outputs/{}.txt'.format(removeFileFormat(fileName)), 'w')
    f.write('{\n')
    for item in lista:
        print(item)
        f.write('[{}, {}], '.format(item[0,0], item[0,1]))
    f.write('\n}')
    f.close()


def main(onlyfiles = None):

    if(onlyfiles == None):
        mypath = getcwd() + r'/pdfs/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    else:
        onlyfiles = [onlyfiles]  
    print(onlyfiles)  
    #mypath = getcwd() + r'/Minimal/'
    for file in onlyfiles:
        if(getFileType(file) == '.PDF'):
            pdfToImg(file)  
        else:
            saveImg(file) 

        invertColor(file)     
        getContour(file)

def saveImg(fileName):
    src = getcwd() + r'/pdfs/{}'.format(fileName)
    dst = getcwd() + r'/Images/'
    
    shutil.copy(src,dst)

def removeFileFormat(fileName):
    return os.path.splitext(fileName)[0]

def getFileType(fileName):
    return os.path.splitext(fileName)[1]

def getContour(fileName):
    print(fileName)
    
    path = getcwd() + r'/Images/{}.jpg'.format(removeFileFormat(fileName))
    im = cv.imread(path)
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    saveCounteurs(contours, im, os.path.splitext(fileName)[0])
    #print(contours[1])
    saveList(contours[1], fileName)
    #imagem = Image.open(path)
    #plotPixels(imagem, contours[1])
main()

#main('teste.jpg')
##https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html