# spring-bloom-project
In this project, we will use near real time glider and satellite observations to consider the onset of the spring bloom in the eastern subpolar North Atlantic.

The rest of this file contains some technical detail that is beyond the scope of the project but you are more than welcome to explore.

# Climatology hydrographic profiles

Here are some notes about pulling the data from [Gary et al. (2018)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JC013350).

Started with the `all.espna.nf.1950to2015.ge200.hb.rchk2_schk2.stb.ALL.hnc.smo.1.15.gz`
series of 3D climatologies where `ALL` can be replaced with a season in the list
`[DJF, MAM, JJA, SON]`.  Used the following line to convert:

```bash
hb_nc2asc all.espna.nf.1950to2015.ge200.hb.rchk2_schk2.stb.JJA.hnc.smo.1.15 -OJJA.hb
```

and then pulled out just the data in deep water in the southern Rockall Trough where the
gliders are operating:

```bash
hb_extract SON.hb -Tb/1000/10000 -Tg/-11.0/-9.0/56.5/57.5 > SON.hb.deep.box
```

and then pulled just the profiles at the center of the boxes
and added all the calculated properties:

```bash
hb_extract SON.hb.deep.box -Tg/-10.2/-10.0/57.0/57.2 | hb_propcalc -Ppr/de/te/th/sa/s0 > p000SON.hb
```

