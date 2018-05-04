# Dreaper Mod The Sims Web Scraper
Project for CMU-ETC-SV 18S

## Getting Started with Scraper

### Prerequisites
  python3 and dependency packages.
  run `chmod 755 install_dep.sh && ./install_dep.sh` to install dependency

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


### Frontend Directory and Files
  - `./SimsReact`
    Frontend app folder
    - `/package.json`
      records npm dependency package info
    - `/webpack.config.js`
      configuration file for the webpack server
    - `/js/components/`
      this folder stores components used across different pages
    - `/js/pages/`
      this folder stores code to render the dashboard
    - `/styles/`
      stores css style

### How to update pack release info?
  Pack release info is hardcoded in frontend. Specifically, you want to look at `./SimsReact/components/LineChartWithTimeRange.js`. If there is any pack release info you would like to change, please modify the records stored object labelInfoDay and labelFormatMonth.


## Getting Started with Backend
run ```npm install``` to install dependencies, and then run ```node index.js``` in ```dbServer```, node express server will be running at ```localhost:3000```

### Backend Directory and Files
  - `./dbServer`
    Backend API server folder
    - `/index.js`
    backend server code, with RESTful APIs
    - `/mongoose_db.js`
    mongoose schema file, used as ORM for MongoDB documents.

### Which database to use?
  Note that you have the option to use either a remote db or a local db. When connecting to mongodb with mongoose, simply change the url in mongoose_db.js.
