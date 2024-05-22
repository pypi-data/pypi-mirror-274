import pathlib
import shutil
import os,time,zipfile
from tqdm import tqdm
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
def delete_files(source_dir, keyword=None):
  files_count = 0
  folders_count = 0
  for root, _, files in os.walk(source_dir):
    for file in files:
      # Construct the full file path
      file_path = os.path.join(root, file)

      # Apply keyword filter if provided
      if keyword and keyword.lower() not in file.lower():
        continue
      # Delete the file
      try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
        files_count += 1
      except Exception as e:
        print(f"Error deleting file: {e}")

    # After deleting files, check if the directory is empty
    if not os.listdir(root):
      # If empty, remove the directory
      try:
        os.rmdir(root)
        print(f"Deleted directory: {root}")
        folders_count += 1
      except Exception as e:
        print(f"Error deleting directory: {e}")
  print(f'{files_count} Files and {folders_count} Folders Deleted')
  
def list_files(source_dir, keyword=None):

  # Check if source directory exists
  if not os.path.exists(source_dir):
    print(f"Error: Source directory '{source_dir}' does not exist.")
    return

  # Loop through files in the source directory
  for filename in os.listdir(source_dir):
    if keyword:
      # Filter based on keyword (lowercase for case-insensitivity)
      if keyword.lower() not in filename.lower():
        continue
    file_size = os.path.getsize(filename)
    print(filename,file_size)

def copy_files(source_dir, destination_dir, keyword=None):
        for root, dirs, files in os.walk(source_dir):
    # Construct the corresponding subdirectory in the destination
            relative_path = os.path.relpath(root, source_dir)
            dest_subdirectory = os.path.join(destination_dir, relative_path)

    # Create the subdirectory in the destination if it doesn't exist
            if not os.path.exists(dest_subdirectory):
                os.makedirs(dest_subdirectory)

            for file in files:
                source_path = os.path.join(root, file)
                file_size = os.path.getsize(source_path)
                destination_path = os.path.join(dest_subdirectory, file)

            # Apply keyword filter if provided
                if keyword and keyword.lower() not in file.lower():
                    continue

                # Copy the file
                try:
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: '{source_path}' to '{destination_path}' size = {(file_size/1024)/1024}MB")
                except Exception as e:
                    print(f"Error copying file: {e} size = {(file_size/1024)/1024}MB")
def move_files(source_dir, destination_dir, keyword=None):
        for root, dirs, files in os.walk(source_dir):
    # Construct the corresponding subdirectory in the destination
            relative_path = os.path.relpath(root, source_dir)
            dest_subdirectory = os.path.join(destination_dir, relative_path)

    # Create the subdirectory in the destination if it doesn't exist
            if not os.path.exists(dest_subdirectory):
                os.makedirs(dest_subdirectory)

            for file in files:
                source_path = os.path.join(root, file)
                file_size = os.path.getsize(source_path)
                destination_path = os.path.join(dest_subdirectory, file)

            # Apply keyword filter if provided
                if keyword and keyword.lower() not in file.lower():
                    continue

                # Copy the file
                try:
                    shutil.move(source_path, destination_path)
                    print(f"Moved: '{source_path}' to '{destination_path}' size = {(file_size/1024)/1024}MB")
                except Exception as e:
                    print(f"Error moving file: {e} size = {(file_size/1024)/1024}MB")
            if not os.listdir(root):
            # If empty, remove the directory
              try:
                os.rmdir(root)
                print(f"Deleted directory: {root}")
              except Exception as e:
                print(f"Error deleting directory: {e}")
def greet(name : str) -> str:
    print(f'Hey {name}!')

def get_folder_details(folder_path: str,colab = False):
  if not colab:
    total_size = 0
    files_count = 0
    folders_count = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            files_count += 1
            a = f'{files_count} Files and {folders_count} Folders are found with the Total Size of {(total_size/1024)/1024} MB'
            spaces_needed = len(str(a)) + 1 
            backspaces = '\b' * spaces_needed
            print(f'{backspaces}{a}', end='', flush=True) 
            time.sleep(0.01)
        folders_count += 1
    return
  total_size = 0
  files_count = 0
  folders_count = 0
  for root, dirs, files in os.walk(folder_path):
      for file in files:
          file_path = os.path.join(root, file)
          total_size += os.path.getsize(file_path)
          files_count += 1
      folders_count += 1
  print(f'{files_count} Files and {folders_count} Folders are found with the Total Size of {(total_size/1024)/1024} MB')
def zip_files(input_folder, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(input_folder):
            count = 0
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, input_folder)  # Preserve relative structure
                zipf.write(file_path, arcname=arcname)
                count += 1
                a = f'{count} / {len(files)} files zipped'
                spaces_needed = len(str(a)) + 1
                backspaces = '\b' * spaces_needed
                print(f'{backspaces}{a}', end='', flush=True)
def unzip_files(zip_filename, extract_dir):
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        total_size = sum(zinfo.file_size for zinfo in zipf.infolist())  # Calculate total size
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Extracting") as pbar:
            for member in zipf.infolist():
                dirname = os.path.dirname(member.filename)
                if dirname:
                    os.makedirs(os.path.join(extract_dir, dirname), exist_ok=True)
                zipf.extract(member, extract_dir)
                pbar.update(member.file_size)
def decrypt(filename : str, key_file : str) -> str:
    with open(key_file, 'rb') as f:
        key = f.read()
    with open(filename, 'rb') as f:
        iv = f.read(16)
        ct = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    with open(filename[:-4], 'wb') as f:
        f.write(pt)
def encrypt(filename : str,path : str,key_path : str) -> str:
    with open(filename, 'rb') as f:
        data = f.read()
    with open(f'{key_path}', 'rb') as f:
        key = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    file_name = os.path.basename(filename)
    with open(f'{path}/{file_name}' + '.enc', 'wb') as f:
        f.write(iv)
        print(iv)
        f.write(ct_bytes)
        print(ct_bytes)