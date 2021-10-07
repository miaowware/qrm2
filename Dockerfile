FROM voidlinux/voidlinux

COPY . /app
WORKDIR /app

ENV PYTHON_BIN python3

RUN \
    echo "**** update packages ****" && \
    xbps-install -Suy && \
    echo "**** install system packages ****" && \
    export runtime_deps='cairo libjpeg-turbo' && \
    export runtime_pkgs="${runtime_deps} python3-pip python3" && \
    xbps-install -y $runtime_pkgs && \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/cache/xbps/*

ARG UID
ENV UID=${UID:-1000}
ARG GID
ENV GID=${GID:-1000}
USER $UID:$GID

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]
