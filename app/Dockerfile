# Node.js build stage
FROM node:16 as node_step

WORKDIR /srv/web/
COPY ./frontend /srv/web/
RUN cd /srv/web \
 && npm install \
 && npm run build

# Python application stage
FROM python:3.10.10-slim-bullseye

EXPOSE 8000

ENV APP_HOME=/app
ENV APP_USER=appuser
ENV APP_USER_ID=2000

# Create a non-root user
RUN groupadd -r $APP_USER && \
    useradd -r -u $APP_USER_ID -g $APP_USER -d $APP_HOME -s /sbin/nologin -c "Docker image user" $APP_USER

# Set environment variables and install system dependencies
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        python-dev \
        curl \
        libgeos-c1v5 \
        gdal-bin \
        postgresql-client \
        libgdal28 \
        libspatialite7 \
        libfreexl1 \
        libgeotiff-dev \
        libwebp6 \
        proj-bin \
        graphviz \
        graphviz-dev \
        git \
        locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Generate locales
RUN sed -i '/nl_NL.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && update-ca-certificates

ENV LANG=nl_NL.UTF-8 \
    LANGUAGE=nl_NL \
    LC_ALL=nl_NL.UTF-8

# Copy and install Python dependencies first
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the application code
COPY . /app/

# Copy static files from the Node.js build stage
COPY --from=node_step /srv/web/public/build /static/
RUN chown -R $APP_USER:$APP_USER /static \
    && chmod -R u+w /static
# Create directories and set permissions
RUN mkdir -p /media \
    && mkdir -p /static \
    && chown -R $APP_USER:$APP_USER /media \
    && chown -R $APP_USER:$APP_USER /static \
    && chmod -R 744 /media \
    && chmod -R 744 /static \
    && mkdir -p /srv/web/var/cache \
    && chown $APP_USER:$APP_USER /srv/web/var/cache \
    && chmod -R ugo+rwx /srv/web/var/cache \
    && chown -R $APP_USER:$APP_USER $APP_HOME

# Set execute permissions for entrypoint and scripts
RUN chmod -R +x /app/deploy

# Switch to the non-root user
USER $APP_USER

ARG GIT_SHA
ENV GIT_SHA=$GIT_SHA
ARG DEPLOY_DATE
ENV DEPLOY_DATE=$DEPLOY_DATE

CMD ["bash", "/app/deploy/docker-entrypoint.sh"]
