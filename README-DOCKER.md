# Docker help for qrm2

You have multiple ways to use docker to run an instance of qrm2.

- [Docker help for qrm2](#docker-help-for-qrm2)
  - [Using docker-compose and the prebuilt-image (recommended)](#using-docker-compose-and-the-prebuilt-image-recommended)
  - [Using docker-compose and building the image](#using-docker-compose-and-building-the-image)
  - [Using pure docker](#using-pure-docker)
    - [[Optional] Building the image](#optional-building-the-image)
    - [Creating the container](#creating-the-container)


## Using docker-compose and the prebuilt-image (recommended)

This is the easiest method for running the bot without any modifications.  
**Do not clone the repository when using this method!**

1. Create a new directory and `cd` into it.

2. Create the `docker-compose.yml` file:

    ```yaml
    version: '3'
    services:
      qrm2:
        image: "ghcr.io/miaowware/qrm2:latest"
        restart: on-failure
        volumes:
          - "./data:/app/data:rw"
    ```

3. Create a subdirectory named `data`.

4. Copy the templates for `options.py` and `keys.py` to `data/`, and edit them.

5. Run `docker-compose`:

    ```none
    $ docker-compose pull
    $ docker-compose up -d
    ```

    *Run without "-d" to test the bot (run in foreground).*



## Using docker-compose and building the image

This is the easiest method to run the bot with modifications.

1. `cd` into the repository.

2. Create the `docker-compose.yml` file:

    ```yaml
    version: '3'
    services:
      qrm2:
        build: .
        image: "qrm2:local-latest"
        restart: on-failure
        volumes:
          - "./data:/app/data:rw"
    ```

3. Create a subdirectory named `data`.

4. Copy the templates for `options.py` and `keys.py` to `data/`, and edit them.

5. Run `docker-compose`:

    ```none
    $ docker-compose build --pull
    $ docker-compose up -d
    ```

    *Run without "-d" to test the bot (run in foreground).*



## Using pure docker

This methods is not very nice to use.  
*I just wanna run the darn thing, not do gymnastics!*


### [Optional] Building the image

1. `cd` into the repository.

2. Run docker build:

    ```none
    $ docker build -t qrm2:local-latest .
    ```


### Creating the container

1. Be in a directory with a `data/` subdirectory, which should contain valid `options.py` and `keys.py` files (copy and edit the templates).

2. Run the container:

    ```none
    $ docker run -d --rm --mount type=bind,src=$(pwd)/data,dst=/app/data --name qrm2 [image]
    ```

    Where `[image]` is either of:
    - `qrm2:local-latest` if you are building your own.
    - `ghcr.io/miaowware/qrm2:latest` if you want to use the prebuilt image.
