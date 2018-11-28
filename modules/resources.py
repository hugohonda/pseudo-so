class ResourceManager:
    """Pseudo OS resource manager.
    """
    def __init__(self):
        self.resources = {'scanner': 0,
                          'printers': [0, 0],
                          'modem': 0,
                          'drivers': [0, 0]}

    def resources_available(self, process_desc):
        """Verify if every resource requested by the process is avaliable.

        Args:
            process_desc (`dict`) Process description.
        Raises:
            ValueError: If some resource is already in use.
        """
        error_msgs = []
        base_msg = lambda driver: f'Resource \'{driver}\' is alredy in use.'
        if process_desc['scanner_req'] and self.resources['scanner']:
            error_msgs.append(base_msg('scanner'))
        if process_desc['printer_id'] != 0 and \
           self.resources['printers'][process_desc['printer_id']]:
            error_msgs.append(base_msg(f"printer {process_desc['printer_id']}"))
        if process_desc['modem_req'] and self.resources['modem']:
            error_msgs.append(base_msg('modem'))
        if process_desc['disk_id'] != 0 and \
           self.resources['drivers'][process_desc['disk_id']]:
           error_msgs.append(base_msg(f"drive {process_desc['disk_id']}"))

        if not process_desc['priority'] and \
           (process_desc['scanner_req'] or process_desc['modem_req'] or
            process_desc['printer_id'] == 1 or process_desc['printer_id'] or
            process_desc['disk_id'] == 1 or process_desc['disk_id'] == 2):
            error_msgs.append('Real-time processes cannot allocate resources.')

        if error_msgs:
            raise ValueError(f"{' '.join(error_msgs)}")

    def free(self, proc):
        """Free resources allocated to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        if proc.scanner_req:
            self.resources['scanner'] = 0
        if proc.modem_req:
            self.resources['modem'] = 0
        if proc.printer_id != 0:
            self.resources['printers'][proc.printer_id] = 0
        if proc.disk_id != 0:
            self.resources['drivers'][proc.disk_id] = 0

    def allocate(self, proc):
        """Allocates resources to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        self.resources['scanner'] = proc.scanner_req
        self.resources['modem'] = proc.modem_req
        if proc.printer_id != 0:
            self.resources['printers'][proc.printer_id] = 1
        if proc.disk_id != 0:
            self.resources['drivers'][proc.disk_id] = 1
