# rename_date

## Description

This script allows to rename multiple files matched by pattern (regular expression) to "Cam YYYY-MM-DD HH\_SS\_(#).extension" or a given pattern
You need to start the script in folder where your files are holded or choose the directory by --input_folder command line argument.

## Usage

You can launch script in CLI mode with parameters, just double-click script in working directory (you might need to have a rename_config.ini)
  or drag the directory on the script via windows manager for it to be the only argument to the script (rename_config.ini would be checked for
  existance in the script's directory in this case)

### Possible command line arguments

- _--input\_folder=\<path/to/folder\>_ or _-if=\<path/to/folder\>_ \[default: _._ \] -
  It's the path to directory where files to rename are located.
- _--regexp=\<regexp\>_ or _-re=\<regexp\>_ \[default: _.\*\\.(\[jJ\]\[pP\]\[gG\]|\[aA\]\[vV\]\[iI\]|\[tT\]\[hH\]\[mM\])_ ] -
  By regular expression you can set which files are going to be renamed. examples:
  - _.\*_ for any file in directory. Basically, you can put dot with star at any RE. You can combine any of them as well.
  - _IMG.\*\\.jpg_ for any file which starts with capital "IMG" and ends with lower ".jpg"
  - _.\*\\.(jpg|avi)_ - any file which ends with dot and "jpg" or "avi"
  - _.\*\.\[jJ\]\[pP\]\[gG\]_ - any file which ends with dot and "jpg" in whichever case
  - _IMG-\[0-9\]+.\*_ - any file which starts with "IMG-", then comes at least one digit, and then anything
- _--output\_pattern=\<time.strftime pattern\>_ or _-op=\<time.strftime pattern\>_ \[default: _Cam %Y-%m-%d %H\_%S_ \] -
  It's the pattern to rename files. Their format will not be changed,
  and if there are some of them with the same patterned-names, "\_#" with number will be added.
  Number will have leading zeros if needed. Default pattern leads to "Cam YYYY-MM-DD HH\_SS\_(#).format"-like output names.
- _--dry\_run_ -
  Run script and output to console every operation which is to be done. You can use it to create bat-file of renaming, if you need.
  Operations are printed anyway, but without this parameter, they are printed to stderr.
- _--verbose_ - output all of the errors
- _--save\_config_ - save current configuration to "rename_example_config.ini"
- _--version_ - show version and exit

### rename_config.ini configuration file

On launch script tries to read \[default\] section of a file "rename_config.ini" in the current working directory. To get an example,
  you can just launch script in any place like `python rename_date.py --dry_run --save_config`, it will be saved as "renamce_example_config.ini",
  or you can give all of the needed parameters to the script and save them as well.  
  The full contents of the \[default\] section (you may skip any of them):

- input_folder
- regular\_expression
- output\_pattern
- no\_exif
