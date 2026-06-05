const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const axios = require('axios');
const ServiceLog = require('./models/ServiceLog');
const serviceRoutes = require('./routes/services');

dotenv.config(); // loads your .env file
const app = express();

app.use(cors());        // allows React frontend to call this backend
app.use(express.json()); // allows server to read JSON request bodies

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.log('MongoDB error:', err));

// Use service routes
app.use('/api/services', serviceRoutes);

// List of services to monitor
const services = [
  { name: 'Google', url: 'https://www.google.com' },
  { name: 'GitHub', url: 'https://www.github.com' },
  { name: 'JSONPlaceholder', url: 'https://jsonplaceholder.typicode.com' },
  { name: 'NASA API', url: 'https://api.nasa.gov' },
  { name: 'Fake Server 1', url: 'https://this-does-not-exist-123abc.com' },
  { name: 'Fake Server 2', url: 'https://dead-service-xyz987.io' },
];

// Poll every 30 seconds and save result to MongoDB
async function pollServices() {
  for (const service of services) {
    const start = Date.now();
    try {
      await axios.get(service.url, { timeout: 5000 });
      const responseTime = Date.now() - start;
      await ServiceLog.create({ name: service.name, url: service.url, status: 'UP', responseTime });
      console.log(`${service.name}: UP (${responseTime}ms)`);
    } catch (err) {
      await ServiceLog.create({ name: service.name, url: service.url, status: 'DOWN', responseTime: 0 });
      console.log(`${service.name}: DOWN`);
    }
  }
}

// Run once immediately, then every 30 seconds
pollServices();
setInterval(pollServices, 30000);

app.listen(process.env.PORT, () => {
  console.log(`Server running on port ${process.env.PORT}`);
});
