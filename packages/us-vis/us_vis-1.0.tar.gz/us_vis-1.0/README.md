This is a series of script that allow to visualize and modify graphs obtain
through umbrella sampling calculations from 
AMBER (https://ambermd.org/index.php) and 
WHAM (http://membrane.urmc.rochester.edu/?page_id=126) software. The required
libraries are: PIL (pillow), python-math, pandas, matplotlib and itertools.  

If working through WSL on Windows you might need to install PyQt5 library for
plots to show up in separate windows.

workflow.py contains examplary workflow you might use to visualize separate
systems as well as merge the pictures into one.

File path should be specififed if the file is not in the same directory as the
scripts and file name should be specified without .csv or .png extensions. 
