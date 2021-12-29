# migrate.py
#import os
#import json 
from configurejson import *
from datetime import datetime
import shutil

LOG = "migrate_log.txt" 

""" class Migration-
Class handles all routines dealing with the movement of files from one directory to 
another. 

"""


class FileMigration:     
    def __init__(self, json_fname: str, default_path: str, status: object, config_json: ConfigureJson) -> None:       
        self.json_fname = json_fname
        self.default_path = default_path
        self.status = status
        self.spath = default_path
        self.config_json = config_json
    
    # the files in the "sort Path" are used as "keys" in a dictionary that contains
    # the destinations of each file, "values". 
    def disperse_files(self) -> None:
        json_data  = self.config_json.get_data(self.json_fname, self.default_path)
        self.spath =  list(json_data.keys())[0]
        self.key_list = self.__make_keylist(json_data) 
        # if no files match the keys in the json_data dict, nothing to do
        if not self.key_list: 
            status_report(self.status, "No relevant file types found.\nNothing to do") 
            self.log_move(note=" Files not found, attempted move at", do_time=True)             
        else:
            from_to_dict = self.__construct_dict(json_data)
            self.__exec_move_instructions(from_to_dict)
   

    # get all files to be moved
    def __make_keylist(self, json_data: dict) -> list:
        spath = self.spath
        types = list(json_data[spath].keys())        
        return [os.path.join(spath,file) for file in os.listdir(spath) if getfile_ext(file) in types and file != LOG]
    
    # make a dict to guide the migration key = From : Value = To
    def __construct_dict(self, json_data: dict) -> dict:
        paths = {}
        spath = self.spath
        for item in self.key_list:
            for key, value in json_data[spath].items(): 
                if getfile_ext(item) == key:
                     paths[item] = os.path.join(value, os.path.basename(item))
        return paths
    
    # make diretories if single directory, inside existing directory,
    # or directorys parents and subs
    def __create_diretories(self, new_path):
        path = ""
        dirs = new_path.split(os.sep)        
        for sub in dirs:
           path += (sub+os.sep)
           if not os.path.exists(path):
               os.mkdir(path)  

      # move em one by one        
    def __exec_move_instructions(self, paths) -> None:
        for _from, _to in paths.items():
            if not os.path.exists(getdir_only(_to)):
                self.log_move(note=f"Destintation path created:\n{getdir_only(_to)}")
                self.__create_diretories(getdir_only(_to))  
            try:
                shutil.move(_from ,_to)    
            except Exception as er:
                showinfo("Error", f"Error while moving files.\n{er}")
                self.log_move(note=f" Error Moving File: {_from}")
            self.log_move(from_path=_from, to_path=_to)

        status_report(self.status, f"{len(self.key_list)} files moved. Check log to confirm.")
        self.log_move(stamp=True) # Stamp with the time and date of move    
    
    # Keeps track of the actions and stores a text file in the sort path
    def log_move(self, from_path: str=None, to_path=None, stamp: bool=False, note: str=None, do_time: bool=False) -> None:
        now = datetime.now()
        date = now.strftime("%b-%d-%Y") 
        time = now.strftime("%H:%M:%S") 
        fname = os.path.join(self.spath, LOG)
        
        if from_path and to_path:
            output = f"\nMOVED:  {os.path.basename(from_path)} \nFROM:   {getdir_only(from_path)}  \nTO:     {getdir_only(to_path)}"
        if stamp:
            output = f"\n----------------------------- MIGRATION COMPLETED at: ({time}) on: ({date}) ----------------------------------"    
        if note:
            output = note
        if do_time:
            output = note + f" Time: {time}  Date: {date}"

        with open(fname, "a") as f:
            f.write(output + "\n")
