import cv2 as cv, os
from os import  getcwd
import utils
from PIL import Image
PROJECTPATH = getcwd()


class Contour:
    def __init__(self, fileName):
        self.fileName = utils.removeFileFormat(fileName)
    

    def start(self):
        print('Pegando contorno da: ' + self.fileName)   
        path = PROJECTPATH + r'/Images/{}.jpg'.format(self.fileName)
        contours, hierarchy = self.getContour(path)
        if(len(contours) > 3):
            print('Tem Varios na Imagem')
        else:
            print('\n\nhierarquia: \n{}\n\n'.format(hierarchy))
            self.saveContours(contours, self.fileName)
            print('MAIOR Y = ', self.reorderContour(contours[1]))
            #self.saveList(contours[1], self.fileName)

        #print(contours[1])
        
        #imagem = Image.open(path)
        #utils.plotPixels(imagem, contours[1])

    def reorderContour(self, contour):
        newList = []
        contourSize = len(contour)
        print('TAMANHO DO CONTORNO: ', contourSize)
        biggestY = 0
        index = 0
        for i in range(contourSize):
            newList.append(contour[i][0])
            if(contour[i][0,1] > biggestY):                
                biggestY = contour[i][0,1] 
                index = i

            

        path = PROJECTPATH + r'/Images/{}.jpg'.format(self.fileName)
        im = Image.open(path)
        newList = newList[index:] + newList[:index]
        
        self.saveList2(newList, self.fileName)
        utils.plotPixels(im, newList)
        return contour[index][0,1]


    def getContour(self,path):        
        im = cv.imread(path)
        imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 127, 255, 0)
        return cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


    def saveContours(self, contours, fileName):
        path = PROJECTPATH + r'/Contours/{}'.format(fileName)
        for c in range (0, len(contours)):

            Originalpath = PROJECTPATH + r'/Images/{}.jpg'.format(self.fileName)
            im = cv.imread(Originalpath)
            cv.drawContours(im, contours, c, (0,255,0), 3)
            cv.imwrite(path + '{}.jpg'.format(c), im)


    def saveList2(self, lista, fileName):
        f = open(PROJECTPATH + r'/Outputs/{}.txt'.format(self.fileName), 'w')
        f.write('{\n')
        for item in lista:
            # print(item)
            f.write('[{}, {}], '.format(item[0], item[1]))
        f.write('\n}')
        f.close()
        print('Contorno da ' + self.fileName + ' salvo\n')


    def saveList(self, lista, fileName):
        f = open(PROJECTPATH + r'/Outputs/{}.txt'.format(self.fileName), 'w')
        f.write('{\n')
        for item in lista:
            # print(item)
            f.write('[{}, {}], '.format(item[0,0], item[0,1]))
        f.write('\n}')
        f.close()
        print('Contorno da ' + self.fileName + ' salvo\n')


if(__name__ == '__main__'):
    import contourfinding
    contourfinding.main()