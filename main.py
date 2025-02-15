# Importo librerias
import pygame
import random

# Inicio pygame y sonido
pygame.init()
pygame.mixer.init()

# Constantes
ANCHO_VENTANA = 900
ALTO_VENTANA = 600
FILAS_GRILLA = 6
COLUMNAS_GRILLA = 6
DIMENSION_CARTA = 87
MARGEN = 12
ANCHO_TOTAL_CARTA = DIMENSION_CARTA + MARGEN
MARGEN_SUPERIOR = 44

# Imagenes
IMG_FONDO = pygame.image.load("recursos/img/fondo2.png")
IMG_CANASTA = pygame.image.load("recursos/img/canasta.png")  
IMG_CARTA_VOLTEADA = pygame.image.load("recursos/img/carta.png")
IMG_DINO_FELIZ = pygame.image.load("recursos/img/dino_feliz.png")
IMG_DINO_TRISTE = pygame.image.load("recursos/img/dino_triste.png")

# Sonidos
SONIDO_GANASTE = pygame.mixer.Sound("recursos/sonido/ganaste.wav")
SONIDO_PERDISTE = pygame.mixer.Sound("recursos/sonido/perdiste.wav")
SONIDO_VOLTEAR = pygame.mixer.Sound("recursos/sonido/voltear-carta.wav")
SONIDO_CORRECTO = pygame.mixer.Sound("recursos/sonido/correcto.mp3")
SONIDO_FONDO = pygame.mixer.Sound("recursos/sonido/fondo.mp3")

# Configuración de la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Compra semanal - MemoTest")
SONIDO_FONDO.play(loops=-1)
SONIDO_FONDO.set_volume(0.4)

# Cargo imágenes de las cartas, creo pares y las mezclo.
imagenes_cartas = []
for i in range(1, 19):
    imagen = pygame.image.load(f"recursos/img/carta{i}.png")
    imagenes_cartas.append(imagen)

imagenes_pares = imagenes_cartas * 2
random.shuffle(imagenes_pares)

# Para el tablero distribui las imágenes en una matriz 6x6
tablero_imagenes = []  
for i in range(FILAS_GRILLA):
    inicio = i * COLUMNAS_GRILLA
    fin = (i + 1) * COLUMNAS_GRILLA
    fila_imagenes = imagenes_pares[inicio:fin]
    tablero_imagenes.append(fila_imagenes)

# Inicializo el tablero con las cartas boca abajo
tablero_estado = []
for i in range(FILAS_GRILLA):
    fila = [False] * COLUMNAS_GRILLA 
    tablero_estado.append(fila)

canasta_inicial = [0, 0]  #fila y columna inicial, esquina superior izquierda
cartas_seleccionadas = [] #guarda las cartas seleccionadas
tiempo_ultimo_descubrimiento = 0 #cuando se descubre la segunda carta, comienza a funcionar
esperando = False #variable de estado
tiempo_total = 190 #tiempo en segundos 190 (3 minutos de juego y 10 segundos de pantalla con explicacion)
tiempo_inicio = pygame.time.get_ticks() #cuenta en milisegundos

# Funciones
def dibujar_canasta():
    fila_canasta = canasta_inicial[0]
    columna_canasta = canasta_inicial[1]

    x = (columna_canasta * ANCHO_TOTAL_CARTA) + MARGEN
    y = (fila_canasta * ANCHO_TOTAL_CARTA) + MARGEN + MARGEN_SUPERIOR

    IMAGEN_CANASTA = pygame.transform.scale(IMG_CANASTA, (45, 45))
    ventana.blit(IMAGEN_CANASTA, (x, y))

def seleccionar_carta():
    global tiempo_ultimo_descubrimiento, esperando
    fila, col = canasta_inicial#desempaquetado
    
    if tablero_estado[fila][col] == False and len(cartas_seleccionadas) < 2:#verifo si la carta esta boca abajo y si no se seleccionaron ya 2 cartas
        tablero_estado[fila][col] = True
        cartas_seleccionadas.append((fila, col))
        
        if len(cartas_seleccionadas) == 2: #si ya se seleccionaron 2 cartas
            esperando = True
            tiempo_ultimo_descubrimiento = pygame.time.get_ticks()

def manejar_seleccion():
    global tiempo_ultimo_descubrimiento, esperando

    if esperando == True:
        if pygame.time.get_ticks() - tiempo_ultimo_descubrimiento > 1000:
            if len(cartas_seleccionadas) == 2:
                (fila1, col1), (fila2, col2) = cartas_seleccionadas #desempaquetado
                
                if tablero_imagenes[fila1][col1] != tablero_imagenes[fila2][col2]:#diferentes
                    tablero_estado[fila1][col1] = False
                    tablero_estado[fila2][col2] = False
                else:#iguales
                    SONIDO_CORRECTO.play()

            cartas_seleccionadas.clear()
            esperando = False

def dibujar_tablero():
    for fila in range(FILAS_GRILLA): #recorro todas las filas
        for columna in range(COLUMNAS_GRILLA): #recorro todas las columnas
            x = (columna * ANCHO_TOTAL_CARTA) + MARGEN
            y = (fila * ANCHO_TOTAL_CARTA) + MARGEN
            
            if tablero_estado[fila][columna] == True:
                dibujar = tablero_imagenes[fila][columna] #si la carta se ve
            else:
                dibujar = IMG_CARTA_VOLTEADA #si la carta esta volteada
            ventana.blit(dibujar, (x, y))

def verificar_ganador():
    for fila in tablero_estado:
        for cartas in fila:
            if not cartas: #si quedan cartas boca abajo
                return False 
    return True #todas las cartas están descubiertas

