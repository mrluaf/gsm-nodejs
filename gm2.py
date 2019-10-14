import serial
import time
from datetime import datetime
from threading import Thread, Lock
import re
import sqlite3


networkLabel = {
    "45204": {
        "name": "Vittel",
        "check_type": "ussd",
        "ussd": "*101#"
    },
    "45205": {
        "name": "Vietnamobile",
        "check_type": "unknown",
        "unknown": "un"
    },
    "45201": {
        "name": "Mobifone",
        "check_type": "ussd",
        "ussd": "*112#"
    },
    "45202": {
        "name": "Vinaphone",
        "check_type": "ussd",
        "ussd": "*110#"
    },
    "": {
        "name": "unknown",
        "check_type": "unknown",
        "unknown": "unknown"
    }
}

# Enable Serial Communication
ser = serial.Serial()
ser.port = "COM7"
ser.baudrate = 115200
ser.timeout = 1

def sendCommand(ser, ser_lock, cmd):
    try:
        ser_lock.acquire()
    except:
        time.sleep(.1)
        return {
            "status": False,
            "reason": "Không gửi được tín hiệu đến Modem"
        }
    else:
        ser.write(''.join([cmd,'\r']).encode())
        ser_lock.release()
        time.sleep(.15)
        return {
            "status": True,
            "msg": ''.join(['Sended: ',cmd])
        }

def checkModem(ser, ser_lock):
    # 1. Send Check SIM Command
    sendCommand(ser, ser_lock, 'AT+CPIN?')
    # 2. Check network
    sendCommand(ser, ser_lock, 'AT+COPS?')
    sendCommand(ser, ser_lock, 'AT+CCID')
    sendCommand(ser, ser_lock, 'AT+CIMI')



def parseCommand(command, conn, c):
    parsedCommnad = {
        "event": []
    }

    if '+CPIN: READY' in command:
        parsedCommnad["event"].append('ready')
        parsedCommnad['ready'] = True
        c.execute('SELECT * FROM COMS WHERE name=?', (ser.port,))
        if c.fetchone() == None:
            isReady_Time = datetime.timestamp(datetime.now())
            c.execute("INSERT INTO COMS (name, isReady, isReady_Time) VALUES (?, ?, ?)",
                (ser.port, True, isReady_Time)
            )
            conn.commit()
        else:
            isReady_Time = datetime.timestamp(datetime.now())
            c.execute("UPDATE COMS SET isReady = ?, isReady_Time =? WHERE name = ?",
                (True, isReady_Time, ser.port)
            )
            conn.commit()




    if '+COPS:' in command:
        regex = r"\+COPS: (\d*),(\d*),(\d*)"
        try:
            match = re.search(regex, command)
            networkId = match.group(len(match.groups()))
        except:
            networkId = ''
        else:
            parsedCommnad["event"].append('sim_info')
            parsedCommnad['sim_info'] = networkLabel[networkId]


    if '\x81\xff\x81\xff\x81\xff' == command:
        parsedCommnad["event"].append('sim_out')

    if '+STIN: 0' in command:
        parsedCommnad["event"].append('sim_changed')

    return parsedCommnad




def doRead(ser, lock):
    conn = sqlite3.connect('modem.db')
    c = conn.cursor()
    while True:
        lock.acquire()
        try:
            rcv1 = ser.read(ser.inWaiting())
            rcv = rcv1.decode("ISO-8859-1")
        except:
            pass
        else:
            if rcv != '':
                # print('<',rcv)
                print(rcv1)
                parResult = parseCommand(rcv, conn, c)
                print(parResult,'\n')

        lock.release()
        time.sleep(.15)

ser.open()
ser_lock = Lock()

th = Thread(target=doRead, args=(ser, ser_lock))
th.daemon = True
th.start()

checkModem(ser, ser_lock)



while True:
    try:
        cmd = input()
    except:
        pass
    else:
        if 'exit' in cmd:
            break
        else:
            ser_lock.acquire()
            ser.write(''.join([cmd,'\r']).encode())
            ser_lock.release()
            time.sleep(.15)
