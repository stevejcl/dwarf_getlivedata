# dwarf_getlivedata
Get live Fits file from Dwaf II

It's a python script that will connect by ftp to your dwarf in STA mode.

You need to enter the ip of the dwarf.
Need also a working directory to copy the file.

It will search for the last session or you can specify one (name of the directory on the dwarf).

You can use it during session because it will search for new files until you stop the script.

You can use it to just copy your files or use it to make a live stacking with Siril, in this case you need a dark master to stack well.
