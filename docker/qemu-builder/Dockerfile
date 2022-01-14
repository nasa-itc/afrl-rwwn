FROM ubuntu:20.04

LABEL maintainer="NASA IV&V ITC Team"

RUN DEBIAN_FRONTEND=noninteractive \
 && apt -y update \
 && apt -y --no-install-recommends install \
        autoconf \
        automake \
        bison \
        ca-certificates \
        flex \
        g++ \
        gcc \
        git \
        libaio-dev \
        libgcrypt20-dev \
        libglib2.0-dev \
        libpixman-1-dev \
        libtool \
        make \
        python3-minimal \
        zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

VOLUME ["/qemu/src", "/qemu/build"]

ENV QEMU_ROOT=/qemu
WORKDIR $QEMU_ROOT

COPY build.py .

ENTRYPOINT ["./build.py"]
CMD ["--help"]

