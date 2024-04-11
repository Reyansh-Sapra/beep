from flask import Flask, render_template, request
import threading
import time
import winsound

app = Flask(__name__)

interval = 1
is_beeping = False
stop_event = threading.Event()

def beep_thread():
    global is_beeping
    while not stop_event.is_set():
        if is_beeping:
            winsound.Beep(1000, 100)  # You can adjust the frequency and duration of the beep here
            time.sleep(interval)

@app.route('/')
def index():
    return render_template('index.html', interval=interval)

@app.route('/start', methods=['POST'])
def start():
    global is_beeping
    is_beeping = True
    stop_event.clear()
    threading.Thread(target=beep_thread).start()
    return '', 204

@app.route('/stop', methods=['POST'])
def stop():
    global is_beeping
    is_beeping = False
    stop_event.set()
    return '', 204

@app.route('/set_interval', methods=['POST'])
def set_interval():
    global interval
    interval = float(request.form['interval'])
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
