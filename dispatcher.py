from modules import ProcessManager, process_parser, disk_info_parser, \
                    DiskManager
import threading
import sys


def correct_format(input_files):
    """Check correct format input.

    Only txt format are acceptable.

    Args:
        input_files (`list`) Files with path and filename.
    """
    return '.txt' in input_files[0] and '.txt' in input_files[1]


def disk(dm, i, op):
    op_result, others = dm.process(op)
    if op_result == 0:
        print ('Operação ' + str(i) + ' => Falha')
        print ('O arquivo ' + op[2] + ' já existe.\n')
    elif op_result == 1:
        print ('Operação ' + str(i) + ' => Sucesso')
        print ('O processo ' + op[0] + ' criou o arquivo ' + op[2] + ' (blocos ' + others[:-2] + ').\n')
    elif op_result == 2:
        print ('Operação ' + str(i) + ' => Falha')
        print ('O processo ' + op[0] + ' não pode criar o arquivo ' + op[2] +' (falta de espaço).\n')
    elif op_result == 3:
        print ('Operação ' + str(i) + ' => Falha')
        print ('O arquivo ' + op[2] + ' não existe.\n')
    elif op_result == 4:
        print ('Operação ' + str(i) + ' => Sucesso')
        print ('O processo ' + op[0] + ' deletou o arquivo ' + op[2] + '.\n')
    elif op_result == 5:
        print ('Operação ' + str(i) + ' => Falha')
        print ('O processo ' + op[0] + ' não pode deletar o arquivo ' + op[2] + '.\n')
    elif op_result == 6:
        print ('Operação ' + str(i) + ' => Falha')
        print ('Não existe o arquivo ' + op[2] +  '.\n')
    elif op_result == 7:
        print ('Operação ' + str(i) + ' => Inválida')
        print ('Não existe o código de operação ' + op[1] +  '.\n')


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
    processes_executions = [0]*len(processes)
    for p in processes:
        processes_executions[int(p['pid'])] = int(p['cpu_time'])
    # read disk files and operations
    n_blocks, files, operations = disk_info_parser(input_files[1])
    dm = DiskManager(n_blocks, files, operations)

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
            threading.Thread(target=pm.new_process, args=[curr_proc]).start()
            # pm.new_process(curr_proc)  # creates process

        pm.next()  # run OS pc
        counter += 1  # increase cpu time

    print('\nSistema de arquivos =>')
    for i, op in enumerate(operations):
        if int(op[0]) >= len(processes_executions) and int(op[0]) > 0:
            print ('Operação ' + str(i) + ' => Falha')
            print ('Não existe o processo ' + op[0] +  '.\n')
        elif processes_executions[int(op[0])] == 0:
            print ('Operação ' + str(i) + ' => Falha')
            print ('O processo ' + op[0] + ' já encerrou o seu tempo de processamento.\n')

        else:
            processes_executions[int(op[0])] = processes_executions[int(op[0])] - 1
            disk(dm, i, op)

    dm.print_disk_map()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        input_files = sys.argv[1:]
    else:
        print('ERROR: Try pass 2 files, the first one about processes and the '
              'second about file system operations.')
        sys.exit()
    main(input_files)
