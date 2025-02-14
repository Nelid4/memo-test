# Importo librerías
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

# Imágenes
IMG_FONDO = pygame.image.load("recursos/img/fondo.jpg")
IMG_CANASTA = pygame.image.load("recursos/img/canasta.png")  
IMG_CARTA = pygame.image.load("recursos/img/carta.png")
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

# Cargar imágenes de las cartas, crear pares y mezclarlas
imagenes_cartas = [pygame.image.load(f"recursos/img/carta{i}.png") for i in range(1, 19)]
imagenes_pares = imagenes_cartas * 2
random.shuffle(imagenes_pares)

# Para el tablero, distribuyo las imágenes en una matriz 6x6
tablero_imagenes = [imagenes_pares[i * COLUMNAS_GRILLA:(i + 1) * COLUMNAS_GRILLA] for i in range(FILAS_GRILLA)]

# Inicializo el tablero con las cartas boca abajo
tablero_estado = [[False] * COLUMNAS_GRILLA for _ in range(FILAS_GRILLA)]

# Variables del juego
canasta_inicial = [0, 0]  # fila y columna inicial, esquina superior izquierda
cartas_seleccionadas = []  # guarda las cartas seleccionadas
tiempo_ultimo_descubrimiento = 0
esperando = False
tiempo_total = 190  # Tiempo en segundos
tiempo_inicio = pygame.time.get_ticks()

# Funciones
def dibujar_canasta():
    MARGEN_SUPERIOR = 44
    x = canasta_inicial[1] * (DIMENSION_CARTA + MARGEN) + MARGEN
    y = canasta_inicial[0] * (DIMENSION_CARTA + MARGEN) + MARGEN + MARGEN_SUPERIOR
    IMAGEN_CANASTA = pygame.transform.scale(IMG_CANASTA, (45, 45))
    ventana.blit(IMAGEN_CANASTA, (x, y))

def dibujar_tablero():
    for fila in range(FILAS_GRILLA):
        for columna in range(COLUMNAS_GRILLA):
            eje_x = columna * (DIMENSION_CARTA + MARGEN) + MARGEN
            eje_y = fila * (DIMENSION_CARTA + MARGEN) + MARGEN
            if tablero_estado[fila][columna]:
                ventana.blit(tablero_imagenes[fila][columna], (eje_x, eje_y))
            else:
                ventana.blit(IMG_CARTA, (eje_x, eje_y))

def manejar_seleccion():
    global tiempo_ultimo_descubrimiento, esperando
    if esperando:
        if pygame.time.get_ticks() - tiempo_ultimo_descubrimiento > 1000:  # Espera 1 segundo
            if len(cartas_seleccionadas) == 2:
                (fila1, col1), (fila2, col2) = cartas_seleccionadas
                if tablero_imagenes[fila1][col1] != tablero_imagenes[fila2][col2]:
                    tablero_estado[fila1][col1] = False
                    tablero_estado[fila2][col2] = False
                else:
                    SONIDO_CORRECTO.play()
                cartas_seleccionadas.clear()
                esperando = False

def seleccionar_carta():
    global tiempo_ultimo_descubrimiento, esperando
    fila, columna = canasta_inicial
    if not tablero_estado[fila][columna] and len(cartas_seleccionadas) < 2:
        tablero_estado[fila][columna] = True
        cartas_seleccionadas.append((fila, columna))
        if len(cartas_seleccionadas) == 2:
            esperando = True
            tiempo_ultimo_descubrimiento = pygame.time.get_ticks()

def mostrar_temporizador(tiempo_restante):
    fuente_temporizador = pygame.font.Font(None, 66)
    minutos = tiempo_restante // 60
    segundos = tiempo_restante % 60
    texto = f"Tiempo: {minutos}:{segundos:02d}"
    
    if minutos == 0 and segundos <= 10:
        texto_renderizado = fuente_temporizador.render(texto, True, (255, 0, 0))
    else:
        texto_renderizado = fuente_temporizador.render(texto, True, (255, 255, 255))
    
    posicion_texto = texto_renderizado.get_rect(topright=(ANCHO_VENTANA - 10, 300))
    ventana.blit(texto_renderizado, posicion_texto)

