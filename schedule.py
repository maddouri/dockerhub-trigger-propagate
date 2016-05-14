
# Procfile
#   clock: python3 schedule.py

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import os

import config
import trigger


# https://stackoverflow.com/a/17551794/865719
logging.basicConfig()

# https://devcenter.heroku.com/articles/clock-processes-python
sched = BlockingScheduler()


"""
# https://apscheduler.readthedocs.org/en/v3.0.5/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler.scheduled_job
# The trigger argument can either be:
# 1. the alias name of the trigger, (e.g. 'date', 'interval' or 'cron')
#    in which case any extra keyword arguments to this method are passed
#    on to the trigger's constructor
# 2. an instance of a trigger class
@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every 1 minute.')
    trigger.triggerTag(config.tagSequence[0])
#"""

"""
# https://apscheduler.readthedocs.org/en/v3.0.5/modules/triggers/cron.html?highlight=day_of_week#apscheduler.triggers.cron.CronTrigger
# day_of_week (int|str) - number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
@sched.scheduled_job('cron', day_of_week='0-6', hour=15, minute=36)
def scheduled_job():
    trigger.triggerTag(config.tagSequence[0])
#"""


# scheduled build trigger
@sched.scheduled_job(**config.triggerScheduling)
def scheduledBuildTrigger():
    trigger.triggerTag(config.tagSequence[0])


if __name__ == '__main__':
    sched.start()
