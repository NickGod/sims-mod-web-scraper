import schedule
import time
import modthesims_scraper

def job():
  print('Running daily job...');
  modthesims_scraper.start_scraping();

if __name__ == "__main__":
  print('Starting...');
  # schedule.every(1).minutes.do(job)
  schedule.every().day.at("08:00").do(job);

  while(True):
    schedule.run_pending();
    time.sleep(600);