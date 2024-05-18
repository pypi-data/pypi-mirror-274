# API for finding same type of files and copy in a specific path

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   

[Follow Doveloper](https://www.instagram.com/nicky_connects/?next=%2F)
## Functionality of the Library

- Copy/Move Files Recursively.
- zip/unzip Files Recursively.
- List all the files and folders and subfolders of given path.
- In google drive you cannot directly see the size of the folder which is possible with sproject.
- count the number of files/folders and subfolders recursively.
- Encrypt and Decrypt the files using AES algorithm.(Better results with Minimum of 8GB RAM)
- You can Split and Merge the large file into Smaller Chunks and viceversa.
- Automatically Playing in Queue
- Play Selected song from Playlist

## Usage

- Make sure you have Python installed in your system.
- Run Following command in the CMD.
 ```
  pip install sproject
  ```
## Example

 ```
 #test.py
from NTools import copy_files

#Make sure you entered the correct file extension.
extension = '.pdf'

# enter the source and destination path as follows
s_path = "your source directory"
d_path = "your destination directory"

# Now the Function call should be like this
copy_files(s_path,d_path,extension)
  ```

## Run the following Script.
 ```
  python test.py
 ```

## Output 
- x files copied
- No files found with the extension

## Note 
- I have tried to implement all the functionality, it might have some bugs also. Ignore that or please try to solve that bug.