def mostrar_temporizador(tiempo_restante):
    fuente_texto = pygame.font.Font(None, 66)
    minutos = tiempo_restante // 60
    segundos = tiempo_restante % 60
    texto = f"Tiempo: {minutos}:{segundos}"

    if minutos == 0 and segundos <= 10:
        escribir_texto = fuente_texto.render(texto, True, (255, 0, 0)) #texto rojo
    else:
        escribir_texto = fuente_texto.render(texto, True, (255, 250, 0)) #texto amarillo

    posicion_texto = escribir_texto.get_rect(topright=(ANCHO_VENTANA - 10, 300))
    pygame.draw.rect(ventana, (16, 44, 84), posicion_texto)
    ventana.blit(escribir_texto, posicion_texto)

def mostrar_pantalla_inicial():
    ventana.fill((0, 0, 0))
    fuente_titulo = pygame.font.Font(None, 50)
    texto_titulo = fuente_titulo.render("Memo test - Compra semanal", True, (255, 255, 255))
    texto_titulo_rect = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))
    ventana.blit(texto_titulo, texto_titulo_rect)

    fuente_chica = pygame.font.Font(None, 30)
    lineas_texto = [
        "El super está por cerrar y tenés que ayudar al último cliente",
        "a buscar parejas iguales de cartas para hacer su compra.",
        "",
        "Usá las teclas W, A, S, D para mover la canasta y ESPACIO para seleccionar una carta.",
        "¡Tenés 3 minutos antes de que cierre el lugar!",
        "",
        "(-- El juego se iniciará automaticamente--)"
    ]

    for i in range(len(lineas_texto)):#imprime linea x linea
        linea = lineas_texto[i]
        texto_chico = fuente_chica.render(linea, True, (255, 255, 255))
        texto_rect = texto_chico.get_rect(center=(ANCHO_VENTANA // 2, (ALTO_VENTANA // 2 + 50) + i * 30)) #me aseguro que haya un margen x cada linea
        ventana.blit(texto_chico, texto_rect)

    pygame.display.flip()
    pygame.time.delay(10000)#espera 10 segundos

def mostrar_pantalla_final(mensaje):
    ventana.fill((0, 0, 0))

    fuente_grande = pygame.font.Font(None, 74)  
    texto = fuente_grande.render(mensaje, True, (255, 255, 255))  
    texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))  
    ventana.blit(texto, texto_rect)  
    
    fuente_chica = pygame.font.Font(None, 36)  
    texto_instrucciones = fuente_chica.render("Presiona R para jugar de nuevo o Q para salir", True, (255, 255, 255))  
    texto_instrucciones_rect = texto_instrucciones.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))  
    ventana.blit(texto_instrucciones, texto_instrucciones_rect)  

    pygame.display.flip()  

def mostrar_dino(imagen_dino):
    ventana.blit(imagen_dino, (0,0))
    pygame.display.flip()
    pygame.time.delay(3500)

#   --- Bucle principal ---
pantalla_inicial_indicador = True
muestra_pantalla_final = False
corriendo = True

while corriendo:
    if pantalla_inicial_indicador == True:
        mostrar_pantalla_inicial()
        pantalla_inicial_indicador = False

    if muestra_pantalla_final == False:
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000 #paso el tiempo a segundos
        tiempo_restante = tiempo_total - tiempo_transcurrido
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and canasta_inicial[0] > 0: #si la tecla presionada fue la W y la canasta no se encuenta al borde de la grilla
                    canasta_inicial[0] -= 1
                elif event.key == pygame.K_s and canasta_inicial[0] < 5:
                    canasta_inicial[0] += 1
                elif event.key == pygame.K_a and canasta_inicial[1] > 0:
                    canasta_inicial[1] -= 1
                elif event.key == pygame.K_d and canasta_inicial[1] < 5:
                    canasta_inicial[1] += 1
                elif event.key == pygame.K_SPACE:
                    seleccionar_carta()
                    SONIDO_VOLTEAR.play()
                    SONIDO_VOLTEAR.set_volume(0.7)
        
        manejar_seleccion()
        ventana.blit(IMG_FONDO, (0, 0))
        dibujar_tablero()
        dibujar_canasta()
        mostrar_temporizador(tiempo_restante)
        
        if verificar_ganador() == True: #si todas las cartas fueron volteadas
            SONIDO_GANASTE.play()
            mostrar_dino(IMG_DINO_FELIZ)
            mostrar_pantalla_final("¡Lo lograste!")
            muestra_pantalla_final = True
        elif tiempo_restante == 0: #si se acabo el tiempo y quedan cartas sin voltear
            SONIDO_PERDISTE.play()
            mostrar_dino(IMG_DINO_TRISTE)
            mostrar_pantalla_final("¡Tiempo agotado! Perdiste.")
            muestra_pantalla_final = True
        pygame.display.flip()

    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: #para volver a jugar
                    pantalla_inicial_indicador = True
                    muestra_pantalla_final = False
                    tiempo_inicio = pygame.time.get_ticks()
                    cartas_seleccionadas = []
                    canasta_inicial = [0, 0]

                    tablero_estado = []#vuelvo a creaer un 6x6 de false
                    for i in range(FILAS_GRILLA):
                        fila = [False] * COLUMNAS_GRILLA 
                        tablero_estado.append(fila)
                    
                    random.shuffle(imagenes_pares)

                    tablero_imagenes = []#vuelvo a colocar las imagenes, de nuevo mezcladas  
                    for i in range(FILAS_GRILLA):
                        inicio = i * COLUMNAS_GRILLA
                        fin = (i + 1) * COLUMNAS_GRILLA
                        fila_imagenes = imagenes_pares[inicio:fin]
                        tablero_imagenes.append(fila_imagenes)

                elif event.key == pygame.K_q: #para salir
                    corriendo = False

pygame.quit()