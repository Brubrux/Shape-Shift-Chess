import gamelib
import random

def dicc_maker(size):
    """genera un diccionario que adapta cada coordenada del tablero al tamaño de la pantalla"""
    dicc = {} 
    for i in range(1,9):
            dicc[i] = (i/10)*size
    return dicc

def dicc_mov():
    """lee el archivo movimientos.txt y devuelve un diccionario con los movimientos disponibles para cada pieza"""

    dicc = {}

    try: archivo=open('movimientos.txt') 
    except: print('ERROR: No se encuentra el archivo movimientos.txt')

    with open('movimientos.txt', 'r') as file:
        for linea in file:
            partes = linea.rstrip().split(',')
            if not partes[0] in dicc:
                dicc[partes[0]] = [[partes[1], partes[2]],]
            else:
                dicc[partes[0]].append([partes[1], partes[2]])
    return dicc            

def hitbox(size, coor_x, coor_y):

    """Recibe el tamaño del tablero, y las coordenadas (x,y) de un clic. 
    Devuelve el lugar en el tablero al que corresponde este clic
    Pre: size, coor_x, coor_y deben ser en int
    Post: tupla de donde tab_x/tab_y son la posicion en el tablero en int, si las coordenadas estan fuera del tablero, se devuelve (0,0)
    """
    s = size
    if not type(coor_x) == int or not type(coor_y) == int: raise TypeError("Las coordenadas deben ser int")
    if not (1/10)*s <= coor_x <= (9/10)*s or not (1/10)*s <= coor_y <= (9/10)*s:
        return 0, 0
    for i in range(1, 9):
        if (i/10)*s <= coor_x < ((i+1)/10)*s: tab_x = i
        if (i/10)*s <= coor_y < ((i+1)/10)*s: tab_y = i
    
    return int(tab_x), int(tab_y)

def contador(lista):
    """recibe una lista y devuelve la cantidad de caracteres distintos a cero que hay en esa lista"""
    piezas = 0
    for lineas in lista:
        for p in lineas:
            if p != 0:
                piezas += 1
    
    return piezas

def creador_tablero_lista():
    """crea un tablero de ajedrez del estilo lista de listas y agrega una pieza random en posicion random
    post: devuelve una lista de listas y una tupla con las coordenadas de la pieza random"""
    tablero_lista = []
    for i in range(1,9):
        listilla = []
        for j in range(1,9):
            listilla.append(0)
        tablero_lista.append(listilla)
    coord_pieza_prima = random.randint(0,7), random.randint(0,7)
    tablero_lista[coord_pieza_prima[0]][coord_pieza_prima[1]] = random.randint(1,6)    #el numero random corresponde a una pieza
    tipo_de_pieza =  piezas_numeradas[tablero_lista[coord_pieza_prima[0]][coord_pieza_prima[1]]]
    return tablero_lista, coord_pieza_prima, tipo_de_pieza

def moverse(tablero, player, comido):
    """
    logica del movimiento en shape shift chess
    pre: tablero es lista de listas, player es una tupla de int, comido es una tupla de int
    post: tupla de las nuevas coordenadas del tablero
    """
    player_x, player_y = player
    tablero[player_x][player_y] = 0
    player_nuevo_x, player_nuevo_y = comido[0], comido[1]
    return int(player_nuevo_x)-1, int(player_nuevo_y)-1

