plain text

TODO:

_Need to do something about if the Home path doesn not exist. How to know before migration
Important incase user deletes the directory 
fix bug that doesnt allow the new spath to be put in the navigation combo until restartt


User Guide:

Navigation:
  _The root drive, the default home path (Downloads folder), or any of the directories stemming from
  Drive C: can be slected from the combo box at the top. When the directory is selected, the treeview will
  be updated. THe Downloads folder, and the Home path (also refered to as sort path) will be #'s 2 and 3
  after drive C.
  _The current Home Path will always be the starting view point of the FileView\Treeview, and will change
  if the user decides to change it.
  _Click on the + Plus sign next to directory names to more consistently open directories. Double clicking
  also works but it less responsive.

Selecting\Entering a File type:
  _The application is ONLY concerend with the files and file types in the Home Path. 
  _Any file can be selected or deleted, but only files in the Home Path can be marked for migration.
  _File types may be selected by clicking on a file that is in the Home path diretory,
  or by typing the extension into the file type combo box. There does not have to be files of the
  entered type in the folder at the time. You can set destinations for future file types if you like.
  _Make sure you are in the Home directory and single click any file. THe File extension will be cast
  to the file type combo box, and if any instructions have been set, the destination will appear
  in the destination box. If not it will remain empty. This allows for faster type selection.
  
Selecting\Entering a Destination:
  _to select the destination, navigate to a different directory than the home path, and double click
  the directory name. THe name will be cast to the destination combo box.
  _Enter the path manually
  _If you want to move a file type to a directory that is yet to exist, Navigate to the parent directory
  and then type in the name of the new directory.


Editing Destination instructions:
   Save
    _Once the Type and Destination requirements have been met, Click the "Save" Button. The instruction will be 
    saved and confirmatiion will be cast to the status bar.
  Delete 
    _Select the file type from the type combobox. The destintation as previously saved will be cast to the destination
    box. Click Delete.
  Update
    _You can pull up any destination for any type previously saved by selecting the type, the relevant path will be cast to the
    Destination and either can be edited, and saved again.

Changing the Home path:
  _Select the "Path" tab next to "Instructions
  _Navigate to a different directory. and click "Select".
  _Click the "Save" button

Viewing Json and Log files:
  _ Click the relevant box to make yoour chice.
  WARNING: ANy changes made to the JSon file can effect the outcome of future migrations. The file may be 
  edited directly with the same results if need be.  

Logging:
  By default whenever a migration is finished, or attempted, a log file will be generated and stored in the current
  Home path. The Files Original and and destintion paths are logged as well as the date and time.