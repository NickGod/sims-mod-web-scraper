// Retrieve
var MongoClient = require('mongodb').MongoClient;
const user_name = 'sims_dev';
const password = 'youcannothackdeaper';


// Connect to the db
MongoClient.connect("mongodb://localhost:27017/sims_test_db", function(err, db) {
  if(!err) {
    console.log("We are connected");
  }
  db.authenticate(user_name, password, function(err, result) {
    // perform artis mapred
    db.sims_new.aggregate([{
            $group: {
                    _id: "$url",
                    'title': { $first: '$title' },
                    'artist': { $max: '$artist' },
                    'artist_url': { $max: '$artist_url' },
                    'category': { $first: '$category' },
                    'game_version': { $max: '$game_version' },
                    'publish_date': { $first: '$publish_date' },
                    'preview_image': { $first: '$preview_image' },
                    'pack_requirement': { $first: '$pack_requirement' },
                    'comments_cnt': { $max: '$comments_cnt' },
                    'views': { $max: '$views' },
                    'thanks': { $max: '$thanks' },
                    'favourited': { $max: '$favourited' },
                    'downloads': { $max: '$downloads' },
                    'comments': { $first: '$comments' },
                    'description': { $last: '$description' },
                    'keywords': { $max: '$keywords' },
                    'url': { $first: '$url' },
                    'tags': { $max: '$tags' },
                    'types': { $max: '$types' },
                    'files': { $max: '$files' },
                    'time_series_data': { $addToSet: "$time_series_data" }
            }},
            { "$addFields": {
                    "time_series_data": {
                      "$reduce": {
                        "input": "$time_series_data",
                        "initialValue": [],
                        "in": { "$setUnion": [ "$$value", "$$this" ] }
                      }
                    }
            }}, {$out : "sims_records_test1"}]);
    console.log("records aggregated");
  })
});