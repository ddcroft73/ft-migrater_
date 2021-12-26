

## User Guide:

### Navigation:

  - The root drive, the default home path (Downloads folder), or any of the directories stemming from
  Drive C: can be selected from the combo box at the top. When the directory is selected, the treeview will
  be updated. THe Downloads folder, and the Home path (also refered to as sort path) will be #'s 2 and 3
  after drive C.
  - The current Home Path will always be the starting view point of the FileView\Treeview, and will change
  if the user decides to change it.
  - Click on the + Plus sign next to directory names to more consistently open directories. Double clicking
  also works but it less responsive.


### Selecting\Entering a File type:<br>
  - The application is ONLY concerend with the files and file types in the Home Path. 
  - Any file can be selected or deleted, but only files in the Home Path can be marked for migration.
  - File types may be selected by clicking on a file that is in the Home path diretory,
  or by typing the extension into the file type combo box. There does not have to be files of the
  entered type in the folder at the time. You can set destinations for future file types if you like.
  - Make sure you are in the Home directory and single click any file. THe File extension will be cast
  to the file type combo box, and if any instructions have been set, the destination will appear
  in the destination box. If not it will remain empty. This allows for faster type selection.
  
### Selecting\Entering a Destination:<br>
  - to select the destination, navigate to a different directory than the home path, and double click
  the directory name. THe name will be cast to the destination combo box.
  - Enter the path manually
  - If you want to move a file type to a directory that is yet to exist, Navigate to the parent directory
  and then type in the name of the new directory. It will be created before the move.

### Editing Destination instructions:
- Save
    - Once the Type and Destination requirements have been met, Click the "Save" Button. The instruction will be 
    saved and confirmatiion will be shown ino the status bar.
- Delete
    - Select the file type from the type combobox. The destintation as previously saved will be cast to the destination
    box. Click Delete.
- Delete All
    - Click "Delete All" All the previoous information will be discarded except for the Home Path. It can only be changed, via the "Path" tab.
- Update
    - You can pull up any destination for any type previously saved by selecting the type, the relevant path will be cast to the
    Destination and can be edited, and saved again.

### Changing the Home path:
  - Select the "Path" tab next to "Instructions
  - Navigate to a different directory. and click "Select".
  - Click the "Save" button

### Viewing Json and Log files:
  - Click the relevant box to make yoour choice.<br>
  **WARNING: Any changes made to the JSon file may effect the outcome of future migrations. The file may be 
  edited directly with the same results if need be, but the results may not show up inside the application right away.**  

### Logging:
  By default whenever a migration is finished, a log file will be generated and stored in the current
  Home path. The Files Original and destintion paths are logged as well as the date and time.
