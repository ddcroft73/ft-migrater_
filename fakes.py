#  fakes.py
#
# generate an array of fake files to demo ft-migrater.
#   Creates Start\Home path directories and fake files for the purpose of demonstrating ft-migrater. 
#   Creates Destination directories for each file type generated to offere a quick demo of ft-migrater.#    
#   tracks the locations and file names, so they can easily be removed after demo.
#   Removes all created directories and files spawneded by the demo 
#   Will not harm any directories or files not created by demo

import random
import os
import sys
import shutil

# ./demo.log was not finding this path on creation of the log, sometimes, but most times it
# would put the log in the demo directory. This is not what i wanted.
# forcing it this way seems to work better.
THIS_PATH = os.path.dirname(os.path.realpath(__file__))
LOG = os.path.join(THIS_PATH, "demo.log")

MIGRATE_LOG = "migrate_log.txt"

         
def getfile_ext(fname: str) -> str:         
    return fname.split(".")[-1]  

# DEMO CREATION ROUTINES----------------------------------------------------------------------------

def help() -> None:
    _help = """\
\n--------------------------------------------------------------------------------\n\
||  To create the basic demo:\n\
||    Usage: <path> <numfiles>   (Do not use spaces in directory names.)\n\
||           <numfiles> may be omitted. Default 10 files will be created.\n\
||
||  To create the demo with destination directories:\n\
||    Usage: <path> <numfiles> <deestination> \n\
||           <numfile> may be omitted. Default 10 files will be created.\n\
||           <destination> may be omitted. Assumes existing directory use\n\
||                         and files will be removed one by one.\n\
||
||  Cleanup:\n\
||    --cleanall    Removes all directories, files and log.\n\
||    --dir         Removes only files, log.\n\
||
||  Will effectively track down all fake files created by this script.
||  No pre-existing directories will be harmed in this demo \
\n--------------------------------------------------------------------------------
    """
    print(_help) 
    exit(0)

# Sets up Basic Demonstration
def create_demo(working_dir: str, num_files: int) -> None:
    file_names = ['_never_gonna', '_give_you', '_up_never', '_gonna_let', '_you_go', '_nevvvaa', "_"]
    file_types = [".htmx", ".cpq", ".pdg", ".txq", ".nyet", ".rand"]
    
    file_list =  make_filelist(file_names, file_types, num_files)
    
    try:
       create_working_dir(working_dir)
       for file in file_list: 
           #print(os.path.join(working_dir, file))
           create_file(os.path.join(working_dir, file))
       print(len(file_list), "files created in", working_dir)    
       
       creation_log(start_dir_name=working_dir)
    except Exception as er:
       print("Error occured creating demo.", er) 
       exit(1) 
    # return only the etrensions [file types] to aid in setting up destinations
    return [getfile_ext(ext) for ext in file_list]

#Makes bogus files to play with. Couldnt think of anything clever here :(
def create_file(fname: str) -> None:
    with open(fname, "w") as f:
        f.write("")    
      
def rand_fname(name_list: list) -> str:
    # much less likely to pick duplicate names, so user gets a more accurate # of demo files  
    rnd_fname = [name_list[random.randint(1,6)] for _ in range(0,random.randint(1,5)) ] 
    return "".join(rnd_fname)

#TODO:
#  CHANGE 2 Back to 5

# dont allow any duplicates
def make_filelist(fnames: list, ftypes: list, numfiles: int) -> list:
    return list(set([rand_fname(fnames) + ftypes[random.randint(0,2)] for _ in range(0,numfiles)]))

# create new directory(s), Do not allow the user to create a directory inside an existing directory.
def create_working_dir(new_dir: str, destinations: bool=False) -> None:      
    path = ""
    subs = new_dir.split(os.sep)
    root = os.path.join(subs[0], os.sep) 
    # only allow directories to be created in root. Check the path to see if  createing 
    # a dir inside one that exists.
    try:
       for sub in subs:
           path += (sub+os.sep)
           if path != root:
               # if any part of this path exists, exit with warning , cleanup previous work
               if os.path.exists(path):
                  raise Exception
               else:
                   os.mkdir(path)   
    except:
        print("Existing path detected.\nCannot create sub directories inside existing directories.")    
        # if destination run, cleanup the HomePath that was already created.
        if destinations: deldir()
            

# allows for deletion of the directories later on.
def creation_log(start_dir_name: str=None, destinations_dir_name: str=None) -> None:      
    if start_dir_name:
        with open(LOG, "w") as log_file:
            log_file.write(start_dir_name)    
        print("Demo log created:", os.path.abspath(LOG))        

    elif destinations_dir_name:
        with open(LOG, "a") as log_file_append:
            log_file_append.write(" " + destinations_dir_name)    
        print("Destinations created in", destinations_dir_name)    

