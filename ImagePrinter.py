from PIL import Image, ImageStat
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt, numpy as np

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

def test(width, heith):
    im = Image.open('Capturar2.PNG')
    rgb_im = im.convert('RGB')
    listofPix = []
    for i in range(0, width):        
        for j in range(0, heith):
            r, g, b = rgb_im.getpixel((i,j))
            if( (r,g,b) < (100, 100, 100) and (r == g == b) ):
                #print(r, g, b)
                listofPix.append((np.abs(i - width) / 3,np.abs(j - heith)/3 ))

    return listofPix

def findFirstPixel(image):
    width, heith = image.size
    for i in range(0, width):        
        for j in range(0, heith):
            r, g, b = rgb_im.getpixel((i,j))
            if( (r,g,b) < (100, 100, 100) and (r == g == b) ):
                return i,j

def getNeighbours(x,y, image):
    width, heith = image.size
    neig = ((1,1), (1,0), (1, -1), (0, -1), (0,1), (-1, 1), (-1, 0), (-1, -1))
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
            else:                
                count += 1
                print(vizinho, count)
    #print("aq",imagem.getpixel(certo), imagem.getpixel(vizinho))
    if(count > 1):
        print("nao tem mais vizinhos")
        
        return None
    return certo

def getImag(image, x, y, lista, removeFromNeigh = None):
    vizinhos = getNeighbours(x,y,image)    
    for vizinho in vizinhos:       
        if(image.getpixel(vizinho) < (100, 100, 100) and not isOnList(vizinho, lista)):            
            #print(vizinho, image.getpixel(vizinho))
            lista.append(vizinho)
            print('vizinho: ',vizinho)
            return vizinho
    print('falhou')
    return None, None

def getImag2(image,x,y,lista):
    vizinhos = getNeighbours(x,y,image)
    certo = getBlackest(vizinhos, image, lista)
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

    


im = Image.open('Capturar4.PNG')
rgb_im = im.convert('RGB')
x,y = findFirstPixel(rgb_im)
print("PRIMEIROS", x,y)
pixelsOrdenados = []
checados = []

for i in range(3000):#418):
    oldx, oldy = x,y
    x,y = getImag2(rgb_im, x, y, checados)
    if(x == None):
        checados.append((oldx,oldy))
        x,y = oldx, oldy
        
        
    pixelsOrdenados.append((x,y))

#print(pixelsOrdenados)

width, heith = im.size

#plottedddd = test(width, heith)


x = []
y = []
for point in pixelsOrdenados:#plottedddd:
    x.append(np.abs(point[0] - width))
    y.append(np.abs(point[1] - heith))

x = np.array(x)
y = np.array(y)


#scatterPlot(x,y)
normalPlot(x,y)