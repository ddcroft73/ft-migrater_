# migrate.py

import os
from configurejson import *
from datetime import datetime
import shutil


""" class Migration-
Class handles all routines dealing with the movement of files from one directory to 
another. 

"""
#  basic steps to migrate files
#
# Make list of all relevent files from the sort path
# Create dict of From\to paths (use the above list as the keys)
# loop over dict to move files


class FileMigration:     
    def __init__(self, json_fname: str, default_path: str, status: object) -> None:       
        self.json_fname = json_fname
        self.default_path = default_path
        self.status = status
        self.spath = default_path
    
    # the files in the "sort Path" are used as "keys" in a dictionary that contains
    # the destinations of each file, "values". 
    def disperse_files(self) -> None:
        _json_data  = ConfigureJson.get_data(self.json_fname, self.default_path)
        self.spath =  list(_json_data.keys())[0]
        self.key_list = self.__make_keylist(_json_data) 
        # if no files match the keys in the json_data dict, nothing to do
        if not self.key_list: 
            status_report(self.status, "No relevant file types found.\nNothing to do") 
            self.log_move(note=" Files not found, attempted move at", do_time=True)             
        else:
            _from_to_dict = self.__construct_dict(_json_data)
            self.__exec_move_instructions(_from_to_dict)
       
    # get all files to be moved
    def __make_keylist(self, json_data: dict) -> list:
        _spath = self.spath
        _types = list(json_data[_spath].keys())        
        return [os.path.join(_spath,file) for file in os.listdir(_spath) if getfile_ext(file) in _types]
    
    # make a dict to guide the migration key = From : Value = To
    def __construct_dict(self, json_data: dict) -> dict:
        _paths = {}
        _spath = self.spath
        for item in self.key_list:
            for key, value in json_data[_spath].items(): 
                if getfile_ext(item) == key:
                     _paths[item] = os.path.join(value, os.path.basename(item))
        return _paths

      # move em one by one        
    def __exec_move_instructions(self, paths) -> None:

        for _from, _to in paths.items():
            if not os.path.exists(getdir_only(_to)):
                self.log_move(note=f"Destintation path created:\n{getdir_only(_to)}")
                os.mkdir(getdir_only(_to))                
            try:
                shutil.move(_from ,_to)    
            except Exception as er:
                showinfo("Error", f"Error while moving files.\n{er}")
                self.log_move(note=f" Error Moving file: {_from}")
            self.log_move(from_path=_from, to_path=_to)

        status_report(self.status, f"{len(self.key_list)} files moved. Check log to confirm.")
        self.log_move(stamp=True) # Stamp with the time and date of move    
    
    # Keeps track of the actions and stores a text file in the sort path
    def log_move(self, from_path: str=None, to_path=None, stamp: bool=False, note: str=None, do_time: bool=False) -> None:
        _now = datetime.now()
        _date = _now.strftime("%b-%d-%Y") 
        _time = _now.strftime("%H:%M:%S") 
        fname = os.path.join(self.spath, "migrate_log.txt")
        if from_path and to_path:
            output = f"\nMOVED:  {os.path.basename(from_path)} \nFROM:   {getdir_only(from_path)}  \nTO:     {getdir_only(to_path)}"
        if stamp:
            output = f"\n----------------------------- MIGRATION COMPLETED at: ({_time}) on: ({_date}) ----------------------------------"    
        if note:
            output = note
        if do_time:
            output = note + f" Time: {_time}  Date: {_date}"


        with open(fname, "a") as f:
            f.write(output + "\n")

"""
        with open("./temp.json", "w") as file:
            json.dump(paths, file, indent=4)
"""