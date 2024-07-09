# dwarf_getlivedata

It's a python script that will connect by ftp to your dwarf in STA mode.

You need to enter the ip of the dwarf first and the dwarf must be running.
Need also a working directory to copy the files.

Without parameter a menu will be displayed.
The parameters like ip of the dwarf II, local directory name can then be saved.

---------------------
Installation
---------------------
1. Clone this repository 

2. Then Install the dwarf_python_api library with :
  
     python -m pip install -r requirements.txt
     python -m pip install -r requirements-local.txt --target .

   This project uses the dwarf_python_api library that must be installed locally in the root path of this project
   with using the parameter --target .

   Don't miss the dot at the end of the line

'Run it with:

python3 ./get_live_data_dwarf.py

---------------------
2 functions provided: 
---------------------
1). Get live Fits file from Dwarf II


It will search for the last Astro session or you can specify one (name of the directory on the dwarf).

You can use it during session because it will search for new files until you stop the script.

You can use it to just copy your files or use it to make a live stacking with Siril, in this case you need a dark master to stack well.

=> direct execution : 
   python3 ./get_live_data_dwarf.py --opt 4 --dir ImportDirSirilName

NB : The IP of the dwarf must be saved first.

---------------------
2). Get last Tele Photo (Photo Mode) file from Dwarf II

It will download the last Tele Photo (Photo Mode) or older taken from the dwarf.
This Photo will be downloaded on the current directory or a specified directory
Secify a number for history param : 0 (default) => last photo, 1 => penultimate and so on

=> direct execution : 
   python3 ./get_live_data_dwarf.py --opt 6
   python3 ./get_live_data_dwarf.py --opt 6 --dir ImportDir --history

NB : The IP of the dwarf must be saved first.