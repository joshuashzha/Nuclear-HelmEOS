# README #

A python wrapper to use the Nuclear EOS driver from http://stellarcollapse.org


### PRE-REQUIREMENTS ###

* python3
* f2py3
* EOSDriver from http://stellarcollapse.org

### INSTALLATION ###

1. Download the EOSDriver from [https://stellarcollapse.org/equationofstate](https://stellarcollapse.org/equationofstate)
2. Edit the ```make.inc``` file
3. Make sure you have FFLAGS ```-fPIC``` (if you failed to generate f2py code)
4. Compile the Fortran source codes by ```make```
5. Generate the python module using f2py (make sure you have eosmodule.mod and nuc_eos.a at the same path with eospy.F90):
``` f2py -m eospy -c eospy.F90 nuc_eos.a -I$HDF5HOME/include -L$HDF5HOME/lib -lhdf5 -lhdf5_fortran -lhdf5 -lz ```
6. Add ```eospy.so``` and ```NuclearEos.py``` to your python path

### USEAGE ###

```
#!python
import numpy as np
import NuclearEosPy as ne

table = "LS220.h5"
neos = ne.NuclearEOS(table)

# get EOS from rho (g/cm^3), temp (K), and ye 
var = neos.getEOSfromRhoTempYe(rho=1e12,temp=1e10,ye=0.3)

print var.xrho,var.xtemp,var.xye
print var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2)
print var.xdedt,var.xdpdrhoe,var.xdpderho

# get EOS from rho (g/cm^3), entropy (kB/baryon) and ye
var = neos.getEOSfromRhoEntrYe(rho=1e12,entr=5.0,ye=0.3,full=True)

print var.xrho,var.xtemp,var.xye
print var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2)
print var.xdedt,var.xdpdrhoe,var.xdpderho
print var.xabar,var.xzbar
print var.xxa,var.xxh,var.xxn,var.xxp
print var.xmu_e,var.xmu_p,var.xmu_n,var.xmuhat

```

or use the original ```nuc_eos_short``` and ```nuc_eos_full`` by:
```
#!python
var = ne.EOSVariable()
var.xrho = 10.0**14.74994
var.xtemp = 63.0
var.xye = 0.2660725

# mode=1 -> coming in with rho,temperature,ye
var = neos.nuc_eos_short(var,mode=1)

var = neos.nuc_eos_full(var,mode=1)
```
 
See further examples and demo in driver.py and NuclearEos.py
