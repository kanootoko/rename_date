# rename_date

This script allows to rename multiple files chosen by pattern (regular expression) to "Cam YYYY-MM-DD HH\_SS\_(#)"
You need to start the script in folder where your files are holded or choose the directory by --input_folder command line argument.

### Possible command line arguments
+ _--help_    
  Shows small help
+ _--input_folder=\<path/to/folder\>_ or _-if=\<path/to/folder\>_ \[default: _._ \]    
  It's the path to directory where files to rename are located.
+ _--regular_expression=\<regexp\>_ or _-re=\<regexp\>_ \[default: _.\*\\.(\[jJ\]\[pP\]\[gG\]|\[aA\]\[vV\]\[iI\]|\[tT\]\[hH\]\[mM\])_ ]    
  By regular expression you can set which files are going to be renamed. examples:
    + _.\*_ for any file in directory. Basically, you can put dot with star at any RE. You can combine any of them as well.
    + _IMG.\*\\.jpg_ for any file which starts with capital "IMG" and ends with lower ".jpg"
    + _.\*\\.(jpg|avi)_ - any file which ends with dot and "jpg" or "avi"
    + _.\*\.\[jJ\]\[pP\]\[gG\]_ - any file which ends with dot and "jpg" in whichever case
    + _IMG-\[0-9\]+.\*_ - any file which starts with "IMG-", then comes at least one digit, and then anything
+ _--output_pattern=\<time.strftime pattern\>_ or _-op=\<time.strftime pattern\>_ \[default: _Cam %Y-%m-%d %H\_%S_ \]    
  It's the pattern to rename files. Their format will not be changed,
  and if there are some of them with the same patterned-names, "\_#" with number will be added.
  Number will have leading zeros if needed. Default pattern leads to "Cam YYYY-MM-DD HH\_SS\_(#).format"-like output names.
+ _--dry\_run_    
  Run script and output to console every operation which is to be done. You can use it to create bat-file of renaming, if you need.
  Operations are printed anyway, but without this parameter, they are printed to stderr.
