# progressbar-topics
# 🐎 Carrera de Caballos Concurrente

**Unidad 2 — Tópicos Avanzados de Software**  
Universidad de Cartagena · Ingeniería en Software · Cereté, Córdoba · 2026

**Integrantes:**
- Alejandra Salgado Polo  
- Daniela Alejandra Petro Martínez  
- Edgar Alexander Matos Rivera  

**Tutor:** Rafael Benedetti

---

## Descripción

Simulación de una carrera de cuatro caballos desarrollada en **Python 3**, donde cada caballo es representado por un **hilo independiente** (`threading.Thread`). La aplicación muestra una interfaz gráfica con barras de progreso en tiempo real y declara automáticamente al primer caballo en alcanzar la meta como ganador.

El proyecto aplica de forma práctica los conceptos fundamentales de programación concurrente: creación de hilos, exclusión mutua, secciones críticas y comunicación entre procesos mediante memoria compartida.

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje de implementación |
| `threading` | Creación y sincronización de hilos |
| `tkinter` | Interfaz gráfica multiplataforma |
| `random` | Avance aleatorio de cada caballo |

---

## Requisitos

- Python 3.8 o superior
- `tkinter` (incluido en la instalación estándar de Python)

Verificar instalación:
```bash
python --version
python -m tkinter
```

---

## Instalación y ejecución

```bash
# Clonar o descargar el repositorio
git clone <url-del-repositorio>
cd carrera-caballos-concurrente

# Ejecutar el programa
python carrera.py
```

---

## Estructura del proyecto

```
carrera-caballos-concurrente/
│
├── carrera.py          # Archivo principal
├── README.md           # Este archivo
└── informe/
    └── informe_unidad2.pdf   # Informe completo de la actividad
```

---

## Arquitectura del programa

El programa se organiza en dos clases principales:

### `Caballo` (hereda de `threading.Thread`)
Representa cada participante de la carrera como un hilo independiente.

```python
class Caballo(threading.Thread):
    def __init__(self, nombre, progressbar, label_porcentaje, callback_meta):
        super().__init__(daemon=True)
        self.nombre = nombre
        self.recorrido = 0
        self.corriendo = False

    def run(self):
        self.corriendo = True
        while self.corriendo and self.recorrido < 100:
            avance = random.randint(1, 15)
            self.recorrido += avance
            ...
```

### `CarreraApp`
Gestiona la ventana principal, los controles, la creación de los hilos y la coordinación del final de la carrera.

---

## Flujo de ejecución

```
Usuario inicia el programa
        │
        ▼
Se construye la GUI (4 barras en 0%)
        │
        ▼
Usuario presiona [Iniciar]
        │
        ▼
Se crean e inician 4 hilos (uno por caballo)
        │
     ┌──┴──────────────────────┐
     ▼                         ▼
Hilo Caballo 1            Hilo Caballo N
avanza aleatoriamente     avanza aleatoriamente
actualiza barra (via       actualiza barra (via
after() en hilo            after() en hilo
principal)                 principal)
     │                         │
     └──────────┬──────────────┘
                ▼
     Primer hilo en llegar a 100%
                │
                ▼
     Lock adquirido → ganador registrado
     Demás hilos reciben señal de parada
                │
                ▼
     Se muestra el ganador en pantalla
```

---

## Conceptos de concurrencia aplicados

| Concepto | Implementación |
|---|---|
| **Hilo** | Clase `Caballo` hereda de `threading.Thread` |
| **Concurrencia** | Cuatro caballos avanzando simultáneamente |
| **Exclusión mutua** | `threading.Lock` con bloque `with self.lock:` |
| **Sección crítica** | Verificación y asignación de `self.ganador` |
| **Comunicación entre hilos** | Memoria compartida (`corriendo`, `recorrido`, `ganador`) |
| **Thread-safety en GUI** | Actualizaciones via `after(0, callback)` de Tkinter |
| **Prevención de deadlock** | Liberación automática del lock con `with`, sin locks anidados |

### Exclusión mutua — fragmento clave

```python
self.lock = threading.Lock()

def anunciar_ganador(self, nombre):
    with self.lock:
        if self.ganador is None:
            self.ganador = nombre
            for c in self.caballos:
                c.detener()
```

### Thread-safety con Tkinter

```python
# Las actualizaciones visuales se delegan al hilo principal
self.progressbar.after(0, self._actualizar_gui)
```

---

## Resultados observados

- El orden de llegada **varía en cada ejecución**, lo cual es coherente con el no determinismo propio de los sistemas concurrentes.
- En ninguna ejecución se registró **más de un ganador**, validando el correcto funcionamiento del `Lock`.
- Las barras de progreso se actualizan de forma **fluida y sin congelamientos**, confirmando el manejo thread-safe con `after()`.
- Al cerrar la ventana durante la carrera, los hilos terminan limpiamente gracias al atributo `daemon=True`.

---

## Referencias

- Ben-Ari, M. (2006). *Principles of Concurrent and Distributed Programming*. Addison-Wesley Professional.
- Goetz, B. et al. (2006). *Java Concurrency in Practice*. Addison-Wesley Professional.
- Python Software Foundation. (2024). [threading — Thread-based parallelism](https://docs.python.org/3/library/threading.html).
- Universidad de Cartagena. (2026). *Módulo Unidad 2 — Programación Concurrente*. Tópicos Avanzados de Programación.

---

*Universidad de Cartagena — Ingeniería en Software — 2026*
