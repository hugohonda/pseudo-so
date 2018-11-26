from modules import ProcessManager, DiskManager, process_parser, \
                    disk_info_parser
import sys


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

    # OS BOOT TIME ---------------
    # read processes to execute
    processes = process_parser(input_files[0])
    # read disk files and operations
    disk_info = disk_info_parser(input_files[1])

    # OS SIMULATION ---------------
    counter = 0  # starts cpu time
    pm = ProcessManager()  # starts process manager
    dm = DiskManager(disk_info, pm)  # starts disk manager
    # while there are processes to simulate and disk operations,
    # pseudo OS continue execution
    while processes or not pm.empty() or not dm.empty():
        print(f'---- Pseudo OS timer: {counter}')
        # execute process when boot time arrive
        if len(processes) and processes[0]['boot_time'] <= counter:
            curr_proc = processes.pop(0)  # next process
            print(f'dispatcher =>')
            pm.new_process(curr_proc)  # creates process

        pm.next()  # run OS pc
        dm.next()  # run disk operation
        counter += 1  # increase cpu time

    print('\nSistema de arquivos =>')
    dm.show_logging()
    dm.show_disk()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        input_files = sys.argv[1:]
    else:
        print('ERROR: Try pass 2 files, the first one about processes and the '
              'second about file system operations.')
        sys.exit()
    main(input_files)
