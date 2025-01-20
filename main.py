import pygame
import constantes

# inicio pygame
pygame.init()

# configuro ventana
screen = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("Compra semanal-MemoTest")

screen.blit(constantes.IMG_FONDO,(0,0))

def dibujar_tablero():#funcion que dibuja el tablero con cartas volteadas
    for fila in range(constantes.FILAS_GRILLA):
        for columna in range(constantes.COLUMNAS_GRILLA):
            eje_x = columna * (constantes.DIMENSION_CARTA + constantes.MARGEN) + constantes.MARGEN
            eje_y = fila * (constantes.DIMENSION_CARTA + constantes.MARGEN) + constantes.MARGEN
            pygame.draw.rect(screen, (255,233,150), (eje_x ,eje_y, constantes.DIMENSION_CARTA, constantes.DIMENSION_CARTA))#dibuja los cuadrados a partir de las medidas


corriendo = True
#bucle principal
while corriendo:
    # captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# si se cierra la ventana
            corriendo = False
            
    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
