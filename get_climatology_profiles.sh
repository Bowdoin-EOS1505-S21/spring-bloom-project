#!/bin/tcsh
#---------------------

foreach mon ( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec )
	hb_nc2asc all.espna.nf.1950to2015.ge200.hb.rchk2_schk2.stb.${mon}.hnc.smo.1.15 -O${mon}.hb
	hb_extract ${mon}.hb -Tb/1000/10000 -Tg/-11.0/-9.0/56.5/57.5 > ${mon}.hb.deep.box
	hb_extract ${mon}.hb.deep.box -Tg/-10.2/-10.0/57.0/57.2 | hb_propcalc -Ppr/de/te/th/sa/s0 > p000${mon}.hb
	gzip ${mon}.hb
	gzip ${mon}.hb.deep.box
end

