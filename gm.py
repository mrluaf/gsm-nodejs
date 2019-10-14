import time
import serial
from unicodeToChar import unicodeToChar
# unicodeToChar.unicodeToChar()

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM7',
    baudrate=115200
)

ser.isOpen()

print ('Enter your commands below.\r\nInsert "exit" to leave the application.')

ser.write("AT\r\n".encode())
time.sleep(1)
print('TEST CONNECT',ser.read(ser.inWaiting()).decode('"ISO-8859-1"'))

ser.write("AT+CMGF=1\r".encode())
time.sleep(1)
print("SET TEXTMODE", ser.read(ser.inWaiting()).decode('"ISO-8859-1"'))

ser.write('AT+CMGL="ALL"\r'.encode())
time.sleep(1)

print("SMSs", str(ser.read(ser.inWaiting()), "ISO-8859-1") )


time.sleep(1)

reply = ser.read(ser.inWaiting()) # Clean buf
print ("Listening for incomming SMS...")
while True:
    reply = ser.read(ser.inWaiting())
    if reply != "":
        # ser.write("AT+CMGR=2\r".encode())
        ser.write('AT+CMGL="ALL"\r'.encode())
        time.sleep(0.5)
        reply = ser.read(ser.inWaiting())
        # reply = ser.readline()
        print ("SMS received. Content:", reply.decode('"ISO-8859-1"'))
    time.sleep(1)
