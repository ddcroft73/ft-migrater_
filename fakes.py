#fakefiles.py
# generate an array of fake files to test ft-migrater, tracks the locations
# and file names, so they can easily be removed after demo.
# Creates directories for user to move the demo files into when using ft-migrater.
# all

# creates as many fake files as needed and puts them in a new, or existing directory
# upt to 5 files types to test out the ability of the ft-migrater and see how it handles multiple file types
# Create directories for user to move the files to from ft-migrater.
# (existing directories may also be used.)  
# Cleans up the mess of scattered files from the computer after demo.
# All files and created directories are removed, no matter where they were migrated to.
#   ASSUMPTIONS:
#     During demo program assumes that only demo files have been moved... (I may code around this) 
#     

#TODO
# Make sure all options work singlularly and dont execeute if irrelevant
# add option to create directories for the migration as well as the demo files
#Finish Help
# Make program so that it overlooks any "real file types" it may come across in the 
# removal of the demo.
# 

import random
import os
import sys
import shutil


# ./demo.log was not finding this path on creation of the log, sometimes, but most times it
# would put the log in the demo directory. This is not what i want.
# forcing it this way seems to work better.
THIS_PATH = os.path.dirname(os.path.realpath(__file__))
LOG = os.path.join(THIS_PATH, "demo.log")
MIGRATE_LOG = "migrate_log.txt"


# DEMO CREATION ROUTINES----------------------------------------------------------------------------
def create_file(fname: str) -> None:
    with open(fname, "w") as f:
        f.write("")    
    
# much less likely to pick duplicate names, so user gets a more accurate # of demo files    
def rand_fname(name_list: list) -> str:
    # create a random # of names, out of a random woed in the list
    rnd_fname = [name_list[random.randint(1,6)] for _ in range(0,random.randint(1,5)) ] 
    return "".join(rnd_fname)

def make_filelist(fnames: list, ftypes: list, numfiles: int) -> list:
    return list(set([rand_fname(fnames) + ftypes[random.randint(0,5)] for _ in range(0,numfiles)]))

def create_working_dir(new_dir: str):    
   # go as deep as needed. 
   if not os.path.exists(new_dir):
      dirs = new_dir.split("\\")
      dirs = dirs[1:]
      root = os.path.abspath(os.sep)
      try:
         os.chdir(root)       
         for dir in dirs:
             if not os.path.exists(dir):
                os.mkdir(dir)   
                os.chdir(dir) 
          
         #creation_log(new_dir)   
      except:
          print("Dir(s) could not be created.. Make sure the string is a valid representation of a path. \n ie C:\\path\\path etc")


def creation_log(dir_name: str) -> None:
    with open(LOG, "w") as log_file:
        log_file.write(dir_name)    
    print("Demo log created:", os.path.abspath(LOG))

def create_homes() -> None:
    # TODO  Creates an array of directories to move the demo files to.
    pass


#DEMO REMOVAL ROUTINES --------------------------------------------------------------------------------

def get_last_created_dir_name() -> str:
    # see if the log exists
     if os.path.exists(LOG):
        with open(LOG, "r") as log_file:
           dir_name = log_file.readlines()[0]
     else:
         print(LOG, "not found.")
         exit(0)
     return dir_name

def remove_directories(path: str) -> None:
    # remove the directoy and all sub directories created for demo
    if os.path.exists(path):
        shutil.rmtree(path) 
        print(path, "has been removed.")
    else:
        print("No such directory.")


# find migrate_log.txt which is created by ft-migrater when files are moved out of
# the Home Path ASSUMES THAT ONLY DEMO FILES WILL BE IN LOG
def get_migratelog_data() -> list:
    # look for the"migrate_log.txt" in the demo directory
    demo_dir = get_last_created_dir_name()
    migrate_log_path = os.path.join(demo_dir, MIGRATE_LOG)
    # open and search the migrate_log.txt  file
    try:
       with open(migrate_log_path, "r") as mlog:        
          file_data = [line.strip("\n") for line in mlog.readlines() if line != "\n" and line[:5] != "FROM:"]

    except FileNotFoundError:
        print("Unable to find migrate_log.txt. Perhaps it was deleted, or the migration was not carried out.")
        exit(0)
    return file_data   

def parse_demofile_paths(data: list) -> list:
    # extract the file naem, and its location from the data list
    # MOVED: is where the filename is 
    # TO: is where the location is
    fname = [] 
    path = []
    # Need to build paths with this info in the order is in the list
    # Build a list of MOVED and a list of TO and then zip them
    for item in data:
        if item[0] == "M":
           fname.append(item[8:]) # remove all but the file info
        if item[0] == "T":
            path.append(item[8:])   
    
    return [os.path.join(path[x], fname[x]) for x in range(len(fname))]


def destroy_demo_files() -> None:
    # get all datat back in a list
    cont = input("WARNING: This program assumes all files in the migrate_log.txt file are demo files.\nAll files returned from the migrate log will be deleted.\n\nContinue (y/n)")
    if cont in ['Y', 'y']:
        mlog_data = get_migratelog_data()
        demofile_paths = parse_demofile_paths(mlog_data)
        try:
            for line in demofile_paths:
                print("Deleting:", line)
                os.remove(line)

        except Exception as er:
            print(f"an error occured removing demo files. {er}")    
        print("All demo files, tracked down and deleted.")    
    else:
        print("Program terminated.")
        exit(0)

def del_demolog(demo_log) -> None:
    try:
        os.remove(demo_log) 
        print("demo log deleted.")
    except Exception as er:
        print("error deleting demo log...", er)    

#   END DEMO REMOVAL CODE ------------------------------------------------------------------------------------------------    



def help() -> None:
    print("\nEnter a directory to create the demo files in. ex. C:\\test\\test etc.")      
    print("arg1 = The directory(s) to store files in.\narg2 = the number of files. 30ish if blank.\n\nTo cleanup after demo type: \n--all to get rid of all files and directories.\n--files to just delete the demo files.")
    exit(0)


def get_args(lst) -> tuple:        
    if len(lst) == 1: # no argumentws
        help()
    else:    
        match lst[1]:   # arg1
           case "--all" :   # destroy all tracks left by demo, files after migration, directories asnd demo log
              destroy_demo_files()
              remove_directories(get_last_created_dir_name()) 
              del_demolog(LOG) 
              exit(0)
           case "--files":  # delete files only , leaves the log and the directory(s)
              destroy_demo_files() 
              exit(0)
           case "--dir":    # delete just directories and all within
              remove_directories(get_last_created_dir_name())  
              del_demolog(LOG) 
              exit(0)   
           case "--log":   # remove the demolog
              del_demolog(LOG) 
              exit(0) 

           case _:          # The Path to create and number of files, any bullshit should be dealt with @ dir creation 
             dir = lst[1]    
        
        # no file number given  
        if len(lst) != 3:  
            numfiles = 50
        elif len(lst) == 3: 
           numfiles = int(lst[2])
    
    return dir, numfiles   




if __name__ == '__main__':


    file_names = ['_never_gonna', '_give_you', '_up_never', '_gonna_let', '_you_go', '_nevvvaa', "_"]
    file_types = [".xxx", ".read", ".psp", ".txt", ".log", ".rand"]
    
    working_dir, num_files = get_args(sys.argv)  
    file_list =  make_filelist(file_names, file_types, num_files)

    try:
       create_working_dir(working_dir)
       creation_log(working_dir)

       for file in file_list: 
           #print(os.path.join(working_dir, file))
           create_file(os.path.join(working_dir, file))

       print(len(file_list), "files created in", working_dir)    
    except:
       help()   # probably a command line error
