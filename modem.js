var Modem = require('gsm-modem');
// USB\VID_19D2&PID_0108&MI_01\6&2A58F534&0&0001
var modem1 = new Modem({
    ports : ['COM7']
});
modem1.connect(function (err) {
    if (err) {
        console.error('Error connecting modem: ', err);
        return;
    }
    // Start giving commands here...
})
