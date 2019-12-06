FROM alpine:3.10

COPY . /app
WORKDIR /app

ENV PYTHON_BIN python3

RUN \
    echo "**** install build packages ****" && \
    apk add --no-cache --virtual=build-dependencies \
        g++ \
        git \
        gcc \
        libxml2-dev \
        libxslt-dev \
        libressl-dev \
        python3-dev && \
    echo "**** install runtime packages ****" && \
    apk add --no-cache \
        libressl \
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
        /var/cache/apk/*

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]
