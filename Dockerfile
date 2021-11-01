FROM ghcr.io/void-linux/void-linux:latest-mini-x86_64
LABEL org.opencontainers.image.source https://github.com/miaowware/qrm2

COPY . /app
WORKDIR /app

ARG REPOSITORY=https://repo-us.voidlinux.org/current
ARG PKGS="cairo libjpeg-turbo"
ARG UID 1000
ARG GID 1000

RUN \
    echo "**** update system ****" && \
    xbps-install -SuyM -R ${REPOSITORY} && \
    echo "**** install system packages ****" && \
    xbps-install -yM -R ${REPOSITORY} ${PKGS} python3 python3-pip && \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/xbps/*

ENV PYTHON_BIN python3
ENV PYTHONUNBUFFERED 1
ENV UID ${UID:-1000}
ENV GID ${GID:-1000}

USER $UID:$GID

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]
