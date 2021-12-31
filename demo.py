#  demo.py
#
# generate an array of fake files to demo ft-migrater.
#   Creates Start\Home path directories and fake files for the purpose of demonstrating ft-migrater. 
#   Creates Destination directories for each file type generated to offere a quick demo of ft-migrater.#    
#   tracks the locations and file names, so they can easily be removed after demo.
#   Removes all created directories and files spawneded by the demo 
#   Will not remove any directories or files not created by demo
#   Will not not create a dir inside an existing directory
#   Will not create sub directories in side root directory
#   If on creation of the destinations an existing dir is detected. will remove all previousy created
#   directories and files, exit and report.
#    

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
DEF_FILES_NUM = 10        

def getfile_ext(fname: str) -> str:         
    return fname.split(".")[-1]  

# DEMO CREATION ROUTINES----------------------------------------------------------------------------

# Sets up Basic Demonstration
def create_demo(working_dir: str, num_files: int) -> None:
    file_names = ['-nothing-here', '-fake-files', '-demo-use', '-empty', '-files', '-blank', "-random"]
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

# dont allow any duplicates
def make_filelist(fnames: list, ftypes: list, numfiles: int) -> list:
    return list(set([rand_fname(fnames) + ftypes[random.randint(0,2)] for _ in range(0,numfiles)]))

# program acts odd if user adds double os.sep, (as per testing for idiots)
# create_working_dir() will make weird ass directories
def cleanup_path(path:str) -> str:    
    clean_path = [sub for sub in path.split(os.sep) if sub != ""]
    return os.sep.join(clean_path)

# Creates new directory(s), Do not allow the user to create a directory inside an existing directory.
# Function may be called 2xs. first to create home path second if applicable to create destinations
# Function will not execute if user tries to create in an existing path, or tries to create 
# destinations inside existing paths. If trying to create destinations, and its an existing path
# or trying to use the root drive to creat destinaitons in, program will raise exception and 
# delete any previuosly created homepath, and only path as defined in demo.log.
#
def create_working_dir(new_dir: str, destinations: bool=False) -> None:      
    new_dir = cleanup_path(new_dir)
    path = ""
    subs = new_dir.split(os.sep)
    root = os.path.join(subs[0], os.sep) 
    # only allow directories to be created if all new, not inside existing        
    try:
       if len(new_dir) < 4: 
          path = new_dir 
          raise Exception  # root exists.. clean and exit

       for sub in subs:
           path += (sub+os.sep)
           if path != root:
               if os.path.exists(path):
                  raise Exception
               else:
                   print('creating',path)
                   os.mkdir(path)  
    except:
        print("Existing path detected.\nCannot create sub directories inside existing directories.")        
        print(f"Program terminated attempting to make:{path} ")  
        # if destinations, cleanup the HomePath that was already created.  
        if destinations:
            deldir()
        else:    
            # If Creating home path destinatioins=False, exit because the program will continue
            # and create the files, and log the directory if not.destinations will exit inside 
            # deldir()
            exit(1)    
            
# THis will make the demonstration of ft-migrater a bit faster. Gives the user a ready made 
# destination to move the files to and they dont need to worry about setting up test directories
# However, Any existing directory can be used. WILL NOT create any sub dirs for the types inside 
# an existiong directory
def create_destinations(filetypes: list, path: str) ->None:
    # create a sub directory only for each type in the file_types list
    dirs = set(filetypes)    
    #create the parent path, if not exists
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


# allows for deletion of the directories later on.
def creation_log(start_dir_name: str=None, destinations_dir_name: str=None) -> None:      
    if start_dir_name:
        with open(LOG, "w") as log_file:
            log_file.write(start_dir_name)    
        print("Demo log created:", os.path.abspath(LOG))        

    elif destinations_dir_name:
        with open(LOG, "a") as log_file_append:
            log_file_append.write(" " + destinations_dir_name)    
        print("Destinations appended to log, created in", destinations_dir_name)    


def demo_exists() -> bool:
    if os.path.exists(LOG):
        return True
    return False    

def demo_report() -> None:
    # determine if it was Home and destinations or just home    
    dest = get_dir_name(destination=True)
    home = get_dir_name(start=True)
    if dest == None:
        print(f"Traces of previous demo found in: \n{home}")
    else:
        print(f"Traces of previous demo found in: \n{home}\n{dest}") 
    print("Run 'demo --dir' to remove demo, Or delete the log and the directories above.")               

#DEMO REMOVAL ROUTINES --------------------------------------------------------------------------------

#lets me know where to find the migrate_log.txt file
#
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
    try:
       if os.path.exists(parent):
           shutil.rmtree(parent) 
           print(parent, "has been removed.")
       else:
           print("No such directory.", parent)

    except PermissionError:
        print("Another application is accesing the directory, perhaps a log file is open in Notepad.")       
        exit(1)


