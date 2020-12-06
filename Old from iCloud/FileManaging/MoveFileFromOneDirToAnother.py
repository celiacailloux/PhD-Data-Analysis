import os
import shutil

src_files = os.listdir(src)
for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if (os.path.isfile(full_file_name)):
        shutil.copy(full_file_name, dest)
        
#PYTHONPATH=/home/alvas/python/lib:/usr/local/python/lib /home/alvas/scripts/bar.py
cp /home/usr/dir/{file1,file2,file3,file4} /home/usr/destination/
