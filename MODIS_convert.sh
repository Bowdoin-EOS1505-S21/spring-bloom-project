#!/bin/tcsh
# Add time axis to MODIS files
# with Ferret.  This allows
# for creating a time series
# with the data within Ferret.

foreach file ( A*MC*.nc )
    echo Working on $file

    ncdump -h $file | grep time_coverage_end | awk  -F\" '{print $2}' | sed "s/T/ /g; s/:/ /g" | awk '{print $1}' > datestr.tmp
    
    set datestr = `cat datestr.tmp`
    rm -f datestr.tmp
    
    set bn = `basename $file .nc`
    
    pyferret -nojnl <<EOF
use $file
define axis/t=${datestr}:${datestr}:1/unit=days time
define grid/t=time gg
let chl = t[g=gg]*0 + CHLOR_A
set variable/title="Chlorophyll_A"/units="mg m^-3" chl
save/file=${bn}.cdf chl[l=1]
quit

EOF
    
end
