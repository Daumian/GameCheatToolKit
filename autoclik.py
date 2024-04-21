import tkinter as tk
import keyboard
import pyautogui as pa
import threading

# Variables globales para el estado del clic automático y la tecla seleccionada
clicker_active = False
clicker_thread = None
selected_key = None

def click_loop():
    """
    Realiza clics automáticos en la posición actual del cursor mientras
    el clic automático esté activo.
    """
    while clicker_active:
        # Obtén la posición actual del cursor
        current_position = pa.position()
        # Realiza un clic en la posición actual
        pa.click(x=current_position.x, y=current_position.y)
        # Pequeña pausa para evitar hacer clics demasiado rápidos
        pa.sleep(0.001)

def toggle_clicker():
    """
    Alterna el estado del clic automático.
    Si está activo, lo desactiva.
    Si está inactivo, lo activa.
    """
    global clicker_active, clicker_thread

    if clicker_active:
        # Si el clic automático está activo, desactívalo
        clicker_active = False
        etiqueta.config(text="Click Automático desactivado")
    else:
        # Si el clic automático está inactivo, actívalo
        clicker_active = True
        etiqueta.config(text="Click Automático activado")
        
        # Iniciar un hilo separado para ejecutar el clic automático
        clicker_thread = threading.Thread(target=click_loop)
        clicker_thread.start()

def register_key():
    """
    Registra la tecla seleccionada para iniciar y detener el clic automático.
    """
    global selected_key

    # Obtener la tecla seleccionada de la entrada
    selected_key = key_entry.get()
    
    # Si ya hay una tecla registrada, desvincúlala
    if selected_key:
        keyboard.unhook_all()
        # Configurar un enlace para la tecla seleccionada que llama a la función toggle_clicker
        keyboard.on_press_key(selected_key, lambda _: toggle_clicker())
        
        # Actualizar la etiqueta con la tecla seleccionada
        etiqueta_key.config(text=f"Tecla seleccionada: {selected_key}")

# Crear ventana principal
ventana = tk.Tk()

# Configurar geometría de la ventana
ventana.geometry("300x200")

# Crear una etiqueta
etiqueta = tk.Label(ventana, text="Click Automático")
etiqueta.pack()

# Crear una etiqueta para indicar cómo seleccionar la tecla
etiqueta_key_instrucciones = tk.Label(ventana, text="Ingresa una tecla para iniciar/apagar:")
etiqueta_key_instrucciones.pack()

# Crear una entrada de texto para ingresar la tecla
key_entry = tk.Entry(ventana)
key_entry.pack()

# Crear un botón para registrar la tecla seleccionada
boton_registrar = tk.Button(ventana, text="Registrar tecla", command=register_key)
boton_registrar.pack()

# Crear una etiqueta para mostrar la tecla seleccionada
etiqueta_key = tk.Label(ventana, text="Tecla seleccionada: Ninguna")
etiqueta_key.pack()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
