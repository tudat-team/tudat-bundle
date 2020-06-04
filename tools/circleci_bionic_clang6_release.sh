#!/usr/bin/env bash

# Echo each command
set -x

# Exit on error.
set -e

# Core deps.
sudo apt-get install build-essential clang cmake

# Create the build dir and cd into it.
mkdir build
cd build

# Clang release build.
CXX=clang++ CC=clang cmake ../ -DCMAKE_BUILD_TYPE=Release
make -j2 VERBOSE=1
ctest -V

set +e
set +x