
# ------------------------------------------------------------------------------------------------
#  File Type Migrater ft-migrater-   main.py  Dec, 2021   DCroft 
#
#   A simple JSon editor GUI. Given a directory full of random files,exports the 
#   files across the computer using instructions set by the user. 
#       
#   Win 1- python 3.10 uses match case
#
#   Basic features as per client requirements: 
#     GUI with display of all files and directories of a predefined path.
#     Ability to move selected files to Recycle Bin.
#     Easy Selection of file types and destinantions.
#     Complete no typing interface. (Destnations may still be typed)
#     If a destination does not exist, it will be created.
#      (new directories can be quickly created by first selecting the parent directory)
#     Quick navigation of the instructions with real time updating. 
#     Ability to Add, Delete, Update instructions for a file type
#     Ability to change the path of the folder being sorted. 
#     Widgets should update according to any relative info, and only relative info
#      (when a file is selected a destination will display if an instruction has been set
#      remain blank if not)
#     Only files in the path to be sorted, "sort path" will be regarded.
#     JSon file viewer (the instructions can be hand edited and the program will adhere)
#  
#  In its simplest terms this program is a Json editor that uses the data to carry out 
#  the export of all file type instructions.    
# ------------------------------------------------------------------------------------------------ 

#TODO WOrk on nodes oening on view\update instead of having to manually open each
# diretory.
# Work on the Back upone function of treeview
# add support for other drives
# maybe incorporate 2 treeviews and redesign the relationship between Drive\Directories\Files

#import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, askquestion 
from send2trash import send2trash
import shutil

# required classes
from configurejson import *
from toolTips import CreateToolTip
from migrate import *
  
# Refactor all code to use pathlib instead of os... or maybe just use it next time  
DOWNLOADS_PATH = os.path.join(os.getenv('USERPROFILE'), 'Downloads') 
JSON_FILE = './instructions.json'   

#----------------------------------------------------------------------------------------
#  COMMAND BUTT0N EVENT FUNCTIONS
#----------------------------------------------------------------------------------------
def del_file(path: str) -> None:
    cont = ""
    cont =askquestion("Send to Recycle Bin", f"Are you are sure you want to delete: {path}\n\nContinue?", icon='question') 
    if cont == 'yes':
        send2trash(path)
        file_browse.update_view(getdir_only(path)) 

def del_directory(path: str) -> None:
    cont = ""
    cont =askquestion("Delete directory", f"Are you are sure you want to delete: {path}\nand all it's contents? \nThis cannot be undone. \n\nContinue?", icon='question') 
    if cont == 'yes':
        file_browse.go_upone(path)
        shutil.rmtree(path)
        parent = os.path.abspath(path)
        file_browse.update_view(getdir_only(parent))

def delete_path() -> None:  
    path = label_selected.cget('text')
    if label_selected.cget('text') == "":
        status_report(status_label," Nothing to remove.")
        return

    if os.path.isfile(path):
        del_file(path)        
    else:
        del_directory(path)

    status_report(status_label, f"{path} was removed.")    

def save() -> None:        
    filetype = filetype_combo.get()
    destination = filetype_dest_combo.get()
    if filetype == "" or destination == "": 
        showinfo("Invalid Type or destination", "File type information cannot be blank.\nPlease enter or select a vaild file type (extension), and\or destination.",
        icon="warning")
    else:    
        path = curr_spath_label.cget('text')
        config.update_data('add', ftype=filetype, spath=path, destination=destination)

def delete_type() -> None:
    filetype = filetype_combo.get()
    path = curr_spath_label.cget('text')
    if filetype == "" or destination == "": 
        showinfo("Invalid Type or destination", "File type information cannot be blank.\nPlease enter or select a vaild file type (extension), and\or destination.",
        icon="warning")
    else: 
        config.update_data('delete', ftype=filetype, spath=path)

# clear dictionary
def delete_all() -> None:
    path = curr_spath_label.cget('text')
    config.update_data('delall', spath=path)                    


def change_spath() -> None:
    new_spath = label_selected.cget('text') 
    if new_spath == "":
        showinfo("Need a path.", "Path cannot be blank.", icon='warning')
        return
    if new_spath == curr_spath_label.cget('text'):
        return
    config.change_spath(new_spath)
    # update the spath variable in the Json class since a change was just made
    config.refresh_data()
    curr_spath_label.configure(text=new_spath)
    file_browse.refresh_directories()
    file_browse.update_view(new_spath)

