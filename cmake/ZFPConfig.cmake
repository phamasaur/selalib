# Find the ZFP compression library,
# http://computation.llnl.gov/projects/floating-point-compression

IF(DEFINED ENV{ZFP_ROOT})
    SET(ZFP_ROOT $ENV{ZFP_ROOT} CACHE PATH "ZFP installation location")
ENDIF()

FIND_PATH(ZFP_INCLUDE_DIR
          NAMES zfp.h
          HINTS ${ZFP_ROOT}
          PATH_SUFFIXES include)

FIND_LIBRARY(ZFP_LIBRARIES
             NAMES zfp libzfp
             HINTS ${ZFP_ROOT}
             PATH_SUFFIXES lib lib64)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ZFP DEFAULT_MSG ZFP_INCLUDE_DIR ZFP_LIBRARIES)

IF(ZFP_FOUND)
    INCLUDE_DIRECTORIES(${ZFP_INCLUDE_DIR})
    MESSAGE(STATUS "ZFP_INCLUDE_DIR:${ZFP_INCLUDE_DIR}")
    MESSAGE(STATUS "ZFP_LIBRARIES:${ZFP_LIBRARIES}")
    ADD_DEFINITIONS(-DUSE_ZFP)
ENDIF()