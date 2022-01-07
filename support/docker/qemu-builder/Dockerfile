#-------------------------------------------------------------------------------
# instructions:
# 1. build container
#    $ docker build -t qemu-builder .
# 2. create docker volume for build cache directory
#    $ docker volume create qemu-builder
# 3. build qemu
#    $ docker run --rm -it -v qemu-builder:/build -v <repo>:/src qemu-builder
#-------------------------------------------------------------------------------

FROM ubuntu:20.04

LABEL maintainer="NASA IV&V ITC Team"

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y --no-install-recommends install \
        autoconf \
        automake \
        bison \
        flex \
        g++ \
        gcc \
        git \
        libaio-dev \
        #libfdt-dev \
        libgcrypt20-dev \
        libglib2.0-dev \
        libpixman-1-dev \
        libtool \
        make \
        python3-minimal \
        zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

VOLUME ["/build"]

ENTRYPOINT ["/src/support/docker/qemu-builder/build.py"]
CMD ["--help"]

