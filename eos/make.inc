F90=gfortran -fPIC -O2

HDF5DIR = ${MESASDK_ROOT}
HDF5INCS=-I${HDF5DIR}/include
HDF5LIBS=-L${HDF5DIR}/lib -lhdf5 -lhdf5_fortran -lhdf5 -lz

#HDF5INCS=-I/Users/pan/anaconda/include
#HDF5LIBS=-L/Users/pan/anaconda/lib -lhdf5 -lhdf5_fortran -lhdf5 -lz
