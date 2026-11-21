#!/usr/bin/env bash
# update_vpx.sh x64|arm64  — compila libvpx 1.17.0 /MT (decoder-only) e instala no repo.
# x64:   "x64 Native Tools Command Prompt for VS 2022"  -> set PATH=C:\msys64\usr\bin;%PATH% -> bash update_vpx.sh x64
# arm64: "x64_arm64 Cross Tools Command Prompt for VS 2022" -> idem -> bash update_vpx.sh arm64
# (VS2026: troque os alvos para *-vs18.)
set -euo pipefail
ARCH="${1:?x64|arm64}"; REPO="$(pwd)"; VER=1.17.0
SHA=7f98aae5c52c46e85b7b26feabcab9b1554605e771bd1df1d6e6a00ee22fa8ed
case "$ARCH" in
  x64)   TARGET=x86_64-win64-vs18; LIBDIR=64 ;;
  arm64) TARGET=arm64-win64-vs18;  LIBDIR=arm64 ;;
  *) exit 1 ;;
esac
WORK="$(mktemp -d)"; cd "$WORK"
curl -fLO "http://downloads.webmproject.org/releases/webm/libvpx-$VER.tar.gz"
echo "$SHA  libvpx-$VER.tar.gz" | sha256sum -c -
tar xzf "libvpx-$VER.tar.gz"; mkdir build; cd build
../libvpx-$VER/configure --target=$TARGET --enable-static-msvcrt \
  --disable-vp8-encoder --disable-vp9-encoder \
  --disable-examples --disable-tools --disable-docs --disable-unit-tests
make -j"$(nproc)"
LIB="$(find . -name vpxmt.lib | head -n1)"; [ -n "$LIB" ] || { echo "vpxmt.lib não achado"; exit 1; }
install -Dm644 "$LIB" "$REPO/bin/windows/vpx/lib/$LIBDIR/libvpx.lib"
for h in vp8.h vp8dx.h vpx_codec.h vpx_decoder.h vpx_frame_buffer.h vpx_image.h vpx_integer.h; do
  install -Dm644 "../libvpx-$VER/vpx/$h" "$REPO/bin/windows/vpx/include/vpx/$h"
done
echo "OK libvpx $VER $ARCH (/MT). Aplique o diff do CMake após instalar x64 E arm64."