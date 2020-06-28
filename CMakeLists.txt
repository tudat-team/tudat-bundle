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
#set(CMAKE_POSITION_INDEPENDENT_CODE ON)
#set(COMPILE_FLAGS "${CMAKE_CXX_FLAGS} -D_GLIBCXX_USE_CXX11_ABI=0")

# Clean cache
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_GLIBCXX_USE_CXX11_ABI=0")

if(EXISTS "${CMAKE_BINARY_DIR}/CMakeCache.txt")
    file(REMOVE "${CMAKE_BINARY_DIR}/CMakeCache.txt")
endif()

# Specific Tudat project name.
project( TudatBundle )

# Add local module path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules/")

message(CMAKE_INSTALL_PREFIX:${CMAKE_INSTALL_PREFIX})
# TODO: Add append procedure for (TUDAT_BUILD_TESTS) with unit_test_framework.
#SET (Boost_FIND_REQUIRED TRUE)
#SET (Boost_FIND_QUIETLY TRUE)
#set (Boost_USE_MULTITHREADED TRUE)
#set (Boost_USE_STATIC_LIBS TRUE)

FIND_PACKAGE(Boost REQUIRED COMPONENTS ${BoostComponenets})
IF (Boost_FOUND)
    INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
    ADD_DEFINITIONS( "-DHAS_BOOST" )
ENDIF()

message(STATUS Boost_VERSION_MAJOR:${Boost_VERSION_MAJOR})
message(STATUS Boost_VERSION_MINOR:${Boost_VERSION_MINOR})

# Silence Deprecated bind placeholders in tests.
add_definitions(-DBOOST_BIND_GLOBAL_PLACEHOLDERS)

# Eigen dependency.
#list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/eigen/cmake)
#add_subdirectory(eigen)
set(EIGEN3_BUILD_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/eigen/)

# CSpice project.
add_subdirectory(cspice-cmake)
set(CSpice_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/cspice/include")

add_subdirectory(tudat-resources)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/tudat-resources/include")
include_directories("${CMAKE_BINARY_DIR}/tudat-resources/include")

# Sofa project.
add_subdirectory(sofa-cmake)
set(Sofa_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/sofa/include")

# Tudat project.
add_subdirectory(tudat)
set(Tudat_BUILD_INCLUDE_DIRS "${CMAKE_CURRENT_SOURCE_DIR}/tudat/include")

# TudatPy project.
set(pybind11_BUILD_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/pybind11/include)
add_subdirectory(pybind11)
add_subdirectory(tudatpy)
