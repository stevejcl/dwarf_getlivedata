import sys

from dwarf_python_api.get_live_data_dwarf import get_live_data, read_config, update_config, getGetLastPhoto

def main():

    run = True
   
    while run:
        try:
            get_live_data()
            run = False
        except KeyboardInterrupt:
            print('Keypress detected - exiting.')
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        
        read_config()

        # If command-line parameters are provided
        option = None
        host = None
        directory = None
        history = 0
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == "--opt":
                if i + 1 < len(sys.argv):
                    option = sys.argv[i + 1]
                    i += 1
                else:
                    print("Error: --opt parameter requires an argument.")
                    sys.exit(1)
            elif sys.argv[i] == "--dir":
                if i + 1 < len(sys.argv):
                    directory = sys.argv[i + 1]
                    i += 1
                else:
                    print("Error: --dir parameter requires an argument.")
                    sys.exit(1)
            elif sys.argv[i] == "--ip":
                if i + 1 < len(sys.argv):
                    host = sys.argv[i + 1]
                    i += 1
                else:
                    print("Error: --ip parameter requires an argument.")
                    sys.exit(1)
            elif sys.argv[i] == "--history":
                if i + 1 < len(sys.argv):
                    history = sys.argv[i + 1]
                    i += 1
                else:
                    print("Error: --ip parameter requires an argument.")
                    sys.exit(1)
            else:
                print(f"Error: Unknown parameter '{sys.argv[i]}'.")
                sys.exit(1)
            i += 1

        if host is not None: 
           ftp_host=host

        if option == "6" and (directory or local_photo_directory):
            if directory is not None: 
                local_photo_directory=directory
            update_config(ftp_host=ftp_host, local_photo_directory=local_photo_directory)
            getGetLastPhoto(history)
        elif option == "4" and (directory or local_directory):
            if directory is not None: 
                local_directory=directory
            update_config(ftp_host=ftp_host, local_directory=local_directory)
            option_4()
        else:
            print("Invalid parameters.")
    else:
        # If no command-line parameters are provided, launch the main menu
        main()


