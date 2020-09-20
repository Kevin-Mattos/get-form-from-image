# -*- coding: utf-8 -*-

import sys, pygame, time, math
from os import  getcwd, listdir
from os.path import isfile, join
from enum import Enum
import pandas as pd, numpy as np

RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
class Estado(Enum):
        BLOQUEADO = 1
        LIVRE = 2
        CHECADO = 3

PROJECTPATH = getcwd()

class Button:
    def __init__(self, x, y, rect, parent = None):
        self.state = Estado.LIVRE
        self.rect = rect
        self.pos = x,y

        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        
        self.color = 255, 255, 255
    
    def __eq__(self, other):
        return self.pos == other.pos
    def __lt__(self, other):
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f
    def __repr__(self):
      return ("{} - g:{} h: {} f: {}").format(self.pos, self.g, self.h, self.f) #f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"
    
    def getPos(self):
        return self.pos
        
    def changeColor(self, color = (255,255,255)):
        pygame.draw.rect(screen, color, self.rect)
        self.state = Estado.BLOQUEADO
        #pygame.display.flip()
    def Checar(self, color):
        self.state = Estado.CHECADO
        pygame.draw.rect(screen, color, self.rect)


class Board:
    def __init__(self, buttons):        
        self.buttons = buttons

    def printAll(self):
        for line in self.buttons:
            for button in line:
                print(button.rect)
    
    def getButtonByPixel(self, pos):
        print(pos)
        vet = getPosByPixel(pos)
        i = vet[0]
        j = vet [1]       
        if(i < 0 or i > gridSize - 1 or j < 0 or j > gridSize - 1):
            return
        return self.buttons[i][j]

    def getButtonVect(self, pos):
        i = pos[0] 
        j = pos [1] 
        
        if(i < 0 or i > gridSize - 1 or j < 0 or j > gridSize - 1):
            return 
        return self.buttons[i][j]

    def getNeighbours(self, i, j):
        but = [self.getButtonVect((i + 1,j))]
        but.append(self.getButtonVect((i - 1,j)))
        but.append(self.getButtonVect((i, j + 1)))
        but.append(self.getButtonVect((i, j - 1)))

        #but.append(self.getButtonVect((i + 1, j + 1)))
        #but.append(self.getButtonVect((i + 1, j - 1)))
        #but.append(self.getButtonVect((i - 1, j + 1)))
        #but.append(self.getButtonVect((i - 1, j - 1)))
        ret = []
        for button in but:
            if(button is not None and button.state == Estado.LIVRE):
                ret.append(button)
        
        return ret
        
def checkIfQuit(ev = None):
    if(ev is None):
        ev = pygame.event.get()
    for event in ev: 

        #print(event)  
        if(event.type == pygame.QUIT):
            print('(x) clicked')
            closeWindow()

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_q):
                print('q pressed, closing')
                closeWindow()

def closeWindow():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

pygame.init()


block_size = 1
margin = 0
fullSize = block_size + margin
gridSize = 800
width, height = gridSize*(fullSize), gridSize * (fullSize)
size = width + block_size, height + block_size

screen = pygame.display.set_mode(size)
white = 111, 115, 120
screen.fill(white)



color = 0,0,0
buttons = []

def getPosByPixel(pos):
    linha = math.floor((pos[0] - fullSize/2)/fullSize)
    coluna = math.floor((pos[1] - fullSize/2)/fullSize)
    
    return linha,coluna

for x in range(math.floor(width/(fullSize))):
    buttons.append([])
    for y in range(math.floor(height/(fullSize))):
        rect = pygame.Rect(x*(block_size+margin) + math.ceil(fullSize/2) ,y*(block_size+margin) + math.ceil(fullSize/2), block_size, block_size)
        buttons[x].append(Button(x,y,rect))
        pygame.draw.rect(screen, color, rect)




def cleanBoard():
    for line in buttons:
        for cell in line:            
            cell.changeColor(color)

def draw_csv(form):   

    for i in form:
        checkIfQuit()
        changeColor(i)       
        #time.sleep(0.02)
        pygame.display.flip()
    
    
    return form

def changeColor(i, color = RED):
    a = board.getButtonVect(i)
    if(a is not None):
        a.changeColor(color)

