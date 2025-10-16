# run_bot.py

import schedule
import time
import datetime

from bot.scanner import perform_scan
from bot.database import create_db_and_tables

def scheduled_job():
    print(f"Triggering scheduled job at {datetime.datetime.now()}...")
    perform_scan()

if __name__ == "__main__":
    # 1. Create the database and tables if they don't exist
    print("Initializing database...")
    create_db_and_tables()
    print("Database is ready.")

    # 2. Define the schedule
    # schedule.every().day.at("09:00").do(scheduled_job)
    # For testing, let's run it every 1 minute
    schedule.every(1).minutes.do(scheduled_job)

    # 3. Run the scan once immediately on startup
    print("Performing initial scan on startup...")
    perform_scan()

    # 4. Start the scheduler loop
    print("Scheduler started. Bot will run on the defined schedule.")
    print("Press Ctrl+C to stop the bot.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
