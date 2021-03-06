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
cmake ../ -DCMAKE_BUILD_TYPE=Debug -DPAGMO_BUILD_TESTS=yes -DCMAKE_CXX_FLAGS="--coverage"
make -j2 VERBOSE=1
ctest -V

# Upload coverage data.
bash <(curl -s https://codecov.io/bash) -x gcov-7

set +e
set +x