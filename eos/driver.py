import numpy as np
import NuclearEos as ne

#
# Reproduce the results of driver.F90 in EOSDriver
#

table="/home/pan/Documents/DATA/Eos/LS220_234r_136t_50y_analmu_20091212_SVNr26.h5"
neos = ne.NuclearEOS(table)

var = ne.EOSVariable()
var.xrho = 10.0**14.74994
var.xtemp = 63.0
var.xye = 0.2660725


var = neos.nuc_eos_short(var,mode=1)
print "###########################################"
print "Short EOS ---------------------------------"
print var.xrho,var.xtemp,var.xye
print var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2)
print var.xdedt,var.xdpdrhoe,var.xdpderho
var = neos.nuc_eos_full(var,mode=ne.EOSMODE_RHOT)
print "###########################################"
print "Full EOS ----------------------------------"
print var.xrho,var.xtemp,var.xye
print var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2)
print var.xdedt,var.xdpdrhoe,var.xdpderho
print var.xabar,var.xzbar
print var.xxa,var.xxh,var.xxn,var.xxp
print var.xmu_e,var.xmu_p,var.xmu_n,var.xmuhat

var.xtemp = 2.0*var.xtemp
var = neos.nuc_eos_full(var,mode=ne.EOSMODE_RHOE)
print "###########################################"
print "Full EOS ----------------------------------"
print var.xrho,var.xtemp,var.xye
print var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2)
print var.xdedt,var.xdpdrhoe,var.xdpderho
print var.xabar,var.xzbar
print var.xxa,var.xxh,var.xxn,var.xxp
print var.xmu_e,var.xmu_p,var.xmu_n,var.xmuhat
print "###########################################"


