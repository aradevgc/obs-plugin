# 🎮 OBS Controller

Aplicación de escritorio para controlar overlays de OBS con cronómetro, marcador y pantalla de ganador.

## 📋 Características

- **⏱️ Cronómetro**: Personalizable en tiempo, color, forma (cuadrado, redondo, círculo) y tipografía
- **📊 Marcador de Puntuaciones**: Múltiples equipos, nombres personalizables, suma/resta de puntos
- **🏆 Pantalla de Ganador**: Muestra al ganador con animación y estilo personalizable
- **🎨 Totalmente Personalizable**: Colores, fuentes, tamaños desde el panel de control
- **🌐 Funciona en Red**: Los overlays se pueden acceder desde cualquier dispositivo en la misma red

## 🚀 Instalación y Uso

### Opción 1: Aplicación macOS (Recomendado)

1. Ejecuta el script de construcción:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

2. Se creará:
   - `dist/OBS Controller.app` - La aplicación
   - `obs-controller.dmg` - Archivo DMG para instalar

3. Abre la aplicación y automáticamente:
   - Se iniciará el servidor
   - Se abrirá el panel de control en tu navegador

### Opción 2: Ejecutar con Python

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el servidor:
   ```bash
   python server/app.py
   ```

## 📖 Cómo usar en OBS

1. Abre la aplicación o ejecuta el servidor
2. El panel de control se abrirá automáticamente en `http://localhost:5000/admin`
3. En OBS, añade una nueva fuente de tipo **"Navegador"** (Browser Source)
4. Usa los siguientes enlaces:

   | Overlay | URL |
   |---------|-----|
   | Cronómetro | `http://localhost:5000/overlay/timer` |
   | Puntuaciones | `http://localhost:5000/overlay/scoreboard` |
   | Ganador | `http://localhost:5000/overlay/winner` |

5. Configura el ancho y alto según necesites (recomendado: 1920x1080)
6. Marca "CSS personalizado" y añade: `body { background: transparent; }`

## 🎛️ Panel de Control

El panel de control te permite:

### Cronómetro
- Iniciar/Pausar/Resetear
- Establecer tiempo inicial
- Cambiar color, forma y tipografía
- Ajustar tamaño de fuente

### Marcador
- Añadir/eliminar equipos
- Cambiar nombres de equipos
- Sumar/restar puntos
- Personalizar colores y fuentes

### Ganador
- Escribir nombre del ganador
- Mostrar/Ocultar con animación
- Personalizar estilo

## 🔗 Uso en Red

Para usar los overlays desde otro dispositivo (ej: otra computadora):

1. El panel mostrará tu IP local automáticamente
2. Usa los enlaces con tu IP en lugar de localhost:
   ```
   http://192.168.1.XXX:5000/overlay/timer
   ```

## 📁 Estructura del Proyecto

```
obs-controller/
├── server/
│   └── app.py              # Servidor Flask principal
├── templates/
│   ├── admin.html          # Panel de control
│   ├── overlay_timer.html  # Overlay del cronómetro
│   ├── overlay_scoreboard.html  # Overlay del marcador
│   └── overlay_winner.html # Overlay del ganador
├── requirements.txt        # Dependencias de Python
├── setup.py               # Configuración para py2app
├── build.sh               # Script de construcción
└── README.md              # Este archivo
```

## 🛠️ Requisitos Técnicos

- Python 3.8+
- Flask
- Flask-SocketIO
- Para crear la app macOS: py2app (solo en macOS)

## 📝 Notas

- Los overlays tienen fondo transparente por defecto
- Los cambios en el panel se reflejan en tiempo real
- El servidor usa el puerto 5000 por defecto

## 🎉 ¡Disfruta!

Creado para streamers y creadores de contenido que necesitan controles profesionales para sus transmisiones.
