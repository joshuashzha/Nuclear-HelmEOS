#
# Python module to use the Nuclear Equation of State from
# http://stellarcollapse.org
#
# Kuo-Chuan Pan
# March 7th, 2016

import numpy as np
import eospy

EOSMODE_RHOE = 0   # coming in with rho, eps, ye   -> solve for temp
EOSMODE_RHOT = 1   # coming in with rho, temp, ye
EOSMODE_RHOS = 2   # coming in with rho, entr, ye  -> solve for temp
EOSMODE_PT   = 3   # coming in with pres, temp, ye ->solve for rho
MeV_to_Kelvin = 1.1604447522806e10

class EOSVariable(object):
    xrho=1.e10       # density [g/cm^3]
    xtemp=0.01       # temperautre [MeV]
    xye=0.5          # electron Fraction []
    xenr=0.0         # energy [erg/g]
    xent=0.0         # entropy [kb/baryon]
    xprs=None        # pressure [dyne/cm^2]
    xcs2=None        # sound speed squre [cm^2/sec^2] (non relativistic)
    xdedt=None
    xdpderho=None
    xdpdrhoe=None
    xmunu=None
    xxa=None
    xxh=None
    xxn=None
    xxp=None
    xabar=None
    xzbar=None
    xmu_e=None
    xmu_n=None
    xmu_p=None
    xmuhat=None
    error=0

class NuclearEOS():
    def __init__(self,table="LS220.h5"):
        """
        initial the EOS and read the table
            table: String : EOS name (HDF5 format)
        """
        eospy.init_table(table)
        self._get_energy_shift()
        return
    def __del__(self):
        #print "deallocate eos talbe"
        #eospy.del_table()
        return
    def del_table(self):
        eospy.del_table()
        return
        
    def _get_energy_shift(self):
        ezero = eospy.get_energy_shift()
        self.energy_shift = ezero
        return

    def nuc_eos_short(self,variable,mode):
        """
        variable: EOSVariable
        key : Int: 0 -> coming in with rho,eps,ye (solve for temp)
                   1 -> coming in with rho,temperature,ye
                   2 -> coming in with rho,entropy,ye (solve for temp)
                   3 -> coming in with pressure,temp,ye (solve for rho)
        """

        eos_out = eospy.eos_short(variable.xrho,variable.xtemp,variable.xye, 
                variable.xenr,variable.xent,keytemp=mode)

        variable.xrho = eos_out[0]
        variable.xtemp = eos_out[1]
        variable.xenr = eos_out[2]
        variable.xprs = eos_out[3]
        variable.xent = eos_out[4]
        variable.xcs2 = eos_out[5]
        variable.xdedt = eos_out[6]
        variable.xdpderho = eos_out[7]
        variable.xdpdrhoe = eos_out[8]
        variable.xmunu = eos_out[9]
        variable.error = eos_out[10]

        return variable
    def nuc_eos_full(self,variable,mode):
        """
        variable: EOSVariable
        key : Int: 0 -> coming in with rho,eps,ye (solve for temp)
                   1 -> coming in with rho,temperature,ye
                   2 -> coming in with rho,entropy,ye (solve for temp)
                   3 -> coming in with pressure,temp,ye (solve for rho)
        """

        eos_out = eospy.eos_full(variable.xrho,variable.xtemp,variable.xye, 
                variable.xenr,variable.xent,keytemp=mode)

        variable.xrho = eos_out[0]
        variable.xtemp = eos_out[1]
        variable.xenr = eos_out[2]
        variable.xprs = eos_out[3]
        variable.xent = eos_out[4]
        variable.xcs2 = eos_out[5]
        variable.xdedt = eos_out[6]
        variable.xdpderho = eos_out[7]
        variable.xdpdrhoe = eos_out[8]

        variable.xxa = eos_out[9]
        variable.xxh = eos_out[10]
        variable.xxn = eos_out[11]
        variable.xxp = eos_out[12]
        variable.xabar = eos_out[13]
        variable.xzbar = eos_out[14]
        variable.xmu_e = eos_out[15]
        variable.xmu_n = eos_out[16]
        variable.xmu_p = eos_out[17]
        variable.xmuhat = eos_out[18]
        variable.error = eos_out[19]

        return variable

    def getEOSfromRhoTempYe(self,rho,temp, ye, full=False):
        """
        get Eos variable from density (g/cm^3), temperature (K), and Ye

        input: rho  [g/cm^3]
               temp [K]
               ye   []

               full : use eos_full or not default=False

        output: var [EOSVariable]

        """
        temp_to_MeV = temp/MeV_to_Kelvin
        var = EOSVariable()
        var.xrho  = rho
        var.xtemp = temp_to_MeV
        var.xye   = ye
    
        if full:
            var = self.nuc_eos_full(var,mode=EOSMODE_RHOT)
        else:
            var = self.nuc_eos_short(var,mode=EOSMODE_RHOT)

        if var.error != 0:
            print("Warning !!! eos.error is not 0")

        return var

    def getEOSfromRhoEntrYe(self,rho,entr,ye,tryTemp=1.e9, full=False):
        """
        get Eos variable from density (g/cm^3), entropy (kB/by), and Ye

        input: rho  [g/cm^3]
               entr [kB/baryon]
               tryTemp [K] : trial temperature (optional)  
               ye   []

               full : use eos_full or not default=False

        output: var [EOSVariable]

        """
        var = EOSVariable()
        var.xrho  = rho
        var.xtemp = tryTemp/MeV_to_Kelvin
        var.xent  = entr
        var.xye   = ye
    
        if full:
            var = self.nuc_eos_full(var,mode=EOSMODE_RHOS)
        else:
            var = self.nuc_eos_short(var,mode=EOSMODE_RHOS)

        if var.error != 0:
            print("Warning !!! eos.error is not 0")

        return var

