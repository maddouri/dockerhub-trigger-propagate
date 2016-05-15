
This is a webapp for driving [Automated Builds](https://docs.docker.com/docker-hub/builds/)
on [Docker Hub](https://hub.docker.com).

It is used to trigger building different tags in a specific order. This is useful when building
a complex image that requires multiple build steps. (e.g. bypassing Docker Hub's [build time
restrictions](https://stackoverflow.com/a/34588866/865719) in [this Stack Overflow question](https://stackoverflow.com/q/36948145/865719))

The current implementation allows driving the build within the same repository.
It is configured to be hosted on [Heroku](https://www.heroku.com/) but can be adapted to run
on other hosts.

The app is composed of 2 processes:

1. [`schedule.py`](./webapp/schedule.py) triggers building the first tag according to the scheduling
   specified in [`config.triggerScheduling`](./webapp/config.py)
2. [`propagate.py`](./webapp/propagate.py) is a webhook (called by Docker Hub) that triggers building subsequent
   tags in the order specified in [`config.tagSequence`](./webapp/config.py)

[Honcho](https://github.com/nickstenning/honcho) is used in order to run both processes on
a single, free [Dyno](https://devcenter.heroku.com/articles/dynos).
(see [Procfile](./Procfile) and [Procfile.honcho](./Procfile.honcho))

## Prerequisites

In order to use this app, you will need a [Docker Hub](https://hub.docker.com) account for the
automated build and a [Heroku](https://www.heroku.com/) account to host and run the app.
Both can be obtained for **free**.

Finally, `git` and [`heroku toolbelt`](https://toolbelt.heroku.com/) are required.
(`docker` is optional, but you probably have it already :) )

## Usage

1. In the terminal
    1. Clone/download this repository

        ```sh
        git clone https://github.com/maddouri/dockerhub-trigger-propagate.git
        wget -qO- https://github.com/maddouri/dockerhub-trigger-propagate/archive/master.tar.gz | tar xvz
        ```
    1. Initialize a new Heroku app

        ```sh
        cd dockerhub-trigger-propagate
        heroku login
        heroku create
        ```
    1. Edit the [`webapp/config.py`](./webapp/config.py) file
    1. Get the base URL of the Heroku app

        ```sh
        $ heroku info
        === my-app-name-1234
        ...
        Web URL:       https://my-app-name-1234.herokuapp.com/
        ```
1. Go to [Docker Hub](https://hub.docker.com)
    1. Create an [Automated Build](https://docs.docker.com/docker-hub/builds/)
    1. In the new Docker Hub repo, go to the **Build Settings** page
    1. Under **Build Settings**, disable the
       _"When active, builds will happen automatically on pushes."_ option
    1. Fill in the **build rules** below the **Build Settings**
    1. Under **Build Triggers**, enable triggers and copy the **Trigger Token**
    1. Go to the repo's **Webhooks** page
    1. Add the Heroku app's URL as a webhook. e.g. if you have set `propagationRoute` to `'/propagate'`
    in [`webapp/config.py`](./webapp/config.py), then webhook URL is:

        ```
        https://my-app-name-1234.herokuapp.com/propagate
        ```
1. In the terminal
    1. Add the **Trigger Token** as an environment variable in Heroku

        ```sh
        heroku config:set DOCKERHUB_TRIGGER_TOKEN='<docker hub trigger token>'
        ```
    1. Push the app to Heroku

        ```sh
        git add .
        git commit -m 'Initial deployment'  # if this fails, remember to use 'git config user.name' and 'git config user.email'
        git push heroku master
        ```
1. Done. You can now monitor the app by looking at the logs

    ```sh
    heroku logs -t
    ```
