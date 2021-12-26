### This script uses a CLI to generate directories and bogus files to demomstrate the use of the ft-migrater.

  - Create a path to use as a home\start path in which to move files out of.
  - Create as many fake files as needed to demo the migration of files by type over the computer.
  - Create a destinaiton path to use as a location to migrate into
    (depending on the types generated, a directory for each will be created.)
  - Cleanup all created diirectories and files after the demo.
  - Only a Home\Start path is required to run the demo. THe files may be moved anywhere into 
  existing directories if desired. 
---  
 
fakes.py attempts to offer a clean precise file and directory setup with which to test [ft-migrater](). If for any reason the program exits, it will clean up all directories ad files if any it has created. Since all directories created will be removed it is not allowed to create sub directories for the demo inside pre-existing directoreis. If the user does not create the destination and wishes to move the demo files in preexisting directories, thes directories will not be removed but the files will be tracked down and desleted one by one.

---
~~~
Usage:  --flag<homepath> <numfiles> <destinationpath>

   Fluff for demo:
       C:\home\path 100 C:\Destination\path
       
       <homepath>         Required
       <numfiles>         May be omitted. d\Default is 10
       <destinationpath>  May be omitted. Wil not be created. Assumes user will use existing directories.
                          when using existing directories all files are tracked and deleted.
    
   Cleanup:
       --cleanall    Delete start\home path.
                     Delete all demo files.
                     Deletes all stand alone destination paths. No matter how deep
                     Delete demo log
       
       --dir         Delete all directories created by demo
                     Delete demo log
~~~


