import pygame
import tkinter
import copy
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox as MessageBox
from tablero import *
from dominio import *
from variable import *
from pygame.locals import *


GREY=(190, 190, 190)
NEGRO=(100,100, 100)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_INFERIOR=60 #altura del margen inferior entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
FILS=2 # número de filas del crucigrama
COLS=3 # número de columnas del crucigrama

LLENA='*' 
VACIA='-'

VARIABLES = None

#########################################################################
# Detecta si se pulsa el botón de FC
######################################################################### 
def pulsaBotonFC(pos, anchoVentana, altoVentana):
    if pos[0]>=anchoVentana//4-25 and pos[0]<=anchoVentana//4+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de AC3
######################################################################### 
def pulsaBotonAC3(pos, anchoVentana, altoVentana):
    if pos[0]>=3*(anchoVentana//4)-25 and pos[0]<=3*(anchoVentana//4)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si se pulsa el botón de reset
######################################################################### 
def pulsaBotonReset(pos, anchoVentana, altoVentana):
    if pos[0]>=(anchoVentana//2)-25 and pos[0]<=(anchoVentana//2)+25 and pos[1]>=altoVentana-45 and pos[1]<=altoVentana-19:
        return True
    else:
        return False
    
######################################################################### 
# Detecta si el ratón se pulsa en la cuadrícula
######################################################################### 
def inTablero(pos):
    if pos[0]>=MARGEN and pos[0]<=(TAM+MARGEN)*COLS+MARGEN and pos[1]>=MARGEN and pos[1]<=(TAM+MARGEN)*FILS+MARGEN:        
        return True
    else:
        return False
    
######################################################################### 
# Busca posición de palabras de longitud tam en el almacen
######################################################################### 
def busca(almacen, tam):
    enc=False
    pos=-1
    i=0
    while i<len(almacen) and enc==False:
        if almacen[i].tam==tam: 
            pos=i
            enc=True
        i=i+1
    return pos
    
######################################################################### 
# Crea un almacen de palabras
######################################################################### 
def creaAlmacen():
    f= open('d1.txt', 'r', encoding="utf-8")
    lista=f.read()
    f.close()
    listaPal=lista.split()
    almacen=[]
   
    for pal in listaPal:        
        pos=busca(almacen, len(pal)) 
        if pos==-1: #no existen palabras de esa longitud
            dom=Dominio(len(pal))
            dom.addPal(pal.upper())            
            almacen.append(dom)
        elif pal.upper() not in almacen[pos].lista: #añade la palabra si no está duplicada        
            almacen[pos].addPal(pal.upper())           
    
    return almacen

######################################################################### 
# Imprime el contenido del almacen
######################################################################### 
def imprimeAlmacen(almacen):
    for dom in almacen:
        print (dom.tam)
        lista=dom.getLista()
        for pal in lista:
            print (pal, end=" ")
        print()
        
#########################################################################  
# Pinta Tablero
#########################################################################
def pintaTablero(variables, tablero):
    for var in variables:
        if var.is_assigned():
            palabra = var.value
            if var.direction == "horizontal":
                for i, letra in enumerate(palabra):
                    tablero.setCelda(var.row, var.col + i, letra)
            else:  # Dirección vertical
                for i, letra in enumerate(palabra):
                    tablero.setCelda(var.row + i, var.col, letra)


#########################################################################  
# Crear Variable
#########################################################################

def creaVariablesH(tablero):
    variables = []
    almacen = creaAlmacen()
    hueco = None
    i=0
    j=0
    
    while i < FILS:
        j = 0  # Reiniciar j en cada iteración de i
        while j < COLS:
            if tablero.getCelda(i, j) == LLENA:
                if j != 0:
                    if hueco is None: #es el primer * que se encuentra en la linea
                        pos = busca(almacen,j)
                        almacen_copia = copy.deepcopy(almacen[pos]) #Si lo pasamos directamente se produce copia por referencia(1 modificación afecta a todos)
                        var = Variable(i,0,"horizontal",j,almacen_copia)
                        variables.append(var)
                        hueco = (i, j)
                    else: #no es el primer * que se encuentra en la linea
                        tam = j-1 - hueco[1]
                        if tam != 0:
                            pos = busca(almacen, tam)
                            almacen_copia = copy.deepcopy(almacen[pos])
                            var = Variable(hueco[0], hueco[1]+1, "horizontal", tam, almacen_copia)
                            variables.append(var)
                        hueco = (i,j)
                else:#* en la primera casilla
                    hueco = (i,j)
                    
            else:
                if j == COLS - 1: 
                    if hueco is None: #no hay * en toda la linea
                        tam = COLS
                        pos = busca(almacen, tam)
                        almacen_copia = copy.deepcopy(almacen[pos])
                        var = Variable(i, 0, "horizontal", tam, almacen_copia)
                        variables.append(var)
                    else:#llegamos a la ultima casilla y hay algun * en la linea
                        tam = COLS - (hueco[1]+1)
                        if tam!=0:
                            pos = busca(almacen, tam)
                            almacen_copia = copy.deepcopy(almacen[pos])
                            var = Variable(hueco[0], hueco[1]+1, "horizontal", tam, almacen_copia)
                            variables.append(var)
                        hueco = None
                        
            j += 1
            
        i += 1
        hueco = None

    return variables


def creaVariablesV(tablero,variablesH): #añadir que ignore verticales de lon. 1 si tambien es horiz. de lon. 1
    variables = []
    almacen = creaAlmacen()
    hueco = None
    i = 0
    j = 0

    while j < COLS:  # Iterar sobre las columnas
        i = 0  # Reiniciar i en cada iteración de j
        while i < FILS:
            if tablero.getCelda(i, j) == LLENA:
                if i != 0:
                    if hueco is None:  # es el primer * que se encuentra en la columna
                        pos = busca(almacen, i)
                        almacen_copia = copy.deepcopy(almacen[pos])
                        var = Variable(0, j, "vertical", i, almacen_copia)
                        variables.append(var)
                        hueco = (i, j)
                            
                    else:  # no es el primer * que se encuentra en la columna
                        tam = i - 1 - hueco[0]
                        if tam !=0:
                            pos = busca(almacen,tam)
                            almacen_copia = copy.deepcopy(almacen[pos])
                            var = Variable(hueco[0] + 1, hueco[1], "vertical", tam, almacen_copia)
                            variables.append(var)
                        hueco = (i, j)
                else:#* en la primera columna
                    hueco = (i, j)
            else:
                if i == FILS - 1:  
                    if hueco is None:# no hay * en toda la columna
                        tam = FILS
                        pos = busca(almacen,tam)
                        almacen_copia = copy.deepcopy(almacen[pos])
                        var = Variable(0, j, "vertical", tam, almacen_copia)
                        variables.append(var)
                    else:#llegamos a la ultima casilla y hay algun * en la columna
                        tam = FILS - (hueco[0] + 1)
                        if tam!=0:
                            pos =  busca(almacen,tam)
                            almacen_copia = copy.deepcopy(almacen[pos])
                            var = Variable(hueco[0] + 1, hueco[1], "vertical", tam, almacen_copia)
                            variables.append(var)
                        hueco = None
            i += 1
        j += 1
        hueco = None
        
    return variables

def restringirDominosConLetra(variables,tablero):
    i=0
    j=0
    while i<FILS:
        while j<COLS: 
            letra = tablero.getCelda(i,j)
            if letra != "*" and letra != "-":
                varH,varV = obtenerVarsDesdeCoords(i,j,variables)
                if varH != None:
                    n=j-varH.col
                    eliminarPalabrasSinLetraEnPos(varH,n,letra)
                if varV != None:
                    n=i-varV.row
                    eliminarPalabrasSinLetraEnPos(varV,n,letra)
            j+=1
        j=0
        i+=1
        
def eliminarPalabrasSinLetraEnPos(var,n,letra):
    for pal in var.domain.getLista():
        if pal[n] != letra:
            var.domain.removePal(pal)
            print(f"Eliminada {pal}")
    
        
def obtenerVarsDesdeCoords(i,j,variables):
    dosvar = [None,None]
    for var in variables:
        if var.direction == "horizontal":
            if var.row <= i and var.length + var.row >= i:
                dosvar[0] = var
        else:
            if var.col <= j and var.length + var.col >= j:
                dosvar[1] = var
    return dosvar

def extraerVariables(tablero):
    global VARIABLES
    if VARIABLES == None:
        variablesH = creaVariablesH(tablero)

        variablesV = creaVariablesV(tablero,variablesH)
        
        #Borrar las variables de len = 1 (menos las que son len 1 tanto horizontal como verticalmente)
        noBorrar = []
        for varH in variablesH:
            for varV in variablesV:
                if (varH.length == 1 and varV.length == 1 and varH.row == varV.row and varH.col == varV.col):
                    noBorrar.append(varH)
                   
                    
        for varH in variablesH[:]:
            if varH.length == 1 and (varH not in noBorrar):
                variablesH.remove(varH)
                
        for varV in variablesV[:]:
            if varV.length == 1:
                variablesV.remove(varV)
                
                  
        variables = variablesH + variablesV
        restringirDominosConLetra(variables,tablero) #quitará las palabras que no coincidan con letras puestas en el tablero
        VARIABLES = copy.deepcopy(variables)
    else:
        variables = copy.deepcopy(VARIABLES)
    return variables
   
#########################################################################  
#AC3
#########################################################################

def preAC3(tablero):
    variables = extraerVariables(tablero)
    print("Variables previas:")
    for var in variables:
        print(var)
        
    if not AC3(variables):
        print ("NO SE HA ENCONTRADO SOLUCION PARA AC3")
    else:
        print ("AC3 APLICADO A LOS DOMINOS")
        for var in variables:
            print(var)
            
        print("LLAMANDO A FC CON LOS DOMINOS RECORTADOS")
        ra
        if not FC(0,variables,tablero):
            print ("NO SE HA ENCONTRADO SOLUCION")
        else:
            print ("SE HA ENCONTRADO SOLUCION")
        
def AC3(variables):
    dominiosPodados = [] #almacenara los índices de las variables que han sido podadas
    i=0
    while i<len(copy.deepcopy(variables)):
        for pal in list(variables[i].domain.getLista()):
            variables[i].assign(pal)
            if not forward(variables[i],variables,dominiosPodados): #verifica si asignar el valor de la variable actual resulta en algun dominio vacio en otras variables no asignadas.
                restaura(variables,variables[i],dominiosPodados)#restauramos todos los dominios
                dominiosPodados = []
                variables[i].domain.removePal(pal)#podamos la palabra que ha causado incosistencia 
            else:
                restaura(variables,variables[i],dominiosPodados)
                dominiosPodados = []
            
            variables[i].unassign()
            
            if variables[i].domain.getLista() == [] : #El dominio de la variable ha sido completamente vaciado por AC3
                return False
        i+=1
    return True


#########################################################################  
# FC
#########################################################################

def preforwardChecking(tablero):
    variables = extraerVariables(tablero)
    for var in variables:
        print(var)
        
    if not FC(0,variables,tablero):
        print ("NO SE HA ENCONTRADO SOLUCION")
    else:
        print ("SE HA ENCONTRADO SOLUCION")
        

    
def FC(i, variables,tablero):
    if i == len(variables):
        # Todas las variables están asignadas, hemos encontrado una solución
        pintaTablero(variables, tablero)
        for var in variables:
            print(var)
        return True
    
    variable = variables[i]
    dominiosPodados = [] #almacenara los índices de las variables que han sido podadas
    for value in variable.domain.getLista():#Probamos las palabras disponibles para la variable
        variable.assign(value)
        #variable.domain.podado.append([value])
        #variable.domain.removePal(value)
        print(value)
        print("Podadas")
        if forward(variable, variables,dominiosPodados):
            #print(f"##ASIGNADA = {variable.value} en {variable.row},{variable.col} | {variable.direction}")
            if FC(i + 1, variables,tablero):
                return True
        
        print(f"##DESASIGNADA = {variable.value}")
        print (variable)
        
        variable.unassign()
        restaura(variables,variable,dominiosPodados)
        dominiosPodados = []
        print("Dominios despues de restaurar")
        for var in variables:
            print(var)
        
    return False


def forward(variable, variables,dominiosPodados):#verifica si asignar el valor de la variable actual resulta en algun dominio vacio en otras variables
    accPodados = []
    valor = variable.value
    for j in range(0, len(variables)):#itera sobre todas las variables
        #print(f"{variables[j].row},{variables[j].col},{variables[j].direction}")
        if variables[j]!= variable:
            if not variables[j].is_assigned():
                for b in list(variables[j].domain.getLista()):#itera sobre los elementos en el dominio actual de variables[j]
                        if b == valor:
                            if variables[j].domain.contienePalabra(valor):#podamos el valor que estamos probando
                                dominiosPodados.append(j)
                                accPodados.append(valor)
                                variables[j].domain.removePal(valor)
                                #print(f"PODADA POR ASIG. {variables[j]}")
                                #print(variables[j].domain.getLista())
                                if len(variables[j].domain.getLista()) == 0:
                                    variables[j].domain.podado.append(accPodados)
                                    return False #el dominio de variables[j] se vuelve vacío (ningún valor válido es posible)
                        else:
                            if not factibleNoAsig(variable,b,variables[j]):# verificar si asignar b violaría alguna restricción específica del problema
                                dominiosPodados.append(j)
                                accPodados.append(b)
                                variables[j].domain.removePal(b)
                                #print(f"PODADOS{variables[j]}")
                            if len(variables[j].domain.getLista()) == 0:
                                variables[j].domain.podado.append(accPodados)
                                return False #el dominio de variables[j] se vuelve vacío (ningún valor válido es posible)

                if not accPodados == []:
                    variables[j].domain.podado.append(accPodados)
                    accPodados = []
            else:
                if not factible(variable,variables[j]):
                    variables[j].domain.podado.append(accPodados)
                    return False

    return True


    
def factibleNoAsig(v1,b,v2):# Devuelve True si es una asignación válida y False si no lo es.
    v2.assign(b)
    if v1.direction != v2.direction:#si tinen la misma orientación no se cruzan
        if not interseccion_var(v1,v2):
            v2.unassign()
            return False
    v2.unassign()
    return True

def factible(v1,v2):# Devuelve True si es una asignación válida y False si no lo es.(siendo v2 una variable ya asignada)
    if v1.direction != v2.direction:#si tinen la misma orientación no se cruzan
        if not interseccion_var(v1,v2):
            return False
    return True




def restaura(variables,variable,dominiosPodados):
    for j in dominiosPodados:
        temp=None
        if variables[j].domain.podado != []:
            #if not variables[j] == variable:
                removed_values = variables[j].domain.podado.pop() 
                
                for value in removed_values:
                    if value!=variable.value:
                        variables[j].domain.addPal(value)
                    else:
                        temp = value
                if temp!= None:
                    variables[j].domain.addPal(temp)



   
def interseccion_var(v1, v2): #Devuelve false si las palabras interseccionan y las letras no coinciden en esta. True en el resto de casos
    # Extraer información de las variables
    if v1.is_assigned() and v2.is_assigned():
        if v1.direction == 'horizontal':
            
            palabra_horizontal = v1.value
            fila1 = v1.row
            columna1 = v1.col
            longitud1 = v1.length
            
            palabra_vertical = v2.value
            fila2 = v2.row
            columna2 = v2.col
            longitud2 = v2.length
        else:
            palabra_horizontal = v2.value
            fila1 = v2.row
            columna1 = v2.col
            longitud1 = v2.length
            
            palabra_vertical = v1.value
            fila2 = v1.row
            columna2 = v1.col
            longitud2 = v1.length
        
        # Verificar si las palabras se cruzan verticalmente
        posicion_cruce = cruzan_con_puntos(fila1, columna1, longitud1, fila2, columna2, longitud2)
        if posicion_cruce != None:
            punto_cruce_palabraH =  posicion_cruce[1] - columna1
            punto_cruce_palabraV =  posicion_cruce[0] - fila2
            # Verificar si las letras en la intersección coinciden
            letra_horizontal = palabra_horizontal[punto_cruce_palabraH]
            letra_vertical = palabra_vertical[punto_cruce_palabraV]
            #print(f"letra_horizontal {letra_horizontal}, letra_vertical{letra_vertical}")

            if letra_horizontal != letra_vertical:
                return False

    return True


def cruzan_con_puntos(fila1, columna1, longitud1, fila2, columna2, longitud2):
    # Calcula las coordenadas de inicio y fin de la primera palabra(HORIZONTAL)
    inicio1 = (fila1, columna1) #(2,0)
    fin1 = (fila1, columna1 + longitud1 - 1)#(2,5)

    # Calcula las coordenadas de inicio y fin de la segunda palabra (VERTICAL)
    inicio2 = (fila2, columna2)#(1, 5)
    fin2 = (fila2 + longitud2 - 1, columna2) #(2,5)
    
    # Verifica si las palabras se cruzan
    if (inicio2[0] <= fila1 <= fin2[0] and inicio1[1] <= columna2 <= fin1[1]):
        # Las palabras se cruzan, determina la posición de cruce
        fila_cruce = max(inicio1[0], inicio2[0])
        columna_cruce = max(inicio1[1], inicio2[1])
        return (fila_cruce, columna_cruce)
    else:
        # Las palabras no se cruzan
        return None
        
#########################################################################  
# Principal
#########################################################################
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    pygame.init()
    
    reloj=pygame.time.Clock()
    
    anchoVentana=COLS*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+FILS*(TAM+MARGEN)+MARGEN
    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Crucigrama")
    
    botonFC=pygame.image.load("botonFC.png").convert()
    botonFC=pygame.transform.scale(botonFC,[50, 30])
    
    botonAC3=pygame.image.load("botonAC3.png").convert()
    botonAC3=pygame.transform.scale(botonAC3,[50, 30])
    
    botonReset=pygame.image.load("botonReset.png").convert()
    botonReset=pygame.transform.scale(botonReset,[50,30])
    
    almacen=creaAlmacen()
    game_over=False
    tablero=Tablero(FILS, COLS)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición y calcular coordenadas matriciales                               
                pos=pygame.mouse.get_pos()                
                if pulsaBotonFC(pos, anchoVentana, altoVentana):
                    print("FC")
                    preforwardChecking(tablero)                                 
                elif pulsaBotonAC3(pos, anchoVentana, altoVentana):                    
                     print("AC3")
                     preAC3(tablero)
                elif pulsaBotonReset(pos, anchoVentana, altoVentana):                   
                    tablero.reset()#########################
                elif inTablero(pos):
                    colDestino=pos[0]//(TAM+MARGEN)
                    filDestino=pos[1]//(TAM+MARGEN)                    
                    if event.button==1: #botón izquierdo
                        if tablero.getCelda(filDestino, colDestino)==VACIA:
                            tablero.setCelda(filDestino, colDestino, LLENA)
                        else:
                            tablero.setCelda(filDestino, colDestino, VACIA)
                    elif event.button==3: #botón derecho
                        c=askstring('Entrada', 'Introduce carácter')
                        tablero.setCelda(filDestino, colDestino, c.upper())   
            
        ##código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        pygame.draw.rect(screen, GREY, [0, 0, COLS*(TAM+MARGEN)+MARGEN, altoVentana],0)
        for fil in range(tablero.getAlto()):
            for col in range(tablero.getAncho()):
                if tablero.getCelda(fil, col)==VACIA: 
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif tablero.getCelda(fil, col)==LLENA: 
                    pygame.draw.rect(screen, NEGRO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                else: #dibujar letra                    
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    fuente= pygame.font.Font(None, 70)
                    texto= fuente.render(tablero.getCelda(fil, col), True, NEGRO)            
                    screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])             
        #pintar botones        
        screen.blit(botonFC, [anchoVentana//4-25, altoVentana-45])
        screen.blit(botonAC3, [3*(anchoVentana//4)-25, altoVentana-45])
        screen.blit(botonReset, [anchoVentana//2-25, altoVentana-45])
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()
 
if __name__=="__main__":
    main()
     
#     variables = [...]  # Crea y llena esta lista con tus objetos Variable

    # Llama a la función FC para encontrar una solución al crucigrama
#     if FC(0, variables):
#         print("Se encontró una solución:")
#         for variable in variables:
#             print(f"Variable: {variable.row}, {variable.col}, {variable.direction}, Valor: {variable.value}")
#     else:
#         print("No se encontró una solución.")
 
