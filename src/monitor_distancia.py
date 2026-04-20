import matplotlib.pyplot as plt
import time
import subprocess

# ? Importamos librerias adicionales.
import pandas as pd #? Crear / Exportar datos en formato CSV.

# ! Clase principal, para monitorear la temperatura del CPU de la Raspberry Pi.
class MonitorTemperaturaRPI:
    def __init__(self, duracion_max=60, intervalo=0.5,  archivo_csv="temp_rpi.csv")):
        # Configuración inicial de parametros.
        self.duracion_max = duracion_max    #! Ventana grafica en segundos
        self.intervalo = intervalo          #! Intervalo de actualización en segundos
        self.tiempos = []                   #! Lista de tiempos relativos
        self.temperaturas = []              #! Lista de temperaturas correspondientes de CPU
        self.inicio = time.time()           #! Tiempo de inicio para calcular tiempos relativos

        #? Umbrales de alerta para temperatura.
        self.umbral_alto = 80.0             #! Temperatura en °C para alerta de sobrecalentamiento (NARANJA)
        self.umbral_critico = 85.0          #! Temperatura en °C para alerta crítica (ROJO)

        #? Configuración de la gráfica.
        plt.ion()                           #! Modo interactivo para actualización en tiempo real
        self.fig, self.ax = plt.subplots()  #! Crear figura y eje para la gráfica

    def leer_temperatura(self):
        #! LEe temperatura de CPU usando un comando nativo de Raspberry PI
        try:
            # Ejecuta 'vcgencmd measure_temp' y procesa la salida para obtener solo el valor numérico de la temperatura.
            salida = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            temp_str = salida.strip().replace("temp=", "").replace("'C", "")
            return float(temp_str)
        except Exception as e:
            print("Error leyendo temperatura:", e)
            return None
        
    #! ################# NUEVA FUNCION PARA VERIFICAR ALERTAS #################
    def verificar_alerta(self, temp):
        #! Evalúa temperatura vs umbrales y muestra alertas
        if temp is None:                     # Ignora lecturas inválidas
            return
        
        # ALERTA CRÍTICA (>85°C - peligro throttling/daño)
        if temp > self.umbral_critico:
            print(f"🚨🚨🚨 ¡CRÍTICO! CPU {temp:.1f}°C > {self.umbral_critico}°C")
            print("Apaga inmediatamente!")
        # ALERTA ALTA (>80°C - precaución)
        elif temp > self.umbral_alto:
            print(f"⚠️⚠️⚠️ ALERTA! CPU {temp:.1f}°C > {self.umbral_alto}°C")
        # NORMAL (<40°C - óptimo)
        elif temp < 40:
            print(f"✅✅✅ CPU fresca: {temp:.1f}°C")

    def actualizar_datos(self):
        #! Actualiza datos: lee temp, agrega lista, mantiene ventana rodante
        ahora = time.time() - self.inicio    #! Tiempo relativo desde inicio (segundos)
        temp = self.leer_temperatura()       #! Lee temperatura actual
        
        if temp is not None:                 #! Solo si lectura válida
            self.tiempos.append(ahora)       #! Agrega tiempo actual
            self.temperaturas.append(temp)   #! Agrega temperatura
            self.verificar_alerta(temp)      #! Chequea alertas
            
            # VENTANA RODANTE: elimina datos > duracion_max
            while self.tiempos and self.tiempos[0] < ahora - self.duracion_max:
                self.tiempos.pop(0)          #! Elimina primer tiempo viejo
                self.temperaturas.pop(0)     #! Elimina primera temp vieja
    """
    def graficar(self):
        self.ax.clear()
        self.ax.plot(self.tiempos, self.temperaturas, color='red')
        self.ax.set_title("Temperatura CPU Raspberry Pi")
        self.ax.set_xlabel("Tiempo transcurrido (s)")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.grid(True)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()"""

    def graficar(self):
        """Redibuja gráfico completo con datos actuales"""
        self.ax.clear()                      # Limpia eje anterior
        
        if self.tiempos:                     # Solo si hay datos
            # Gráfico línea principal
            self.ax.plot(self.tiempos, self.temperaturas, color='red', linewidth=2)
            
            # Color dinámico según temp actual
            temp_actual = self.temperaturas[-1]
            color_linea = ('green' if temp_actual < self.umbral_alto 
                          else 'orange' if temp_actual < self.umbral_critico 
                          else 'red')
            self.ax.plot(self.tiempos, self.tiempos, color=color_linea)  # Sobreescribe
            
            # LÍNEAS UMBRALES HORIZONTALES
            self.ax.axhline(y=self.umbral_alto, color='orange', linestyle='--', 
                          label=f'Alerta {self.umbral_alto}°C')
            self.ax.axhline(y=self.umbral_critico, color='red', linestyle='--', 
                          label=f'Crítico {self.umbral_critico}°C')
            
            # Título dinámico con temp actual
            self.ax.set_title(f"Temperatura CPU RPi - Actual: {temp_actual:.1f}°C")
        
        # Etiquetas y formato
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.grid(True, alpha=0.3)        #! Rejilla suave
        self.ax.legend()                     #! Muestra leyenda umbrales
        self.fig.canvas.draw()               #! Redibuja canvas
        self.fig.canvas.flush_events()       #! Actualiza ventana

    def guardar_csv(self):
        """Exporta datos a CSV con timestamps"""
        if self.tiempos:                     # Solo si hay datos
            # Crea DataFrame con 3 columnas
            df = pd.DataFrame({
                'tiempo_s': self.tiempos,                    #! Tiempo relativo (s)
                'temperatura_C': self.temperaturas,          #! Temperatura (°C)
                'timestamp': [time.strftime('%Y-%m-%d %H:%M:%S', 
                                          time.localtime(self.inicio + t)) 
                            for t in self.tiempos]  # Timestamp absoluto
            })
            df.to_csv(self.archivo_csv, index=False)     # Guarda sin índice
            print(f"📊 Datos guardados en {self.archivo_csv} ({len(self.tiempos)} muestras)")

    def ejecutar(self):
        """Bucle principal: monitoreo infinito hasta Ctrl+C"""
        try:
            print(" Monitoreo iniciado. Ctrl+C para parar.")
            # Bucle hasta que cierren ventana matplotlib
            while plt.fignum_exists(self.fig.number):
                self.actualizar_datos()          #! Lee y procesa datos
                self.graficar()                  #! Redibuja gráfico
                time.sleep(self.intervalo)       #! Pausa entre ciclos

        except KeyboardInterrupt:            #! Ctrl+C del usuario
            print("\n⏹ Monitoreo interrumpido por usuario.")

        finally:                             #! SIEMPRE ejecuta (cleanup)
            self.guardar_csv()               #! Guarda datos finales
            print("Monitoreo finalizado.")
            plt.ioff()                       #! Desactiva modo interactivo
            plt.close(self.fig)              #! Cierra ventana gráfica


if __name__ == "__main__":
    # Crea instancia con ventana 5min, update 1s
    monitor = MonitorTemperaturaRPI(duracion_max=300, intervalo=1.0)
    monitor.ejecutar()                   # Inicia monitoreo