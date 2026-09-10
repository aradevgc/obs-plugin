from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import socket
import threading
import webbrowser
import time
import os

# Obtener la ruta base del directorio del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.config['SECRET_KEY'] = 'obs-controller-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Estado global
state = {
    'timer': {
        'active': False,
        'time': 0,
        'initial_time': 0,
        'style': {
            'color': '#ffffff',
            'shape': 'square',
            'font': 'Arial',
            'fontSize': 72
        }
    },
    'scoreboard': {
        'teams': [
            {'name': 'Equipo 1', 'score': 0},
            {'name': 'Equipo 2', 'score': 0}
        ],
        'style': {
            'color': '#ffffff',
            'font': 'Arial',
            'fontSize': 48
        }
    },
    'winner': {
        'name': 'Gran Ganador',
        'visible': False,
        'style': {
            'color': '#ffd700',
            'font': 'Arial',
            'fontSize': 96
        }
    }
}

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/overlay/timer')
def overlay_timer():
    return render_template('overlay_timer.html', timer=state['timer'])

@app.route('/overlay/scoreboard')
def overlay_scoreboard():
    return render_template('overlay_scoreboard.html', scoreboard=state['scoreboard'])

@app.route('/overlay/winner')
def overlay_winner():
    return render_template('overlay_winner.html', winner=state['winner'])

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(state)

@app.route('/api/timer', methods=['POST'])
def update_timer():
    data = request.json
    if 'action' in data:
        action = data['action']
        if action == 'start':
            state['timer']['active'] = True
            state['timer']['time'] = state['timer'].get('initial_time', state['timer'].get('time', 0))
        elif action == 'pause':
            state['timer']['active'] = False
        elif action == 'reset':
            state['timer']['active'] = False
            state['timer']['time'] = state['timer'].get('initial_time', 0)
    if 'time' in data:
        state['timer']['time'] = int(data['time'])
        state['timer']['initial_time'] = int(data['time'])
    if 'style' in data:
        state['timer']['style'].update(data['style'])
    socketio.emit('timer_update', state['timer'])
    return jsonify(state['timer'])

@app.route('/api/scoreboard', methods=['POST'])
def update_scoreboard():
    data = request.json
    if 'teams' in data:
        state['scoreboard']['teams'] = data['teams']
    if 'style' in data:
        state['scoreboard']['style'].update(data['style'])
    if 'add_team' in data:
        state['scoreboard']['teams'].append({'name': data['add_team'], 'score': 0})
    if 'remove_team' in data:
        idx = int(data['remove_team'])
        if 0 <= idx < len(state['scoreboard']['teams']):
            state['scoreboard']['teams'].pop(idx)
    if 'update_score' in data:
        idx = int(data['update_score']['index'])
        delta = int(data['update_score']['delta'])
        if 0 <= idx < len(state['scoreboard']['teams']):
            state['scoreboard']['teams'][idx]['score'] += delta
    socketio.emit('scoreboard_update', state['scoreboard'])
    return jsonify(state['scoreboard'])

@app.route('/api/winner', methods=['POST'])
def update_winner():
    data = request.json
    if 'name' in data:
        state['winner']['name'] = data['name']
    if 'visible' in data:
        state['winner']['visible'] = data['visible']
    if 'style' in data:
        state['winner']['style'].update(data['style'])
    socketio.emit('winner_update', state['winner'])
    return jsonify(state['winner'])

@socketio.on('connect')
def handle_connect():
    emit('timer_update', state['timer'])
    emit('scoreboard_update', state['scoreboard'])
    emit('winner_update', state['winner'])

def open_browser():
    time.sleep(1.5)
    local_ip = get_local_ip()
    print(f"\n{'='*50}")
    print("🎮 OBS Controller iniciado!")
    print(f"{'='*50}")
    print(f"\n📋 Panel de Control:")
    print(f"   http://localhost:5000/admin")
    print(f"\n🌐 Enlaces para OBS (desde otros dispositivos):")
    print(f"   Cronómetro:     http://{local_ip}:5000/overlay/timer")
    print(f"   Puntuaciones:   http://{local_ip}:5000/overlay/scoreboard")
    print(f"   Ganador:        http://{local_ip}:5000/overlay/winner")
    print(f"\n{'='*50}")
    print("Presiona Ctrl+C para detener el servidor\n")
    webbrowser.open('http://localhost:5000/admin')

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
