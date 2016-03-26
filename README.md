A very simple command line peg solitaire game thrown together in a couple of hours.

To run execute either
```
make run
```
or
```
python src/main.py
```

Optional (to add a system-wide command 'pegs'):
	
1) Set environment variable $SCRIPTS to point to some (non-protected) directory.  For example, the following code might be added to your '~/.bashrc' file
```
export SCRIPTS='/home/username/Scripts'
```
followed by execution of
```
source ~/.bashrc
```
Make sure this directory exists.

2) Execute:
```
make install
```
This will copy the bash script 'pegs' from the bin subdirectory to '/bin/' and copy the current version of the python source code to a new directory in the $SCRIPTS path.

3) The game can now be run by executing
```
pegs
```
from the command prompt.
