var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
  keyPath: 'certs/5be93a5826-private.pem.key',
  certPath: 'certs/5be93a5826-certificate.pem.crt',
  caPath: 'certs/AmazonRootCA1.pem',
  host: "a3f23zc7he5tzr-ats.iot.ap-southeast-1.amazonaws.com",
  port: 8883,
  clientId: "raspi-water-pump",
  region: 'ap-southeast-1'
});

//
// Device is an instance returned by mqtt.Client(), see mqtt.js for full
// documentation.
//
device.on('connect', function() {
  console.log('connect');
  device.subscribe('raspi-water-pump/data');
});

module.exports.device = device