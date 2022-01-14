FROM ubuntu:20.04

LABEL maintainer="NASA IV&V ITC Team"

RUN DEBIAN_FRONTEND=noninteractive \
 && apt -y update \
 && apt -y --no-install-recommends install \
        libaio1 \
        libglib2.0-0 \
        libpixman-1-0 \
 && rm -rf /var/lib/apt/lists/*

VOLUME ["/qemu"]

ENV QEMU_ROOT=/qemu
ENV PATH=${QEMU_ROOT}/bin:${PATH}
WORKDIR $QEMU_ROOT

