FROM ubuntu:noble AS base

# Install run-time dependencies in base image
RUN apt-get -y update && apt-get install -y \
    libc6 \
    libstdc++6 \
    libprotobuf32 \
    libnl-route-3-200 \
    python3 \
    python3-pip

FROM base AS build
ARG NSJAIL_VERSION=3.4

# build dependencies
RUN apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler

RUN git clone --branch ${NSJAIL_VERSION} --recursive https://github.com/google/nsjail.git /nsjail

RUN cd /nsjail && make clean && make

FROM base AS run

# Copy over build result and trim image
RUN rm -rf /var/lib/apt/lists/*
COPY --from=build /nsjail/nsjail /bin