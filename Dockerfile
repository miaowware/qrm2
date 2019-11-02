FROM python:3-alpine

COPY . /app
WORKDIR /app

VOLUME /app/data

RUN \
    echo "**** install build packages ****" && \
    apk add --no-cache --virtual=build-dependencies \
        g++ \
        git \
        gcc \
        libxml2-dev \
        libxslt-dev \
        openssl-dev \
        python3-dev && \
    echo "**** install runtime packages ****" && \
    apk add --no-cache \
        openssl \
        py3-lxml \
        py3-pip \
        python3 && \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    apk del --purge \
        build-dependencies && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/apk/* && \
    echo "**** prepare scripts ****" && \
    chmod +x docker-run.sh

CMD ["sh", "docker-run.sh", "--pass-errors"]
