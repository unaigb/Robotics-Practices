#=========================================
#          CÓDIGO REALIZADO POR          
#      UNAI GARCÍA BLANCO
#   JORGE CABALLERO GONZÁLEZ
#=========================================

import cv2
import numpy as np
import os
import random

def calcularVerticeAbajoDer(r):
    return (r[0] + r[2], r[1] + r[3])

def calcularDesplazamientoHorizontal(ai, ad, src):
    distder = src.shape[1] - ad[0]
    distizq = ai[0]
    return distder - distizq

def calcularDesplazamientoVertical(ai, ad, src):
    distabajo = src.shape[0] - ad[1]
    distarriba = ai[1]
    return distarriba - distabajo

def traducirVertical(d):
    rango = 25
    if d < -rango:
        return "Mover hacia arriba"
    elif d > rango:
        return "Mover hacia abajo"
    else:
        return "Correcto"

def traducirHorizontal(d):
    rango = 25
    if d < -rango:
        return "Mover hacia la derecha"
    elif d > rango:
        return "Mover hacia la izquierda"
    else:
        return "Correcto"

def calcularTamano(r, src):
    tam = src.shape[0] / 3
    rango = 20
    if abs(tam - r[2]) < rango:
        return True
    else:
        return False
    
def traducirTamano(r, src):
    tam = src.shape[0] / 3
    rango = 20
    if (tam - r[2]) < -rango:
        return "Reducir"
    elif (tam - r[2]) > rango:
        return "Agrandar"
    elif (tam - r[2]) < rango:
        return "Correcto"

def imprimirResultados(contour, src):
    r = cv2.boundingRect(contour)
    print("+-------DATOS DE LA IMAGEN-------+")
    print("Largo Imagen: ", src.shape[1])
    print("Ancho Imagen: ", src.shape[0])

    print("+----------DATOS DEL QR----------+")
    print("Ancho: ", r[2])
    print("Alto: ", r[3])
    print("Vertice Arriba-Izquierda X: ", r[0], " Vertice Arriba-Izquierda Y: ", r[1])
    ai = (r[0], r[1])
    ad = calcularVerticeAbajoDer(r)
    print("Vertice Abajo-Derecha X: ", ad[0], " Vertice Abajo-Derecha Y: ", ad[1])

    print("Desplazamiento vertical: ", calcularDesplazamientoVertical(ai, ad, src), " (", traducirVertical(calcularDesplazamientoVertical(ai, ad, src)), ")")
    print("Desplazamiento horizontal: ", calcularDesplazamientoHorizontal(ai, ad, src), " (", traducirHorizontal(calcularDesplazamientoHorizontal(ai, ad, src)), ")")

    print("Tamaño adecuado: ", calcularTamano(r, src))

    print("+-------------ROBOT-------------+")
    print("Ordenes: Tamanho -->", traducirTamano(r, src), "| Vertical -->", traducirVertical(calcularDesplazamientoVertical(ai, ad, src)), "| Horizontal -->", traducirHorizontal(calcularDesplazamientoHorizontal(ai, ad, src)), "\n")

    return ai, ad, r

def cargar_imagenes():
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_carpeta = os.path.join(ruta_actual, 'images')
    archivos = os.listdir(ruta_carpeta)
    imagenes = [cv2.imread(os.path.join(ruta_carpeta, archivo)) for archivo in archivos if archivo.endswith('.png')]
    
    return imagenes

