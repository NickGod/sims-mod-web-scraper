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
MongoClient.connect("mongodb://sims_dev:youcannothackdreaper@localhost:27017/sims_test_db", function(err, client) {
  if(!err) {
    console.log("We are connected");
  } else {
    console.log(err)
  }

  const db = client.db('sims_test_db');

  // perform keywords mapred
  db.collection('sims_records_test').mapReduce(
                       mapFunction1,
                       reduceFunction1,
                       { out: "keyword_mapred_date"}
                     );
  client.close();
  console.log("keyword collection generated");
});