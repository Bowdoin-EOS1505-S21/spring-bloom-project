#!/bin/sh
# Download script based on https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+cURL+And+Wget
fetch_urls() {
        while read -r line; do
            curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n -f -Og $line && echo || exit_with_error "Command failed with error. Please retrieve the data manually."
        done;
}
fetch_urls <<'EDSCEOF'
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20030912020121.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20031212020152.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20031522020182.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20031822020213.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20032132019243.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20032442019273.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20032742019304.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20033052019334.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20033352019365.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20040012020031.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20040322020060.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20040612020091.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20040922020121.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20041222020152.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20041532020182.L3m_MC_CHL_chlor_a_9km.nc
https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20041832020213.L3m_MC_CHL_chlor_a_9km.nc
EDSCEOF