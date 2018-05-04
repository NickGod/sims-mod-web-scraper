// Retrieve
var MongoClient = require('mongodb').MongoClient;
const user_name = 'sims_dev';
const password = 'youcannothackdeaper';

// creator map reduce
var mapFunction1 = function() {
          var key = this.artist;
          var keywords_with_stat = {};
          var d_stat = this.downloads;
          var v_stat = this.views;
          var title = this.title;

      if (key === null || key === undefined)
        return;
          if (this.keywords !== null && this.keywords !== undefined && Object.keys(this.keywords).length > 0) {
            Object.keys(this.keywords).forEach(function(k) {
              keywords_with_stat[k] = {
                  downloads: d_stat,
                  views: v_stat,
                  mods: [title]
              };
            });
          }

          var value = {
                url: this.artist_url,
                views: this.views,
                downloads: this.downloads,
                keywords: keywords_with_stat,
                mods: [this.title]
           }
            emit(key, value);
        };

var reduceFunction1 = function(key, values) {
          var reducedObject = {
            artist_url: "",
            views: 0,
            downloads: 0,
            keywords: {},
            mods: []
          };

          values.forEach(function(value) {
            reducedObject.views += value.views;
            reducedObject.downloads += value.downloads;
            reducedObject.mods = reducedObject.mods.concat(value.mods);
            if (reducedObject.artist_url === "" && value.url !== undefined)
                reducedObject.artist_url = value.url;

            if (Object.keys(reducedObject.keywords).length === 0) {
              reducedObject.keywords = value.keywords;
            } else {
              Object.keys(value.keywords).forEach(function(keyword) {
                if (keyword in reducedObject.keywords) {
                  reducedObject.keywords[keyword].downloads += value.keywords[keyword].downloads;
                  reducedObject.keywords[keyword].views += value.keywords[keyword].views;
                  if (reducedObject.keywords[keyword].mods !== undefined)
                    reducedObject.keywords[keyword].mods = reducedObject.keywords[keyword].mods.concat(value.keywords[keyword].mods);
                  else
                    reducedObject.keywords[keyword].mods = value.keywords[keyword].mods;
                } else {
                  reducedObject.keywords[keyword] = value.keywords[keyword];
                }
              });
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
                         { out: "artists"}
                       );
    console.log("artists collection generated");
  })
});