def select_path() -> None:
    path = label_selected.cget('text')
    if not os.path.isfile(path) and  path != "":
        change_spath_label.configure(text=path)

def view_json() -> None:
    showinfo("CAUTION"," Any changes made to the JSon file could result in abnormal performance. Changes may not be seen immedietley.", icon='warning')
    subprocess.call(['notepad.exe', JSON_FILE])  

def view_log() -> None:
    path = list(config.get_data(JSON_FILE,DOWNLOADS_PATH).keys())[0]
    fname = os.path.join(path, "migrate_log.txt")
    if os.path.exists(fname):
        subprocess.call(['notepad.exe', fname])
    else:
        showinfo("No Such File.", "No log has been created yet, or it was deleted.")    

def number_files() -> str:
    # So the user knows how many files are about to be moved.
    data = config.get_data(JSON_FILE,DOWNLOADS_PATH)
    spath = list(data.keys())[0]
    types = list(data[spath].keys()) 
    cnt = 0
    for file in os.listdir(spath):
        if getfile_ext(file) in types:
           cnt+=1
    return cnt

def move_files() -> None: 
    cont = askquestion("Confirm Request", f"You are about to move {number_files()} files.\nDo you wish to continue?")
    if cont == 'yes':
        migrate.disperse_files()

def exit_() -> None:
    main_win.quit()
    main_win.destroy()
    exit()


def create_directory() -> None:
    path = label_selected.cget('text')
    dir = new_directory.get()
    if os.path.isdir(path) and dir != "":
        new_path =os.path.join(path, dir)
        os.mkdir(new_path)
        file_browse.update_view(path)
        new_directory.delete(0, tk.END)
        status_report(status_label, f"Created {new_path}")
    else: status_report(status_label, "Nothing to Create")    

def upone_directoryy() -> None:
    file_browse.go_upone(label_selected.cget('text'))

# Checks to see if the homepath in the json is valid. 
# return it if it is, alert if not, load default path
def load_homepath() -> str:    
    path = list(config.get_data(JSON_FILE, DOWNLOADS_PATH).keys())[0]
    if not os.path.exists(path):
        showinfo("Home Path Not Found", "The current home path can not be found.", icon='info')
        return DOWNLOADS_PATH
    return path            

#-----------------------------------------------------------------------------------------
#  GUI EVENT HANDLERS
#----------------------------------------------------------------------------------------
def curr_path_changed(event=None):
    spath = change_spath_label.cget('text')
    curr_spath_label.configure(text=spath)
    file_browse.update_view(spath)

def filetype_changed(event=None):
    _type = file_type.get()
    _destination =  destination.get()
    if _type != "":
       config.show_instructions(_type)
       config.instruction_report(_type, _destination)
    
def type_destination_changed(event=None):
    file_browse.update_view(destination.get())


