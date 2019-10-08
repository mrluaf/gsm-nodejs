const gsm = require('gsm');
var serialport = require('serialport');
// var SerialPort = serialport.SerialPort;

serialport.list(function (err, ports) {
  ports.forEach(function(p) {
    console.log(p.comName, '|', p.pnpId, '|', p.manufacturer);
  });
});


var port = new serialport("COM7", {
     baudRate: 9600,
     dataBits: 8,
     parity: 'none',
     stopBits: 1,
     flowControl: false
});

port.on("open", onOpen);
port.on('error', onError);
port.on('data', onDataReceived);

// console.log(port);

function onOpen(error) {
    if(!error){
        console.log('Port open sucessfully');
        if(port.isOpen){
            send(port, "0839543774", "TEST798789");
            read(port);
        }
    }
}

function onDataReceived(data){
    console.log("Received data: " + data);
}

function onError(error){
    console.log(error);
}

function onClose(error){
    console.log('Closing connection');
    console.log(error);
}

function send(serial, toAddress, message) {
    serial.write("AT+CMGF=1");
    serial.write('\r');
    serial.write("AT+CMGS=\"" + toAddress + "\"");
    serial.write('\r');
    serial.write(message);
    serial.write('\r');
}

function read(serial){
    console.log('READ MSG');
    serial.write("AT+CMGF=1");
    serial.write('\r');
    serial.write("AT+CPMS=\"SM\"");
    serial.write('\r');
    serial.write("AT+CMGL=\"ALL\"");
    serial.write('\r');
}
