def process_parser(filename):
    """Parse processes to execute.

    Args:
        filename (`str`) Filename with relative path. The file contains
                         processes information.
    Returns:
        Ascending ordered (by boot time) ``list`` of processes to execute.
    """
    processes = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                processes.append(
                    mount_process(
                        line.strip().replace(',', '').split(' '),
                        len(processes)))
            except ValueError as err:
                print('ERROR: The process couldn\'t be started due to :'
                      f'{err}')

    # sort by processes boot time
    return sorted(processes, key=lambda proc: proc['boot_time'])


def mount_process(process_desc, new_pid):
    """Mount a process description.

    Args:
        process_desc (`list`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id
                              separated with comma.
    Returns:
        ``dict```of a process complete information.
    Raises:
        ValueError: If some parameter is not valid or not informed.
    """
    fields = ['boot_time', 'priority', 'cpu_time', 'blocks',
              'printer_id', 'scanner_req', 'modem_req', 'disk_id']
    process_info = {k: int(v) for k,v in zip(fields, process_desc)}

    if check_valid_params(process_info):
        process_info['pid'] = new_pid
        return process_info
    else:
        raise ValueError('Incomplete params to start a process.'
              'It should be informed 8 params: boot_time, priority, '
              'cpu_time, blocks, printer_id, scanner_req, modem_req and '
              'disk_id separated with comma.')


def check_valid_params(process_info):
    """Checks if all params informed is valid.

    Args:
        process_info (`dict`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id.
    Returns:
        ``True`` if all params is valid, ``False`` otherwise.
    """
    id_range = range(2)
    return len(process_info) == 8 and \
           process_info['printer_id'] in id_range and \
           process_info['disk_id'] in id_range and \
           process_info['scanner_req'] in id_range[:2] and \
           process_info['modem_req'] in id_range[:2]

def read_files_file(filename):
    """Parse files and operations.

    Args:
        filename (`str`) Filename with relative path. The file contains 
                         the number of blocks, number of segments (n); n lines,
                         each with one file details; and lines in each with
                         one operation details.
    Returns:
        Number of blocks, list of files read.
    """
    files = []
    operations = []
    with open(filename) as data_file:
        data = data_file.readlines()
        # Linha 1: Quantidade de blocos do disco
        n_blocks = int(data[0])
        # Linha 2: Quantidade de segmentos ocupados no disco (n)
        n_segments = int(data[1])
        # Arquivos
        for line in data[2: n_segments + 2]:
            line = line.strip('\n')
            file_name, first_block, blocks = line.split(', ')
            new_file = (file_name, first_block, blocks)
            files.append(new_file)

        # Operações
        for line in data[n_segments + 2:]:
            line = line.strip('\n')                
            line = line.split(', ')
            if len(line) == 3:
                line.append('0')
            operations.append({'id': line[0],
                                'code': line[1],
                                'name': line[2],
                                'blocks': line[3]})

    return n_blocks, files, operations
