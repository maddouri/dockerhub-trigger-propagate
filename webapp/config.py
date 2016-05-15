
from os import getenv

# example configuration for https://hub.docker.com/r/maddouri/void-docker/

# docker hub user name
userName = 'maddouri'
# docker hub repository name
repoName = 'void-docker'

# build trigger token
# obtained from "Build Settings > Build Trigger"
# https://devcenter.heroku.com/articles/config-vars
# https://devcenter.heroku.com/articles/getting-started-with-python#define-config-vars
# environment variables can be set using:
# heroku config:set DOCKERHUB_TRIGGER_TOKEN='<docker hub trigger token>'
triggerToken = getenv('DOCKERHUB_TRIGGER_TOKEN', 'null')

# ordered sequence of tags to be built
tagSequence = [
    'init',
    'step-1',
    'step-2',
    'step-3',
    'latest'
]

# build trigger configuration
#
# https://apscheduler.readthedocs.org/en/v3.0.5/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler.scheduled_job
# The "trigger" argument can either be:
# 1. the alias name of the trigger, (e.g. 'date', 'interval' or 'cron')
#    in which case any extra keyword arguments to this method are passed
#    on to the trigger's constructor
# 2. an instance of a trigger class
#
# https://apscheduler.readthedocs.org/en/v3.0.5/modules/triggers/cron.html?highlight=day_of_week#apscheduler.triggers.cron.CronTrigger
# day_of_week (int|str) - number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
#
# more examples can be found in schedule.py
#
# the following example configures a daily trigger at a fixed time
triggerScheduling = {
    'trigger'     : 'cron',
    'day_of_week' : '0-6',
    'hour'        : 0,
    'minute'      : 0
}

# path to the build propagation web app handler
#
# this is the argument to Flask's `app.route()` http://flask.pocoo.org/docs/0.10/api/#url-route-registrations
#
# e.g. if the web app is registered at https://glacial-meadow-43653.herokuapp.com/
#      and you set the route to '/propagate' and the port to 80
#      then you can register the following url in https://docs.docker.com/docker-hub/webhooks/
#      https://glacial-meadow-43653.herokuapp.com/propagate
propagationRoute = '/propagate'
# port for the build propagation web app handler
propagationPort  = 80
# port to use when not running in localhost, @see propagate.py
propagationPort_dev = 5000

# delay (in seconds) before triggering the next build
# avoids "Ignored, build throttle" error in docker hub
propagationDelay = 100  # 120sec seems to be Ok
