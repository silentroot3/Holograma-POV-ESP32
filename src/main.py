from machine import Pin
import time

sensor = Pin(16, Pin.IN)

led_pins = [13, 12, 14, 27, 26, 33, 25, 32]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

TIEMPO_VUELTA_US = 20000

COLUMNAS_TOTALES = 40

TIEMPO_COLUMNA_US = TIEMPO_VUELTA_US // COLUMNAS_TOTALES

PULSO_US = 50

letra_H = [
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
]

letra_O = [
    [0,1,1,1,1,1,0],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [0,1,1,1,1,1,0],
]

letra_L = [
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0],
    [1,1,1,1,1,1,1],
]

letra_A = [
    [0,1,1,1,1,1,0],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
]

espacio = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
]

def unir_letras(*args):
    if not args:
        return []
    
    filas = len(args[0])
    resultado = [[] for _ in range(filas)]
    
    for letra in args:
        for fila in range(filas):
            resultado[fila].extend(letra[fila])
    
    return resultado

patron_completo = unir_letras(letra_H, espacio, letra_O, espacio, letra_L, espacio, letra_A)

ANCHO_TOTAL = len(patron_completo[0]) if patron_completo else COLUMNAS_TOTALES

def apagar_todos():
    for led in leds:
        led.value(0)

def mostrar_columna(col):
    if col < ANCHO_TOTAL:
        for i in range(8):
            leds[i].value(patron_completo[i][col])
    else:
        apagar_todos()

ultimo_estado = 1

try:
    while True:
        estado_actual = sensor.value()
        
        if ultimo_estado == 1 and estado_actual == 0:
            for col in range(ANCHO_TOTAL):
                mostrar_columna(col)
                
                time.sleep_us(PULSO_US)
                
                apagar_todos()
                
                time.sleep_us(TIEMPO_COLUMNA_US - PULSO_US)
        
        ultimo_estado = estado_actual
        time.sleep_us(10)

except KeyboardInterrupt:
    apagar_todos()