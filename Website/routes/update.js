var express = require('express');
var router = express.Router();
var db=require('../database');

/* router.use((req, res, next)=>{

    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Header", "Origin, X-Requested-With, Content-Type, Accept");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS");
    console.log("Headers applied");
    next();
}); */


router.get('/update', function(req, res, next){
	
	var id = req.psid;
	console.log("id: "+ id);

	var sql3='UPDATE sensor SET Sensor_State = "R" WHERE Sensor_ID = '+ id;
	db.query(sql3, function (err, data) {
		if (err) throw err;
	});
	next();
});

module.exports = router;