""" FileView class
treeview w/bundled widgets - DCroft (HobblinCobbler) 12Dec2021
Handles click selection of file and double click selection of directory
HAndles all loading, saving, manipulation of path information used to populate
and run the treeView, and combobox at the top to deliver the paths 

"""  
class FileView(object): 
    def __init__(self, master: str, path: str, text: str) -> None:
        self.nodes = {}
        frame = tk.Frame(master)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical',  command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.__update_path(text)
        
        self.tree.place(width=565, height=150, x =0, y=0)
        ysb.place(x=568, y=2, height =158)
        xsb.place(x=0, y=155, width=570)
        frame.place(width=595, height=175, x =-10, y=-10)

        # only gives access to the main directories off the root drive. Just a bit
        # to hasten the navigation of the drive. No support for other drives... yet
        self.directory_selected = tk.StringVar()
        self.directory_box = ttk.Combobox(main_win, textvariable=self.directory_selected, state='readonly')
        self.directory_box['values'] = self.__get_directories()
        self.directory_box.current(0)
        self.directory_box.place(width=312,x=10, y=20) #510
        self.directory_box.bind('<<ComboboxSelected>>', self.__path_changed)
        CreateToolTip(self.directory_box, "Select a directory to view its contents.")
        
        abspath = os.path.abspath(path)
        self.__insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.__open_node)
        self.tree.bind("<<TreeviewSelect>>", self.__select_item)
        self.tree.bind("<Double-1>", self.__set_destination_directory)        
        self.curr_path = abspath  
    
    def update_view(self, path: str) -> None:
        abspath = os.path.abspath(os.sep)
        # Dont allow any Bullshit to influence the treeview
        if os.path.isfile(path) or os.path.isdir(path):
           self.__set_path(os.path.join(abspath, path))
           self.__update_path(path)

    def refresh_directories(self) -> None:
        self.directory_box['values'] = self.__get_directories()
        
    def go_upone(self, path) -> None:
        subs = path.split(os.sep)
        root = subs[0] + os.sep
        
        if path != root and os.path.exists(path):
            parent = os.sep.join(subs[:-1])
            label_selected.configure(text=parent)
            self.update_view(parent)
        else: 
            status_report(status_label,"Already at root.")    
        

    # works in conjunction with os.path.isfile()
    def isfile(self,path) -> bool:
       res = True
       if "." not in path:
         res = False
       return res

    def __insert_node(self, parent: str, text: str, abspath: str) -> None:
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')      
    
    def __set_path(self, path: str) -> None:  
        self.tree.delete(*self.tree.get_children())      
        self.__insert_node('', path, path)  
        self.__update_path(path)   
    
    def __update_path(self, path: str) -> None:
        self.curr_path = path
        self.tree.heading('#0', text=path, anchor='w') 

    # Gets the top level directories stemming from the root drive
    def __get_directories(self) -> list:
        cdrive_paths = [p for p in os.listdir(os.path.abspath(os.sep))]   
        return self.__format_directories(cdrive_paths)

    # formats the directories in the root path to be useful as starting points in 
    # the treeview control. Maintains the root directory and the default sort path
    # as the first 2 always, Downloads folder will always be kept if spath is changed
    def __format_directories(self, lst: list) -> list:
        spath = list(config.get_data(JSON_FILE, DOWNLOADS_PATH).keys())[0]
        first_two = [os.path.abspath(os.sep)] + [os.path.join(spath)]  
        dloads_path = [os.path.join(DOWNLOADS_PATH)]        
        # if the default path was changed, retain access to the Downloads dir
        if spath != DOWNLOADS_PATH:          
            first_two += dloads_path

        root = os.path.abspath(os.sep)        
        #cleanup    Some directories cause Permissiion Errors
        formatted_dirs = first_two + [os.path.join(root, path) for path in lst if not self.isfile(path) 
                             and path != 'Documents and Settings' 
                             and path != "System Volume Information"
                             and path[0] != "$"]   
        return formatted_dirs

    def __get_selected(self) -> str:
        path = self.curr_path
        try:
            item = self.tree.selection()[0]
            parent_iid = self.tree.parent(item)
            node = []
            # go backward until reaching root
            while parent_iid != '':
                node.insert(0, self.tree.item(parent_iid)['text'])
                parent_iid = self.tree.parent(parent_iid)
            i = self.tree.item(item, "text")
            path = os.path.join(*node, i)
        except Exception or PermissionError:
            #get a tuple index error here. THis seems to passify it
            path = self.curr_path
        return path      

    def __path_changed(self,event=None) -> None:
        self.update_view(self.directory_selected.get())  

    def __open_node(self, event=None) -> None:
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)        
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            # sort the files according to extension, want to accomodate first zip, pdf, png, so reverse the sort
            # to make them easier to get at.
            files_dirs = sorted([file for file in os.listdir(abspath)], key=lambda x: getfile_ext(x), reverse=True)
            for path in files_dirs:
                if getfile_ext(path) != "ini":  # this could mess something up if moved.
                   self.__insert_node(node, path, os.path.join(abspath, path))              

    def __select_item(self, event=None) -> None:
        self.curr_path = self.__get_selected()
        self.__update_path(self.curr_path)   
        label_selected.configure(text=self.curr_path)
        if os.path.isfile(self.curr_path):           
           # only concerened with instructions for filetype in the spath
           if not os.path.isfile(self.curr_path) or getdir_only(self.curr_path) == curr_spath_label.cget('text'):
              filetype_combo.set(getfile_ext(self.curr_path))
              config.show_instructions(file_type.get())

    def __set_destination_directory(self, event=None) -> None:
        destination = curr_spath_label.cget('text')
        selection = self.__get_selected()
        if not os.path.isfile(selection):
           if destination != selection:
               filetype_dest_combo.set(selection)
