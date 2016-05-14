
import requests

import config


# Trigger Action ###################################################################################

# @TODO add shorthands for some of these examples
#
# # Trigger all tags/branchs for this automated build.
# $ curl -H "Content-Type: application/json" --data '{"build": true}' -X POST <URL>
#
# # Trigger by docker tag name
# $ curl -H "Content-Type: application/json" --data '{"docker_tag": "master"}' -X POST <URL>
#
# # Trigger by Source branch named staging
# $ curl -H "Content-Type: application/json" --data '{"source_type": "Branch", "source_name": "staging"}' -X POST <URL>
#
# # Trigger by Source tag named v1.1
# $ curl -H "Content-Type: application/json" --data '{"source_type": "Tag", "source_name": "v1.1"}' -X POST <URL>


# http://docs.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests
def trigger(payload):
    baseUrl = 'https://registry.hub.docker.com/u/{}/{}/trigger/{}/'
    url     = baseUrl.format(config.userName,
                             config.repoName,
                             config.triggerToken)

    print('trigger.trigger(): triggering url={} , json={}'.format(url, payload))
    requests.post(url, json=payload)

# trigger building <tag>
def triggerTag(tag):
    if tag == None:
        print("trigger.triggerTag(): tag == None. Not triggering anything")
        return
    else:
        trigger({'docker_tag': tag})