def get_migratelog_data() -> list:
    # look for the"migrate_log.txt" in the demo\START directory
    demo_dir = get_dir_name(start=True)
    migrate_log_path = os.path.join(demo_dir, MIGRATE_LOG)
    
    try:
       with open(migrate_log_path, "r") as mlog:                   
          file_data = [line.strip("\n") for line in mlog.readlines() if line != "\n" and line[:5] != "FROM:"]

    except FileNotFoundError:
        print("Unable to find migrate_log.txt. Perhaps it was deleted, or the migration was not carried out.\nAllowing directories to be removed...")
        file_data = None        
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
# each file afterthet were  moved to random directories. So if the user decides to not create the 
# destinations path this will effectively remove all the files. If the user just used the 
# directories created by the program, then they will be deleted with those directories
#
def destroy_demo_files() -> None:
    mlog_data = get_migratelog_data()    
    # if not a migrate log, files have not been moved. exit and let 
    # remove_directory() cleanup
    if mlog_data == None: return

    demofile_paths = parse_demofile_paths(mlog_data)
    try:
        for cnt, path in enumerate(demofile_paths):
           print("Deleting:", path)
           os.remove(path)
    except Exception as er:
        print(f"An error occured removing demo files. \n{er}")    

    print(f" {cnt+1} demo files tracked down and deleted.")      

def del_demolog(demo_log) -> None:
    try:
        os.remove(demo_log) 
        print("demo log deleted.")
    except Exception as er:
        print("error deleting demo log...", er)    


# Cleanup routines
def deldir() -> None:
    remove_directory(get_dir_name(start=True)) 
    remove_directory(get_dir_name(destination=True))
    del_demolog(LOG)    
    exit(0)

# Even though this function will facilitate a total clean of all directories created by sript
# It is best utilized when ft-migrter moves files to random directories selected by user.
def cleanall() -> None:    
    destroy_demo_files()
    deldir()
    exit(0)

#   END DEMO REMOVAL CODE ------------------------------------------------------------------------------------------------    

def help() -> None:
    _help = """\
\n------------------------------------------------------------------------------------------\n\
||  To create the basic demo:\n\
||    
||    Usage: <path> <numfiles>   (Do not use spaces in directory names.)\n\
||    
||           <numfiles> may be omitted. Default 10 files will be created.\n\
||
||  To create the demo with destination directories:\n\
||    
||    Usage: <path> <numfiles> <deestination> \n\
||    
||           <numfile>       may be omitted. Default 10 files will be created.\n\
||           <destination>   may be omitted. Assumes existing directory use\n\
||                           and files will be removed one by one.\n\
||
||  Cleanup:\n\
||    --cleanall    Removes all directories, files and log.\n\
||    --dir         Removes all directories but will not remove any files\n\
||                  that were moved to existing directories. use ---clearall.\n\
||                  Removes log.
||
||  Will effectively track down all fake files created by this program.
||  No pre-existing directories will be removed by this program. \
\n-----------------------------------------------------------------------------------------
    """
    print(_help) 
    exit(0)        

"""
Opted not to use an argumrnt parser, first time with CLI so... will learn it

accepts 3 arguments only
arg[1] - either a path, or a command
arg[2] - num of files, or path to the destinationd directoies
arg[3] - destination path

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
                   start_dir = arg[1] if not arg[1].isdigit() else help()
                   numfiles = DEF_FILES_NUM     

        case 3:           # user entered 2 arguments,  
            # one is demo path, 2 is either numfiles, or destination path 
            if arg[2].isdigit():
                doing = 'basic'
                start_dir = arg[1]     if not arg[1].isdigit() else help()
                numfiles = int(arg[2])
            else:  # path, destPath
                doing = 'full'    
                start_dir = arg[1] if not arg[1].isdigit() else help()
                dest_dir = arg[2]  
                numfiles = DEF_FILES_NUM                

        case 4:           # user entered 3 arguments
            # path, numfiles, destination path
            doing = 'full'
            start_dir = arg[1]     if not arg[1].isdigit() else help()
            numfiles = int(arg[2]) if arg[2].isdigit() else DEF_FILES_NUM
            dest_dir = arg[3]      if not arg[3].isdigit() else help()
           
        case _:           # user has no idea how to use the demo
            help()    

    if not demo_exists(): 
        #execute the demo. create directories and spawn fake files
        match doing:
            case 'full':   
                files_types = create_demo(start_dir, numfiles) 
                create_destinations(files_types, dest_dir)
            case 'basic':
                create_demo(start_dir, numfiles)
    else:
        demo_report()
        



if __name__ == '__main__':
    parse_args(sys.argv)
    



