const mongoose = require('mongoose');

const ServiceLogSchema = new mongoose.Schema({
  name: String,          // name of the service e.g. "Google"
  url: String,           // URL being monitored
  status: String,        // "UP" or "DOWN"
  responseTime: Number,  // how long it took to respond in ms
  checkedAt: {
    type: Date,
    default: Date.now    // automatically saves the time of each check
  }
});

module.exports = mongoose.model('ServiceLog', ServiceLogSchema);
