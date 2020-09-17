import matplotlib.pyplot as plt, numpy as np

import os
import shutil

from pdf2image import convert_from_path
from PIL import Image
import PIL.ImageOps  

PROJECTPATH = os.getcwd()

def pdfToImg(fileName):
    path = PROJECTPATH + r'/pdfs/{}'.format(fileName)
    pages = convert_from_path(path, 500)
    for page in pages:
        filePath = PROJECTPATH + r'/Images/{}.jpg'.format(removeFileFormat(fileName)) 
        page.save(filePath, 'JPEG')
        

def saveImgOnRightFolder(fileName):
    src = PROJECTPATH + r'/pdfs/{}'.format(fileName)
    dst = PROJECTPATH + r'/Images/'
    
    shutil.copy(src,dst)


def invertColor(fileName):
    fileName = removeFileFormat(fileName)
    print('Invertendo cor da: ' + fileName)
    fileName = PROJECTPATH + r'/Images/{}.jpg'.format(fileName) 
    
    image = Image.open(fileName)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(fileName)





def removeFileFormat(fileName):
    return os.path.splitext(fileName)[0]

def getFileType(fileName):
    return os.path.splitext(fileName)[1]



def plotPixels(im, pixelsOrdenados):
    _,heith = im.size
    x = []
    y = []
    for point in pixelsOrdenados:
        
        x.append(np.abs(point[0]) - 4000)
        y.append(np.abs(point[1] - heith) - 4000)

    x = np.array(x)
    y = np.array(y)
    normalPlot(x,y)

def normalPlot(x,y):

    #f2 = interp1d(x, y, )
    #plt.plot(f2(x))
    plt.plot(x, y)    
    plt.grid()
    plt.show()

