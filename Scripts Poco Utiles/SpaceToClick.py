import tkinter as tk
import keyboard
import pyautogui as pa

# Crear ventana principal
ventana = tk.Tk()

# Configurar geometría de la ventana
ventana.geometry("300x200")

# Crear una etiqueta que indica la acción de presionar "espacio"
etiqueta = tk.Label(ventana, text="Cada que presiones la tecla 'Espacio' se hará un clic.")
etiqueta.pack()

# Función para manejar eventos de teclado
def manejar_evento_tecla(evento):
    if evento.name == 'space':
        # Hacer clic en la posición actual del cursor
        pa.click()

# Registrar el manejador de eventos para la tecla 'espacio'
keyboard.on_press(manejar_evento_tecla)

# Iniciar el bucle principal de la ventana
ventana.mainloop()

# Desregistrar el manejador de eventos cuando se cierre la aplicación
keyboard.unhook(manejar_evento_tecla)
