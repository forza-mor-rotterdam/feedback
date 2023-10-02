
# Feedback
Voor het verwerken van Feedback van Meldingen Openbare Ruimte

## Tech Stack
[Turbo JS](https://turbo.hotwired.dev/), [SCSS](https://sass-lang.com/)

## Get Started 🚀
To get started, install [Docker](https://www.docker.com/)

### Start MOR core application
https://github.com/forza-mor-rotterdam/feedback

### Create local dns entry
Add '127.0.0.1  feedback.mor.local' to your hosts file

### create docker networks
~~~bash
    docker network create feedback_network
    docker network create mor_bridge_network
~~~

### Build and run Docker container
~~~bash
    docker compose build

    docker compose up
~~~

This will start a webserver.

In terminal go to 'app/frontend' and start front-end and watcher by typing

~~~
    npm run watch
~~~


Authorize via the Django admin: http://feedback.mor.local:8003/admin/
You can view the website on http://feedback.mor.local:8003.
