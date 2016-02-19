# MUMPS lib requires linking to a blas library.
# It is up to the user of this module to find a BLAS and link to it.
# MUMPS requires SCOTCH or METIS (partitioning and reordering tools) as well

IF(DEFINED ENV{MUMPS_ROOT})
   SET(MUMPS_ROOT $ENV{MUMPS_ROOT} CACHE PATH "mumps location")
ELSE()
   SET(MUMPS_ROOT /usr/local CACHE PATH "mumps location")
ENDIF()

FIND_PATH(MUMPS_INCLUDE_DIRS
	    NAMES dmumps_struc.h
	    HINTS ${MUMPS_ROOT}
	    PATH_SUFFIXES include Include INCLUDE
	    DOC "PATH TO dmumps_struc.h")

FIND_LIBRARY(MUMPS_LIBRARY NAMES dmumps
		 HINTS ${MUMPS_ROOT}
		 PATH_SUFFIXES lib Lib LIB
		 DOC "PATH TO libdmumps.a")

FIND_LIBRARY(MUMPS_COMMMON_LIBRARY NAMES mumps_common
		 HINTS ${MUMPS_ROOT}
		 PATH_SUFFIXES lib Lib LIB
		 DOC "PATH TO libmumps_common.a")

FIND_LIBRARY(MUMPS_SIMPLE_LIBRARY NAMES mumps_simple
		 HINTS ${MUMPS_ROOT}
		 PATH_SUFFIXES lib Lib LIB
		 DOC "PATH TO libmumps_simple.a")

SET(MUMPS_LIBRARIES ${MUMPS_LIBRARY};${MUMPS_COMMON_LIBRARY};${MUMPS_SIMPLE_LIBRARY})

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MUMPS DEFAULT_MSG MUMPS_INCLUDE_DIRS MUMPS_LIBRARIES)

IF(MUMPS_FOUND)
  MESSAGE(STATUS "MUMPS_INCLUDE_DIRS:${MUMPS_INCLUDE_DIRS}")
  MESSAGE(STATUS "MUMPS_LIBRARIES:${MUMPS_LIBRARIES}")
  ADD_DEFINITIONS(-DMUMPS)
ENDIF(MUMPS_FOUND)

MARK_AS_ADVANCED(MUMPS_INCLUDE_DIRS
                 MUMPS_LIBRARY
                 MUMPS_COMMON_LIBRARY
                 MUMPS_SIMPLE_LIBRARY
                 MUMPS_LIBRARIES)
                 