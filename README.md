[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xB5owuT7)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23101896&assignment_repo_type=AssignmentRepo)
# Lab03: Visualización interactiva de datos en Raspberry Pi usando Python y Matplotlib

## Integrantes
GRUPO 5


## Documentación# 📡 Monitor de Distancia en Tiempo Real con HC-SR04 y Raspberry Pi

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![RPi.GPIO](https://img.shields.io/badge/RPi.GPIO-Compatible-green.svg)](https://pypi.org/project/RPi.GPIO/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-TkAgg-orange.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)](https://www.raspberrypi.org/)

Sistema de monitoreo de distancia en tiempo real usando el sensor ultrasónico **HC-SR04** conectado a una **Raspberry Pi**. El programa realiza mediciones periódicas, las visualiza en una gráfica dinámica y reporta el estado en consola, todo implementado bajo un enfoque orientado a objetos.

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Requisitos](#-requisitos)
- [Conexión del Hardware](#-conexión-del-hardware)
- [Uso](#-uso)
- [Estructura del Código](#-estructura-del-código)
- [Documentación de la Clase](#-documentación-de-la-clase)
- [Preguntas Frecuentes y Decisiones de Diseño](#-preguntas-frecuentes-y-decisiones-de-diseño)
- [Modificaciones y Extensiones](#-modificaciones-y-extensiones)
- [Consideraciones de Seguridad](#-consideraciones-de-seguridad)
- [Fórmula de Cálculo de Distancia](#-fórmula-de-cálculo-de-distancia)
---

## 📖 Descripción General

Este proyecto implementa la clase `MonitorDistanciaHC_SR04`, que encapsula toda la lógica necesaria para:

- ✅ Configurar y controlar el sensor HC-SR04 mediante los pines GPIO de la Raspberry Pi.
- ✅ Leer distancias en centímetros de forma continua y periódica.
- ✅ Almacenar un historial de mediciones en una ventana de tiempo configurable.
- ✅ Graficar en tiempo real la evolución de la distancia usando `matplotlib`.
- ✅ Mostrar el estado de cada medición en consola.

---

## 🧰 Requisitos

### Hardware

| Componente         | Descripción                           |
|--------------------|---------------------------------------|
| Raspberry Pi       | Cualquier modelo con pines GPIO       |
| Sensor HC-SR04     | Sensor ultrasónico de distancia       |
| Cables de conexión | Jumper wires hembra-macho             |

### Hardware

| Componente         | Descripción                           |
|--------------------|---------------------------------------|
| Raspberry Pi       | Cualquier modelo con pines GPIO       |
| Sensor HC-SR04     | Sensor ultrasónico de distancia       |
| Cables de conexión | Jumper wires hembra-macho             |

### Software

| Librería   | Versión recomendada |
|------------|---------------------|
| Python     | 3.6+                |
| RPi.GPIO   | 0.7.0+              |
| matplotlib | 3.x+                |

---

## 🔌 Conexión del Hardware

```
    HC-SR04                Raspberry Pi (BCM)
   ┌─────────┐            ┌──────────────────────┐
   │   VCC   │ ─────────► │ Pin 2  - 5V Power    │
   │   GND   │ ─────────► │ Pin 6  - Ground      │
   │   TRIG  │ ─────────► │ GPIO23 - Pin 16      │
   │   ECHO  │ ─────────► │ GPIO24 - Pin 18 ⚠️   │
   └─────────┘            └──────────────────────┘
```

> ⚠️ **Advertencia de voltaje:** El pin `ECHO` del HC-SR04 opera a **5V**, mientras que los GPIOs de la Raspberry Pi toleran un máximo de **3.3V**. En entornos de producción, se recomienda interponer un divisor de voltaje con resistencias de **1kΩ** y **2kΩ** para proteger el pin GPIO. Este script fue diseñado para pruebas rápidas sin resistencias externas, usando el pull-up interno como mitigación parcial.

---

## 🚀 Uso

### Ejecución básica

    sudo python3 monitor_distancia.py

### Salida esperada en consola

```
HC-SR04 SIN RESISTENCIAS
VCC=Pin2(5V), GND=Pin6, TRIG=GPIO23, ECHO=GPIO24
Ctrl+C para salir

Dist: 23.4 cm [OK]
Dist: 24.1 cm [OK]
Dist: -1 cm   [ERROR]
Dist: 22.8 cm [OK]
```

### Detener el programa

Presiona `Ctrl+C`. El programa ejecutará automáticamente `GPIO.cleanup()` y cerrará la ventana gráfica de forma segura.

### Parámetros configurables

| Parámetro      | Tipo    | Valor por defecto | Descripción                                  |
|----------------|---------|-------------------|----------------------------------------------|
| `trig_pin`     | `int`   | `23`              | Pin GPIO para la señal TRIG                  |
| `echo_pin`     | `int`   | `24`              | Pin GPIO para la señal ECHO                  |
| `duracion_max` | `int`   | `60`              | Segundos de historial visibles en la gráfica |
| `intervalo`    | `float` | `1.0`             | Segundos de pausa entre cada medición        |

**Ejemplo con parámetros personalizados:**

    monitor = MonitorDistanciaHC_SR04(
        trig_pin=17,
        echo_pin=27,
        duracion_max=120,
        intervalo=0.5
    )
    monitor.ejecutar()

---

## 🗂️ Estructura del Código

```
MonitorDistanciaHC_SR04
│
├── __init__(trig_pin, echo_pin, duracion_max, intervalo)
│       Inicializa pines GPIO, listas de datos y la figura de matplotlib.
│
├── leer_distancia()
│       Envía el pulso TRIG, mide la duración del pulso ECHO
│       y calcula la distancia resultante en centímetros.
│
├── actualizar_datos()
│       Registra la medición actual con su timestamp relativo
│       y elimina datos que superen la ventana de tiempo definida.
│
├── graficar()
│       Limpia y redibuja la gráfica en tiempo real con los
│       datos almacenados en las listas de tiempos y distancias.
│
└── ejecutar()
        Bucle principal: coordina la lectura, actualización,
        graficación y reporte en consola. Gestiona la salida
        segura con Ctrl+C.
```

### Flujo de ejecución

```
 ┌─────────────────────────────────────────────────────┐
 │                      INICIO                         │
 └────────────────────────┬────────────────────────────┘
                          │
                          ▼
 ┌─────────────────────────────────────────────────────┐
 │   __init__()                                        │
 │   - Configurar pines GPIO (TRIG=OUT, ECHO=IN)       │
 │   - Inicializar listas vacías: tiempos, distancias  │
 │   - Registrar tiempo de inicio: self.inicio         │
 │   - Crear figura matplotlib en modo interactivo     │
 └────────────────────────┬────────────────────────────┘
                          │
                          ▼
 ┌─────────────────────────────────────────────────────┐
 │   ejecutar() → Bucle infinito                       │
 │                                                     │
 │   ┌─────────────────────────────────────────────┐   │
 │   │  actualizar_datos()                         │   │
 │   │  - Calcular tiempo relativo                 │   │
 │   │  - Llamar leer_distancia()                  │   │
 │   │     ├─ Enviar pulso TRIG (15µs)             │   │
 │   │     ├─ Esperar flanco de subida en ECHO     │   │
 │   │     ├─ Medir duración pulso ECHO            │   │
 │   │     └─ Retornar distancia (cm) o None       │   │
 │   │  - Agregar datos a listas                   │   │
 │   │  - Depurar datos fuera de ventana de tiempo │   │
 │   └──────────────────┬──────────────────────────┘   │
 │                      │                              │
 │                      ▼                              │
 │   ┌─────────────────────────────────────────────┐   │
 │   │  graficar()                                 │   │
 │   │  - ax.clear() → limpiar eje anterior        │   │
 │   │  - ax.plot()  → trazar nuevos datos         │   │
 │   │  - canvas.draw() → renderizar gráfica       │   │
 │   └──────────────────┬──────────────────────────┘   │
 │                      │                              │
 │                      ▼                              │
 │          Imprimir estado en consola                 │
 │                      │                              │
 │                      ▼                              │
 │          time.sleep(self.intervalo)                 │
 │                      │                              │
 │                      └──────────────► (repetir)     │
 └─────────────────────────────────────────────────────┘
                          │
                   Ctrl+C │
                          ▼
 ┌─────────────────────────────────────────────────────┐
 │   finally:                                          │
 │   - GPIO.cleanup()   → liberar pines               │
 │   - plt.close()      → cerrar ventana gráfica      │
 └─────────────────────────────────────────────────────┘
```

---

## 📚 Documentación de la Clase

### `MonitorDistanciaHC_SR04`

    class MonitorDistanciaHC_SR04:
        """
        Monitor de distancia en tiempo real para el sensor ultrasónico HC-SR04.

        Atributos:
            trig_pin     (int)   : Pin GPIO de salida para la señal TRIG.
            echo_pin     (int)   : Pin GPIO de entrada para la señal ECHO.
            duracion_max (int)   : Segundos máximos del historial en la gráfica.
            intervalo    (float) : Pausa en segundos entre cada ciclo de medición.
            tiempos      (list)  : Lista de timestamps relativos de cada medición.
            distancias   (list)  : Lista de distancias medidas en centímetros.
            inicio       (float) : Timestamp Unix del momento de inicio.
            fig          (Figure): Figura de matplotlib para la gráfica.
            ax           (Axes)  : Eje de la figura de matplotlib.
        """

### Métodos

#### `__init__(trig_pin, echo_pin, duracion_max, intervalo)`
Inicializa la instancia del monitor. Configura los pines GPIO, las listas de almacenamiento de datos, el timestamp de inicio y la ventana gráfica interactiva de `matplotlib`.

#### `leer_distancia() → float | None`
Ejecuta el ciclo completo de disparo y lectura del sensor:
1. Estabiliza el pin TRIG en `LOW` durante 60ms.
2. Emite un pulso `HIGH` de 15µs en el TRIG.
3. Espera el flanco de subida del ECHO (timeout: 200ms).
4. Mide la duración del pulso `HIGH` en ECHO.
5. Calcula la distancia: `distancia = duración × 17150` cm.
6. Retorna la distancia si está en rango válido `(0, 400)` cm, de lo contrario `None`.

#### `actualizar_datos()`
Registra la medición más reciente junto con su tiempo relativo. Depura automáticamente los datos más antiguos que `duracion_max` segundos para mantener la ventana deslizante.

#### `graficar()`
Limpia el eje actual con `ax.clear()` y redibuja la gráfica completa con los datos actuales. Configura etiquetas, título, límites del eje Y y grilla, luego fuerza el renderizado con `canvas.draw()` y `flush_events()`.

#### `ejecutar()`
Método de entrada principal. Ejecuta el bucle de monitoreo continuo, coordinando la lectura, actualización y graficación. Maneja la interrupción por teclado (`Ctrl+C`) y garantiza la limpieza de recursos en el bloque `finally`.

---

## ❓ Preguntas Frecuentes y Decisiones de Diseño

---

### 1. ¿Qué función cumpliría `plt.fignum_exists(self.fig.number)` en el ciclo principal?

`plt.fignum_exists(self.fig.number)` **no está implementada en este script**, pero representa una mejora importante. Esta función retorna `True` si la ventana gráfica con el número dado sigue existiendo, es decir, si el usuario no la ha cerrado manualmente.

Sin esta verificación, si el usuario cierra la ventana de `matplotlib` con el botón ✕, el bucle `while True` continuará ejecutándose e intentando renderizar en una figura destruida, lo que genera excepciones no controladas.

**Implementación recomendada:**

    def ejecutar(self):
        try:
            while plt.fignum_exists(self.fig.number):
                self.actualizar_datos()
                ultima = self.distancias[-1]
                estado = "OK" if ultima > 0 else "ERROR"
                print(f"Dist: {ultima} cm [{estado}]")
                self.graficar()
                time.sleep(self.intervalo)
            print("\nVentana cerrada. Finalizando...")
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario.")
        finally:
            GPIO.cleanup()
            plt.close()

**Comparativa de comportamiento:**

| Situación                       | Sin `fignum_exists`          | Con `fignum_exists`         |
|---------------------------------|------------------------------|-----------------------------|
| Usuario cierra la ventana con ✕ | Excepción no controlada      | Salida limpia y controlada  |
| Usuario presiona Ctrl+C         | `KeyboardInterrupt` capturado| `KeyboardInterrupt` capturado|
| Ventana sigue abierta           | Bucle continúa               | Bucle continúa              |

---

### 2. ¿Por qué se usa `time.sleep(self.intervalo)` y qué pasa si se quita?

`time.sleep(self.intervalo)` **suspende la ejecución del hilo principal** durante el número de segundos indicado por `intervalo` (por defecto `1.0` s). Cumple tres roles fundamentales:

- 🕐 **Control de frecuencia de muestreo:** Define cada cuánto se toma una medición, evitando saturar el sensor.
- 💻 **Eficiencia de CPU:** Durante el `sleep`, el proceso libera la CPU, permitiendo que el sistema operativo atienda otros procesos.
- 🔊 **Estabilidad del sensor:** El HC-SR04 requiere tiempo de reposo entre lecturas para que los ecos anteriores se disipen completamente y no interfieran con el siguiente pulso.

**Consecuencias de eliminar `time.sleep()`:**

| Consecuencia             | Descripción                                                                  |
|--------------------------|------------------------------------------------------------------------------|
| ⚠️ CPU al 100%           | El bucle se ejecuta sin pausa, monopolizando el procesador                   |
| ⚠️ Mediciones erróneas   | El sensor puede capturar ecos residuales del pulso anterior                  |
| ⚠️ Gráfica congelada     | `matplotlib` no tiene tiempo de procesar eventos de la ventana               |
| ⚠️ Inestabilidad del SO  | Otros procesos del sistema pueden verse afectados                            |
| ⚠️ Desgaste del hardware | La activación continua del TRIG puede sobrecalentar el circuito del sensor   |

---

### 3. ¿Qué ventaja tiene usar `__init__` para inicializar listas y variables?

El método `__init__` es el **constructor de la clase** en Python y se ejecuta automáticamente al instanciar el objeto. Centralizar la inicialización en él ofrece múltiples beneficios:

- 📦 **Encapsulamiento:** Todos los atributos del objeto están declarados en un único lugar, facilitando la lectura y el mantenimiento del código.
- 🔄 **Estado inicial predecible:** Garantiza que cada instancia comienza con un estado limpio (`tiempos = []`, `distancias = []`), sin datos residuales.
- 🔧 **Inyección de parámetros:** Los argumentos con valores por defecto permiten reutilizar la clase con distintas configuraciones sin modificar el código fuente.
- 🧪 **Instancias independientes:** Si se crean múltiples monitores, cada uno mantiene su propio estado aislado:

```
monitor_sala   = MonitorDistanciaHC_SR04(trig_pin=23, echo_pin=24)
monitor_garage = MonitorDistanciaHC_SR04(trig_pin=17, echo_pin=27)
```

- 🐞 **Facilita el debugging:** Al conocer el estado inicial exacto de cada atributo, es más sencillo rastrear errores relacionados con valores inesperados.

---

### 4. ¿Qué se está midiendo con `self.inicio = time.time()`?

`time.time()` retorna el **timestamp Unix** actual: el número de segundos transcurridos desde el **1 de enero de 1970 a las 00:00:00 UTC**.

Al almacenarlo en `self.inicio` durante la construcción del objeto, se fija un **punto de referencia temporal** correspondiente al momento exacto en que el monitor inició su operación. Esto permite calcular, en cada medición, cuántos segundos han transcurrido desde el arranque:

    ahora = time.time() - self.inicio
    # Resultado: 0.0 al iniciar, 1.0 al segundo, 60.0 al minuto, etc.

Esta referencia es la base del eje X de la gráfica y del mecanismo de ventana deslizante que elimina datos antiguos.

---

### 5. ¿Qué hace exactamente `subprocess.check_output(...)`?

> 📌 Esta función **no está presente en este script**. Pertenece a implementaciones de monitores con sensores de temperatura **DS18B20**, donde el valor del sensor se lee desde el sistema de archivos virtual del kernel Linux (`/sys/bus/w1/`).

En ese contexto, su funcionamiento es el siguiente:

    import subprocess

    salida = subprocess.check_output(
        ['cat', '/sys/bus/w1/devices/28-xxxx/w1_slave'],
        stderr=subprocess.STDOUT
    )

**Paso a paso:**

| Paso | Acción                                                                  |
|------|-------------------------------------------------------------------------|
| 1    | Lanza un subproceso del SO ejecutando el comando especificado           |
| 2    | Espera a que el subproceso finalice                                     |
| 3    | Si el código de retorno es `0` (éxito), retorna la salida como `bytes`  |
| 4    | Si el código de retorno es distinto de `0`, lanza `CalledProcessError`  |

**Ejemplo de salida retornada (DS18B20):**

    b'50 01 4b 46 7f ff 0c 10 1c : crc=1c YES\n50 01 4b 46 7f ff 0c 10 1c t=21062\n'

Donde `t=21062` representa una temperatura de **21.062 °C**.

---

### 6. ¿Por qué se almacena `ahora = time.time() - self.inicio` en lugar del tiempo absoluto?

Se utiliza tiempo **relativo** (segundos desde el inicio del monitoreo) en lugar de tiempo **absoluto** (timestamp Unix) por las siguientes razones:

| Aspecto                  | Tiempo Relativo                        | Tiempo Absoluto (Unix)                      |
|--------------------------|----------------------------------------|---------------------------------------------|
| **Legibilidad**          | `0, 1, 2, 3...` segundos              | `1718392847.23...` (ilegible directamente)  |
| **Eje X de la gráfica**  | Intuitivo: "segundos desde el inicio" | Requiere conversión a fecha/hora legible    |
| **Ventana deslizante**   | `tiempos[0] < ahora - duracion_max`   | Cálculo equivalente pero más confuso        |
| **Portabilidad**         | Independiente del huso horario        | Depende de la configuración del sistema     |

**Implementación de la ventana deslizante usando tiempo relativo:**

    while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
        self.tiempos.pop(0)
        self.distancias.pop(0)

> Esto garantiza que la gráfica siempre muestre únicamente los últimos `duracion_max` segundos de mediciones, manteniendo el tamaño de las listas acotado y el rendimiento estable.

---

### 7. ¿Por qué se usa `self.ax.clear()` antes de graficar?

`self.ax.clear()` **borra completamente el contenido del eje** (trazados, etiquetas, título, límites) antes de redibujar con los datos actualizados. Sin esta llamada, cada iteración añadiría una nueva línea encima de las anteriores:

```
Sin ax.clear():                       Con ax.clear():
─────────────────────────────────     ─────────────────────────────────
Iteración 1:  1 línea                 Iteración 1:  1 línea (actualizada)
Iteración 2:  2 líneas superpuestas   Iteración 2:  1 línea (actualizada)
Iteración 50: 50 líneas apiladas      Iteración 50: 1 línea (actualizada)
→ Resultado: lento e incorrecto       → Resultado: rápido y preciso
```

**Flujo completo de actualización de la gráfica:**

    def graficar(self):
        self.ax.clear()                                           # 1. Borrar contenido anterior
        self.ax.plot(self.tiempos, self.distancias, 'g-',         # 2. Trazar nuevos datos
                     linewidth=2)
        self.ax.set_title("HC-SR04 Distancia (Sin Resistencias)") # 3. Restaurar metadatos
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Distancia (cm)")
        self.ax.set_ylim(-2, 150)
        self.ax.grid(True)
        self.fig.canvas.draw()                                    # 4. Renderizar en pantalla
        self.fig.canvas.flush_events()                            # 5. Procesar eventos pendientes

> 💡 **Alternativa de mayor rendimiento:** Para actualizaciones muy frecuentes (< 100ms), se puede usar `line.set_data(x, y)` sobre un objeto `Line2D` existente, evitando recrear el trazado completo. Esta técnica se conoce como *blitting* y es significativamente más eficiente en aplicaciones de alta frecuencia.

---

### 8. ¿Qué captura el bloque `try...except` dentro de `leer_distancia()`?

El bloque `try...except` en `leer_distancia()` actúa como una **red de seguridad amplia** que intercepta cualquier excepción no controlada producida durante la comunicación con el sensor, retornando `None` en su lugar para no interrumpir el ciclo principal.

    def leer_distancia(self):
        try:
            # ... toda la lógica de medición
            return distance if 0 < distance < 400 else None
        except:
            return None  # Fallo silencioso → el dato se registra como -1

**Tipos de error que puede capturar:**

| Tipo de Excepción     | Causa probable                                                    |
|-----------------------|-------------------------------------------------------------------|
| `RuntimeError`        | Pin GPIO mal configurado o conflicto de acceso con otro proceso   |
| `UnboundLocalError`   | `pulse_end` no llega a asignarse si el ECHO no genera flanco ↑    |
| `TimeoutError`        | Sensor sin respuesta (objeto demasiado lejano o fallo hardware)   |
| `Exception` general   | Ruido eléctrico, conexión floja o fallo transitorio del sensor    |

> ⚠️ **Buena práctica:** Usar `except:` sin tipo específico silencia **todos** los errores, incluyendo errores de programación. En un entorno de producción se recomienda capturar excepciones específicas:

    except (RuntimeError, UnboundLocalError, ValueError) as e:
        print(f"[WARN] Error en lectura: {e}")
        return None

---

## 🔧 Modificaciones y Extensiones

### 9. ¿Cómo guardar las distancias en un archivo `.csv`?

Para persistir las mediciones en un archivo CSV, se puede extender la clase con los siguientes cambios:

**Paso 1 — Importar `csv` y crear el archivo con encabezados en `__init__`:**

    import csv
    import os

    def __init__(self, trig_pin=23, echo_pin=24, duracion_max=60,
                 intervalo=1.0, archivo_csv="distancias.csv"):
        # ... inicialización existente sin cambios ...

        self.archivo_csv = archivo_csv
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Tiempo_s", "Distancia_cm", "Estado"])
        print(f"[CSV] Registrando datos en: {self.archivo_csv}")

**Paso 2 — Añadir el método `guardar_csv()`:**

    def guardar_csv(self, tiempo, distancia):
        """Agrega una fila con la medición actual al archivo CSV."""
        estado = "OK" if distancia > 0 else "ERROR"
        with open(self.archivo_csv, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([round(tiempo, 3), distancia, estado])

**Paso 3 — Invocarlo desde `actualizar_datos()`:**

    def actualizar_datos(self):
        ahora = time.time() - self.inicio
        dist = self.leer_distancia()
        self.tiempos.append(ahora)
        self.distancias.append(dist or -1)
        self.guardar_csv(ahora, dist or -1)  # ← Nueva línea

        while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
            self.tiempos.pop(0)
            self.distancias.pop(0)

**Ejemplo del archivo `distancias.csv` generado:**

    Tiempo_s,Distancia_cm,Estado
    0.000,23.4,OK
    1.012,24.1,OK
    2.034,-1,ERROR
    3.051,22.8,OK
    4.063,21.5,OK

**Lectura posterior con pandas para análisis de datos:**

    import pandas as pd
    df = pd.read_csv("distancias.csv")
    print(df.describe())
    df.plot(x="Tiempo_s", y="Distancia_cm", title="Historial de Distancias")

---

## ⚠️ Consideraciones de Seguridad

| Riesgo                       | Descripción                                                                | Mitigación recomendada                                   |
|------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------|
| 🔋 Sobrevoltaje en ECHO      | El pin ECHO opera a 5V; los GPIO toleran máx. 3.3V                        | Divisor de voltaje con resistencias 1kΩ y 2kΩ            |
| 🔌 GPIO no liberado          | Sin `GPIO.cleanup()`, los pines quedan configurados al salir               | Usar bloque `finally` (ya implementado)                  |
| 🌡️ Variación por temperatura | La velocidad del sonido varía con la temperatura ambiente                  | Ajustar factor: `v = (331.3 + 0.606 × T) / 2` cm/s      |
| 🔄 Interferencia entre pulsos| Sin `time.sleep()`, los ecos residuales afectan la siguiente medición      | Mantener `intervalo` ≥ 0.06s entre mediciones            |
| 🐍 `except:` genérico        | Oculta errores de programación al capturar todas las excepciones           | Especificar los tipos de excepción esperados             |

---

## 📐 Fórmula de Cálculo de Distancia

```
         Duración del pulso ECHO (s)  ×  Velocidad del sonido (cm/s)
Dist =  ─────────────────────────────────────────────────────────────
                                    2

Donde:
  Velocidad del sonido ≈ 34300 cm/s  (a ~20 °C al nivel del mar)
  División por 2: el sonido recorre la distancia de ida Y de vuelta.

  Simplificado en el código:
  distance = duration × 17150   →   (34300 / 2 = 17150)
```

**Ajuste por temperatura ambiente:**

    velocidad_sonido = 331.3 + (0.606 * temperatura_celsius)  # m/s
    factor_cm        = (velocidad_sonido * 100) / 2           # cm/s ajustado
    distance         = duration * factor_cm

---