from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
# @app.route('/run-serial')
# def run_serial():
#     ser = serial.Serial('COM4', 9600, timeout=2)
#     time.sleep(2)  # Wait for Arduino to reset if needed
#     ser.write(b'P')
#     time.sleep(1)  # Give Arduino time to respond
#     line = ser.readline().decode('utf-8').strip()
#     ser.close()
#     return {'result': line}

if __name__ == '__main__':
    app.run(debug=True)