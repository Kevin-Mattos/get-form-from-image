import cv2 as cv, os, numpy as np
from os import  getcwd
import utils
from PIL import Image

PROJECTPATH = getcwd()


class Contour:
    def __init__(self, fileName):
        self.fileName = utils.removeFileFormat(fileName)
        self.contours = None
        self.reorderedContours = None
    

    def start(self):
        print('Pegando contorno da: ' + self.fileName)   
        path = PROJECTPATH + r'/Images/{}.jpg'.format(self.fileName)
        contours, hierarchy = self.getContour(path)
        self.contours = contours
        print('\n\nhierarquia: \n{}\n\n'.format(hierarchy))
        #self.saveContours(contours, self.fileName)
# =============================================================================
#         if(False):#len(contours) > 3):
#             print('Tem Varios na Imagem')
#             print('\n\nhierarquia: \n{}\n\n'.format(hierarchy))
#             self.saveContours(contours, self.fileName)
# 
#         else:
#             self.saveContours(contours, self.fileName)
# =============================================================================

            #print('MAIOR Y = ', self.reorderContour(contours[2]))
            #print('\n\nhierarquia: \n{}\n\n'.format(hierarchy))
            #self.saveContours(contours, self.fileName)
            #self.saveList(contours[1], self.fileName)

        #print(contours[1])
        
        #imagem = Image.open(path)
        #utils.plotPixels(imagem, contours[1])



    def filterCountours(self):
        
        selectedCountours = []
        antAr = None
        proxAr = None
        for i in range(0, len(self.contours) - 1):
        #for i in range(0, len(self.contours)):
            if(i>0):
                antAr = cv.contourArea(self.contours[i - 1])
            else:
                antAr = None
                
            proxAr = cv.contourArea(self.contours[i + 1])            
            contour = self.contours[i]
            print('i: {}, areaAnt: {} areaProx: {}'.format(i,antAr, proxAr))
            if(antAr  != None):
                if(antAr >= cv.contourArea(contour) >= proxAr):
                    selectedCountours.append(contour)
                    
            elif(cv.contourArea(contour) > proxAr):
                selectedCountours.append(contour)
                
        #self.contours = selectedCountours
        return selectedCountours[0::2]    
            #print(cv.contourArea(contour))
            
        

    def saveCSVs(self, contours):
        #contours = np.array(contours)
                
        biggestYs = self.getBiggestYs(contours)    
    
        reorderedContours = self.reorderContours(biggestYs, contours)
        self.reorderedContours = reorderedContours
        self.saveMatrix(reorderedContours)
        return biggestYs

    def saveMatrix(self, contours):
        i = 0
        for ordered in contours:
            np.savetxt(PROJECTPATH + r'/Outputs/{}_{}.csv'.format(i, self.fileName), ordered, delimiter=',', fmt='%5.0f')
            i+=1
        
    def reorderContours(self, biggestYs, contours):
        reorderedCount = []
        
        for i  in range(len(biggestYs)):  
            contour = contours[i][:,0]
            reord = np.append(contour[biggestYs[i]:], contour[ :biggestYs[i] + 1], axis = 0)            
            reorderedCount.append(reord)
            
        
        return reorderedCount

    def getBiggestYs(self, contours):
        ys = []
        for contour in contours:
            
            test = contour[:, 0,:]
            maxes = np.argwhere(test[:, 1] == np.amax(test[:, 1]))
            index = int(len(maxes)/2) 
            yMax = maxes[index,0]
            
            ys.append(yMax)
            
        return np.array(ys)

    

    def getContour(self,path):        
        im = cv.imread(path)
        flippedIm = cv.flip(im, 0)
        imgray = cv.cvtColor(flippedIm, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 127, 255, 0)
        return cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)


    def saveContours(self, contours, fileName = None):
        if(fileName == None):
            path = PROJECTPATH + r'/Contours/{}'.format(self.fileName)
        else:
            path = PROJECTPATH + r'/Contours/{}'.format(fileName)
            
        for c in range (0, len(contours)):
            print('salvando contorno {}'.format(c))
            Originalpath = PROJECTPATH + r'/Images/{}.jpg'.format(self.fileName)
            im = cv.imread(Originalpath)
            flippedIm = cv.flip(im, 0)
            cv.drawContours(flippedIm, contours, c, (0,255,0), 3)
            cv.imwrite(path + '_{}.jpg'.format(c), flippedIm)


    def saveList2(self, lista, fileName):

        npAr = np.array(lista)
        np.savetxt(PROJECTPATH + r'/Outputs/{}_csv.csv'.format(self.fileName), npAr, delimiter=',', fmt='%5.0f')

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
    contourfinding.deletaImagens()
    contourfinding.main(['untitled.jpg'])