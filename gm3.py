import serial
import time


# Enable Serial Communication
ser = serial.Serial()
ser.port = "COM7"
ser.baudrate = 115200
ser.timeout = 2
ser.open()

waitTimeout = 10

def sendCommand(ser, cmd):
    ser.write(''.join([cmd,'\r']).encode())
    time.sleep(.15)
    rcv1 = ser.read(ser.inWaiting())
    rcv = rcv1.decode("ISO-8859-1")
    return [rcv]

result = sendCommand(ser, 'AT')
print(result)
