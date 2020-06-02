
cmake_minimum_required(VERSION 3.16)

project(TESTing LANGUAGES CXX)

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} /home/ggarrett/anaconda3/envs/test/lib)
set(CMAKE_INCLUDE_PATH ${CMAKE_INCLUDE_PATH} /home/ggarrett/anaconda3/envs/test/include)

set(_TUDAT_FIND_BOOST_UNIT_TEST_FRAMEWORK ON)

include(lib/cmake/tudat/tudat-config.cmake)
#include(lib/cmake/tudat/tudat_export.cmake)

#set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} /opt/local/lib)

# Find Tudat package.
find_package(Tudat)
include_directories("${Tudat_INCLUDE_DIRS}")
include_directories("${Boost_INCLUDE_DIRS}")
include_directories("${EIGEN3_INCLUDE_DIRS}")

set(CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ${Tudat_LIBRARY_DIRS})

message(TUDAT_LIOB_DIR: ${Tudat_LIBRARY_DIRS})
# Message what has been found.
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
            ${Boost_LIBRARIES})
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
