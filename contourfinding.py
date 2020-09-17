from os.path import isfile, join
from os import listdir, getcwd, remove

import cv2 as cv

import utils
from contour import Contour


def deletaImagens():

    folders = ['Images', 'Outputs', 'Contours']

    for folder in folders:
        mypath =  getcwd()  + r'/{}/'.format(folder)
        onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            # print(file)
            remove(file)




def main(onlyfiles = None):

    if(onlyfiles == None):
        mypath = getcwd() + r'/pdfs/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    print(onlyfiles)  
    
    for file in onlyfiles:
        if(utils.getFileType(file) == '.PDF' or utils.getFileType(file) == '.pdf'):
            utils.pdfToImg(file)  
        else:
            utils.saveImgOnRightFolder(file) 

        utils.invertColor(file)   

        a = Contour(file)  
        a.start()



if(__name__ == '__main__'):
    deletaImagens()
    main(['Imagesteste2.jpg'])




#main('teste.jpg')
##https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html