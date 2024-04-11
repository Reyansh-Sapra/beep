from flask import Flask, render_template, request
import threading
import winsound

app = Flask(__name__)

interval = 1
is_beeping = False
stop_event = threading.Event()

def beep_thread():
    global is_beeping
    while not stop_event.is_set():
        if is_beeping:
            winsound.Beep(1000, 100)  # Adjust frequency and duration of the beep here

@app.route('/', methods=['GET', 'POST'])
def index():
    global interval, is_beeping
    if request.method == 'POST':
        if 'start' in request.form:
            interval = float(request.form['interval'])
            is_beeping = True
            stop_event.clear()
            threading.Thread(target=beep_thread).start()
        elif 'stop' in request.form:
            is_beeping = False
            stop_event.set()
    return render_template('index.html', interval=interval, is_beeping=is_beeping)

if __name__ == '__main__':
    app.run(debug=True)

