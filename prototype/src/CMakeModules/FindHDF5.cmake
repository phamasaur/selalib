#-----------------------------------------------------------------------------
# User Options
#-----------------------------------------------------------------------------
SET (HDF5_ENABLE_PARALLEL @HDF5_ENABLE_PARALLEL@)
#Ne pas mettre cette variable sur OFF, il y a une variable HDF_PARALLEL_ENABLED pour cela
SET (HDF5_BUILD_FORTRAN   @HDF5_BUILD_FORTRAN@)
SET (HDF5_ENABLE_F2003    @HDF5_ENABLE_F2003@)
SET (HDF5_BUILD_HL_LIB    @HDF5_BUILD_HL_LIB@)


find_path(HDF5_INCLUDE_DIRS NAMES hdf5.h
	HINTS ${HDF5_ROOT}
	PATH_SUFFIXES include hdf5/include
	DOC "PATH TO hdf5.h")

find_path(HDF5_INCLUDE_DIR_FORTRAN NAMES hdf5.mod
	HINTS ${HDF5_ROOT}
	PATH_SUFFIXES include hdf5/include include/fortran
	DOC "PATH to hdf5.mod")

find_library(HDF5_HDF5_LIBRARY NAMES hdf5
	HINTS ${HDF5_ROOT}
	PATH_SUFFIXES lib hdf5/lib
	DOC "PATH TO libhdf5.dylib")

find_library(HDF5_HDF5_FORTRAN_LIBRARY NAMES hdf5_fortran
	HINTS ${HDF5_ROOT}
	PATH_SUFFIXES lib hdf5/lib
	DOC "PATH TO libhdf5_fortran.a")

#find_library(HDF5_Z_LIBRARY NAMES z
#	HINTS ${HDF5_ROOT}
#	PATH_SUFFIXES lib hdf5/lib
#	DOC "PATH TO libz.dylib")

find_package(ZLIB)

#set(HDF5_LIBRARIES @HDF5_HDF5_FORTRAN_LIBRARY@;@HDF5_HDF5_LIBRARY@;@HDF5_Z_LIBRARY@)

set(HDF5_LIBRARIES @HDF5_HDF5_FORTRAN_LIBRARY@;@HDF5_HDF5_LIBRARY@ ${ZLIB_LIBRARIES})

IF ( HDF5_INCLUDE_DIRS         AND
     HDF5_HDF5_LIBRARY         AND
     HDF5_HDF5_FORTRAN_LIBRARY AND
     ZLIB_FOUND )
  set(HDF5_FOUND YES)
  IF(HDF5_INCLUDE_DIR_FORTRAN)
  INCLUDE_DIRECTORIES(${HDF5_INCLUDE_DIR_FORTRAN})
  ELSE()
  INCLUDE_DIRECTORIES(${HDF5_INCLUDE_DIRS}/fortran)
  ENDIF()
ENDIF()

IF(HDF5_ENABLE_PARALLEL) 
   MESSAGE(STATUS "HDF5 parallel supported")
ELSE(HDF5_ENABLE_PARALLEL)
   MESSAGE(STATUS "HDF5 parallel not supported")
ENDIF()
IF(HDF5_BUILD_FORTRAN)   
   MESSAGE(STATUS "HDF5 was compiled with fortran on")
ELSE(HDF5_BUILD_FORTRAN)   
   MESSAGE(STATUS "HDF5 was compiled with fortran off")
ENDIF()
IF(HDF5_BUILD_HL_LIB)    
   MESSAGE(STATUS "HDF5 was compiled with high level on")
ELSE(HDF5_BUILD_HL_LIB)    
   MESSAGE(STATUS "HDF5 was compiled with high level off")
ENDIF()
IF(HDF5_ENABLE_F2003)
   MESSAGE (STATUS "HDF5 FORTRAN 2003 Standard enabled")
ELSE(HDF5_ENABLE_F2003)
   MESSAGE (STATUS "HDF5 FORTRAN 2003 Standard disabled")
ENDIF()
