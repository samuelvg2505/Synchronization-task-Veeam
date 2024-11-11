import os
from filecmp import dircmp
import time
import shutil

src = 'C:/Users/samue/Documents/GitHub/test-task-veeam/src/'
replica = 'C:/Users/samue/Documents/GitHub/test-task-veeam/replica/'

dcmp = dircmp(src, replica)

def print_diff_files(dcmp):
    for name in dcmp.left_only: #copy file to replica

        creation_date = time.ctime(os.path.getctime(dcmp.left+"/"+name))
        if(os.path.isdir(dcmp.left+"/"+name)):
            print("New directory %s in src folder created at %s. Copying to replica" % (name, creation_date))
            shutil.copytree(dcmp.left+"/"+name, dcmp.right+"/"+name)
        else:
            print("New file %s in src folder created at %s. Copying to replica" % (name, creation_date))
            shutil.copy2(dcmp.left+"/"+name, dcmp.right+"/"+name)

    for name in dcmp.right_only: #delete file from replica

        creation_date = time.ctime(os.path.getctime(dcmp.right+"/"+name))
        if(os.path.isdir(dcmp.right+"/"+name)):
            print("Directory %s in replica folder created at %s was deleted in src folder. Deleting the directory" % (name, creation_date))
            shutil.rmtree(dcmp.right+"/"+name)
        else:
            print("New file %s in replica folder created at %s was deleted in src folder. Deleting the file" % (name, creation_date))
            os.remove(dcmp.right+"/"+name)

    for name in dcmp.diff_files: #delete file from replica and copy new one

        creation_date = time.ctime(os.path.getctime(dcmp.left+"/"+name))
        mod_date = time.ctime(os.path.getmtime(dcmp.left+"/"+name))
        if(not os.path.isdir(dcmp.left+"/"+name)):
            print("File %s in src folder created at %s was modified at %s. Copying to replica" % (name, creation_date, mod_date))
            shutil.copy2(dcmp.left+"/"+name, dcmp.right+"/"+name)

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

print_diff_files(dcmp)