if __name__=='__main__':

    #
    # Reproduce the results of driver.F90 in EOSDriver
    #

    table="/home/pan/Documents/DATA/Eos/LS220_234r_136t_50y_analmu_20091212_SVNr26.h5"
    neos = NuclearEOS(table)

    print("###########################################")
    print("Energy shift =",neos.energy_shift)

    var = EOSVariable()
    var.xrho = 10.0**14.74994
    var.xtemp = 63.0
    var.xye = 0.2660725


    var = neos.nuc_eos_short(var,mode=EOSMODE_RHOT)
    print("###########################################")
    print("Short EOS ---------------------------------")
    print(var.xrho,var.xtemp,var.xye)
    print(var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2))
    print(var.xdedt,var.xdpdrhoe,var.xdpderho)
    var = neos.nuc_eos_full(var,mode=EOSMODE_RHOT)
    print("###########################################")
    print("Full EOS ----------------------------------")
    print(var.xrho,var.xtemp,var.xye)
    print(var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2))
    print(var.xdedt,var.xdpdrhoe,var.xdpderho)
    print(var.xabar,var.xzbar)
    print(var.xxa,var.xxh,var.xxn,var.xxp)
    print(var.xmu_e,var.xmu_p,var.xmu_n,var.xmuhat)

    var.xtemp = 2.0*var.xtemp
    var = neos.nuc_eos_full(var,mode=EOSMODE_RHOE)
    print("###########################################")
    print("Full EOS ----------------------------------")
    print(var.xrho,var.xtemp,var.xye)
    print(var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2))
    print(var.xdedt,var.xdpdrhoe,var.xdpderho)
    print(var.xabar,var.xzbar)
    print(var.xxa,var.xxh,var.xxn,var.xxp)
    print(var.xmu_e,var.xmu_p,var.xmu_n,var.xmuhat)
    print("###########################################")


    print(" get EOS from rho, temp, ye")
    var = neos.getEOSfromRhoTempYe(rho=1e12,temp=1e10,ye=0.3)
    print("-------------------------------------------")
    print(var.xrho,var.xtemp,var.xye)
    print(var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2))
    print(var.xdedt,var.xdpdrhoe,var.xdpderho)
    print("###########################################")
    print(" get EOS from rho, entr, ye")
    var = neos.getEOSfromRhoEntrYe(rho=1e12,entr=5.0,ye=0.3)
    print("-------------------------------------------")
    print(var.xrho,var.xtemp,var.xye)
    print(var.xenr,var.xprs,var.xent,np.sqrt(var.xcs2))
    print(var.xdedt,var.xdpdrhoe,var.xdpderho)

