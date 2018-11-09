import sys
import time
import os

MINUTE = 60

# back_up_repeat.py ###########################################################
# HOW TO SET:                                                                 #
#     Edit interval_time, to change minutes. Default was 7 minutes            #
#     Edit save_amount for how many copies can be saved. Default 5, I used 10 #
#         for test. it will Overwrite the first backup when it reaches the    #
#         save_amount.                                                        #
#     Change the FLAGS dictionary's "manual_directory",                       #
#         "interactive_directory", and "argument_directory" to set how the    #
#         program finds directories.
#     Add access files by typing strings in the square brackets of            #
#         files_to_save.                                                      #
#     Start every string with an r to prvent backslashes and spaces from      #
#         messing up the dir name. Also, last character can only be a         #
#         backslash if you use two. e.g. r"C:\\user\\"                        #
# HOW TO USE:                                                                 #
#     Run the script before opening your file or it may not allow the         #
#         program to read the file.                                           #
#     Let it run as a window in the background, if an issue occurs with your  #
#         database and you want the latest back up, look in the console to    #
#         see what database was saved last,                                   #
#     close the Python save file and rename the back up to remove the '.bak'  #
#         extention and view the database for errors.                         #
# HOW TO CLOSE:                                                               #
#     Use CTRL-C in the window the python program is running in. If this      #
#         doesn't work try Ctrl-d.                                            #
# BACK_UP_REPEAT BASIC INFO:                                                  #
#     Author: Shane Delaney                                                   #
#     Version: 0.1.3                                                          #
#     Version 1.0 will be more user friendly                                  #
###############################################################################

interval_time = 10 * MINUTE
save_amount = 7

files_to_save = ["My manual directory"]


FLAGS = {
    "test_environment": False,  # Should be False by default in master repo.
    "manual_directory": False,  # set to true to type in files_to_save var
    "interactive_directory": True,
    "argument_directory": False,
    "interactive_flags": {
        "dot_required": True,
        "accb_required": False,
        "py_required": False
    }
}

# ^ Easy Config Stuff ^ #######################################################
#
# Below is code ###############################################################

if 'HOME' in os.environ:
    HOME_DIRECTORY = os.environ['HOME']
else:
    HOME_DIRECTORY = 'No home directory found'

# cool sys.platform == "win32", "darwin", or "linux" and "linux2"


def main():
    if not FLAGS["manual_directory"] and FLAGS["interactive_directory"]:
        files_to_save = interactive_mode()
    elif not FLAGS["manual_directory"] and FLAGS["argument_directory"]:
        files_to_save = sys.argv[1:]
    if len(files_to_save) < 1:
        print("Error: you must have args of file names to run this script.")
    else:
        for console_arg in files_to_save:
            if not os.path.isfile(console_arg):
                print("Error:", console_arg, "not found")
                exit(1)
        backup_counter = 1
        while True:
            for console_arg in files_to_save:
                file_raw_n_and_e = fileRawName(console_arg)
                contents_given_file = ""
                with open(console_arg, 'rb') as given_file:
                    contents_given_file = given_file.read()
                    given_file.close()
                # all_backups_take = False
                # for backup_num in range(1, save_amount + 1):
                backup_name = file_raw_n_and_e[0] + "_" + str(backup_counter) \
                    + "." + file_raw_n_and_e[1] + ".bak"
                if backup_counter == save_amount:
                    writeAFile(backup_name, contents_given_file)
                    print(backup_name, "saved.")
                    backup_counter = 1
                else:
                    writeAFile(backup_name, contents_given_file)
                    print(backup_name, "saved.")
                    backup_counter += 1
            time.sleep(interval_time)


def fileRawName(path_string):
    new_path_string = ""
    new_ext_string = ""
    recording_path = False
    # note for non database this will need to change for files
    # with no period or hidden files
    for character in path_string[::-1]:
        # if character == "/" or character == "\\":
            # break
        if recording_path:
            new_path_string += str(character)
        elif character == ".":
            recording_path = True
        else:
            new_ext_string += str(character)
    return [new_path_string[::-1], new_ext_string[::-1]]


def writeAFile(file_name, file_contents):
    # Need to check for errors
    with open(file_name, 'wb') as opened_file_write:
        opened_file_write.write(file_contents)
        opened_file_write.close()


