# Feedback
Voor het verwerken van Feedback van MOR na het klikken van een duimpje in een MeldR email. Geeft metrics door aan Grafana.

## Tech Stack

[Django](https://www.djangoproject.com/start/), [Turbo JS](https://turbo.hotwired.dev/), [SCSS](https://sass-lang.com/)

## Get Started 🚀

To get started, install [Docker](https://www.docker.com/)

#### We use the Makefile for commonly used commands

### Start MOR core application

https://github.com/forza-mor-rotterdam/mor-core

### Create local dns entry

Add '127.0.0.1 feedback.mor.local' to your hosts file

### create docker networks

Use the Makefile command:

```bash
    make create_docker_networks
```

or:

```bash
    docker network create feedback_network
    docker network create mor_bridge_network
```

### Build and run Docker container

Use the Makefile command:

```bash
    make run_and_build
```

or:

```bash
    docker compose build
    docker compose up
```

To only run the docker container use:

```bash
    make run
```

This will start a webserver.
Authorize via the Django admin: http://feedback.mor.local:8010/admin/
You can login with the following credentials:

- Email: admin@admin.com
- Password: insecure
  You can view the website on http://feedback.mor.local:8010

### Frontend

Use the Makefile command:

```bash
    make run_frontend
```

or in terminal go to 'app/frontend' and start front-end and watcher by typing

```bash
    npm install
    npm run watch
```

### Code style

Pre-commit is used for formatting and linting
Make sure pre-commit is installed on your system

```bash
    brew install pre-commit
```

and run

```bash
    pre-commit install
```

To manually run the pre-commit formatting run

```bash
    make format
```

Pre-commit currently runs black, flake8, autoflake, isort and some pre-commit hooks. Also runs prettier for the frontend.
