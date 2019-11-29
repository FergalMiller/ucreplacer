# ucreplacer.py

ucreplacer is a script that quickly replaces all occurrences of specified illegal characters with its unicode escaped counterpart.

Illegal characters are specified before running.

ucreplacer can be used on a single target file; or a target directory and file extension and be specified. ucreplacer will replace all illegal characters in files that match the specified target.

### Set up

ucreplacer relies on `native2ascii`. Ensure this is available on your system.

To specify the characters you would like escaped you must put them in an `illegalchars.txt` file.
This must be in the same directory as `ucreplacer.py`.

ucreplacer will create a `temp.txt` and `schema.txt` so the script will need read/write/delete permissions.

### Running

Single file character replacement is the default. You may pass ucreplacer the file path as an argument, if not you will be prompted for it.

e.g. `ucreplacer.py rootdir/mydir/test.properties`

Bulk file character replacement can be achieved by running ucreplacer with `bulk` as the first argument. 
You can supply the target directory and target file extension as arguments (in that order), if not you will be prompted for them.

e.g. `ucreplacer.py bulk rootdir/mydir .properties`

__**Be aware that there is no way (using ucreplacer) to undo the actions carried out by ucreplacer, so please ensure your target file or directory is correct before running.**__

