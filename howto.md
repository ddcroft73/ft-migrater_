

## User Guide:

### Navigation:

  - The root drive, the default home path (Downloads folder), or any of the directories stemming from
  drive C: can be selected from the combo box at the top. When the directory is selected, the file view will
  be updated. ThHe Downloads folder, and the Home path (also refered to as sort\start path) will be #'s 2 and 3
  after drive C.
  - The current Home path will always be the starting view point of the file view, and will change
  if the user decides to change to another home path.
  - Click on the + Plus sign next to directory names to more consistently open directories. Double clicking
  also works but it less responsive.
  - Click the small button witht the '<' to navigate to the parent of the current directory.
  - Manage Directory
     - Delete - Navigate to the directory you want to delete, select it, click Remove. This action cannot be undone.
     - Create - To create a directory, but not mark it as a destination, navigate to the directory you wish to create in. Select it. Type in the name. Click Create.
      


### Selecting\Entering a file type:<br>
  - The application is ONLY concerend with the file types in the Home Path. These are the only files you are allowed to select for movement. 
  - Any file can be selected or deleted, but only files in the Home Path can be marked for migration.
  - File types may be selected by clicking on a file that is in the Home path diretory,
  or by typing the extension into the file type combo box. There does not have to be files of the
  entered type in the folder at that time. You can set destinations for future file types if you like.
  - Make sure you are in the Home directory and single click any file. THe File extension will be cast
  to the file type combo box. If any instructions have been set, the destination will appear
  in the destination box when selected. If not it will remain empty. This allows for faster type selection.
  
### Selecting\Entering a Destination:<br>
  - To select the destination, navigate to a different directory than the home path, and DOUBLE click
  the directory name. THe name will be cast to the destination combo box.
  - Or enter the path manually
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
  - Click the relevant box to make yoour choice.
  **WARNING: Any changes made to the JSon file may effect the outcome of future migrations. The file may be 
  edited directly with the same results if need be, but the results may not show up inside the application right away.**  

### Logging:
  By default whenever a migration is finished, a log file will be generated and stored in the current
  Home path. The files original and destintion paths are logged as well as the date and time.
