### This script uses a CLI to generate directories and bogus files to demomstrate the use of the ft-migrater.

  - Create a path to use as a home\start path in which to move files out of.
  - Create as many fake files as needed to demo the migration of files by type over the computer.
  - Create a destinaiton path to use as a location to migrate into
    (depending on the types generated, a directory for each will be created.)
  - Cleanup all created diirectories and files after the demo.
  - Only a Home\Start path is required to run the demo. THe files may be moved anywhere into 
  existing directories if desired. 
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

### Behavior 

   #### fakes.py attempts to offer a clean precise file and directory setup with which to test [ft-migrater]() 
---

WARNING: For destinations, existing directories may be used. However DO NOT create a home path or
a destination INSIDE of an existing directoy. All parent as well as sub directories associated with
this demo will be removed. FIle removal is safe and effective and will not leave any bogus files after
demo.
