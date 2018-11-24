import os
import sys
from process_manager import ProcessManager, Process

class Parser:
    def __init__(self):
        self.read_process_file()
        self.read_files_file()

    def read_process_file(self):
        FILE_PATH = str(os.getcwd()) + '/data/' + 'processes.txt'
        with open(FILE_PATH) as data_file:
            for line in data_file:
                start_time, priority, cpu_time, n_blocks, \
                printer, scanner, modem, disk = line.split(', ')
                pm = ProcessManager.getInstance()
                pm.newProcess(
                                int(start_time), int(priority), int(cpu_time),
                                int(n_blocks), int(printer), int(scanner),
                                int(modem), int(disk)
                )

    def read_files_file(self):
        FILE_PATH = str(os.getcwd()) + '/data/' + 'files.txt'
        with open(FILE_PATH) as data_file:
            files = []
            operations = []
            cnt = 0
            for line in data_file:
                if(line[-1] == '\n'):
                    line = line[:-1]

                # Linha 1: Quantidade de blocos do disco
                if(cnt == 0):
                    blocks_total = line

                # Linha 2: Quantidade de segmentos ocupados no disco (n)
                elif(cnt == 1):
                    busy_segments = line
                # Arquivos
                elif(cnt < int(busy_segments)+2):
                    file_name, first_block, n_blocks = line.split(', ')
                    new_file = (file_name, first_block, n_blocks)
                    files.append(new_file)
                
                # Operações
                else:
                    #Delete operation
                    if(len(line.split(', ')) == 3):
                        pid, opcode, file_name = line.split(', ')
                        new_operation = (pid, opcode, file_name)
                    #Create operation
                    else:
                        pid, opcode, file_name, create_n_blocks = line.split(', ')
                        new_operation = (pid, opcode, file_name, create_n_blocks)

                    operations.append(new_operation)
                cnt +=1             
            
            for p in ProcessManager.getInstance().processes :
                print(f"P: {p}")
            
parser = Parser()