#TODO               
# Dont let the same path be loaded int to the destination box as the Home path    
               # This is juat aggravating 
               """ showinfo("Same Destination", "Can't move to the same destination.\nIf you want to overlook a type, don't set any instructions.")
           else:"""
               

#----------------------------------------------------------------------------------
#  START BULK GUI CODE..  
#
# THe more i think about this app the more I am certain i could have 
# designed it so that the entire interface was wrapped in a class a lot 
# like i Did the FileView class. 
#----------------------------------------------------------------------------------- 
TK_WIDTH = 600
TK_HEIGHT = 445

main_win = tk.Tk()
TK_X = int(main_win.winfo_screenwidth()/2 - TK_WIDTH/2)
TK_Y = int(main_win.winfo_screenheight()/2.5 - TK_HEIGHT/2)
 # Set window in center screen with following way.
main_win.geometry(f"{TK_WIDTH}x{TK_HEIGHT}+{TK_X}+{TK_Y}")
main_win.resizable(False,False)
main_win.title('ft-migrater v1') # load the current version to the title
#      TreeView Frame
tree_frame = ttk.LabelFrame(main_win, borderwidth=15)
tree_frame.place(height=200, width=TK_WIDTH -10, x=3, y=25)

#=================================== TABBED CONTRAOL TO HOUSE ACCESS TO INSTRUCTIONS\SETTINGS ========================
tabControl = ttk.Notebook(main_win)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Instructions')
tabControl.add(tab2, text='Path')
tabControl.place(width=580, height=175,x=10,y=250)
#==================================== END TAB SETTINGS ==============================================================

#===================================== MANAGE DIRECTORY WIDGETS =========================================================

upone_button = ttk.Button(main_win, text="<", command=upone_directoryy)   
upone_button.place(width=30,height=23, x=322, y=19)
CreateToolTip(upone_button, "Go to parent directory")
new_directory = ttk.Entry()
new_directory.place(width=175, x=413-60, y=20)
CreateToolTip(new_directory, "Type in the directory name, navigate to the parent, and click 'Create'")
create_button = ttk.Button(main_win, text="Create", command=create_directory)   
create_button.place(width=57,height=23, x=530, y=19)
CreateToolTip(create_button, "Navigate to the directory you want to create in and select it, type in the new directory name and click 'Create'")

#===================================== CREATE DIRECTORY WIDGETS=========================================================

#==================================== SELECTED LABEL\BUTTON =========================================================
label_selected = ttk.Label(main_win, borderwidth=3, relief='solid',justify="left") # background="white",
label_selected.place(height=23, width=575, x=(10), y=225)
CreateToolTip(label_selected,"The current directory being sorted.")
# 
# File Delete Button
del_file_button = ttk.Button(main_win, text="Delete", command=delete_path)   
del_file_button.place(width=60,height=24, x=525, y=225)
CreateToolTip(del_file_button, "Move file to Recycle Bin.") 
#===================================== END SELECTION ================================================================

#===================================== FILETYPE ACTIONS ==============================================================
#
# File Type label 
label_file_type = ttk.Label(tab1, text="File types:")
label_file_type.place(height=25, width=400, x=(10), y=5,  bordermode='inside')
# # FILE TYPE COMBO BOX
file_type = tk.StringVar()
filetype_combo = ttk.Combobox(tab1, textvariable=file_type, state='readwrite')
filetype_combo.place(width=50, height=20, x=10, y=30)
filetype_combo.bind('<<ComboboxSelected>>', filetype_changed)
CreateToolTip(filetype_combo, text="Enter a file type to be moved, or select a file above and the type will be entered for you.") 
#========================================== END FILE TYPES =======================================================

#========================================== HOMEPATH TAB1 ========================================================
#
# Path of where to move file types:
label = ttk.Label(tab1, text="Current Path:",justify="left")
label.place(height=23, width=230, x=(110), y=5)
#Label FOR THE PATH TO BE SORTED.
curr_spath_label = ttk.Label(tab1, borderwidth=3, relief='solid', background="white", justify="left")
curr_spath_label.place(height=23,width=455,x=110, y=30)
# the first item in the list is always the one being supported
#
#========================================== HOMEPATH TAB1 =======================================================

