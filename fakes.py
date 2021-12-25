#fakefiles.py
# generate an array of fake files to demo ft-migrater, tracks the locations
# and file names, so they can easily be removed after demo.
# Creates directories for user to move the demo files into when using ft-migrater.
# all

# creates as many fake files as needed and puts them in a new, or existing directory
# upt to 5 files types to test out the ability of the ft-migrater and see how it handles multiple file types
# Create directories for user to move the files to from ft-migrater.
# (existing directories may also be used.)  
# Cleans up the mess of scattered files from the computer after demo.
# All files and created directories are removed, no matter where they were migrated to.
#   WARNING:
#     Although existing directories may be used for the demo, --cleanall will delete them all
#     and --cleanstart will delete the demo Home\Start path. 
#     --files will not delete any directories from your computer.


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

         
def getfile_ext(fname: str) -> str:         
    return fname.split(".")[-1]  

# DEMO CREATION ROUTINES----------------------------------------------------------------------------

def help() -> None:
    _help = """\
To create the basic demo:\n\
   Usage:  C:\path 10 or C:\path (Do not use spaces in directory names.)\n\
   If the 2nd is omitted the default 10 files will be created.\n\
\n\
To create the demo with destination directories:\n\
   Usage:  C:\path 10 C:\Destination\path or C:\ path C:\Destintaion\Path\n\
\n\
Cleanup:\n\
   --cleanall    Removes all directories and files\n\
   --cleanstart  Removes all files and the start directory\n\
   --files       Removes only files. Reserves your directories\n    
\n\
WARNING: only use --cleanall and --cleanstart if the demo created the directories for you.\n\
ALL DIRECTORIES WILL BE DELETED. --files will not remove any directories, but it will track\n\
down all the fake files.    

    """
    print(_help) 
    exit(0)

# 
def create_demo(working_dir: str, num_files: int) -> None:
    file_names = ['_never_gonna', '_give_you', '_up_never', '_gonna_let', '_you_go', '_nevvvaa', "_"]
    file_types = [".htmx", ".cpq", ".pdg", ".txq", ".nyet", ".rand"]
    
    file_list =  make_filelist(file_names, file_types, num_files)
    
    try:
       create_working_dir(working_dir)
       creation_log(start_dir_name=working_dir)

       for file in file_list: 
           #print(os.path.join(working_dir, file))
           create_file(os.path.join(working_dir, file))

       print(len(file_list), "files created in", working_dir)    

    except Exception as er:
       print("Error occured creating demo.", er) 
       exit(1) 
    
    return [getfile_ext(ext) for ext in file_list]


def create_file(fname: str) -> None:
    with open(fname, "w") as f:
        f.write("")    
    
# much less likely to pick duplicate names, so user gets a more accurate # of demo files    
def rand_fname(name_list: list) -> str:
    # create a random # of names, out of a random woed in the list
    rnd_fname = [name_list[random.randint(1,6)] for _ in range(0,random.randint(1,5)) ] 
    return "".join(rnd_fname)

# TODO:
# Change File types randoms back to 5
def make_filelist(fnames: list, ftypes: list, numfiles: int) -> list:
    return list(set([rand_fname(fnames) + ftypes[random.randint(0,2)] for _ in range(0,numfiles)]))

# create directory new, or inside existing
def create_working_dir(new_dir: str) -> None:      
    path = ""
    subs = new_dir.split(os.sep)
    try:
       for sub in subs:
           path += (sub+os.sep)
           if not os.path.exists(path):
              #make this the start path to create in
              start_path = path
              os.mkdir(start_path)

    except Exception as er:
        print("Error Creating directory", er)         
        exit(1) 


# logs the Start directory name and the destination name if applicable
def creation_log(start_dir_name: str=None, destinations_dir_name: str=None) -> None:   
    
    if start_dir_name:
        with open(LOG, "w") as log_file:
            log_file.write(start_dir_name)    
        print("Demo log created:", os.path.abspath(LOG))        

    elif destinations_dir_name:
        with open(LOG, "a") as log_file_append:
            log_file_append.write(" " + destinations_dir_name)    
        print("Destinations created in", destinations_dir_name)    

# given a list of the file types created in create_demo(), make a directory for 
# each type inside the path passed in
def create_destinations(file_types: list, path: str) ->None:
    # create a sub directory for each type inside the directory user
    # entered
    dirs = set(file_types)
    #create the working directoy
    create_working_dir(path)
    try:
        os.chdir(path)
        for dir in dirs:
          if not os.path.exists(dir):
             os.mkdir(dir)

        creation_log(destinations_dir_name=path)
    except Exception as er:
        print("Error creating sub directories in", path, er)     
        exit(1)   

    

#DEMO REMOVAL ROUTINES --------------------------------------------------------------------------------

