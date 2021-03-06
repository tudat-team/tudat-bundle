#!/usr/bin/env bash

# Echo each command
set -x

# Exit on error.
set -e

# Core deps.
sudo apt-get install build-essential cmake

# Create the build dir and cd into it.
mkdir build
cd build

# GCC build with coverage.
cmake ../ -DCMAKE_BUILD_TYPE=Release
make -j2 VERBOSE=1
ctest -V

set +e
set +x