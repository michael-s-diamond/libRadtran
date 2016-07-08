"""
Create input files for libRadtran AAC calculations
"""

#Import libraries
import numpy as np

def write_cloud_file(output_file,tau,ref,zbot,ztop,verbose=False,append_directly_below=False):
    """
    Adapted from Sam LeBlanc
    
    Purpose:

        Program to write out the cloud file profile
        for either ic_file or wc_file in 1D settings
        outputs 3 columns: 
            # z [km]    IWC/LWC [g/m^3]    Reff [um]
            
        ** translates tau and ref to lwc/iwc with the equation LWP = 2/3*tau*ref and LWC=LWP/z_extent*0.001
        ** Writes out file based on layer properties, not level properties. (given value of ref and tau are for a cloud from zbot to ztop)
    
    Input: 
  
        output_file: full path to file to be written
        tau: value of cloud optical thickness
        ref: value of effective radius in microns
        ztop: location in km of cloud top
        zbot: location in km of cloud bottom
    
    Output:

        output_file
                
    
    Keywords: 

        verbose: (default False) if true prints out info about file writing 
        append_directly_below: (default False) if true then opens a already existing file and only writes out the last line as an append
    
    Dependencies:

        numpy
    
    Required files:
   
        none
    
    Example:

        ...
        
    Modification History:
    
        Written (v1.0): Samuel LeBlanc, 2015-06-26, NASA Ames, from Santa Cruz, CA
        Modified (v1.1): Samuel LeBlanc, DC8 flying above Korea, 2016-05-02
        Modified (v.1.m): Michael Diamond, 2016-07-07, Hawthorne, NY
    """
    if (zbot >= ztop):
        raise ValueError('*** Error ztop must be larger than zbot ***')
    if (ztop < 1.0):
        print('ztop is smaller than one, check units, ztop should be in km')
        if verbose:
            print('..file preperations continuing')
    if tau:
        if np.isnan(tau):
            raise ValueError('*** Error tau is NaN ***')
    if ref:
        if np.isnan(ref):
            raise ValueError('*** Error ref is NaN ***')
    lwp = 2.0/3.0*tau*ref
    lwc = lwp/(ztop-zbot)*0.001
    if verbose:
        print('..Cloud water content is: %f' % lwc)
    if not append_directly_below:
        try:
            output = file(output_file,'w')
        except Exception,e:
            print 'Problem with accessing file, return Exception: ',e
            return
        if verbose:
            print('..printing to file: %s' % output_file)
        output.write('# z [km]    LWC [g/m^3]    Reff [um] \n')
        output.write('%4.4f\t%4.5f\t%3.2f\n' % (ztop,0,0))
        output.write('%4.4f\t%4.5f\t%3.2f\n' % (zbot,lwc,ref))
    else:
        try:
            output = file(output_file,'a')
        except Exception,e:
            print 'Problem with accessing file, return Exception: ',e
            return
        output.write('%4.4f\t%4.5f\t%3.2f\n' % (zbot,lwc,ref))
    output.close() 
    if verbose:
        print('..File finished write_cloud_file, closed')