def main():
    imagenes = cargar_imagenes()
    indice_imagen = random.randint(0, len(imagenes) - 1)

    cv2.namedWindow('Imagen QR', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagen QR', 600, 700)

    while True:
        src = imagenes[indice_imagen]

        if src is None:
            return -1

        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        bw = cv2.Canny(gray, 0, 50, 5)
        cv2.imshow("After canny", bw)
        contours, _ = cv2.findContours(bw.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        imprimirResultados(contours[0], src)

        # Crea una imagen en blanco para mostrar los controles
        controles = np.zeros((100, src.shape[1], 3), dtype=np.uint8)

        # Define el texto y divídelo en líneas
        texto = "Controles:\nw: Mover arriba | a: Mover izquierda | s: Mover abajo \nd: Mover derecha | e: Agrandar | r: Reducir | q: Salir"
        lineas = texto.split('\n')

        # Dibuja cada línea por separado
        y = 25
        for linea in lineas:
            cv2.putText(controles, linea, (10, y), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)
            y += 30  # Ajusta este valor según el espacio que quieras entre líneas

        # Concatena la imagen original con la imagen de los controles
        src = np.concatenate((src, controles), axis=0)

        cv2.imshow('Imagen QR', src)
        tecla = cv2.waitKey(0)

        #Tecla W
        if tecla == ord('w') and indice_imagen == 0:
            indice_imagen = 1
        elif tecla == ord('w') and indice_imagen == 2:
            indice_imagen = 0
        elif tecla == ord('w') and indice_imagen == 8:
            indice_imagen = 3
        elif tecla == ord('w') and indice_imagen == 3:
            indice_imagen = 5
        elif tecla == ord('w') and indice_imagen == 7:
            indice_imagen = 4
        elif tecla == ord('w') and indice_imagen == 4:
            indice_imagen = 6
        elif tecla == ord('w') and indice_imagen == 11:
            indice_imagen = 9
        elif tecla == ord('w') and indice_imagen == 9:
            indice_imagen = 10
        elif tecla == ord('w') and indice_imagen == 17:
            indice_imagen = 12
        elif tecla == ord('w') and indice_imagen == 12:
            indice_imagen = 14
        elif tecla == ord('w') and indice_imagen == 16:
            indice_imagen = 13
        elif tecla == ord('w') and indice_imagen == 13:
            indice_imagen = 15

        #Tecla S
        elif tecla == ord('s') and indice_imagen == 1:
            indice_imagen = 0
        elif tecla == ord('s') and indice_imagen == 0:
            indice_imagen = 2
        elif tecla == ord('s') and indice_imagen == 5:
            indice_imagen = 3
        elif tecla == ord('s') and indice_imagen == 3:
            indice_imagen = 8
        elif tecla == ord('s') and indice_imagen == 6:
            indice_imagen = 4
        elif tecla == ord('s') and indice_imagen == 4:
            indice_imagen = 7
        elif tecla == ord('s') and indice_imagen == 10:
            indice_imagen = 9
        elif tecla == ord('s') and indice_imagen == 9:
            indice_imagen = 11
        elif tecla == ord('s') and indice_imagen == 14:
            indice_imagen = 12
        elif tecla == ord('s') and indice_imagen == 12:
            indice_imagen = 17
        elif tecla == ord('s') and indice_imagen == 15:
            indice_imagen = 13
        elif tecla == ord('s') and indice_imagen == 13:
            indice_imagen = 16

        #Tecla A
        elif tecla == ord('a') and indice_imagen == 3:
            indice_imagen = 0
        elif tecla == ord('a') and indice_imagen == 0:
            indice_imagen = 4
        elif tecla == ord('a') and indice_imagen == 8:
            indice_imagen = 2
        elif tecla == ord('a') and indice_imagen == 2:
            indice_imagen = 7
        elif tecla == ord('a') and indice_imagen == 5:
            indice_imagen = 1
        elif tecla == ord('a') and indice_imagen == 1:
            indice_imagen = 6
        elif tecla == ord('a') and indice_imagen == 12:
            indice_imagen = 9
        elif tecla == ord('a') and indice_imagen == 9:
            indice_imagen = 13
        elif tecla == ord('a') and indice_imagen == 17:
            indice_imagen = 11
        elif tecla == ord('a') and indice_imagen == 11:
            indice_imagen = 16
        elif tecla == ord('a') and indice_imagen == 14:
            indice_imagen = 10
        elif tecla == ord('a') and indice_imagen == 10:
            indice_imagen = 15
        elif tecla == ord('a') and indice_imagen == 19:
            indice_imagen = 18
        elif tecla == ord('a') and indice_imagen == 18:
            indice_imagen = 20

        #Tecla D
        elif tecla == ord('d') and indice_imagen == 4:
            indice_imagen = 0
        elif tecla == ord('d') and indice_imagen == 0:
            indice_imagen = 3
        elif tecla == ord('d') and indice_imagen == 7:
            indice_imagen = 2
        elif tecla == ord('d') and indice_imagen == 2:
            indice_imagen = 8
        elif tecla == ord('d') and indice_imagen == 6:
            indice_imagen = 1
        elif tecla == ord('d') and indice_imagen == 1:
            indice_imagen = 5
        elif tecla == ord('d') and indice_imagen == 13:
            indice_imagen = 9
        elif tecla == ord('d') and indice_imagen == 9:
            indice_imagen = 12
        elif tecla == ord('d') and indice_imagen == 16:
            indice_imagen = 11
        elif tecla == ord('d') and indice_imagen == 11:
            indice_imagen = 17
        elif tecla == ord('d') and indice_imagen == 15:
            indice_imagen = 10
        elif tecla == ord('d') and indice_imagen == 10:
            indice_imagen = 14
        elif tecla == ord('d') and indice_imagen == 20:
            indice_imagen = 18
        elif tecla == ord('d') and indice_imagen == 18:
            indice_imagen = 19

        #Tecla E
        elif tecla == ord('e') and indice_imagen == 17:
            indice_imagen = 8
        elif tecla == ord('e') and indice_imagen == 11:
            indice_imagen = 2
        elif tecla == ord('e') and indice_imagen == 16:
            indice_imagen = 7
        elif tecla == ord('e') and indice_imagen == 12:
            indice_imagen = 3
        elif tecla == ord('e') and indice_imagen == 9:
            indice_imagen = 0
        elif tecla == ord('e') and indice_imagen == 13:
            indice_imagen = 4
        elif tecla == ord('e') and indice_imagen == 14:
            indice_imagen = 5
        elif tecla == ord('e') and indice_imagen == 10:
            indice_imagen = 1
        elif tecla == ord('e') and indice_imagen == 15:
            indice_imagen = 6
        elif tecla == ord('e') and indice_imagen == 3:
            indice_imagen = 19
        elif tecla == ord('e') and indice_imagen == 0:
            indice_imagen = 18
        elif tecla == ord('e') and indice_imagen == 4:
            indice_imagen = 20

        #Tecla R
        elif tecla == ord('r') and indice_imagen == 8:
            indice_imagen = 17
        elif tecla == ord('r') and indice_imagen == 2:
            indice_imagen = 11
        elif tecla == ord('r') and indice_imagen == 7:
            indice_imagen = 16
        elif tecla == ord('r') and indice_imagen == 3:
            indice_imagen = 12
        elif tecla == ord('r') and indice_imagen == 0:
            indice_imagen = 9
        elif tecla == ord('r') and indice_imagen == 4:
            indice_imagen = 13
        elif tecla == ord('r') and indice_imagen == 5:
            indice_imagen = 14
        elif tecla == ord('r') and indice_imagen == 1:
            indice_imagen = 10
        elif tecla == ord('r') and indice_imagen == 6:
            indice_imagen = 15
        elif tecla == ord('r') and indice_imagen == 19:
            indice_imagen = 3
        elif tecla == ord('r') and indice_imagen == 18:
            indice_imagen = 0
        elif tecla == ord('r') and indice_imagen == 20:
            indice_imagen = 4

        #Tecla Q
        elif tecla == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()