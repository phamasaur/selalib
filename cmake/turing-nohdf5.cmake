SET(ZLIB_LIBRARIES "/bglocal/cn/pub/zlib/1.2.5/lib/libz.a" CACHE FILEPATH " " FORCE)
SET(BLAS_LIBRARIES "/bgsys/ibm_essl/prod/opt/ibmmath/essl/5.1/lib64/libesslbg.a" CACHE FILEPATH " " FORCE) 
SET(LAPACK_LIBRARIES "/bglocal/cn/pub/LAPACK/3.4.2/lib/liblapacke.a;/bglocal/cn/pub/LAPACK/3.4.2/lib/liblapack.a" CACHE FILEPATH " " FORCE)
SET(MUDPACK_ENABLED       OFF  CACHE BOOL   " " FORCE)
SET(FISHPACK_ENABLED      OFF  CACHE BOOL   " " FORCE)
SET(HDF5_ENABLED          OFF  CACHE BOOL   " " FORCE)
SET(HDF5_PARALLEL_ENABLED OFF  CACHE BOOL   " " FORCE)
SET(Fortran_COMPILER      IBM  CACHE STRING " " FORCE)