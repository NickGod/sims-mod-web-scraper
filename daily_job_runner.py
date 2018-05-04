import schedule
import time
import modthesims_scraper
import os

def job():
  print('Running daily job...');
  modthesims_scraper.start_scraping();
  os.system("cd db_operations && ./db_op.sh")

if __name__ == "__main__":
  print('Starting...');
  schedule.every().day.do(job);

  while(True):
    schedule.run_pending();
    time.sleep(600);