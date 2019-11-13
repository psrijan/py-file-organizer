#!/usr/bin/env python3

import datetime
import glob
import logging  # logging information
import os  # navigate through the os directory structure
import shutil  # library to use shell copying

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s %(message)s")
cur_dir = "/home/srijan/Downloads"

# Dicrectories to redirect the files into 
movies_dir = cur_dir + "/movies"
music_dir = cur_dir + "/music"
document_dir = cur_dir + "/documents"
image_dir = cur_dir + "/images"
code_dir = cur_dir + "/code"
zip_dir = cur_dir + "/zip"

# file extension the python script recognizes
# Future Reference: The keys of the dir_map are actually variables
# these points to eg movies_dir = /home/srijan/Downloads/moveis
# Key Value will look like   /home/srijan/Downloads/moveis  :  ["./*.avi", "./*.m4v", "./*3gp", "./*mpeg-2", "./*mpeg4"]
dir_map = {
    movies_dir: ["./*.avi", "./*.m4v", "./*3gp", "./*mpeg-2", "./*mpeg4"],
    music_dir: ["./*.mp3", "./*.wav"],
    image_dir: ["*.jpeg", "*.jpg", "*.gif"],
    document_dir: ["*.pdf", "*.doc", "*.docx", "*.PDF", "*.xlsx"],
    code_dir: ["*.py", "*.java", "*.sh", "*.c", "*.js", "*.csv", "*.html"],
    zip_dir: ["*.zip", "*.rar", "*.gz", "*.7z"]
}


# function to identify the type of file that is being used.
def create_required_directory():
    logging.debug("Current Directory is: {} ".format(os.getcwd()))
    os.chdir(cur_dir)
    logging.debug("Current Directory is: {} ".format(os.getcwd()))

    for dir_name in dir_map:
        logging.debug(dir_name)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logging.debug("Created Music Directory")


#
def dest_file_name(file, dest_dir):
    file_name = file.replace(cur_dir, "")
    logging.debug("Only File Name: {} ".format(file_name))

    dest_file_name = dest_dir + file_name
    if not os.path.isfile(dest_file_name):
        return ""

    counter = 0

    # handle the case where there are already files with similar names in the destination folder
    # add a index value to represent the new file name
    while os.path.isfile(dest_file_name):
        logging.debug("")
        index = file_name.rfind(".")  # find the index where the extension starts
        name = file_name[:index]  # get all values from beginning to index of string
        extension = file_name[index:]  # get all values from index to last of string
        new_file_name = name + "(" + str(counter) + ")" + extension  # if file name present add counter
        dest_file_name = dest_dir + new_file_name
        counter += 1

    logging.debug("Your File Name is {} ".format(new_file_name))
    return new_file_name


# Main Function to Move File
def move_all_files():
    for dest_dir, extensions in dir_map.items():
        for extension in extensions:
            files = glob.iglob(os.path.join(cur_dir, extension))

            for file in files:
                if os.path.isfile(file):
                    try:
                        dest_filename = dest_file_name(file, dest_dir)
                        actual_dest_dir = ""

                        # If a new file is required due to conflict with files in the dest directory, rename the file
                        if not dest_filename == "":
                            actual_dest_dir = dest_dir + "/" + dest_filename
                        else:
                            actual_dest_dir = dest_dir

                        logging.debug("Copying {} to {}".format(file, actual_dest_dir))
                        shutil.move(file, actual_dest_dir)  # Move files to the respective directory
                    except shutil.Error:
                        logging.debug("There is already a file with the filename {}".format(file))


# Starter Function
def move_files():
    logging.debug("Start of Move file on {} ".format(datetime.datetime.now()))
    create_required_directory()
    move_all_files()


move_files()
