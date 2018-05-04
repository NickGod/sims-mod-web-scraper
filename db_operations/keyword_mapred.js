// Retrieve
var MongoClient = require('mongodb').MongoClient;
const user_name = 'sims_dev';
const password = 'youcannothackdeaper';

// emit keyword and its count
var mapFunction1 = function() {
            for (var key in this.keywords) {
             const object = {
              count: 1,
              startDate: Date.parse(this.publish_date)/1000,
              endDate: Date.parse(this.publish_date)/1000
             }
                       emit(key, object);           
            }
                   };

// reduce on count
var reduceFunction1 = function(keyword, values) {
              var reducedObject = {
                count: 0,
                startDate: "",
                endDate: ""
              }
              values.forEach( function(value) {
                reducedObject.count += value.count;
                timestamp = value.startDate;

                if (reducedObject.startDate === ""|| timestamp < reducedObject.startDate) {
                  reducedObject.startDate = timestamp;
                }
                if (reducedObject.endDate === "" || timestamp > reducedObject.endDate) {
                  reducedObject.endDate = timestamp;
                }
              });

                          return reducedObject;
                      };


// Connect to the db
MongoClient.connect("mongodb://localhost:27017/sims_test_db", function(err, db) {
  if(!err) {
    console.log("We are connected");
  }
  db.authenticate(user_name, password, function(err, result) {
    // perform artis mapred
    db.sims_records_test.mapReduce(
                         mapFunction1,
                         reduceFunction1,
                         { out: "keyword_mapred_date"}
                       );
    console.log("keyword collection generated");
  })
});