#Need to open the LOG and extract the path of the directory 
# the demo was created in, or the path to the destination dir
def get_dir_name(start: bool=False, destination: bool=False) -> str:    
     if os.path.exists(LOG):
         if start:
            with open(LOG, "r") as log_file:
               dir_name = log_file.readlines()[0].split()[0]
         if destination:
            with open(LOG, "r") as log_file:
               dir_name = log_file.readlines()[0].split()[1]       
     else:
         print(LOG, "not found.\nProgram Terminated")
         exit(1)
     return dir_name


# remove the all directories created by demo
# WARNING: WILL REMOVE ANY DIRECTORY
def remove_directory(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path) 
        print(path, "has been removed.")
    else:
        print("No such directory.\nProgram Terminated.", path)
        exit(1)


# find migrate_log.txt which is created by ft-migrater when files are moved out of
# the Home Path ASSUMES THAT ONLY DEMO FILES WILL BE IN LOG
def get_migratelog_data() -> list:
    # look for the"migrate_log.txt" in the demo\START directory
    demo_dir = get_dir_name(start=True)
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


# Destroys all Fake Demo files that were generated. THis routine
# will find the location of ALL the files that ft-migrater moved in the demo.
# and remove them from the computer.
def destroy_demo_files() -> None:
    # get all datat back in a list
    mlog_data = get_migratelog_data()
    demofile_paths = parse_demofile_paths(mlog_data)
    try:
        for path in demofile_paths:
           print("Deleting:", path)
           os.remove(path)

    except Exception as er:
        print(f"An error occured removing demo files. {er}")        
    print("All demo files, tracked down and deleted.")       


def del_demolog(demo_log) -> None:
    try:
        os.remove(demo_log) 
        print("demo log deleted.")
    except Exception as er:
        print("error deleting demo log...", er)    

#   END DEMO REMOVAL CODE ------------------------------------------------------------------------------------------------    


def cleanall() -> None:    
    print("\nWARNING: If you moved any demo files using ft-migrater to a directory you need, \nie. Ones not created by the demo, this option will delete it.")
    cont = input("\n--cleanall: Remove:\n\nAll fake demo files.\nRemove created starting directory.\nRemove destination diretories.\nDelete the demo log.\n\nContinue? [y,n]")
    print(cont)
    if cont in ['Y', 'y']:
        destroy_demo_files()
        remove_directory(get_dir_name(start=True)) 
        remove_directory(get_dir_name(destination=True))
        del_demolog(LOG) 
    else:
        print("Program Terminated.")    
    exit(0)
    
def cleanstart() -> None:
     cont = input("Clean start: Remove:\n\n All fake demo files.\nRemove created starting directory.\nDelete the demo log.\n\nContinue? [y,n]")
     if cont in ['Y', 'y']:
         print("clean only files and the starting directory.")
         destroy_demo_files()
         remove_directory(get_dir_name(start=True)) 
         del_demolog(LOG)
     else:
        print("Program Terminated.")   
     exit(0)  

def clean_only_files() -> None:
     cont = input("Delete only the Fake files used in the demo.\n\nContinue? [y,n]")
     if cont in ['Y', 'y']:
         print('Delete only the fake files')
         destroy_demo_files()
         del_demolog(LOG)
     else:
       print('Program Termited.')      
     exit(0)              

         
"""
3 arguments only
arg[1] - either a path, or a command
arg[2] - num of files, or path to the destinationd directoies
arg[3] -path, numfiles, destination

To create the basic demo:
   C:\path 10, or C:\path If the 2nd is omitted the default 10 files will be created

To create the demo with destination directories:
   C:\path 10 C:\Destination\path or C:\ path C:\Destintaion\Path   

Cleanup:
   --cleanall    Removes all directories and files
   --cleanstart  Removes all files and the start directory
   --files       Removes only files. reserves your directories  
"""
def parse_args(arg) -> None:                    
    dest_dir = "" # assume basic demo

    # decide what dealing with, and make assignments...
    match len(arg):
        case 1:          # no argumentws, or one argument
            help()

        case 2:          # one argument, cleanup or using basic demo with default number of files
            match arg[1]:
                case "--cleanall":
                    cleanall()
                case "--cleanstart":
                    cleanstart()                    
                case "--files":
                    clean_only_files()      

            # basic default demo
            doing = 'basic'
            start_dir = arg[1]
            numfiles = 10     
        case 3:           # user entered 2 arguments,  
            # one is demo path, 2 is either numfiles, or destination path 
            if arg[2].isdigit():
                doing = 'basic'
                start_dir = arg[1]
                numfiles = int(arg[2])
            else:  # path, destPath
                doing = 'full'    
                start_dir = arg[1]
                dest_dir = arg[2]
                numfiles = 10                
        case 4:           # user entered 3 comands
            # path, numfiles, destination path
            doing = 'full'
            start_dir = arg[1]
            numfiles = int(arg[2]) 
            dest_dir = arg[3]  
     
    #execute the demo. create directories and spawn fake files
    match doing:
        case 'full':   
            files_types = create_demo(start_dir, numfiles) 
            create_destinations(files_types, dest_dir)
        case 'basic':
            create_demo(start_dir, numfiles)
            

# START PROGRAM
if __name__ == '__main__':
    parse_args(sys.argv)
    



