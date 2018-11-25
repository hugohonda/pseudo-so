from modules import ProcessManager
import sys

# from modules import filesystem
# from modules import memory
# from modules import process_manager
# from modules import queue
# from modules import resource_manager
# import os

# rm = resource_manager.ResourceManager()

def correct_format(files):
    """Check correct format input.

    Only txt format are acceptable.

    Args:
        files (`list`) Files with path and filename.
    """
    return '.txt' in files[0] and '.txt' in files[1]

def main(files):
    """Pseudo operation system main function.

    Receive the files passed by command line from the user and starts
    process manager and file system.

    Args:
        files (`list`) Files with path and filename.
    """
    if not correct_format(files):
        print('ERROR: Files with wrong format. Try only \'txt\' format.')
        sys.exit()
    # start process manager
    pm = ProcessManager(files[0])
    pm.start()

    # # inicialização dos recursos
    # rm.newResource(type='scanner')
    # rm.newResource(type='printer')
    # rm.newResource(type='printer')
    # rm.newResource(type='modem')
    # rm.newResource(type='drive')
    # rm.newResource(type='drive')
    # print(rm.getCounts())
    #
    # pid = 0
    # offset = 0
    # blocks = 64
    # priority = 0
    # time = 3
    # printers = 0
    # scanners = 0
    # modems = 0
    # drives = 0

    # print(f'''dispatcher =>
    #     PID: {pid}
    #     offset: {offset}
    #     blocks: {blocks}
    #     priority: {priority}
    #     time: {time}
    #     printers: {printers}
    #     scanners: {scanners}
    #     modems: {modems}
    #     drives: {drives}''')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        files = sys.argv[1:]
    else:
        print('ERROR: Try pass 2 files, the first one about processes and the '
              'second about file system operations.')
        sys.exit()
    main(files)