def verificar_ganador():
    for fila in tablero_estado:
        if not all(fila):
            return False
    return True

def mostrar_pantalla_final(mensaje):
    ventana.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    texto = font.render(mensaje, True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))
    ventana.blit(texto, texto_rect)
    
    font_pequeña = pygame.font.Font(None, 36)
    texto_reiniciar = font_pequeña.render("Presiona R para jugar de nuevo o Q para salir", True, (255, 255, 255))
    texto_reiniciar_rect = texto_reiniciar.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))
    ventana.blit(texto_reiniciar, texto_reiniciar_rect)
    pygame.display.flip()

def mostrar_pantalla_inicial():
    ventana.fill((0, 0, 0))
    fuente_titulo = pygame.font.Font(None, 50)
    texto_titulo = fuente_titulo.render("Memo test - Compra semanal", True, (255, 255, 255))
    texto_titulo_rect = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))
    ventana.blit(texto_titulo, texto_titulo_rect)

    font_pequeña = pygame.font.Font(None, 30)
    lineas_texto = [
        "El super está por cerrar y tenés que ayudar al último cliente",
        "a buscar parejas iguales de cartas para hacer su compra.",
        "",
        "Usá las teclas W, A, S, D para mover la canasta y ESPACIO para seleccionar una carta.",
        "¡Tenés 3 minutos antes de que cierre el lugar!",
        "",
        "(-- El juego se iniciará automaticamente--)"
    ]

    x_centro = ANCHO_VENTANA // 2
    y_base = ALTO_VENTANA // 2 + 50
    espaciado = 30

    for i, linea in enumerate(lineas_texto):
        texto_renderizado = font_pequeña.render(linea, True, (255, 255, 255))
        texto_rect = texto_renderizado.get_rect(center=(x_centro, y_base + i * espaciado))
        ventana.blit(texto_renderizado, texto_rect)
    pygame.display.flip()
    pygame.time.delay(10000)

def mostrar_dino(imagen_dino):
    ventana.blit(imagen_dino, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3500)

# Bucle principal
muestra_pantalla_final = True
mostrar_pantalla_inicial_indicador = True
corriendo = True

while corriendo:
    if mostrar_pantalla_inicial_indicador:
        mostrar_pantalla_inicial()
        mostrar_pantalla_inicial_indicador = False

    if muestra_pantalla_final:
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        tiempo_restante = tiempo_total - tiempo_transcurrido
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and canasta_inicial[0] > 0:
                    canasta_inicial[0] -= 1
                elif event.key == pygame.K_s and canasta_inicial[0] < FILAS_GRILLA - 1:
                    canasta_inicial[0] += 1
                elif event.key == pygame.K_a and canasta_inicial[1] > 0:
                    canasta_inicial[1] -= 1
                elif event.key == pygame.K_d and canasta_inicial[1] < COLUMNAS_GRILLA - 1:
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
        
        if verificar_ganador():
            SONIDO_GANASTE.play()
            mostrar_dino(IMG_DINO_FELIZ)  # Muestra el dino feliz antes de la pantalla final
            mostrar_pantalla_final("¡Ganaste!")
            muestra_pantalla_final = False
        elif tiempo_restante <= 0:
            SONIDO_PERDISTE.play()
            mostrar_dino(IMG_DINO_TRISTE)  # Muestra el dino triste antes de la pantalla final
            mostrar_pantalla_final("¡Tiempo agotado! Perdiste.")
            muestra_pantalla_final = False

        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reiniciar el juego
                    mostrar_pantalla_inicial_indicador = True
                    muestra_pantalla_final = True
                    tiempo_inicio = pygame.time.get_ticks()
                    cartas_seleccionadas = []
                    tablero_estado = [[False] * COLUMNAS_GRILLA for _ in range(FILAS_GRILLA)]
                    random.shuffle(imagenes_pares)
                    tablero_imagenes = [imagenes_pares[i * COLUMNAS_GRILLA:(i + 1) * COLUMNAS_GRILLA] for i in range(FILAS_GRILLA)]
                elif event.key == pygame.K_q:
                    corriendo = False

pygame.quit()