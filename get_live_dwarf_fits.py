from ftplib import FTP
import os
import shutil
from time import sleep
import configparser
import time

# FTP connection details
global ftp_host
ftp_host = ''
# Local directory to copy files to
global local_directory
local_directory = ''
# Dwarf directory to copy files from
global last_directory
last_directory = 'DWARF_RAW_M42_EXP_6_GAIN_60_2024-01-11-23-37-19-246'

def fn_wait_for_user_input(seconds_to_wait,message):
    #print('waiting for',seconds_to_wait, 'seconds ...' )
    print (message, seconds_to_wait)
    start_time = time.time()
    try:
        while (time.time() - start_time ) < seconds_to_wait:
            '''
            parenthesis, from inside out:
            time.time() which is current time    - start time, if it is more than 10 seconds, time's up :)
            int ; so we don't count 10 -1,02=8; instead we will count 10-1 = 9, meaning 9 seconds remaining, not 8
            seconds to wait - everything else ; so we get reverse count from 10 to 1, not from 1 to 10
            '''
            print("%d" %  (  seconds_to_wait -   int(  (time.time() - start_time )   )    )    ) 
            time.sleep(1)
        print('No keypress detected.')
        return 1 #no interrupt after x seconds
    except KeyboardInterrupt:
        print('Keypress detected - exiting.')
        return 0 #interrupted
        
    

# Function to download a file from the FTP server
def download_file(ftp, remote_file, local_file):
    try:
        with open(local_file, 'wb') as local_file_obj:
            ftp.retrbinary('RETR ' + remote_file, local_file_obj.write)
    except Exception as e:
        print (f"Exception: {e}")
        print (f"During copy: {remote_file} -> {local_file}")

# Function to get the modification date of a file on the FTP server
def get_file_mtime(ftp, remote_file):
    return ftp.voidcmd(f"MDTM {remote_file}")

# Function to get the modification date of a directory on the FTP server
def get_dir_mtime(remote_dir):
    return remote_dir[-23:]

def stacking():
    global ftp_host
    global local_directory
    global last_directory

    # Create an FTP_TLS instance
    ftp = FTP()

    # Connect to the FTP server
    print (f"Try to connect to : {ftp_host}")
    # Connect to the FTP server
    ftp.connect(ftp_host)

    ftp.login("Anonymous","")
    ftp.set_pasv(True)
    print(f"Connected to {ftp_host}")

    # Remote directory on the FTP server to monitor
    remote_directory = '/DWARF_II/Astronomy/'

    # Create Tmp directory if need
    local_path_tmp = os.path.join(local_directory, "tmp")

    if (not os.path.exists(local_path_tmp)):
        os.makedirs(local_path_tmp)

    # File extension to filter for (e.g., '.fits')
    file_extension = '.fits'
    file_tmp = '.tmp'

    # Set to keep track of downloaded files
    downloaded_files = set()

    files = ftp.mlsd("/DWARF_II/Astronomy/DWARF_RAW_Manual_EXP_13_GAIN_90_2024-01-07-00-40-14-712")

    if (not last_directory):
        print(f"Search the last directory...")

        #remote_subdirectories = []
        #for d in ftp.nlst(remote_directory):
        #    print(f"Find {d}")
        #    print(f"{ftp.cwd(d)}")
        #    verif = ftp.cwd(d)
        #    if (ftp.cwd(d).startswith('250')):
        #        print("OK FTP")
        #        if (d.startswith(remote_directory+'DWARF_RAW')):
        #            print("OK")
        #            timestamp = d[-23:]
        #            print (timestamp)
        #            remote_subdirectories.append(d)

        # Get the list of subdirectories in the remote directory
        remote_subdirectories = [d for d in ftp.nlst(remote_directory) if (ftp.cwd(d).startswith("250") and d.startswith(remote_directory+'DWARF_RAW'))]
        print(f"Found {len(remote_subdirectories)} directories")

        # Sort subdirectories by modification date (most recent first)
        remote_subdirectories.sort(key=lambda x: get_dir_mtime(x), reverse=True)

    else:
        remote_subdirectories = []
        remote_subdirectories.append(remote_directory + last_directory)
        print(f"Using the directory : {remote_subdirectories[0]}")

    # Choose the most recent subdirectory
    if remote_subdirectories:
        most_recent_subdirectory = remote_subdirectories[0]
        print(f"Processing files in directory: {most_recent_subdirectory}")

        # Change to the most recent subdirectory
        ftp.cwd(most_recent_subdirectory)
        wait_number = 0
        old_wait_number = 0
        processing = True

        while processing:

            # Get the list of files in the most recent subdirectory
            remote_files = ftp.nlst()

            # Sort files by modification date (oldest first)
            remote_files.sort(key=lambda x: get_file_mtime(ftp, x))

            # Find and download new files with the specified extension
            for remote_file in remote_files:
                if remote_file.endswith(file_extension) and remote_file not in downloaded_files:
                    # Found new files
                    print ("Found new file")
                    old_wait_number = wait_number

                    print(f"Find File : {remote_file} from directory: {most_recent_subdirectory}")
                    remote_path = most_recent_subdirectory + "/" + remote_file
                    local_path = os.path.join(local_directory, remote_file)

                    # use a local tmp in a subdirectory : need for Sirl as the transfert is slow
                    local_tmp = remote_file.replace(file_extension, ".tmp")
                    local_file_tmp = os.path.join(local_path_tmp, local_tmp)

                    if (os.path.isfile(local_file_tmp)):
                        os.remove(local_file_tmp)
                    if (os.path.isfile(local_path)):
                        os.remove(local_path)

                    download_file(ftp, remote_path, local_file_tmp)
                    print(f"Downloaded file: {remote_file}")
                    print(f"From directory: {most_recent_subdirectory} to {local_file_tmp}")
                    # rename tmp file
                    os.rename(local_file_tmp, local_path)
                    print(f"New File copied : {remote_file}") 
                    downloaded_files.add(remote_file)

            wait_number += 15

            if (wait_number - old_wait_number)  > 3:
                if fn_wait_for_user_input(5, "No more files since 30 seconds, the program will contine if you don't press CTRL-C within 5 seconds:" )  == 1:
                    old_wait_number = wait_number
                    print('continuing ....')
                else:
                    print('not continuing.')
                    processing = False

            if (processing):
                # Pause before checking again
                sleep(2)  # You can adjust the frequency of checking

        # Move back to the parent directory
        ftp.cwd('..')

    print(f"Stacking Finished")
    display_menu()

