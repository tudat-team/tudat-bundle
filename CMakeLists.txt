#    Copyright (c) 2010-2019, Delft University of Technology
#    All rigths reserved
#
#    This file is part of the Tudat. Redistribution and use in source and
#    binary forms, with or without modification, are permitted exclusively
#    under the terms of the Modified BSD license. You should have received
#    a copy of the license with this file. If not, please or visit:
#    http://tudat.tudelft.nl/LICENSE.


# Specify minimum CMake version required to compile Tudat.
cmake_minimum_required( VERSION 2.8.10 )

cmake_policy(SET CMP0069 NEW)


# https://stackoverflow.com/questions/30380257/how-can-ld-library-path-be-changed-within-cmake
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
#set(COMPILE_FLAGS "${CMAKE_CXX_FLAGS} -D_GLIBCXX_USE_CXX11_ABI=0")

# Clean cache

if(EXISTS "${CMAKE_BINARY_DIR}/CMakeCache.txt")
    file(REMOVE "${CMAKE_BINARY_DIR}/CMakeCache.txt")
endif()

# Specific Tudat project name.
project( TudatBundle )

# Add local module path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules/")

# TODO: Add append procedure for (TUDAT_BUILD_TESTS) with unit_test_framework.
# Legacy add_boost module.
set(BoostComponents filesystem system regex date_time thread
        serialization chrono atomic unit_test_framework)
set(BoostVersion 1.64.0)
set(BoostSHA1 51421ef259a4530edea0fbfc448460fcc5c64edb)
include(add_boost)

# Eigen dependency.
#list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/eigen/cmake)
#add_subdirectory(eigen)
find_package(Eigen3 REQUIRED)
set(EIGEN3_INCLUDE_DIRS ${EIGEN3_INCLUDE_DIR})

# CSpice project.
add_subdirectory(cspice)
#find_package(CSpice REQUIRED)
set(CSpice_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/cspice/include")

# Sofa project.
add_subdirectory(sofa)
#find_package(Sofa REQUIRED)
set(Sofa_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/sofa/include")

# Tudat project.
add_subdirectory(tudat)
set(Tudat_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/tudat/include")

# TudatPy project.
set(pybind11_DIR "${CMAKE_CURRENT_SOURCE_DIR}/pybind11/share/cmake/pybind11/")
add_subdirectory(tudatpy)
