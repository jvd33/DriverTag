__author__ = 'SWEN356 Team 4'

#!flask/bin/python
from app import app
import schedule
from threading import Thread
from app.daily_update import *

if __name__=="__main__":
    schedule.every().day.at("11:55").do(run_every_10_seconds)
    t = Thread(target=run_schedule)
    t.start()
    print("Started")
    app.run(port=5000, debug=True, use_reloader=False)