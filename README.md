﻿# rename_date

This script allows to rename multiple files chosen by pattern (regular expression) to "Cam YYYY-MM-DD HH\_SS\_(#)"
You need to start the script in folder where your files are holded or choose the directory by --input_folder command line argument.

### Possible command line arguments
+ --help    
  Shows small help
+ --input_folder=&ltpath/to/folder&gt or -if=&ltpath/to/folder&gt \[default: . \]    
  It's the path to directory where files to rename are located.
+ --regular_expression=&ltregexp&gt or -re=&ltregexp&gt \[default: .\*\\.(\[jJ\]\[pP\]\[gG\]|\[aA\]\[vV\]\[iI\]|\[tT\]\[hH\]\[mM\]) ]    
  By regular expression you can set which files are going to be renamed. examples:
    + ".\*" for any file in directory. Basically, you can put dot with star at any RE. You can combine any of them as well.
    + "IMG.\*\\.jpg" for any file which starts with capital "IMG" and ends with lower ".jpg"
    + ".\*\\.(jpg|avi)" - any file which ends with dot and "jpg" or "avi"
    + ".\*\.\[jJ\]\[pP\]\[gG\]" - any file which ends with dot and "jpg" in whichever case
    + "IMG-\[0-9\]+.\*" - any file which starts with "IMG-", then comes at least one digit, and then anything
+ --output_pattern=&lttime.strftime pattern&gt or -op=&lttime.strftime pattern&gt \[default: Cam %Y-%m-%d %H\_%S\]    
  It's the pattern to rename files. Their format will not be changed,
  and if there are some of them with the same patterned-names, "\_#" with number will be added.
  Number will have leading zeros if needed. Default pattern leads to "Cam YYYY-MM-DD HH\_SS\_(#).format"-like output names.
+ --dry\_run    
  Run script and output to console every operation which is to be done. You can use it to create bat-file of renaming, if you need.
  Operations are printed anyway, but without this parameter, they are printed to stderr.