def check_ext_required(string_path, ext_name, is_ending=True):
    if is_ending:
        if string_path[:len(ext_name)] == ext_name:
            return True
        else:
            return False
    else:
        for character in string[::-1]:
            if character == ".":
                return True
            elif character == "/" or character == "\\":
                return False
        return False


def interactive_aesthetics(ugly_text, is_beginning=True,
                           is_ending=True, box_size=70,
                           top_type="-", bottom_type="-",
                           left_aesth_text="| ",
                           right_aesth_text=" |"):
    '''Surrounds ugly_text in a box and prints.'''
    text_lines = []
    char_on_line_count = 0
    last_ind = 0
    # Maybe make this do closest whitespace instead.
    room_for_text = box_size - len(left_aesth_text) - len(right_aesth_text)
    for ind, character in enumerate(ugly_text):
        char_on_line_count += 1
        if character == '\n' or char_on_line_count > room_for_text\
           or ind >= len(ugly_text) - 1:
            cur_ind = ind
            if ind >= len(ugly_text) - 1:
                cur_ind += 1
            text_lines.append(ugly_text[last_ind:cur_ind])
            last_ind = ind
            if character == '\n':
                last_ind += 1
            char_on_line_count = 0
    box_type = {
        "-": "-" * box_size,
        "+-": "+" + "-" * (box_size - 2) + "+",
        "_": "_" * box_size,
        "hash": r"#" * box_size,
        "_/": '\\' + '_' * (box_size - 2) + '/',
        "layered": (' ' + '_' * (box_size - 2) + ' \n' +
                    '/' + '-' * (box_size - 2) + '\\\n' +
                    '|' + r'*' * (box_size - 2) + '|\n' +
                    '+' + '-' * (box_size - 2) + '+'),
    }
    top_box = box_type[top_type]
    bottom_box = box_type[bottom_type]
    if is_beginning:
        print(top_box)
    for line in text_lines:
        right_space_balance = " " * (room_for_text - len(line))
        print(left_aesth_text + line + right_space_balance + right_aesth_text)
    if is_ending:
        print(bottom_box)


def interactive_mode():
    recommended_save_locations = {
        "win32": [
            HOME_DIRECTORY +
            r'\OneDrive - College of the North Atlantic\database\\',
        ],
        "darwin": [
            HOME_DIRECTORY + r'Do not really know how a mac works',
        ],
        "linux": [
            HOME_DIRECTORY + r'/Documents/',
        ],
        "access_name": [
            r'Center.accdb',
            r'Appalachia.accdb',
            r'Programming.accdb',
            r'Beauty.accdb',
            r'Animal.accdb',
            r'Riverview.accdb',
        ]
    }
    recommended_save_locations["linux2"] = recommended_save_locations["linux"]
    user_option = ""
    dir_search_input = "Type in the directory you are looking for: "
    user_dir = ""
    is_valid_option = False
    option_count = 1

    interactive_aesthetics(
        'Please select an option from the list below: \n ', is_ending=False)
    interactive_aesthetics(
        '1. Manually type in directory of save file from scratch',
        False, False)
    for ind, recommend in enumerate(recommended_save_locations[sys.platform]):
        option_count += 1
        interactive_aesthetics(str(option_count) + '. Begin with "' + recommend
                               + '" and work your way up', False, False)
    interactive_aesthetics("-" * 66, False, False)
    option_count += 1
    interactive_aesthetics(str(option_count) + '. Quit the program')
    while not is_valid_option:
        user_option = int(input("Input a number that matches an option."))
        if user_option >= 1 and user_option <= option_count:
            is_valid_option = True
            if user_option > 1 and user_option < option_count:
                user_plat_dir = \
                    recommended_save_locations[sys.platform][user_option - 2]
                dir_search_input = "Type the rest: " + user_plat_dir
                user_dir += user_plat_dir
            elif user_option == option_count:
                return ""
    user_dir += input(dir_search_input)
    return [user_dir]


if __name__ == "__main__" and not FLAGS["test_environment"]:
    main()
elif FLAGS["test_environment"]:
    '''Put testing function below, main will be disabled.'''
    print("Results:", interactive_mode())
