import uuid


class Process:
    """Process entity.

    Creates a process object.

    Args:
        process_desc (`dict`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id.
    """
    def __init__(self, process_desc, offset, pid):
        for k, v in process_desc.items():
            setattr(self, k, int(v))
        self.offset = offset
        self.pid = pid

    def __str__(self):
        return (
            f'\tPID: {self.pid}\n'+
            f'\toffset: {self.offset}\n'+
            f'\tblocks: {self.blocks}\n'+
            f'\tpriority: {self.priority}\n'+
            f'\ttime: {self.cpu_time}\n'+
            f'\tprinters: {self.printer_id}\n'+
            f'\tscanners: {self.scanner_req}\n'+
            f'\tmodems: {self.modem_req}\n'+
            f'\tdrivers: {self.disk_id}\n\n'+
            f'process {self.pid} =>'
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
            new_pid = len(self.processes)
            new_offset = self.calc_offset(new_pid)
            # creates a process with the process description
            self.processes.append(Process(process_info, new_offset, new_pid))
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

    def calc_offset(self, new_pid):
        """Calculates process offset.

        Args:
            new_pid (`int`) New process ID.

        Returns:
            ``int`` with new process offset number.
        """
        # first process start with offset 0
        return 0 if new_pid == 0 else self.processes[new_pid-1].blocks+1
