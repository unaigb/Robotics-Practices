#=========================================
#          CÓDIGO REALIZADO POR          
#      UNAI GARCÍA BLANCO
#   JORGE CABALLERO GONZÁLEZ
#=========================================

import pygame
import math
import sys

def menu():
    print("\n\n===============================================================")
    print("                BIENVENIDO A LA SIMULACIÓN DE ROBOT                ")
    print("===============================================================\n\n")
    print("1. Usar valores predeterminados")
    print("2. Configurar valores")
    print("3. Salir")
    opcion = input("\nSelecciona una opción: ")
    return opcion

def configurar():
    global wheel_sep
    global lw_radius
    global rw_radius
    global encoder_res

    while True:
        wheel_sep = float(input("Introduce la separación de las ruedas (en metros): "))
        lw_radius = float(input("Introduce el radio de la rueda izquierda (en metros): "))
        rw_radius = float(input("Introduce el radio de la rueda derecha (en metros): "))
        encoder_res = float(input("Introduce la resolución del encoder (en grados): "))

        print(f"\nHas introducido los siguientes valores:")
        print(f"Separación de las ruedas: {wheel_sep} metros")
        print(f"Radio de la rueda izquierda: {lw_radius} metros")
        print(f"Radio de la rueda derecha: {rw_radius} metros")
        print(f"Resolución del encoder: {encoder_res} grados")

        confirmacion = input("\n¿Son correctos estos valores? (S/N): ").upper()
        if confirmacion == 'S':
            juego()
            break
        elif confirmacion == 'N':
            configurar()

