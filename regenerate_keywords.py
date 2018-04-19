from pymongo import MongoClient


from keyword_generation import generate_ngram_keywords_for_doc;

# connect to db
client = MongoClient('localhost',
                      username='sims_dev',
                      password='youcannothackdreaper',
                      authSource='sims_test_db',
                      authMechanism='SCRAM-SHA-1');

db = client.sims_test_db;
collection = db.sims_records_test;
item_count = 0;


def regenerate_keyword_for_doc(document):
  if ('description' in document):
    new_keywords = generate_ngram_keywords_for_doc(document);
    document['keywords'] = new_keywords;

    collection.update_one({'_id': document['_id']}, {"$set": document}, upsert=True);


if __name__ == "__main__":
    cursor = collection.find({});
    for document in cursor:
      regenerate_keyword_for_doc(document);
      item_count += 1;
      print("************ %d items parsed ************" % (item_count));





