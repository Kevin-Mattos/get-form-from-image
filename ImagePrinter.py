from threading import Thread
from os import listdir, getcwd
import os
from os.path import isfile, join
from PIL import Image, ImageStat
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt, numpy as np

class ImagemClass():

                def __init__ (self, image, fileName):                      
                      self.image = image
                      self.file = fileName

                def run(self):
                    pixelsOrd = getOrderedMatrix(self.image)
                    saveList(pixelsOrd, self.file)
                    plotPixels(self.image, pixelsOrd)


def scatterPlot(x,y):
    
    plt.scatter(x, y)    
    plt.grid()
    plt.show()

def normalPlot(x,y):
    print(x)
    #f2 = interp1d(x, y, )
    #plt.plot(f2(x))
    plt.plot(x, y)    
    plt.grid()
    plt.show()

def getImgFromPDF():    
    pages = convert_from_bytes(open(r'C:\Users\PICHAU\Documents\VS code\Fernando\sadas.PDF', 'rb').read())
    #(r'C:\Users\PICHAU\Documents\VS code\Fernando\sadas.PDF',500)
    #for page in pages:
    #        page.save('out.jpg', 'JPEG')


def findFirstPixel(rgb_im):
    width, heith = rgb_im.size
    for i in range(0, width):        
        for j in range(0, heith):
            r, g, b = rgb_im.getpixel((i,j))
            if( (r,g,b) < (100, 100, 100) and (r == g == b) ):
                return i,j

def getNeighbours(x,y, image):
    width, heith = image.size
    neig = ((1,1), (1,0), (1, -1), (0, -1), (0,1), (-1, 1), (-1, 0), (-1, -1))#((-1,0),(0,-1),(1,0), (0,1))#
    listofOneigh = []
    for neighbour in neig:
        if(x + neighbour[0] >= 0 and y + neighbour[1] >= 0):
            if(x + neighbour[0] < width and y + neighbour[1] < heith):             
                listofOneigh.append((x+neighbour[0], y + neighbour[1]))
    return listofOneigh

def getBlackest(vizinhos, imagem, lista):
    count = 0
    menor = (255,255,255)
    certo = vizinhos[0]

    

    for vizinho in vizinhos:        
        if(imagem.getpixel(vizinho) < menor):
            if(not isOnList(vizinho, lista)):            
                menor = imagem.getpixel(vizinho)
                
                certo = vizinho
                print('color: ', imagem.getpixel(certo))
                #se tem 2, verificar se vai qual vai travar nos proximos 3 passos!
            else:      
                count += 1
                #print(vizinho, count)
        
            
    #print("aq",imagem.getpixel(certo), imagem.getpixel(vizinho))
    if(count > 1):
        print("nao tem mais vizinhos")        
        return None
    return certo
def changeColor(img, coord):
    white = (255,255,255)
    img.putpixel( coord, white)


def getBlackest2(vizinhos, imagem, lista):
    vizinhosOrdenados = sorted(vizinhos, key = comparator, reverse= True)
    remover = []
    for i in range(len(vizinhosOrdenados)):
        if(isOnList(vizinhosOrdenados[i], lista)):
            remover.append(vizinhosOrdenados[i])
        else:
            pass#lista.append(vizinhosOrdenados[i])
    
    for viz in remover:
        vizinhosOrdenados.remove(viz)
    return vizinhosOrdenados

def comparator(item):
    return imagem.getpixel(item)

def getImag2(image,x,y,lista):
    vizinhos = getNeighbours(x,y,image)
    certo = getBlackest(vizinhos, image, lista)
    #certo = getBlackest2(vizinhos,image, lista)[0]
    print('certo:', certo)
    if(certo == None):          
        return None, None
    if(not isOnList(certo, lista)): 
        lista.append(certo)
        #print('certo: ',certo)
        return certo
    #print('falhou')
    return None, None
    
def isOnList(vizinho, lista):
    for item in lista:
        if(vizinho == item):
            return True
    return False


def getOrderedMatrix(im): 
    
    rgb_im = im.convert('RGB')
    x,y = findFirstPixel(rgb_im)
    print("PRIMEIROS", x,y)
    pixelsOrdenados = [(x,y)]
    checados = []
    for i in range(4000):#418):
        oldx, oldy = x,y
        x,y = getImag2(rgb_im, x, y, checados)
        if(x == None):
            checados.append((oldx,oldy))
            x,y = oldx, oldy        
        
        pixelsOrdenados.append((x,y))

    return pixelsOrdenados

def plotPixels(im, pixelsOrdenados):
    width, heith = im.size

    x = []
    y = []
    for point in pixelsOrdenados:
        x.append(np.abs(point[0]))
        y.append(np.abs(point[1] - heith))

    x = np.array(x)
    y = np.array(y)
    normalPlot(x,y)

def saveList(lista, name):
    f = open(getcwd() + r'/Outputs/{}.txt'.format(os.path.splitext(name)[0]), 'w')
    f.write('{\n')
    for item in lista:
        f.write('[{}, {}], '.format(item[0], item[1]))
    f.write('\n}')
    f.close()

def main(onlyfiles = None):
    mypath = getcwd() + r'/Images/'
    if(onlyfiles == None):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    else:
        onlyfiles = [onlyfiles]
    
    #mypath = getcwd() + r'/Minimal/'
    for file in onlyfiles:
        teste(file)
        imagem = Image.open(mypath + file)
        a = ImagemClass(imagem, file)
        a.run()

        #pixelsOrd = getOrderedMatrix(imagem)
        #saveList(pixelsOrd, file)
        # plotPixels(imagem, pixelsOrd)

def teste(file):
    path = getcwd() + r'/Images/'
    imagem = Image.open(path + file)
    width, heith = imagem.size
    pixels = imagem.load()
    preto = 80
    
    for i in range(0, width):        
        for j in range(0, heith):
            if(imagem.getpixel((i,j)) > (preto, preto, preto)):
                pixels[i,j] = (255,255,255)
    imagem.save(getcwd() + r'/Minimal/{}'.format(file))




def findHighestY(imagem):
    width, heith = imagem.size
    for i in range(0, width):        
        for j in range(0, heith):
            pass



main()




#https://www.mathworks.com/matlabcentral/answers/123943-how-can-i-find-pixel-coordinates-of-a-perimeter-in-a-binary-image
#PERCORRER A BORDA E VERIFICAR SE É VIZINHO DE PRETO
#TRACE BOUNDARIES 
#https://datacarpentry.org/image-processing/08-edge-detection/

#https://stackoverflow.com/questions/25379752/how-can-i-extract-the-boundary-curve-of-an-image-region-in-scikit-image
#https://groups.google.com/forum/#!topic/scikit-image/rXRS0KT2PdU

#scikit-image.

#https://github.com/scikit-image/scikit-image/issues/1131