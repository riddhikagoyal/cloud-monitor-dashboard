const express = require('express');
const router = express.Router();
const ServiceLog = require('../models/ServiceLog');

// GET /api/services/latest — returns latest status of each service
router.get('/latest', async (req, res) => {
  try {
    const services = await ServiceLog.aggregate([
      { $sort: { checkedAt: -1 } },
      { $group: { _id: "$name", latest: { $first: "$$ROOT" } } }
    ]);
    res.json(services);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/services/history/:name — returns last 20 logs for a specific service
router.get('/history/:name', async (req, res) => {
  try {
    const logs = await ServiceLog.find({ name: req.params.name })
      .sort({ checkedAt: -1 })
      .limit(20);
    res.json(logs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
