
from flask import Flask, render_template, request
from mypalletizer import MyPalletizer

import MyPalletizerProcess

from queue import Queue
from threading import Thread

import time
import math
import json

app = Flask(__name__, static_folder='static')

task_queue = Queue()
result_queue = Queue()
PORTNAME = '/dev/ttyUSB0'

def deg2rad(deg):
    rad = []
    for d in deg:
        r = d *(math.pi / 180.0)
        rad.append(r)
    
    return rad

def rad2deg(rad):
    deg = []
    for r in rad:
        d = r *(180.0/ math.pi)
        deg.append(d)
    
    return deg

@app.route('/')
def index():
    return render_template('index.html', static_url='./static/')

@app.route('/get_angle')
def get_angle():
    task_queue.put(['get_radians'])

    time.sleep(0.5)

    while result_queue.empty():
        time.sleep(0.01)

    radians = result_queue.get()

    degrees = rad2deg(radians)

    return json.dumps(degrees)

@app.route('/set_angle', methods=['POST'])
def set_angle():
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        try:
            l_sf_f = [float(s) for s in data]
            task_queue.put(['sync_send_angles', l_sf_f, 50])
            while result_queue.empty():
                time.sleep(0.01)
            radians = json.loads(get_angle())
        except Exception as e:
            pass 
    return "set_angle"

if __name__ == '__main__':
    mp_process = MyPalletizerProcess.MyPalletizerProcess(task_queue, result_queue, PORTNAME)
    mp_thread = Thread(target=mp_process.run)
    mp_thread.start()

    app.run(host='0.0.0.0', port=8090, threaded=True)