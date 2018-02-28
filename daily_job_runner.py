import schedule
import time
import modthesims_scraper
from datetime import datetime, timedelta

def job():
  print('Running daily job...');
  modthesims_scraper.start_scraping();

if __name__ == "__main__":
  print('Starting at: %s' % str(datetime.now()));
  schedule.every().day.at("10:00").do(job);
  while(True):
    schedule.run_pending();
    time.sleep(600);
