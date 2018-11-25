from modules import ProcessManager, process_parser, read_files_file

import time
import sys

# from modules import filesystem
# from modules import resource_manager

# rm = resource_manager.ResourceManager()

def correct_format(input_files):
    """Check correct format input.

    Only txt format are acceptable.

    Args:
        input_files (`list`) Files with path and filename.
    """
    return '.txt' in input_files[0] and '.txt' in input_files[1]

def main(input_files):
    """Pseudo operation system main function.

    Receive the files passed by command line from the user and starts
    the pseudo operating system.

    Args:
        input_files (`list`) Files with path and filename.
    """
    if not correct_format(input_files):
        print('ERROR: input_files with wrong format. Try only \'txt\' format.')
        sys.exit()
    # init Disk
    n_blocks, files, operations = read_files_file(input_files[1])

    # OS BOOT TIME ---------------
    # read processes to execute
    processes = process_parser(input_files[0])
    

    # OS SIMULATION ---------------
    counter = 0  # starts cpu time
    pm = ProcessManager()  # starts process manager
    # while there are processes to simulate, pseudo OS continue execution
    while processes or not pm.empty():
        print(f'---- Pseudo OS timer: {counter}')
        # execute process when boot time arrive
        if len(processes) and processes[0]['boot_time'] <= counter:
            curr_proc = processes.pop(0)  # next process
            print(f'dispatcher =>')
            pm.new_process(curr_proc)  # creates process

        pm.next()  # run OS pc
        counter += 1  # increase cpu time

    # TODO : starts file system
    # fs = FileSystem(files[1])
    # fs.start()

    # TODO : start resources manager
    # rm.newResource(type='scanner')
    # rm.newResource(type='printer')
    # rm.newResource(type='printer')
    # rm.newResource(type='modem')
    # rm.newResource(type='drive')
    # rm.newResource(type='drive')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        input_files = sys.argv[1:]
    else:
        print('ERROR: Try pass 2 files, the first one about processes and the '
              'second about file system operations.')
        sys.exit()
    main(input_files)
