# Dreaper Mod The Sims Web Scraper
Project for CMU-ETC-SV 18S

## Getting Started with Scraper

### Prerequisites
  python3 and dependency packages
  run `chmod 755 install_dep.sh && ./install_dep.sh` to install dependency for the scraper.

  Notice that nltk package will require you to download their wordnet model. nltk package is used to get rid of plurals in the keywords.

  simply enter `nltk.download('wordnet')` in your python3 prompt line to complete download.

  To be able to run scraper successfully, you need to have a mongodb instance running on host 27017.

### Directory and Files
  - `daily_job_runner.py`
    This script runs the scraper and needed db oeprations daily

  - `modthesims_scraper.py`
    This script scrapes data from modthesims, and uses keyword generation script to generate keywords.

  - `keyword_generation.py`
    This script is a module for keyword generation.

  - `stop_words`
    A list of words that should be ignored during keyword generation

  - `regenrate_keywords.py`
    This script regenerates keyword on existing collection. By default, it regenerates keyword on collection `sims_records_test`

  - `./db_operations/`
    db related scripts included here
      - `artist_mapred.js`
        a mongodb js script that performs map reduce to generate `artists` collection
      - `collection_aggregation.js`
        a mongodb js script that aggregates duplicate records from `sims_new` collection to `sims_records_test` collection
      - `keyword_mapred.js`
        a mongodb js script that performs map reduce to generate `keyword_mapred_date` collection.
      - `db_op.sh`
        shellscript that runs above three scripts with mongoshell

### Logging
  `modthesims_scraper.py` does generate log for every run. The logs should be helpful to track what went wrong when the scraper was running. By default, `modthesims_scraper.py` will print how many mods it has scraped as it traverses every page in the specified category. The detailed log will be persisted to the log starting with the running timestamp.


### How to run the whole tool?

Note that the scraper assumes a mongodb instance runs on the same host. To run the scraper once, simply run `python3 modthesims_scraper.py`.

To run the scraper daily, you can use a tool called pm2. pm2 can be obtained via command `npm install -g pm2`. You can use pm2 to run `daily_job_runner.py` as a background process. To be able to do this, simply run `pm2 start daily_job_runner.py --interpreter=python3`.

Normally, you will not need to use `regenerate_keywords.py`, but if you do, simply run `python3 regenerate_keywords.py`, which will repopulate keywords for each mod in the designated collection.