def getMaiorMenor(form):
    
    maiorX = max(form[:,0])
    maiorY = max(form[:,1])
    menorX = min(form[:,0])
    menorY = min(form[:,1])
    
    if(menorX <= menorY):
        menor = menorX
    else:
        menor = menorY
        
    if(maiorX >= maiorY):
        maior = maiorX
    else:
        maior = maiorY
    
    return maior/(gridSize - 2), menor
    

def formatForms(forms, maior, menor):
    newForms = []
    for form in forms:
        print("maior x: {}, maior y: {}".format(max(form[:,0]), max(form[:,1])))
        print("menor x: {}, menor y: {}".format(min(form[:,0]), min(form[:,1])))
    # =============================================================================
    #     form[:,0] = (form[:,0]/35).astype(np.int64)
    #     form[:,1] = (form[:,1]/17).astype(np.int64)
    # =============================================================================
        form[:,1] = form[:,1] - menor#min(form[:,1])
        form = np.floor((form/(maior))).astype(np.int64)
        top = [form[0]]        
        print('tamanho form1: {}'.format(len(form)))
        _, index = np.unique(form, axis = 0, return_index=True)
        form =  form[np.sort(index)]
        form = np.concatenate((form , top), axis = 0)
        
        print('tamanho form2: {}'.format(len(form)))
        newForms.append(form)
        print("maior x: {}, maior y: {}".format(max(form[:,0]), max(form[:,1])))
        print("menor x: {}, menor y: {}".format(min(form[:,0]), min(form[:,1])))
        
       
        print('==============================')
    return newForms


def centralizeForms(forms):
    newForms = []
    
    #_,menor = getMaiorMenor(forms[0])  
    menor = min(forms[0][:, 1])#int(min(forms[0][:, 1])/2)
    meio =  min(forms[0][:, 0])#int(min(forms[0][:, 0])/2)
    for form in forms:
        form[:, 1] = form[:, 1] - menor
        form[:, 0] = form[:, 0] - meio
        newForms.append(form)
    return newForms
    

def drawMultiple(files = ['2_csv0.csv', 'Peca2_csv0.csv']):
    
    
    
    forms = getForms(files)
   
    forms = centralizeForms(forms)
    
    
    maior,menor = getMaiorMenor(forms[0])   
    forms = formatForms(forms, maior, menor)
    
    for i in range(len(forms)):#fileName in files:
        form = forms[i]
        array = draw_csv(form)
        if( i < len(forms) - 1):
            goToNext(array, forms, i)
            
   
def goToNext(form, forms, i):
    
    nextForm = forms[i + 1]
    for j in range(form[-1, -1], nextForm[-1, -1], -1):
        changeColor((form[-1,0], j))       
        #time.sleep(1)
        pygame.display.flip()
 
def getForms(files):
    forms = []
    for i in range(len(files)):
        file = PROJECTPATH + r'/Outputs/{}'.format(files[i])
        form = pd.read_csv(file).to_numpy()
        
        forms.append(form)
    return forms
        
    
def getFiles(folder):
    mypath = getcwd() + r'/{}/'.format(folder)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles
        #cleanBoard()

#pygame.display.flip()
ev = pygame.event.get()
board = Board(buttons)

#drawMultiple(['Peca2_csv2.csv', 'Peca2_csv10.csv', 'Peca2_csv26.csv', 'Peca2_csv30.csv'])#)#
#drawMultiple(['Imagesteste2_csv2.csv', 'Imagesteste2_csv4.csv'])
files = getFiles('Outputs')
files.sort(key = lambda x:int(x.partition('_')[0]))

print(files)
drawMultiple(files)

# =============================================================================
# time.sleep(1)
# closeWindow()
# =============================================================================
while(1):           
    # proceed events
    pygame.display.flip()
    ev = pygame.event.get()
    checkIfQuit(ev)
    for event in ev:      
        #print(event)       
        
            
        if(pygame.mouse.get_pressed()[0] == 1):
            print("Mouse clicked!")  
            a = board.getButtonByPixel(event.pos)
            if(a is not None):
                a.changeColor(RED)
           
    

