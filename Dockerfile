FROM ghcr.io/void-linux/void-glibc-full

COPY . /app
WORKDIR /app

ARG REPOSITORY=https://repo-fastly.voidlinux.org/current
ARG PKGS="cairo libjpeg-turbo libgcc"
ARG UID 1000
ARG GID 1000

RUN \
    echo "**** update system ****" && \
    xbps-install -Suy xbps -R ${REPOSITORY} && \
    xbps-install -uy -R ${REPOSITORY} && \
    echo "**** install system packages ****" && \
    xbps-install -y -R ${REPOSITORY} ${PKGS} python3 && \
    echo "**** install pip packages ****" && \
    python3 -m venv botenv && \
    botenv/bin/pip install -U pip setuptools wheel && \
    botenv/bin/pip install --ignore-requires-python -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/xbps/*

ENV PYTHONUNBUFFERED=1

USER $UID:$GID

CMD ["/bin/sh", "run.sh", "--pass-errors"]
