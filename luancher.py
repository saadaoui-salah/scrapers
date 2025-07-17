import schedule
import time
import subprocess

def job():
    SPIDER_NAME = "suruga-ya"
    PROJECT_DIR = "./"
    subprocess.run(
        ["scrapy", "crawl", SPIDER_NAME],
        cwd=PROJECT_DIR
    )
    print("Running job...")


schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)