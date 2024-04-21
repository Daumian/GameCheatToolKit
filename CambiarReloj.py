import tkinter as tk
from datetime import datetime, timedelta
import ctypes
import subprocess

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Ajustar Hora y Fecha")

# Establecer el tamaño inicial de la ventana
ventana.geometry("400x200")

# Crear una etiqueta para mostrar un mensaje inicial
message_label = tk.Label(ventana, text="El horario actual es", font=("Helvetica", 16))
message_label.pack(pady=5)

# Crear una etiqueta para mostrar la hora y fecha actual
time_label = tk.Label(ventana, text="", font=("Helvetica", 16))
time_label.pack(pady=10)

# Variables globales para almacenar la fecha actual
current_date = datetime.now()

# Definición de la estructura SYSTEMTIME usando ctypes para interactuar con la API de Windows
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", ctypes.c_ushort),
        ("wMonth", ctypes.c_ushort),
        ("wDayOfWeek", ctypes.c_ushort),
        ("wDay", ctypes.c_ushort),
        ("wHour", ctypes.c_ushort),
        ("wMinute", ctypes.c_ushort),
        ("wSecond", ctypes.c_ushort),
        ("wMilliseconds", ctypes.c_ushort),
    ]

# Función para actualizar la etiqueta con la hora y fecha actual
def update_time():
    """
    Actualiza la etiqueta con la hora y fecha actualizadas.
    """
    # Formatear la hora y fecha actual
    current_time = current_date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Actualizar el texto de la etiqueta
    time_label.config(text=current_time)
    
    # Programar la próxima actualización en 1 segundo (1000 ms)
    ventana.after(1000, update_time)

# Función para ajustar la hora del sistema
def adjust_system_time(hour, minute, second):
    now = datetime.now()
    time_string = f"{hour:02}:{minute:02}:{second:02}"
    date_string = f"{now.day:02}/{now.month:02}/{now.year}"
    
    # Comando para cambiar la fecha y hora del sistema en Windows
    command = f'date {date_string} && time {time_string}'
    subprocess.run(command, shell=True, check=True)

# Función para añadir un día a la fecha actual y actualizar el sistema
def add_one_day():
    """
    Añade un día a la fecha actual y actualiza la fecha y hora del sistema.
    """
    global current_date
    
    # Añadir un día a la fecha actual
    current_date += timedelta(days=1)
    
    # Convertir la fecha a una estructura compatible con la API de Windows
    time_tuple = current_date.timetuple()
    
    # Crear una instancia de SYSTEMTIME
    system_time = SYSTEMTIME()
    
    # Completar la estructura con la fecha y hora
    system_time.wYear = time_tuple.tm_year
    system_time.wMonth = time_tuple.tm_mon
    system_time.wDayOfWeek = time_tuple.tm_wday
    system_time.wDay = time_tuple.tm_mday
    system_time.wHour = time_tuple.tm_hour
    system_time.wMinute = time_tuple.tm_min
    system_time.wSecond = time_tuple.tm_sec
    system_time.wMilliseconds = 0  # No se necesitan milisegundos
    
    # Llamar a la API de Windows para ajustar la hora del sistema
    ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time))
    
    # Actualizar la etiqueta con la nueva fecha y hora
    update_time()

# Función para ajustar la fecha y hora del sistema según los botones
def ajustar_hora_agregar(minutos=0, horas=0, dias=0):
    global current_date
    
    # Agregar el tiempo especificado a la fecha actual
    current_date += timedelta(minutes=minutos, hours=horas, days=dias)
    
    # Actualizar la hora del sistema
    add_one_day()

# Botones para ajustar la hora y fecha
boton_5M = tk.Button(ventana, text="+5M", command=lambda: ajustar_hora_agregar(minutos=5))
boton_5M.pack(side=tk.LEFT, padx=(55, 5), pady=10)

boton_30M = tk.Button(ventana, text="+30M", command=lambda: ajustar_hora_agregar(minutos=30))
boton_30M.pack(side=tk.LEFT, padx=5, pady=10)

boton_1H = tk.Button(ventana, text="+1H", command=lambda: ajustar_hora_agregar(horas=1))
boton_1H.pack(side=tk.LEFT, padx=5, pady=10)

boton_6H = tk.Button(ventana, text="+6H", command=lambda: ajustar_hora_agregar(horas=6))
boton_6H.pack(side=tk.LEFT, padx=5, pady=10)

# Botón para añadir un día a la fecha actual
add_one_day_button = tk.Button(ventana, text="Añadir un día", command=add_one_day)
add_one_day_button.pack(side=tk.LEFT, padx=5, pady=10)

# Iniciar la actualización continua de la hora y fecha
update_time()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
