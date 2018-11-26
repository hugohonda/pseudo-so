import threading

class ResourceManager:
    """Pseudo OS resource manager.
    """
    def __init__(self):
        self.resources = {'scanner': {'id': 0, 'sem': threading.Semaphore()},
                          'printers': [{'id': 0, 'sem': threading.Semaphore()}, {'id': 0, 'sem': threading.Semaphore()}],
                          'modem': {'id': 0, 'sem': threading.Semaphore()},
                          'drivers': [{'id': 0, 'sem': threading.Semaphore()}, {'id': 0, 'sem': threading.Semaphore()}]}

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

        if not process_desc['priority']:
            error_msgs.append('Real-time processes cannot allocate resources.')

        if error_msgs:
            raise ValueError(f"{' '.join(error_msgs)}")

    def free(self, proc):
        """Free resources allocated to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        if proc.scanner_req:
            self.resources['scanner']['id'] = 0
            self.resources['scanner']['sem'].release()
        if proc.modem_req:
            self.resources['modem']['id'] = 0
            self.resources['modem']['sem'].release()
        if proc.printer_id != 0:
            self.resources['printers'][proc.printer_id]['id'] = 0
        if proc.disk_id != 0:
            self.resources['drivers'][proc.disk_id]['id'] = 0

    def allocate(self, proc):
        """Allocates resources to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        if not proc.scanner_req:
            self.resources['scanner']['id'] = proc.scanner_req
            self.resources['scanner']['sem'].acquire()
        if not proc.modem_req:
            self.resources['modem']['id'] = proc.modem_req
            self.resources['modem']['sem'].acquire()
        if proc.printer_id != 0:
            self.resources['printers'][proc.printer_id]['id'] = 1
        if proc.disk_id != 0:
            self.resources['drivers'][proc.disk_id]['id'] = 1
