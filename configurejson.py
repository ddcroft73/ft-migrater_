

import json
import os
from tkinter.messagebox import askquestion, showinfo

# a couple utility functions
def getdir_only(fname: str) -> str:
    return '\\'.join(fname.split('\\')[0:-1])

def getfile_ext(fname: str) -> str:         
    return fname.split(".")[-1]  

def status_report(status: object, report: str) -> None:
    status.configure(text=report)

"""class ConfigureJson-
Handles all the data saved in json format, add, delete, update
as well as the updating of all widgets from the GUI, and 
rountines used to export the files using the data stored
in said Json.
"""

class ConfigureJson:
    def __init__(self, json_file: str, default_path: str,  
                type_cbox: object, type_dest_cbox: object, status: object,
                curr_spath_label: object, change_spath_label: object) -> None:        
        self.curr_json_data = {}
        self.json_file = json_file
        self.default_path = default_path
        self.type_cbox = type_cbox
        self.type_dest_cbox = type_dest_cbox
        self.curr_spath_label = curr_spath_label
        self.status = status
        self.change_spath_label = change_spath_label

    
    def get_data(self, fname: str, default_path: str=None) -> dict:  
        try: 
           with open(fname) as file:
              data = json.load(file)           
        except FileNotFoundError:     
          data = self.__create_json(fname, default_path) 

        except IndexError:
            showinfo("No Data Found", "JSon data has been corrupted. Restart program to create new file with default path.")
            os.remove(fname) 

        self.curr_json_data = data  
        return data

    def load_data(self) -> None:
        data = self.get_data(self.json_file, self.default_path)
        self.__populate_widgets(data)
        
    # Designates a new Sort/Home Path
    def change_spath(self, new_spath: str) -> None:
        data = self.get_data(self.json_file)
        old_spath = list(self.curr_json_data.keys())[0]
        data[new_spath] = data[old_spath]        
        del data[old_spath]
        self.__write(self.json_file, data )      
        status_report(self.status, f" {new_spath} is the new sort path.")

    def instruction_report(self, ftype: str, destination: str):
        self.status.configure(text=f" File type: {ftype.upper()}   Will be moved to: {destination.upper()} ")

    # lets the user see what has been set up and what has not, to make the 
    # setting of instructions and navigation easier\faster
    def show_instructions(self, data: str) -> None:
        spath = list(self.curr_json_data.keys())[0]
        try:
            value = self.curr_json_data[spath][data]
            self.type_dest_cbox.set(value)
        except KeyError:
            self.type_dest_cbox.set('') 

    # WHen a new spath (Home Path) is saved. Makes sure 
    # im still working with current data
    def refresh_data(self) -> None:
        data = self.get_data(self.json_file)
        self.curr_json_data = data

    def update_data(self, action: str, ftype: str=None,destination: str=None, spath: str=None) -> None:
        data = self.get_data(self.json_file)

        match action:        
            case "add":                
                self.__add(data, ftype, destination, spath)
            case 'delete':
                self.__del(data, ftype, spath)   
            case 'delall':
                self.__delall(data, spath)    

        self.curr_json_data = data 
        self.__write(self.json_file, data) 
        self.type_cbox['values'] = self.__dividata('types', data)
        self.type_dest_cbox['values'] = self.__dividata('destinations', data)

    def __populate_widgets(self, d_json: dict) -> None:    
        self.type_cbox['values'] =self.__dividata('types', d_json)  
        self.type_cbox.current(0)
        self.type_dest_cbox['values'] = self.__dividata('destinations', d_json) 
        self.type_dest_cbox.current(0)
        self.change_spath_label.configure(text=self.__dividata('path', d_json))   
        self.curr_spath_label.configure(text=self.__dividata('path', d_json)) 

    def __write(self,fname: str, data: dict) -> None:
        with open(fname, "w") as file:
            json.dump(data, file, indent=4) 

    def __create_json(self, fname: str, default_path: str) -> dict:
        d_template = {
          default_path : {}
        }    
        self.__write(fname, d_template)
        return d_template        
        
    
    def __dividata(self, whatpart: str, d_data: dict) -> list:
        spath = list(d_data.keys())[0]
        match whatpart:
          case 'path':
              target = spath
          case 'types':
             target = list(d_data[spath].keys()) 
             if not target:
                target = [""]  
          case 'destinations':
             target = list(d_data[spath].values()) 
             if not target:
                target = [""]
        return target        

    # tests for 3 possibilities
    # False if not saved at all                           (False)
    # True\False if Type is already saved,                (True,False)
    # and True\True if Type and destination are the same  (True, True)
    def __type_saved(self, ftype: str, dest: str,  data: dict) -> bool:
        spath = list(data.keys())[0]
        types = list(data[spath].keys())
        destinations = list(data[spath].values())
        if ftype in types and dest in destinations:       
            return (True, True)
        elif ftype in types and not dest in destinations: 
            return (True, False)
        return False

    # add a new type destination to dictionary or update type destination
    def __add(self, data: dict, ftype:str, destination: str, spath: str) -> None:
        result = self.__type_saved(ftype, destination, data)
        if result == (True, False):  # Destination does not match, but type has been saved, Could Overwrite
            cont = askquestion("Overwrite Previous Instruction?", 
                    f"File Type: {ftype.upper()} is marked for migration already.\nAre you sure you want to change the destination?", 
                    icon='question')                    
            if cont == 'no': 
               return
        elif result == (True, True): # Destination is the same  
              status_report(self.status, f" File Type: {ftype.upper()} has already been marked for this destination.")
              return

       
        if not os.path.exists(destination):
            cont = askquestion("No such directory", f"{destination} does not exist.\nSave anyway?")
            if cont == 'no': return        
        # save new instruction or update to new destination
        data[spath].update({ftype : destination})
        self.instruction_report(ftype, destination) 

    def __del(self, data: dict, ftype: str, spath: str) -> None:
        cont = askquestion("Delete current instruction", 
            f"Are you sure you want to delete File Type: {ftype.upper()}?", 
            icon='question')
        if cont == 'yes':        
           del data[spath][ftype]
           # select the first item unles this was the last then clear
           if len(data[spath]) > 0:
              self.type_cbox.current(0)
              self.type_dest_cbox.current(0)
           else:                
              self.type_cbox.set('')
              self.type_dest_cbox.set('') 

    def __delall(self, data: dict, spath: str) -> None:
         cont = askquestion("Clear all instructions?", "Are you sure you want to delete all instructions?", icon="question")
         if cont == 'yes':
            data[spath].clear()               
            self.type_cbox.set('')
            self.type_dest_cbox.set('') 

            
        