# THis will make the demo of ft-migrater a bit faster. Gives the user a ready made 
# destination to move the files to and they dont need to worry about setting up test directories
# However, Any existing directory can be used.
def create_destinations(filetypes: list, path: str) ->None:
    # create a sub directory only for each type in the file_types list
    dirs = set(filetypes)    
    create_working_dir(path, destinations=True)
    try:
        # mkes sure create the dir in the right parent.
        # dont need the full path
        os.chdir(path)
        for dir in dirs:
          if not os.path.exists(dir):
             os.mkdir(dir)

        creation_log(destinations_dir_name=path)
    except Exception as er:
        print("Error creating sub directories in", path, er)     
        exit(1)   
    
#DEMO REMOVAL ROUTINES --------------------------------------------------------------------------------

#lets me know where to find the migrate_log.txt file
def get_dir_name(start: bool=False, destination: bool=False) -> str:    
     
     try: 
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
     except IndexError:
        # this just means the user did not create a new destination direcctory
        # and opted to use existing. There is no path to retreive. 
        dir_name = None
     return dir_name


# make sure to get the parent directory and not just the
# last path created. C:\path\path, always get the parent as well
def remove_directory(path: str) -> None:
    # exit because there was no directory saved to delete. user defined 
    # destination path.
    if path == None: return

    subs = path.split(os.sep)
    parent = os.sep.join(subs[:2])

    if os.path.exists(parent):
        shutil.rmtree(parent) 
        print(parent, "has been removed.")
    else:
        print("No such directory.", parent)


def get_migratelog_data() -> list:
    # look for the"migrate_log.txt" in the demo\START directory
    demo_dir = get_dir_name(start=True)
    migrate_log_path = os.path.join(demo_dir, MIGRATE_LOG)
    
    try:
       with open(migrate_log_path, "r") as mlog:                   
          file_data = [line.strip("\n") for line in mlog.readlines() if line != "\n" and line[:5] != "FROM:"]

    except FileNotFoundError:
        print("Unable to find migrate_log.txt. Perhaps it was deleted, or the migration was not carried out.")
        exit(0)
    return file_data   


def parse_demofile_paths(data: list) -> list:
    # extract the complete file path from the data list
    # TO:    is where the location is
    # MOVED: is where the filename is 
    path = []
    fname = [] 
    # Need to build paths with this info in the order is in the list
    # all i care about is file path\name
    for item in data:
        if item[0] == "M":
           fname.append(item[8:])
        if item[0] == "T":
            path.append(item[8:])       
    return [os.path.join(path[x], fname[x]) for x in range(len(fname))]


# Destroys all generated Fake Demo files . 
# routine uses the the log generated by ft-migrater to retreive the locations of
# each file afterthet were  moved. So if the user decides to not create the 
# destinations path this will  effectively remove all the files. 
def destroy_demo_files() -> None:
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


def cleanall() -> None:    
    destroy_demo_files()
    remove_directory(get_dir_name(start=True)) 
    remove_directory(get_dir_name(destination=True))
    del_demolog(LOG) 
    exit(0)

def deldir() -> None:
    remove_directory(get_dir_name(start=True)) 
    remove_directory(get_dir_name(destination=True))
    del_demolog(LOG)    
    exit(0)


#   END DEMO REMOVAL CODE ------------------------------------------------------------------------------------------------    

         
"""
Opted not to use an argumrnt parser, firdt time with CLI so...

accepts 3 arguments only
arg[1] - either a path, or a command
arg[2] - num of files, or path to the destinationd directoies
arg[3] -path, numfiles, destination

To create the basic demo:
   C:\path 10, or C:\path If the 2nd is omitted the default 10 files will be created

To create the demo with destination directories:
   C:\path 10 C:\Destination\path or C:\ path C:\Destintaion\Path   

Cleanup:
   --cleanall    Removes directories, files, and log
   --dir         Removes directories created by demo, log
                 does not remove existing directories  
"""
def parse_args(arg) -> None:                    
    dest_dir = "" # assume basic demo

    # decide what dealing with, and make assignments...
    match len(arg):
        case 1:          # no arguments given
            help()

        case 2:          # one argument, cleanup or using basic demo with default number of files
            match arg[1]:
                case "--cleanall":
                    cleanall()  
                case "--dir":
                    deldir()   
                case _:
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
        case 4:           # user entered 3 arguments
            # path, numfiles, destination path
            doing = 'full'
            start_dir = arg[1]
            numfiles = int(arg[2]) 
            dest_dir = arg[3]  

        case _:           # user has no idea how to use the demo
            help()    
     
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
    



