var Modem = require('./gsm.js');


function onSMS (sms) {
    console.log('onSMS', sms);
}
function onUSSD (ussd) {
    console.log('onUSSD', ussd);
}
function onStatusReport (report) {
    console.log('onStatusReport', report);
}
function onDisconnect (modem) {
    console.log('onDisconnect');
}


var modem1 = new Modem({
    port : 'COM26',
    // notify_port : '/dev/ttyUSB1',
    onDisconnect : onDisconnect,
    balance_ussd : '*101#',
    dollar_regexp : /(-?\d+)\s*rub/,
    cents_regexp : /(-?\d+)\s*kop/,
    debug : false
});
modem1.on('message', onStatusReport);
modem1.on('report', onStatusReport);
modem1.on('USSD', onUSSD);

modem1.connect(function () {

    modem1.getAllSMS(function (err, sms) {
        console.log('SMSes:', sms);
    });

    // modem1.getUSSD('*101#',(err, balance_money) => {
    //   console.log('Balance:', balance_money);
    // });

    modem1.getMessagesFromStorage('"ALL"', (er, allms) => {
      console.log(allms);
    })

    modem1.customATCommand('AT\r', (err, data) => {
      if (err) {
        console.log(err);
      }
      console.log(data);
    })

    // modem1.sendSMS({
    //     receiver : '1414',
    //     text : 'TTTB',
    //     request_status : true
    // }, function (err, data) {
    //     if (err) {
    //       console.log(err);
    //     }
    //     console.log('sendSMS', data);
    // });

    // modem1.deleteAllSMS (function(err){
    //     if (err === undefined) {
    //         console.log ('all messages were deleted');
    //     } else {
    //         console.log ('messages were not deleted');
    //     }
    // });

});
