#!/bin/bash

# OBS Controller - Script de construcción para macOS
# Este script crea la aplicación .app y el archivo .dmg

echo "🎮 OBS Controller - Constructor de Aplicación"
echo "=============================================="
echo ""

# Verificar si estamos en macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "⚠️  Advertencia: Este script está diseñado para macOS"
    echo "   Puedes ejecutar la aplicación directamente con Python:"
    echo "   pip install -r requirements.txt"
    echo "   python server/app.py"
    echo ""
    read -p "¿Continuar de todos modos? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Construir la aplicación .app
echo "🔨 Construyendo aplicación .app..."
python setup.py py2app

# Verificar si se creó la aplicación
if [ -d "dist/OBS Controller.app" ]; then
    echo "✅ Aplicación creada exitosamente!"
    echo ""
    echo "📁 Ubicación: dist/OBS Controller.app"
    echo ""
    
    # Crear DMG (solo en macOS)
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "💿 Creando archivo DMG..."
        
        # Crear carpeta temporal para el DMG
        mkdir -p dmg_temp
        cp -r "dist/OBS Controller.app" dmg_temp/
        
        # Crear enlace a Aplicaciones
        ln -s /Applications dmg_temp/Aplicaciones
        
        # Crear el DMG
        hdiutil create -volname "OBS Controller" -srcfolder dmg_temp -ov -format UDZO obs-controller.dmg
        
        # Limpiar
        rm -rf dmg_temp
        
        echo "✅ DMG creado exitosamente!"
        echo ""
        echo "📁 Ubicación: obs-controller.dmg"
    fi
    
    echo ""
    echo "=============================================="
    echo "✨ ¡Construcción completada!"
    echo "=============================================="
    echo ""
    echo "📋 Instrucciones:"
    echo "   1. Abre 'OBS Controller.app' o instala desde el DMG"
    echo "   2. El servidor se iniciará automáticamente"
    echo "   3. Usa los enlaces en el panel de control para OBS"
    echo ""
else
    echo "❌ Error: No se pudo crear la aplicación"
    exit 1
fi