def display_menu():
    print("")
    print("------------------")
    print(f"1. Current Dwarf IP: {ftp_host}")
    print(f"2. Current Siril Stacking Directory: {local_directory}")
    print(f"3. Use Last Dwarf Session (empty) or Specify Session Directory: {last_directory}")
    print(f"4. Launch Live Stacking")
    print("0. Exit")

def get_user_choice():
    choice = input("Enter your choice (1-4) or 0 to exit: ")
    return choice

def option_1():
    print("You selected Option 1: Setting Current Dwarf IP")
    print("")
    # Add your Option 1 functionality here
    input_data(1)

def option_2():
    print("You selected Option 2:  Setting Current Siril Stacking Directory")
    print("")
    # Add your Option 2 functionality here
    input_data(2)

def option_3():
    print("You selected Option 3: Setting Use Last Dwarf Session (empty) or Specify Session Directory")
    print("")
    # Add your Option 3 functionality here
    input_data(3)

def option_4():
    print("You selected Option 4: Launch Live Stacking")
    print("")
    # Add your Option 4 functionality here

    global ftp_host
    global local_directory
    global last_directory

    if (not ftp_host):
        print("The Dwarf IP can't be empty!")
        return 

    if (not local_directory):
        print("The Siril directory can't be empty!")
        return 

    update_config(ftp_host, local_directory, last_directory)

    stacking()

def update_config(ftp_host, local_directory, last_directory):
    config = configparser.ConfigParser()

    if (not os.path.isfile('config.ini')):
        config.add_section('CONFIG')
        config.set('CONFIG','FTP_HOST','')
        config.set('CONFIG','LOCAL_DIRECTORY','')
        config.set('CONFIG','LAST_DIRECTORY','')
        print("Create the Config file!")

    else: 
        config.read('config.ini')

    # Update the value in the CONFIG section
    config['CONFIG']['FTP_HOST'] = ftp_host
    config['CONFIG']['LOCAL_DIRECTORY'] = local_directory
    config['CONFIG']['LAST_DIRECTORY'] = last_directory

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def read_config():
    global ftp_host
    global local_directory
    global last_directory

    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        ftp_host = config.get('CONFIG', 'FTP_HOST')
        local_directory = config.get('CONFIG', 'LOCAL_DIRECTORY')
        last_directory = config.get('CONFIG', 'LAST_DIRECTORY')
    except configparser.NoSectionError:
        print("ConfigFile not found.")
        return None
    except configparser.NoOptionError:
        print("Data not found.")
        return None

def input_data(type):
    global ftp_host
    global local_directory
    global last_directory

    if (type == 1):
        ftp_host_input = input("Enter the Dwarf IP: ")
        print("You entered:", ftp_host_input)
        if (ftp_host_input):
            print("You entered:", ftp_host_input)
            ftp_host = ftp_host_input
        else:
            print("Can't be empty, no change")

    if (type == 2):
        local_directory_input = input("Enter the Siril Stacking Directory: ")
        print("You entered:", local_directory_input)
        if (local_directory_input):
            local_directory = local_directory_input
        else:
            print("Can't be empty, no change")

    if (type == 3):
        last_directory = input("Set Last Dwarf Session (empty) or Specify Session Directory: ")
        print("You entered:", last_directory)

    update_config(ftp_host, local_directory, last_directory)

def main():

    read_config()

    while True:
        display_menu()
        user_choice = get_user_choice()

        if user_choice == '1':
            option_1()

        elif user_choice == '2':
            option_2()

        elif user_choice == '3':
            option_3()

        elif user_choice == '4':
            option_4()

        elif user_choice == '0':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

if __name__ == "__main__":
    main()


