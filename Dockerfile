FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# arm64 multiarch on focal (glibc 2.31)
RUN dpkg --add-architecture arm64 && \
    sed -i 's/^deb http/deb [arch=amd64] http/g' /etc/apt/sources.list && \
    echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    gcc-10-aarch64-linux-gnu \
    g++-10-aarch64-linux-gnu \
    binutils-aarch64-linux-gnu \
    pkg-config \
    git \
    ca-certificates \
    ccache \
    python3 \
    libsdl2-dev:arm64 \
    && rm -rf /var/lib/apt/lists/*

ENV TARGET=universal
COPY build.sh /build.sh
RUN chmod +x /build.sh
COPY patches/ /patches/

WORKDIR /build
ENTRYPOINT ["/build.sh"]
