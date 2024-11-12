import os
from filecmp import dircmp
import time
import shutil
import sys
import logging

def sync_files(dcmp, logger):
    for name in dcmp.left_only: #copy file to replica

        creation_date = time.ctime(os.path.getctime(dcmp.left+"/"+name))
        if(os.path.isdir(dcmp.left+"/"+name)):
            logger.info("New directory '%s' in src folder created at %s. Copying directory to replica" % (name, creation_date))
            shutil.copytree(dcmp.left+"/"+name, dcmp.right+"/"+name)
        else:
            logger.info("New file '%s' in src folder created at %s. Copying file to replica" % (name, creation_date))
            shutil.copy2(dcmp.left+"/"+name, dcmp.right+"/"+name)

    for name in dcmp.right_only: #delete file from replica

        if(os.path.isdir(dcmp.right+"/"+name)):
            logger.info("Directory '%s' was deleted in src folder. Deleting '%s' from replica" % (name, name))
            shutil.rmtree(dcmp.right+"/"+name)
        else:
            logger.info("File '%s' was deleted in src folder. Deleting '%s' from replica" % (name, name))
            os.remove(dcmp.right+"/"+name)

    for name in dcmp.diff_files: #copy the modified file from src to replica

        mod_date = time.ctime(os.path.getmtime(dcmp.left+"/"+name))
        if(not os.path.isdir(dcmp.left+"/"+name)):
            logger.info("File '%s' in src folder was modified at %s. Copying file to replica" % (name, mod_date))
            shutil.copy2(dcmp.left+"/"+name, dcmp.right+"/"+name)

    for sub_dcmp in dcmp.subdirs.values():
        sync_files(sub_dcmp, logger)

def main():
    src = sys.argv[1]
    replica = sys.argv[2]
    sync_period = float(sys.argv[3])
    log_file_path = sys.argv[4]

    starttime = time.monotonic()

    logger = logging.getLogger(__name__)
    #file logger
    logging.basicConfig(filename=log_file_path, encoding='utf-8', format="{asctime}: [{levelname}] {message}", style="{", datefmt="%Y-%m-%d %H:%M", level=logging.INFO) 

    #console logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info('Starting synchronization program...')

    while True:
        logger.info("Synchronizing....")
        dcmp = dircmp(src, replica)
        sync_files(dcmp, logger)
        logger.info("Folders Synched!")
        time.sleep(sync_period - ((time.monotonic() - starttime) % sync_period))


if __name__ == '__main__':
    main()