def juego():
    # Inicializar Pygame
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1100, 900))
    pygame.display.set_caption("Simulación de Robot")

    # Parámetros del robot
    wheel_separation = wheel_sep
    left_wheel_radius = lw_radius
    right_wheel_radius = rw_radius
    encoder_resolution = encoder_res
        
    # Tamaño del marco en píxeles
    frame_size = 50

    # Estado inicial del robot
    x: float = 0.0  # Ahora el robot inicia en el centro de la pantalla
    y: float = 0.0  # Ahora el robot inicia en el centro de la pantalla
    theta: float = 0.0
    new_x: float = 0.0
    new_y: float = 0.0
    new_theta: float = 0.0
    encoder_left: float
    encoder_right: float
    delta_distance: float
    distance_left: float
    distance_right: float
    delta_theta: float

    # Crear una superficie de texto
    font = pygame.font.Font(None, 24)  # Puedes ajustar el tamaño de la fuente según tus preferencias
    text_surface = font.render("", True, (0, 0, 0))  # Inicialmente, el texto está vacío

    # Lista para almacenar las posiciones anteriores del robot
    robot_path = []

    running = True
    while running:
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:  # Avanzar en línea recta
                encoder_left = encoder_right = 10
            elif keys[pygame.K_k]:  # Retroceder en línea recta
                encoder_left = encoder_right = -10
            elif keys[pygame.K_j]:  # Girar a la izquierda
                encoder_left, encoder_right = -10, 10
            elif keys[pygame.K_l]:  # Girar a la derecha
                encoder_left, encoder_right = 10, -10
            elif keys[pygame.K_u]:  # Avanzar con giro a la izquierda
                encoder_left, encoder_right = 3, 10
            elif keys[pygame.K_o]:  # Avanzar con giro a la derecha
                encoder_left, encoder_right = 10, 3
            else:
                encoder_left = encoder_right = 0


            # Calcular la distancia recorrida por cada rueda
            distance_left = 2 * math.pi * left_wheel_radius * (encoder_left / encoder_resolution)
            distance_right = 2 * math.pi * right_wheel_radius * (encoder_right / encoder_resolution)

            # Calcular el cambio en la orientación y la posición
            delta_theta = (distance_right - distance_left) / wheel_separation
            delta_distance = (distance_right + distance_left) / 2
            new_theta = theta + delta_theta
            new_x = x + delta_distance * math.cos(new_theta)
            new_y = y + delta_distance * math.sin(new_theta)

            # Comprobar si las nuevas coordenadas están dentro de los límites de la pantalla
            if (-screen.get_width()/200 + frame_size/100 <= new_x <= screen.get_width()/200 - frame_size/100
                and -screen.get_height()/200 + frame_size/100 <= new_y <= screen.get_height()/200 - frame_size/100):
                # Si las nuevas coordenadas están dentro de los límites, actualizar el estado del robot
                theta = new_theta
                x = new_x
                y = new_y
            else:
                # Si las nuevas coordenadas están fuera de los límites, no actualizar el estado del robot
                # Esto es equivalente a hacer que el robot se detenga cuando llega a un muro
                pass

            # Agregar la posición actual a la lista del recorrido
            robot_path.append((int((x + screen.get_width()/200) * 100), screen.get_height() - int((y + screen.get_height()/200) * 100)))

        # Dibujar el mapa de coordenadas
        screen.fill((255, 255, 255))

        for i in range(frame_size, screen.get_width() - frame_size, 100):
            pygame.draw.line(screen, (200, 200, 200), (i, frame_size), (i, screen.get_height() - frame_size))
            label = font.render(str((i-screen.get_width()/2)/100), True, (0, 0, 0))
            screen.blit(label, (i, screen.get_height()/2))

        for i in range(frame_size, screen.get_height() - frame_size, 100):
            pygame.draw.line(screen, (200, 200, 200), (frame_size, i), (screen.get_width() - frame_size, i))
            label = font.render(str((i-screen.get_height()/2)/100), True, (0, 0, 0))
            screen.blit(label, (screen.get_width()/2, screen.get_height()-i))

        # Dibujar el eje de coordenadas
        pygame.draw.line(screen, (0, 0, 0), (screen.get_width()/2, frame_size), (screen.get_width()/2, screen.get_height() - frame_size))  # Eje vertical
        pygame.draw.line(screen, (0, 0, 0), (frame_size, screen.get_height()/2), (screen.get_width() - frame_size, screen.get_height()/2))  # Eje horizontal

        # Dibujar el marco
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((frame_size, frame_size), (screen.get_width() - 2*frame_size, screen.get_height() - 2*frame_size)), 2)

        # Actualizar el texto a mostrar
        text1 = f"orientación: {theta:.2f} rad | x: {x:.2f} m | y: {y:.2f} m"

        text_surface1 = font.render(text1, True, (0, 0, 0))

        # Dibujar el robot y su recorrido
        pygame.draw.circle(screen, (0, 0, 0), (int((x + screen.get_width()/200) * 100), screen.get_height() - int((y + screen.get_height()/200) * 100)), 10)

        # Dibujar la línea roja del recorrido
        if len(robot_path) > 1:
            pygame.draw.lines(screen, (255, 0, 0), False, robot_path, 2)

        # Dibujar la flecha de orientación
        arrow_length = 20  # Longitud de la flecha
        # Convertir las coordenadas del robot a píxeles y desplazar el origen al centro de la pantalla
        robot_x_pixel = int((x + screen.get_width()/200) * 100)
        robot_y_pixel = screen.get_height() - int((y + screen.get_height()/200) * 100)
        # Calcular las coordenadas de la flecha
        arrow_x = robot_x_pixel + arrow_length * math.cos(theta)
        arrow_y = robot_y_pixel - arrow_length * math.sin(theta)  # Restar porque el eje y está invertido en Pygame
        pygame.draw.line(screen, (0, 0, 0), (robot_x_pixel, robot_y_pixel), (arrow_x, arrow_y), 2)

        # Dibujar la cabeza de la flecha
        arrow_head_length = 10
        arrow_head_angle = math.pi / 6  # Ángulo de la cabeza de la flecha
        arrow_head_x1 = int(arrow_x - arrow_head_length * math.cos(theta + arrow_head_angle))
        arrow_head_y1 = int(arrow_y + arrow_head_length * math.sin(theta + arrow_head_angle))  # Sumar porque el eje y está invertido en Pygame
        arrow_head_x2 = int(arrow_x - arrow_head_length * math.cos(theta - arrow_head_angle))
        arrow_head_y2 = int(arrow_y + arrow_head_length * math.sin(theta - arrow_head_angle))  # Sumar porque el eje y está invertido en Pygame
        pygame.draw.line(screen, (0, 0, 0), (arrow_x, arrow_y), (arrow_head_x1, arrow_head_y1), 2)
        pygame.draw.line(screen, (0, 0, 0), (arrow_x, arrow_y), (arrow_head_x2, arrow_head_y2), 2)

        # Dibujar las superficies de texto en la esquina inferior derecha
        screen.blit(text_surface1, (screen.get_width() - text_surface1.get_width() - 10, screen.get_height() - text_surface1.get_height() - 10))

        pygame.display.flip()
    
    pygame.quit()

# Bucle principal
while True:
    opcion = menu()
    if opcion == "1":
        wheel_sep = 0.5  # metros
        lw_radius = 0.1  # metros
        rw_radius = 0.1  # metros
        encoder_res = 360  # grados
        juego()
        break
    elif opcion == "2":
        # Permitir al usuario configurar los ajustes
        configurar()
        break
    elif opcion == "3":
        # Salir del programa
        sys.exit()
    else:
        print("Opción no válida. Por favor, intenta de nuevo.")
