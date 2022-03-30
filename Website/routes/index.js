var express = require('express');
var router = express.Router();
var db=require('../database');

router.get('/update', function(req, res, next){
	
	var id = req.query.psid;
	console.log("id: "+ id);

	var sql3='UPDATE sensor SET Sensor_State = "R" WHERE Sensor_ID = '+ id;
	console.log(sql3);
	db.query(sql3, function (err, data) {
		if (err) throw err;
	});
	next();
});

router.get('/index', function(req, res, next) {
    var sql='SELECT COUNT(*) AS count FROM sensor WHERE Sensor_State = "A"';
	var sql2='SELECT * FROM sensor';
	let count
    db.query(sql, function (err, data) {
		db.query(sql2, function (err,data2, fields){
			if (err) throw err;
			count = data[0].count;
			res.render('index', {count: count, lots: data2, error: false});	
		});
	});
});

module.exports = router;