

# User Guide:

## Navigation:
  - The root drive, the default home path (Downloads folder), or any of the directories stemming from Drive C: can be slected from the combo box at the top. When the directory is selected, the treeview will  be updated. THe Downloads folder, and the Home path (also refered to as sort path) will be #'s 2 and 3 after drive C.
  - The current Home Path will always be the starting view point of the File Viewer, and will change if the user decides to change it.
  - Back\Up one diretory - Click on the + Plus sign next to directory names to more consistently open directories. Double clicking also works but it less responsive.
  - Manage Directories
      - Create - Navigate to the directory with file viewer and select the directory which you want to create a directory in. Type the name in the box next to the 'Create' button. Click 'Create'. THis does not mark the new directory as a destination. See Selecting\Entering a Destination.
      - Remove - Naviagte to the directory you wish to remove, select the name, click 'Delete'. THis action unlike file delete can not be undone.

## Selecting\Entering a File type:
  - The application is ONLY concerend with the files and file types in the Home Path. 
  - Any file can be selected or deleted, but only files in the Home Path can be marked for migration.
  - File types may be selected by clicking on a file that is in the Home path diretory, or by typing the extension into the file type combo box. There does not have to be files of the entered type in the folder at the time. You can set destinations for future file types if you like.
  - Make sure you are in the Home directory and single click any file. THe File extension will be cast  to the file type combo box, and if any instructions have been set, the destination will appear in the destination box. If not it will remain empty. This allows for faster type selection.
  - Once a destination has been set for a type of file, that destination is added to the destination drop down box and can be used for a quick jump to view that directories contents and may be also selected to save as another destination for a different file type.
  
## Selecting\Entering a Destination:
  - To select the destination, navigate to a different directory than the home path, and DOUBLE click the directory name. THe name will be cast to the destination drop down box.
  - Or... Enter the path manually.
  - If you want to move a file type to a directory that is yet to exist, Navigate to the parent directory and then type in the name of the new directory.


## Editing Destination instructions:
  - Save:
      - Once the Type and Destination requirements have been met, Click the "Save" Button. The instruction will be  saved and confirmatiion will be posted to the status bar.
  - Delete:
      - Select the file type from the type combobox. The destintation as previously saved will be displayed in the destination box. Click Delete.
  - Update:
    - You can pull up any destination for any type previously saved by selecting the type, the relevant path will be displayed in the  Destination and can be edited, and saved again.

## Changing the Home path:
  - Select the "Path" tab next to "Instructions.
  - Navigate to a different directory. and click "Select".
  - Click the "Save" button.

## Viewing Json and Log files:
   Click the relevant box to make yoour chice.  <br><br>WARNING: Any changes made to the JSon file will effect the outcome of future migrations. The file may be  edited directly with the same results if need be, and the results of the edit may not show up right away in the application.  

## Logging:
  By default whenever a migration is finished, or attempted, a log file will be generated and stored in the current
  Home path. The Files Original and and destination paths are logged as well as the date and time.