def movimientos_disponibles(tablero, coordenadas_pieza):
    """
    pre: coordenadas pieza debe ser tupla de int, tablero lista de lista
    post: una lista con todos los movimientos posibles para hacer en el tablero desde esas coordenadas
    """
    assert type(coordenadas_pieza) == tuple
    assert type(coordenadas_pieza[0]) == int
    
    x0, y0 = coordenadas_pieza
    tipo_de_pieza = piezas_numeradas[tablero[x0][y0]] 

    movimientos_pieza = dicc_movi[tipo_de_pieza] #solo con torre
    movimientos_posibles = []

    for p in movimientos_pieza: #movimientos sin continuidad
        sumadores_xy = p[0].split(';')
        dx, dy = int(sumadores_xy[0]), int(sumadores_xy[1])
        
        if p[1] == 'false':
            x1, y1 = int(x0) + dx, int(y0) + dy 
            
            if not 0<= x1 <=7 or not 0<= y1 <=7 : #si la ubicacion esta fuera de rango, descarta el movimiento y busca otro 
                continue
            
            movimientos_posibles.append((x1,y1))



        while p[1] == 'true': #movimientos con continuidad

            movimientos_loop = []
            
            if dx == 0 or dy == 0: #movimientos paralelos
                movimientos_paralelos = []
                if dx != 0:
                    for i in range(1,8):
                        x1 = x0 +(dx*i)
                        y1 = y0               
                        if not 0<= x1 <=7 or not 0<= y1 <=7: #si la ubicacion esta fuera de rango, descarta el movimiento y busca otro 
                            break
                        movimientos_paralelos.append((x1,y1))
                if dy != 0:
                    for i in range(1,7):
                        y1 = y0 +(dy*i)
                        x1 = x0
                        if not 0<= x1 <=7 or not 0<= y1 <=7 : #si la ubicacion esta fuera de rango, descarta el movimiento y busca otro 
                            break
                        movimientos_paralelos.append((x1,y1))
                movimientos_loop.extend(movimientos_paralelos) 
            
            elif dx != 0 and dy != 0: #movimientos diagonales
                movimientos_diagonales = []
                i, j= 0, 0
                while True:
                    x1 = x0 + (i*dx)
                    y1 = y0 + (j*dy)
                    if not 0<= x1 <=7 or not 0<= y1 <=7 : #si la ubicacion esta fuera de rango, descarta el movimiento y busca otro 
                        break
                    movimientos_diagonales.append((x1, y1))
                    i += 1
                    j += 1
                movimientos_loop.extend(movimientos_diagonales)
            movimientos_posibles.extend(movimientos_loop)    
            break
    
    return movimientos_posibles

def comestibles(tablero, player):
    """
    recibe un tablero y la posicion del jugador, devuelve todos los casilleros donde el jugador puede comer una pieza
    """
    casillas_disponibles = movimientos_disponibles(tablero, player)
    lista_comestibles = []
    for coord in casillas_disponibles:
        if tablero[coord[0]][coord[1]] != 0:
            lista_comestibles.append(coord)
    return lista_comestibles

def randomizador(tablero, anterior):
    """inserta una pieza random que es comible por la anterior
    pre: lista es el tablero(lista de listas), anterior es la posicion de la ultima pieza en el tablero(tupla(x,y))
    post: tablero actualizado (list), tupla de la nueva ultima pieza"""
    
    x0, y0 = anterior[0], anterior[1]
    tipo_pieza_anterior = tablero[x0][y0]
    movimientos_posibles = movimientos_disponibles(tablero,anterior)
    casilleros_disponibles = []
    
    for p in movimientos_posibles:
        if tablero[p[0]][p[1]] == 0:
            casilleros_disponibles.append(p)
    #print((x0, y0),casilleros_disponibles, piezas_numeradas[tipo_pieza_anterior])    


     
    x1, y1 = random.choice(casilleros_disponibles)
    tablero[x1][y1] = random.randint(1, 6)
    coord_pieza_nueva = x1, y1   

    return tablero, coord_pieza_nueva, tipo_pieza_anterior

def color(n):
    """recibe un numero (int) y: si es par devuelve 'black', si es impar devuelve 'white'
    """
    if n%2!=0: return 'grey'
    return 'black'

def tablero_imagen(size):
    """recibe el ancho de la ventana e imprime un tablero de ajedrez acorde"""
    s = size

    for i in range(1,9):
        for j in range(1,9):
            gamelib.draw_rectangle( (j/10)*s , (i/10)*s , ((j+1)/10)*s , ((i+1)/10)*s, fill = color(j-i))
  
    for i in range(1,10):
        for j in range(1, 10):
            gamelib.draw_line((j/10)*s, 0.1*s, (j/10)*s, 0.9*s, fill = 'brown', width = '3')
        for j in range(1,10):
            gamelib.draw_line(0.1*s, (j/10)*s, 0.9*s, (j/10)*s, fill = 'brown', width = '3')

def creador_juego(n):
    tablero, anterior, pieza = creador_tablero_lista()
    player = anterior
    for i in range(n):
        tablero, anterior, pieza = randomizador(tablero, anterior)
    return tablero, player      



dicc_movi = (dicc_mov())
piezas_numeradas = {
    1: 'peon',
    2: 'torre',
    3: 'caballo',
    4: 'alfil',
    5: 'reina',
    6: 'rey',
    }
piezas_color = {
    1: 'peon_blanco.gif',
    1.1: 'peon_rojo.gif',
    2: 'torre_blanco.gif',
    2.1: 'torre_rojo.gif',
    3: 'caballo_blanco.gif',
    3.1: 'caballo_rojo.gif',
    4: 'alfil_blanco.gif',
    4.1: 'alfil_rojo.gif',
    5: 'reina_blanco.gif',
    5.1: 'reina_rojo.gif',
    6: 'rey_blanco.gif',
    6.1: 'rey_rojo.gif',
    }
