import uuid


class Process:
    """Process entity.

    Creates a process object.

    Args:
        process_desc (`dict`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id.
    """
    def __init__(self, process_desc):
        for k, v in process_desc.items():
            setattr(self, k, v)
        self.pid = uuid.uuid4()

    def __str__(self):
        return (
            f'Process ID: {self.pid}\n'+
            f'Boot time: {self.boot_time}\n'+
            f'Priority: {self.priority}\n'+
            f'CPU time: {self.cpu_time}\n'+
            f'Blocks: {self.blocks}\n'+
            f'Printer ID: {self.printer_id}\n'+
            f'Scanner: {self.scanner_req}\n'+
            f'Modem: {self.modem_req}\n'+
            f'Disk ID: {self.disk_id}'
        )


class ProcessManager:
    """Process manager from pseudo operating system.

    Args:
        filename (`str`) Filename with relative path. The file contains
                         processes information.
    """
    def __init__(self, filename):
        self.filename = filename
        self.processes = []

    def start(self):
        """Starts process manager.
        """
        with open(self.filename, 'r') as f:
            for line in f:
                try:
                    self.new_process(line.strip().replace(',', '').split(' '))
                except ValueError as err:
                    print('ERROR: The process couldn\'t be started due to :'
                          f'{err}')

    def new_process(self, process_desc):
        """Starts a new process.

        Args:
            process_desc (`list`) Process description. Parameters: boot_time,
                                  priority, cpu_time, blocks, printer_id,
                                  scanner_req, modem_req and disk_id
                                  separated with comma.
        Raises:
            ValueError: If some parameter is not valid or not informed.
        """
        fields = ['boot_time', 'priority', 'cpu_time', 'blocks',
                  'printer_id', 'scanner_req', 'modem_req', 'disk_id']
        process_info = {k: v for k,v in zip(fields, process_desc)}

        if self.check_valid_params(process_info):
            # creates a process with the process description
            self.processes.append(Process(process_info))
        else:
            raise ValueError('Incomplete params to start a process.'
                  'It should be informed 8 params: boot_time, priority, '
                  'cpu_time, blocks, printer_id, scanner_req, modem_req and '
                  'disk_id separated with comma.')

    def check_valid_params(self, process_info):
        """Checks if all params informed is valid.

        Args:
            process_info (`dict`) Process description. Parameters: boot_time,
                                  priority, cpu_time, blocks, printer_id,
                                  scanner_req, modem_req and disk_id.
        Returns:
            ``True`` if all params is valid, ``False`` otherwise.
        """
        id_range = ['0', '1', '2']
        return len(process_info) == 8 and \
               process_info['printer_id'] in id_range and \
               process_info['disk_id'] in id_range and \
               process_info['scanner_req'] in id_range[:2] and \
               process_info['modem_req'] in id_range[:2]
