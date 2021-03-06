
cmake_minimum_required(VERSION 3.16)

project(TESTing LANGUAGES CXX)

# Find Tudat package.
find_package(Tudat)

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

add_subdirectory(examples)
