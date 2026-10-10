FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
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
    wget \
    && rm -rf /var/lib/apt/lists/*

# focal's SDL2 is 2.0.10; imgui's SDL renderer backend needs 2.0.17+.
# Built only to compile and link against; devices bring their own SDL2.
RUN wget -q https://github.com/libsdl-org/SDL/releases/download/release-2.28.5/SDL2-2.28.5.tar.gz && \
    tar xzf SDL2-2.28.5.tar.gz && cd SDL2-2.28.5 && \
    ./configure --host=aarch64-linux-gnu CC=aarch64-linux-gnu-gcc-10 --prefix=/opt/sdl2 \
        --disable-static --disable-video-x11 --disable-video-wayland --disable-video-kmsdrm \
        --disable-video-opengl --disable-pulseaudio --disable-pipewire --disable-jack --disable-sndio && \
    make -j"$(nproc)" && make install && \
    cd / && rm -rf SDL2-2.28.5 SDL2-2.28.5.tar.gz

ENV TARGET=universal
COPY build.sh /build.sh
RUN chmod +x /build.sh
COPY patches/ /patches/

WORKDIR /build
ENTRYPOINT ["/build.sh"]
