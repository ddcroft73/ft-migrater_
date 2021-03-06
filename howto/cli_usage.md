### This script uses a CLI to generate directories and bogus files to demonstrate the use of the ft-migrater.

  - Create a path to use as a home\start path in which to move files out of.
  - Create as many fake files as needed to demo the migration of files by type over the computer.
  - Create a destinaiton path to use as a location to migrate into
    (depending on the types generated, a directory for each will be created.)
  - Cleanup all created diirectories and files after the demo.
  - Only a Home\Start path is required to run the demo. THe files may be moved anywhere into 
  existing directories if desired. 
---  
 
[demo.py](/ft-migrater_/demo.py) attempts to offer a clean precise file and directory setup with which to demo [ft-migrater](). If for any reason the program exits, it will clean up all directories and files if any, it has created. Since all directories created will be removed it is not allowed to create sub directories for the demo inside pre-existing directoreis. If the user does not create the destination and wishes to move the demo files in preexisting directories, thes directories will not be removed but the files will be tracked down and deleted one by one.

---
~~~
Usage:  demo.py <homepath> <numfiles> <destinationpath>

   Fluff for demo:
       demo.py C:\home\path 100 C:\Destination\path
       
       <homepath>         Required
       <numfiles>         May be omitted. Default is 10
       <destinationpath>  May be omitted. Wil not be created. Assumes user will use existing
                          directories. When using existing directories all files are tracked
                          and deleted.
    
   Cleanup:
       demo.py <option>
       --cleanall    Delete all demo files.
                     Delete home path.
                     Delete demo log.
                     
       --dir         Delete all directories created by demo
                     Delete demo log
                     
       Use --cleanall if you moved files to existing directories to seek them all out. If You did not
       move files to existing diretories, --dir will suffice because it deletes all directories created 
       by fakes.py. If you did both, use --cleanall.
~~~

WARNING: The file, demo.log contains the names of the directories to be removed by the --dir command and --cleanall. The program will not append any names that are not associated with the demo, or any directory names that are not safe to be deleted. But does not check to see if they were put there by the program before deletion. 
DO NOT EDIT THIS FILE, with any other directory names, and run a cleanup. It will delete the directories.
