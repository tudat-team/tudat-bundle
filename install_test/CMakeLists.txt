
cmake_minimum_required(VERSION 3.16)

project(TESTing LANGUAGES CXX)

list(APPEND CMAKE_MODULE_PATH "/home/ggarrett/CLionProjects/tudat-team/tudat-bundle/tudat/cmake_modules/")

#set(CMAKE_PREFIX_PATH /home/ggarrett/CLionProjects/tudat-team/tudat-bundle/install_test)
set(CMAKE_PREFIX_PATH /home/ggarrett/miniconda3/envs/tudat-bundle-env)
set(Boost_DIR /home/ggarrett/CLionProjects/tudat-team/tudat-bundle/boost/stage)
set(Boost_INCLUDE_DIR /home/ggarrett/CLionProjects/tudat-team/tudat-bundle/boost)

set(_TUDAT_FIND_BOOST_UNIT_TEST_FRAMEWORK ON)

find_package(CSpice)
find_package(Sofa)
find_package(Boost)
find_package(Eigen3)

#add_definitions(-DTUDAT_BUILD_WITH_SOFA_INTERFACE=on)
#add_definitions(-DTUDAT_BUILD_WITH_JSON_INTERFACE=on)

set(CMAKE_PREFIX_PATH /home/ggarrett/CLionProjects/tudat-team/tudat-bundle/install_test)

find_package(Tudat)

include_directories("${Tudat_INCLUDE_DIRS}")
include_directories("${Sofa_INCLUDE_DIRS}")
include_directories("${CSpice_INCLUDE_DIRS}")
include_directories("${Boost_INCLUDE_DIRS}")
include_directories("${EIGEN3_INCLUDE_DIRS}")

message(STATUS ---- SPICE)
message("${CSpice_INCLUDE_DIRS}")
message("${CSpice_LIBRARY_DIRS}")
message("${CSpice_LIBRARIES}")

message(STATUS ---- SOFA)
message("${Sofa_INCLUDE_DIRS}")
message("${Sofa_LIBRARY_DIRS}")
message("${Sofa_LIBRARIES}")

message(STATUS ---- BOOST)
message("${Boost_INCLUDE_DIRS}")
message("${Boost_LIBRARY_DIRS}")
message("${Boost_LIBRARIES}")

message(STATUS ---- EIGEN)
message("${EIGEN3_INCLUDE_DIRS}")
message("${EIGEN3_LIBRARY_DIRS}")
message("${EIGEN3_LIBRARIES}")

message(STATUS ---- TUDAT)
message("${Tudat_INCLUDE_DIRS}")
message("${Tudat_LIBRARY_DIRS}")
message("${Tudat_PROPAGATION_LIBRARIES}")

message(TUDAT_LIB_DIR: ${Tudat_LIBRARY_DIRS})
message(Tudat_PROPAGATION_LIBRARIES: "${Tudat_PROPAGATION_LIBRARIES}")
message(Tudat_INCLUDE_DIRS: "${Tudat_INCLUDE_DIRS}")
message(Tudat_LIBRARY_DIRS: "${Tudat_LIBRARY_DIRS}")

function(TUDAT_ADD_EXECUTABLE arg1 arg2)
    # arg1: executable name
    # arg2: sources
    if (CMAKE_BUILD_TYPE MATCHES DEBUG)

        message("Tudat EXECUTABLE: ${arg1}")
        message("ARGN: ${ARGN}")
    endif ()
    add_executable(${arg1} ${arg2})
    target_link_libraries(${arg1}
            ${ARGN}
            ${Boost_LIBRARIES}
            ${Sofa_LIBRARIES}
            ${CSpice_LIBRARIES}
            )
    set_target_properties(${arg1}
            PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${INSTALL_INCLUDE_DIR}"
            ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
            LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
            RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
            )
endfunction()

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_GLIBCXX_USE_CXX11_ABI=0")

add_subdirectory(examples)
