var http = require('http');
var https = require('https');

http.globalAgent.maxSockets = 50;
https.globalAgent.maxSockets = 50;

var request = require('request');
const async = require('async');

function makeid(length) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

var cvs = []
var count = 0
async.eachLimit([...Array(100000)], 100, (item, next) => {
  count += 1
  var link = 'https://www.topcv.vn/xem-cv/'+makeid(32)
  console.log(count, link);
  request({
      url: link,
  }, (error, response, body) => {
      if (!error && response.statusCode == 200) {
          console.log(body);
          cvs.append(body)
          console.log(cvs.length);
          next()
      } else {
        console.log(response.statusCode);
        next()
      }
  });
}, err => {
  console.log('DONE');
  console.log(cvs);
  console.log(cvs.length);
})
// console.log(makeid(32));
