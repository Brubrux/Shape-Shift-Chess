import gamelib
from funciones_trabajo import *

ancho_ventana = 440
alto_ventana = (11/10)*ancho_ventana
dicc_tab_screen = dicc_maker(ancho_ventana)


def nuevo_nivel(n):
    '''inicializa el estado del juego para el numero de nivel dado
    (añade n+2 piezas random en posiciones random)
    '''
    tablero, player = creador_juego(n)
    
    return tablero, player

def juego_mostrar(tablero, player, nivel, comestibles):
    '''dibuja la interfaz de la aplicación en la ventana'''
    b = ancho_ventana
    h = alto_ventana
    
    gamelib.draw_begin()
    gamelib.draw_image('img/fondo.gif', 0, 0)
    gamelib.draw_text('Shape Shifter Chess', 0.5*b, 0.05*h, size = int(0.045*b))
    tablero_imagen(ancho_ventana)

        
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] != 0:
                assert type(tablero[i][j]) == int 
                if i == player[0] and j == player[1]:
                    gamelib.draw_image('img/'+ piezas_color[tablero[i][j]+0.1], int(dicc_tab_screen[i+1]), int(dicc_tab_screen[j+1]))
                else:
                    gamelib.draw_image('img/'+piezas_color[tablero[i][j]], int(dicc_tab_screen[i+1]), int(dicc_tab_screen[j+1]))
    rectangulos_rojos = comestibles
    for p in rectangulos_rojos:
            x, y = p[0]+1, p[1]+1 
            gamelib.draw_rectangle(dicc_tab_screen[x],dicc_tab_screen[y],dicc_tab_screen[x]+44,dicc_tab_screen[y]+44, fill = '', width = '2', outline = 'yellow')
    
    gamelib.draw_rectangle(10, 410, 430, 464, fill = 'brown', outline = 'black', width = '2')
    gamelib.draw_text(f'Nivel: {nivel-1}', 44, 424)
    gamelib.draw_text('''Reintentar: O ''', 71, 444)
    gamelib.draw_text('Salir: P', 380, 424)
    gamelib.draw_text('Ver 1.0 Brubru Games.sa',360,478, size = '8')
    gamelib.draw_end()

def juego_mostrar_inicio(mensaje):

    b = ancho_ventana
    h = alto_ventana

    gamelib.draw_begin()
    

    gamelib.draw_image('img/fondo.gif', 0, 0)
    gamelib.draw_rectangle(10, 70, 430,120, fill = 'brown')
    gamelib.draw_text('Shape Shifter Chess', 0.5*b, 0.2*h, size = int(0.07*b), fill = 'white')
    gamelib.draw_rectangle(50, 150, 400,250, fill = 'brown')
    gamelib.draw_text(mensaje, 220,200, size = '12')

    gamelib.draw_end()



def main():
    
    gamelib.title("Shape Shifter Chess")
    gamelib.resize(ancho_ventana, alto_ventana)
    
    while gamelib.is_alive():
        try:
            save = open('save.txt', 'r')

            mensaje = 'Se encontro una partida guardada.\nDesea continuar?(y/n)'
            juego_mostrar_inicio(mensaje)
            
            ev = gamelib.wait()

            if not ev:
                save.close()
                break

            elif ev.type == gamelib.EventType.KeyPress and ev.key == 'y':
                for linea in save:
                    datos = linea.rstrip('n').split(',')
                    nivel = int(datos[0])
                    tablero, player = nuevo_nivel(nivel)
                    disponibles=comestibles(tablero, player)
                break
                            
                    
            elif ev.type == gamelib.EventType.KeyPress and ev.key == 'n':
                nivel = 2
                tablero, player = nuevo_nivel(nivel)
                disponibles=comestibles(tablero, player)
                break
                  
                        

                                
                        
                    
        except: 
            mensaje = 'No se encontro partida guardada.\nPresione n para iniciar nuevo juego'
            opciones = '', ''
            juego_mostrar_inicio(mensaje)
            ev = gamelib.wait()
            if not ev:break

            elif ev.type == gamelib.EventType.KeyPress and ev.key == 'n':
                nivel = 2
                tablero, player = nuevo_nivel(nivel)
                disponibles=comestibles(tablero, player)
                break    
            
    
    while gamelib.is_alive():   

        juego_mostrar(tablero, player, nivel, disponibles)

        ev = gamelib.wait()

        if not ev:
            break
        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            print(f'''se ha presionado el botón del mouse: {ev.x} {ev.y}, Posicion{hitbox(ancho_ventana, ev.x, ev.y)}''')
            
            x_clic, y_clic = hitbox(ancho_ventana, ev.x, ev.y)
            if x_clic == 0 or y_clic == 0: continue
                        
            for p in disponibles:
                if x_clic == p[0]+1 and y_clic == p[1]+1:
                    print(player)
                    player = moverse(tablero, player, (x_clic, y_clic))
                    print(player)
                disponibles = comestibles(tablero, player)
            if contador(tablero) == 1:
                print('si')
                nivel += 1
                tablero, player = nuevo_nivel(nivel)
                disponibles = comestibles(tablero, player)
            
        elif ev.type == gamelib.EventType.KeyPress and ev.key == 'o' or ev.key == 'O':
            tablero, player = nuevo_nivel(nivel)
            disponibles = comestibles(tablero, player)
            print(f'se ha presionado la tecla: {ev.key}')
        elif ev.type == gamelib.EventType.KeyPress and ev.key == 'p' or ev.key == 'P':
            tablero_guardado = ''
            for linea in tablero:
                for c in linea:
                    tablero_guardado += str(c)
            with open('save.txt', 'w') as save:
                save.write(f'{nivel},{player},{tablero_guardado}\n')
            return

gamelib.init(main)