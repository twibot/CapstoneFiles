var express = require('express');
var router = express.Router();
var db=require('../database');

router.get('/count', function(req, res, next) {
    var sql='SELECT COUNT(*) AS count FROM sensor WHERE Sensor_State = "A"';
	let count
    db.query(sql, function (err, data) {
    if (err) throw err;
    count = data[0].count;
	res.render('count', {count: count, error: false});
  });
});
module.exports = router;