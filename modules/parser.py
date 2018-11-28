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
                print('ERROR: The process couldn\'t be started due to : '
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
    process_info = {k: int(v) for k, v in zip(fields, process_desc)}
    result = False
    try:
        result = check_valid_params(process_info)
        if result:
            process_info['pid'] = new_pid
            if process_info['disk_id']:
                process_info['disk_id'] -= 1
            if process_info['printer_id']:
                process_info['printer_id'] -= 1
            return process_info
        else:
            raise ValueError('Incomplete params to start a process.'
                'It should be informed 8 params: boot_time, priority, '
                'cpu_time, blocks, printer_id, scanner_req, modem_req and '
                'disk_id separated with comma.')
    except Exception as e:
        raise e

def check_valid_params(process_info):
    """Checks if all params informed is valid.

    Args:
        process_info (`dict`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id.
    Returns:
        ``True`` if all params is valid, ``False`` otherwise.
    """
    id_range = range(3)
    if not process_info['printer_id'] in id_range:
        raise ValueError(f"Invalid Printer ID ( {process_info['printer_id']} ), please choose a value between 0 and 2")
    if not process_info['disk_id'] in id_range:
        raise ValueError(f"Invalid Disk ID ( {process_info['disk_id']} ), please choose a value between 0 and 2")
    if not process_info['scanner_req'] in id_range[:2]:
        raise ValueError(f"Invalid Scanner ( {process_info['scanner_req']} ), please choose a value between 0 and 1")
    if not process_info['modem_req'] in id_range[:2]:
        raise ValueError(f"Invalid Modem ( {process_info['modem_req']} ), please choose a value between 0 and 1")
    return len(process_info) == 8 and \
           process_info['printer_id'] in id_range and \
           process_info['disk_id'] in id_range and \
           process_info['scanner_req'] in id_range[:2] and \
           process_info['modem_req'] in id_range[:2]


def disk_info_parser(filename):
    """Parse files and operations.

    Args:
        filename (`str`) Filename with relative path. The file contains
                         the number of blocks, number of segments (n); n lines,
                         each with one file details; and lines in each with
                         one operation details.
    Returns:
        `dict` of (`int`, `list`, `list`). Number of blocks,
        list of files (`list` of `str`) and list of operations
        (`list` of `dict`).
    """
    with open(filename) as f:
        file_data = f.read().splitlines()

    # disk number of blocks
    n_blocks = int(file_data[0])
    # segments occupied in the disk
    n_segments = int(file_data[1])

    files = [f.replace(',', '').split(' ') for f in file_data[2:n_segments+2]]
    operations = []
    for it, line in enumerate(file_data[n_segments+2:]):
        line = line.replace(',', '').split(' ')
        if len(line) == 3:
            line.append(0)
        info = {'id': it, 'pid': int(line[0]), 'op': int(line[1]),
                'filename': line[2], 'blocks': int(line[3])}
        operations.append(info)

    return {'blocks': n_blocks, 'files': files, 'operations': operations}
