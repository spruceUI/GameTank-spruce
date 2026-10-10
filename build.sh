#!/bin/bash
set -e

GTE_VERSION="${GTE_VERSION:-9896544460d5bb7dd89c2d2bc0f5c97a6f31d2e0}"
OUTPUT_DIR="${OUTPUT_DIR:-/output}"
TARGET="${TARGET:?TARGET must be universal or a30}"

case "$TARGET" in
    universal)
        CROSS=aarch64-linux-gnu
        export CC=${CROSS}-gcc-10
        export CXX=${CROSS}-g++-10
        OPTFLAGS="-O2 -mcpu=cortex-a53"
        export SDL_CFLAGS="-I/opt/sdl2/include -I/opt/sdl2/include/SDL2 -D_REENTRANT"
        export SDL_LIBS="-L/opt/sdl2/lib -lSDL2 -lpthread"
        ;;
    a30)
        TOOLCHAIN=/opt/a30
        SYSROOT=$TOOLCHAIN/arm-a30-linux-gnueabihf/sysroot
        CROSS=arm-a30-linux-gnueabihf
        export PATH="$TOOLCHAIN/bin:$PATH"
        export CC=${CROSS}-gcc
        export CXX=${CROSS}-g++
        export PKG_CONFIG_LIBDIR="$SYSROOT/usr/lib/pkgconfig"
        export PKG_CONFIG_SYSROOT_DIR="$SYSROOT"
        OPTFLAGS="-O2 -mcpu=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=hard"
        export SDL_CFLAGS="-I$SYSROOT/usr/include/SDL2 -D_REENTRANT"
        export SDL_LIBS="-lSDL2 -lpthread"
        ;;
    *)
        echo "unknown TARGET $TARGET"; exit 1 ;;
esac
STRIP=${CROSS}-strip

export CCACHE_DIR="${CCACHE_DIR:-/ccache}"
ccache --max-size=500M
ccache --zero-stats

# The Makefile calls sdl2-config directly; answer it from the target's SDL2.
mkdir -p /tmp/bin
cat > /tmp/bin/sdl2-config <<'EOF'
#!/bin/sh
case "$1" in
    --cflags) [ -n "$SDL_CFLAGS" ] && echo "$SDL_CFLAGS" || exec pkg-config --cflags sdl2 ;;
    --libs)   [ -n "$SDL_LIBS" ] && echo "$SDL_LIBS" || exec pkg-config --libs sdl2 ;;
esac
EOF
chmod +x /tmp/bin/sdl2-config
export PATH="/tmp/bin:$PATH"

echo "=== Cloning GameTankEmulator $GTE_VERSION ==="
git clone https://github.com/clydeshaffer/GameTankEmulator.git gte
cd gte
git checkout "$GTE_VERSION"
git submodule update --init --depth 1 src/mos6502 src/imgui/ext/implot

# A patch that fails must fail the build.
for dir in /patches/common /patches/$TARGET; do
    for patch in "$dir"/*.patch; do
        [ -f "$patch" ] || continue
        git apply "$patch" && echo "Applied: $(basename "$patch")" || exit 1
    done
    for patch in "$dir"/*.py; do
        [ -f "$patch" ] || continue
        python3 "$patch" && echo "Applied: $(basename "$patch")" || exit 1
    done
done

echo "=== Building GameTankEmulator ($TARGET) ==="
make -j"$(nproc)" bin \
    CC="ccache $CC" CPPC="ccache $CXX" \
    OPTIM_FLAGS="$OPTFLAGS" \
    LIBRARY_PATHS="-static-libstdc++ -static-libgcc"

mkdir -p "$OUTPUT_DIR"
cp build/GameTankEmulator "$OUTPUT_DIR/"
$STRIP -s "$OUTPUT_DIR/GameTankEmulator"
git rev-parse HEAD > "$OUTPUT_DIR/commit_hash.txt"

echo "=== Dependencies ==="
${CROSS}-readelf -d "$OUTPUT_DIR/GameTankEmulator" | grep NEEDED

echo "=== ccache stats ==="
ccache --show-stats

ls -la "$OUTPUT_DIR/"
