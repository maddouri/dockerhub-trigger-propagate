
# Procfile
#   web: gunicorn propagate:app --log-file -
#   web: gunicorn webapp.propagate:app --log-file -


from flask import Flask, request, jsonify
import os
import re
import sys
import threading
import time

from . import config
from . import trigger

# @TODO improve error handling/exceptions

# @TODO implement proper error handling for the web api
# http://blog.luisrei.com/articles/flaskrest.html#h5o-8
# set the resp.status to something indicating an error
# http://flask.pocoo.org/docs/0.10/patterns/apierrors/

# @TODO the callback url sent by the docker hub webhook

app = Flask(__name__)


# https://stackoverflow.com/a/35614301/865719
@app.route(config.propagationRoute, methods=['POST'])
def propagate():

    print('Reading request...')

    # read request
    errorMessage, callbackUrl, tag = readRequest(request)
    if errorMessage != None:
        return createErrorPayload(errorMessage)

    print('Validating request...')

    # validate request
    errorMessage = validateRequest(callbackUrl, tag)
    if errorMessage != None:
        return createErrorPayload(errorMessage)

    print('Docker Hub built tag [' + tag +  ']')

    # trigger the next build
    # launch an asynchronous task that waits before triggering the build
    # this avoids "Ignored, build throttle" in docker hub
    nextTag = getNextTag(tag)
    if nextTag != None:
        print('Queuing trigger for tag [{}]'.format(nextTag))
        threading.Thread(target=asyncTriggerTag, args=[nextTag, config.propagationDelay]).start()
    else:
        print('No more builds to trigger')

    # done
    return createSuccessPayload({
        'prev_tag': tag,
        'next_tag': nextTag if nextTag != None else 'null'
    })


def createErrorPayload(message):
    print('error message: {}'.format(message))
    return jsonify({
        'state'      : 'error',
        'description': str(message)
    })


def createSuccessPayload(message):
    return jsonify({
        'state'      : 'success',
        'description': str(message)
    })


def readRequest(req):
    try:
        content = req.json
        return None, content['callback_url'], content['push_data']['tag']
    except (ValueError, KeyError) as e:
        print(e)
        return e, None, None
    except:
        print(sys.exc_info()[0])
        return sys.exc_info()[0], None, None


def isValidCallback(callbackUrl):
    validRx = r'^https://registry\.hub\.docker\.com/u/' + config.userName + r'/' + config.repoName + r'/hook/[0-9A-Za-z]{1,128}/$'
    return re.match(validRx, callbackUrl) != None


def isValidTag(tag):
    return tag in config.tagSequence


def validateRequest(callbackUrl, tag):
    if not isValidCallback(callbackUrl):
        return 'Invalid callback URL'

    if not isValidTag(tag):
        return 'Wrong tag name. Expected one of {}, received [\'{}\']'.format(config.tagSequence, tag)


def getNextTag(tag):
    nextTagIndex = config.tagSequence.index(tag) + 1
    if nextTagIndex < len(config.tagSequence):
        return config.tagSequence[nextTagIndex]


def asyncTriggerTag(tag, delay_sec):
    # http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support#h5o-13
    with app.app_context():
        time.sleep(delay_sec)
        trigger.triggerTag(tag)


if __name__ == '__main__':
    # https://stackoverflow.com/a/19184024/865719
    # run `printenv` in `heroku run bash`
    # in Heroku
    if 'DYNO' in os.environ:
        app.run(host='0.0.0.0', port=config.propagationPort, debug=True)
    # at localhost
    else:
        app.run(port=config.propagationPort_dev, debug=True)
