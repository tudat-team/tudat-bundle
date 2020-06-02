#
#add_subdirectory( "${CMAKE_CURRENT_SOURCE_DIR}/satellitePropagatorExamples/SatellitePropagatorExamples/")
#
message("Building Tudat tutorials.")
add_subdirectory(tudat)


if (TUDAT_BUILD_PAGMO_TUTORIALS)
    message("Building pagmo tutorials.")
    add_subdirectory(pagmo)
endif ()
