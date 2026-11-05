#Grupo 2

import sys
import os
import tty
import termios
import serial
import time
import math
from pycreate2 import Create2

def clear_terminal():
    # Limpiar la terminal dependiendo del sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def getch():
    """Función para obtener la entrada de teclado sin necesidad de presionar enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
    

def main():
    # Dirección de conexión del robot
    port = '/dev/ttyUSB0'
   
    # Inicializar el robot
    bot = Create2(port)
    bot.start()
    bot.safe()
    
    # Obtiene los valores de los sensores
    sensors = bot.get_sensors()

    # Los encoders de las ruedas derecha e izquierda
    encoder_derecha1 = sensors.encoder_counts_right
    encoder_izquierda1 = sensors.encoder_counts_left
    
    #Variables de distancia
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0
    
    # Características roomba
    ticks_por_vuelta =  508.8
    diametro_rueda =  72
    sep_ruedas = 235

    # Bucle principal
    print("Control del robot Roomba 600")
    print("Presiona las teclas 'w', 'a', 's', 'd', 'q', 'e' para mover el robot.")
    print("Presiona 'r' para salir.")

    try:
        while True:

            char = getch()
            if char == 'w':
                bot.drive_direct(200, 200)  # Avanzar
            elif char == 'a':
                bot.drive_direct(200, -200)  # Rotar a la izquierda
            elif char == 's':
                bot.drive_direct(-200, -200)  # Retroceder
            elif char == 'd':
                bot.drive_direct(-200, 200)  # Rotar a la derecha
            elif char == 'e':
                bot.drive_direct(66, 200)  # Girar a la derecha
            elif char == 'q':
                bot.drive_direct(200, 66)  # Girar a la izquierda
            elif char == 'r':
                break  # Salir del bucle
            
            # Añade un pequeño retardo para no saturar la salida
            time.sleep(1)
            bot.drive_stop();
            
            # Obtiene los valores de los sensores
            sensors = bot.get_sensors()
    
            # Los encoders de las ruedas derecha e izquierda
            encoder_derecha2 = sensors.encoder_counts_right
            encoder_izquierda2 = sensors.encoder_counts_left
    
            # Calcula la distancia recorrida por cada rueda
            distancia_derecha = 2 * math.pi * (diametro_rueda/2) * ((encoder_derecha2-encoder_derecha1)/ticks_por_vuelta)
            distancia_izquierda = 2 * math.pi * (diametro_rueda/2) * ((encoder_izquierda2-encoder_izquierda1)/ticks_por_vuelta)

            # Calcula la distancia total recorrida
            delta_s = (distancia_derecha + distancia_izquierda) / 2
            delta_theta = (distancia_derecha - distancia_izquierda) / sep_ruedas
            
            # Actualiza el ángulo del robot
            theta += delta_theta
            
            # Calcula el cambio en x e y
            delta_x = delta_s * math.cos(theta)
            delta_y = delta_s * math.sin(theta)

            # Actualiza la posición del robot
            x += delta_x
            y += delta_y


            # Imprime los resultados
            clear_terminal()
            print(f"Posición actual:\n Orientación = {math.degrees(theta):.4f} grados \n x = {x:.4f} mm \n y = {y:.4f} mm")

			# Los encoders de las ruedas derecha e izquierda
            encoder_derecha1 = encoder_derecha2
            encoder_izquierda1 = encoder_izquierda2
		
           
    except KeyboardInterrupt:
           print('shutting down ... bye')

    # Detener el robot y cerrar la conexión
    bot.drive_direct(0, 0)
    bot.close()

if __name__ == "__main__":
    main()

