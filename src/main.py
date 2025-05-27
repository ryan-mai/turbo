import serial

# Replace 'COM3' with your Arduino's port and 9600 with your baud rate
ser = serial.Serial('COM4', 9600, timeout=1)

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(f"Received from Arduino: {line}")