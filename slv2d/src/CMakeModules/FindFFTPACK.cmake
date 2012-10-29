FIND_LIBRARY(FFTPACK_LIBRARIES
		NAMES dfftpack
		HINTS /usr/local
		PATH_SUFFIXES lib 
		DOC "PATH TO libdfftpack")

IF (FFTPACK_LIBRARIES)
   MESSAGE(STATUS "FFTPACK FOUND")
ELSE()
   MESSAGE(STATUS "FFTPACK NOT FOUND ... BUILD SOURCE")
   #SET(SELALIB_DIR ${PROJECT_SOURCE_DIR}/../../prototype/src)
   ADD_SUBDIRECTORY(dfftpack)
   SET(FFTPACK_LIBRARIES dfftpack)
ENDIF(FFTPACK_LIBRARIES)

SET(FFTPACK_FOUND YES)