#========================================== HOMEPATH\SETTINGS TAB2 ==============================================
# #  - SETTINGS FRAME -
settings_frame = ttk.LabelFrame(tab2, borderwidth=15, text="Change directory:")
settings_frame.place( height=135, width=TK_WIDTH -35, x=5, y=10)
# change to curr_spath
change_spath_label = ttk.Label(tab2,  borderwidth=3, relief='solid', background="white", justify="left")
change_spath_label.place(height=23, width=545,x=15, y=30)
CreateToolTip(change_spath_label, "The path currently being sorted. Select and save different directory to sort a different path. ")
#add new  Home path Button
change_path_button = ttk.Button(tab2, text="Save", command=change_spath)   
change_path_button.place(width=100,height=24, x=460, y=56)
CreateToolTip(change_path_button, "Add selected directory as a path to be sorted.")
# Select Button
select_button = ttk.Button(tab2, text="Select", command=select_path)   
select_button.place(width=100,height=24, x=360, y=56)
CreateToolTip(select_button, "Add selected directory as a path to be sorted.")
# view Json Button
json_button = ttk.Button(tab2, text="View Json", command=view_json)   
json_button.place(width=100,height=24, x=260, y=56)
CreateToolTip(json_button, "View json Source.")
# view Json Button
log_button = ttk.Button(tab2, text="View Log", command=view_log)   
log_button.place(width=100,height=24, x=160, y=56)
CreateToolTip(log_button, "View file migration log.")
#=========================================== END HOMEPATH TAB2 ==================================================

#=========================================== DESTINATIONS =======================================================
#
# File Destination for download folder moves Label 
label_file_action = ttk.Label(tab1, text="Destination:")
label_file_action.place(height=25, width=150, x=(10), y=55,  bordermode='inside')
#
destination = tk.StringVar()
filetype_dest_combo = ttk.Combobox(tab1, textvariable=destination, state='readwrite')
filetype_dest_combo.place(width=555,x=10, y=80)
filetype_dest_combo.bind('<<ComboboxSelected>>', type_destination_changed)
CreateToolTip(filetype_dest_combo, "Double click the folder above to select as the file types destination. Or enter the path of a directory you wish to create. If the path does not exist it will be created.")
#=========================================== END DESTINATIONS ===================================================

    
# ========================================== COMMAND BUTTONS ====================================================
#Delete  Button
delete_button = ttk.Button(tab1, text="Delete", command=delete_type)   
delete_button.place(width=100,height=25, x=5, y=115)
CreateToolTip(delete_button, "Deletes the instructions for a selected file type.")
#Delete All Button
delete_all_button = ttk.Button(tab1, text="Delete All", command=delete_all)   
delete_all_button.place(width=100,height=25, x=105, y=115)
CreateToolTip(delete_all_button, "Deletes all the instructions.")
#Save Button
save_button = ttk.Button(tab1, text="Save", command=save)   
save_button.place(width=100,height=25, x=205, y=115)
CreateToolTip(save_button, "Saves the instructions for this file type.")
#Sort Button
sort_button = ttk.Button(tab1, text="Move", command=move_files)   
sort_button.place(width=80,height=25, x=410, y=115)
CreateToolTip(sort_button, "Execute the sort instructions.")
#Exit Button
exit_button = ttk.Button(tab1, text="Exit", command=exit_)   
exit_button.place(width=80,height=25, x=490, y=115)
CreateToolTip(exit_button, "Good-Bye")
# Statusbar
status_label = ttk.Label(main_win, borderwidth=3,  relief='solid',justify="left")
status_label.place(height=20, width=590, x=(5), y=420)
CreateToolTip(status_label, "Status Bar")
#
#============================================= END COMMAND BUTTONS ==============================================



if __name__ == '__main__':
 
    # load app        
    config = ConfigureJson(JSON_FILE, DOWNLOADS_PATH, filetype_combo, filetype_dest_combo, status_label, curr_spath_label, change_spath_label)
    file_browse = FileView(tree_frame, path=load_homepath(), text="Select file or directory")
    migrate = FileMigration(JSON_FILE, DOWNLOADS_PATH, status_label, config)
    status_report(status_label, " Moves all files by type to pre designated locations.")
    config.load_data()      
    
    main_win.mainloop() 

