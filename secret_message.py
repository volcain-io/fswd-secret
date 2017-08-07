import os
import shutil
import re
from random import *
import time


# Returns a list of our images which represents every single character on the alphabet (A-Z) and a dot ('.') & a whitespace (' ')
# root_dir is the directory of the alphabet images
def get_list(root_dir=os.getcwd() + '/alphabet/'):
    # get list of files of the given directory
    list_of_filenames = os.listdir(root_dir)
    # sort list lexicographically
    list_of_filenames.sort()

    output = []
    # cycle through the list of files and put them all to a list
    for filename in list_of_filenames:
        # check if we have a file
        if os.path.isfile(os.path.join(root_dir, filename)):
            output.append(filename)

    return output


# Ask the user which secret message to encrypt
# returns the first 28 characters of the user input in uppercase representation
def get_input():
    # read single line from console / user input
    print("Please enter your secret message to encrypt")
    user_input = raw_input("max. 28 characters (allowed characters are A-Z, whitespace, .): ").upper()

    if ( user_input ):
        # replace all whitespace characters to a single whitespace character
        regex = re.compile('[\s]+')
        user_input = regex.sub(' ', user_input)
        # remove any charachter which is not in the range: A-Z, a-z, ., whitespace
        regex = re.compile('[^A-Z\.\s]')
        user_input = regex.sub('', user_input)
    else:
        print("Your input is empty. Please try again. (press CTRL-C to quit)")
        get_input()

    # return the first 28 characters of the user input
    return user_input[:28]


# creates the new secret message from the images by
def create_new_images(secret_message, root_dir=os.getcwd() + '/alphabet/', output_folder='output'):
    # directory of the alphabet images
    list = get_list()
    # directory to put the secret message into
    dir_output = root_dir + output_folder + '/'
    # if the directory already exists than delete it the folder tree
    if ( os.path.exists(dir_output) ):
        shutil.rmtree(dir_output)
    # create new directory output
    os.mkdir(dir_output)
    # loop through each character of the secret message
    # and get the corresponding images and put them into the output folder
    for idx, ch in enumerate(secret_message):
        new_value = None
        # all characters in the range of A-Z
        if ( ord(ch) >= 65 and ord(ch) <= 90 ):
            new_value = list[ord(ch)-65]
        # ' ' whitespace character
        if ( ord(ch) == 32 ):
            new_value = list[len(list)-1]
        # '.' dot character
        if ( ord(ch) == 46 ):
            new_value = list[len(list)-2]
        # we need the old value to copy it to new place
        old_value = list[idx]
        # copy the image into the output folder
        if ( new_value is not None ):
            shutil.copy(root_dir + new_value, dir_output + encrypt_filename(old_value))


# puts a random number before or after the filename
def encrypt_filename(filename):
    # random number between 1 and 100
    random_number = str(randint(1, 100))
    append = randint(0, 1)
    if ( append ):
        filename = filename[:-4] + random_number + filename[-4:]
    else:
        filename = random_number + filename

    return filename


# start creating the secret message
def create_secret_message(output_folder='output'):
    user_input = get_input()
    create_new_images(user_input)


### START DECRYPTING MESSAGE ###

def decrypt_secret_message(root_dir=os.getcwd() + '/alphabet/', folder='output'):
    # directory of the images
    dir_images = root_dir + folder + '/'
    # get list of files of the given directory
    list_of_files = os.listdir(dir_images)

    for filename in list_of_files:
        old_filename = dir_images + '/' + filename
        new_filename = dir_images + '/' + filename.translate(None, '0123456789')
        os.rename(old_filename, new_filename)


### START TO CREATE THE SECRET ###
create_secret_message()
### SUSPEND THREAD FOR 10 SECONDS ###
time.sleep(10)
### DECRYPT SECRET MESSAGE ###
decrypt_secret_message()
