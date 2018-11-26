class ResourceManager:
    def __init__(self, resources={}):
        self.resources_dict = { 'scanner': False,
                                'printers': [False, False],
                                'modem': False,
                                'drivers': [False, False]}

    def resources_avaliable(self, process_desc):
        """Verify if every resource requested by the process is avaliable.

        Args:
            process_desc (`dict`) Process description.
        Raises:
            ValueError: If some resource is already in use.
        """
        if process_desc['scanner_req'] == 1:
            if self.resources_dict['scanner'] == True:
                raise ValueError(f'Resource scanner alredy in use')
        if process_desc['printer_id'] != 0:
            if self.resources_dict['printers'][process_desc.printer_id] == True:
                raise ValueError(f'Resource printer {process_desc.printer_id} alredy in use')
        if process_desc['modem_req'] == True:
            if self.resources_dict['modem'] == 1:
                raise ValueError(f'Resource modem alredy in use')
        if process_desc['disk_id'] != 0:
            if self.resources_dict['drivers'][process_desc.disk_id] == True:
                raise ValueError(f'Resource drive {process_desc.disk_id} alredy in use')

    def free_resources(self, process_desc):
        """Set every use process's resource flag to False

        Args:
            process_desc (`dict`) Process description.
        """
        if process_desc['scanner_req'] == 1:
            self.resources_dict['scanner'] = False
        if process_desc['printer_id'] != 0:
            self.resources_dict['printers'][process_desc['printer_id']] = False
        if process_desc['modem_req'] == 1:
            self.resources_dict['modem'] = False
        if process_desc['disk_id'] != 0:
            self.resources_dict['drivers'][process_desc['disk_id']] = False

    def get_resources(self, process_desc):
        if process_desc['scanner_req'] == 1:
            self.resources_dict['scanner'] = True
        if process_desc['printer_id'] != 0:
            self.resources_dict['printers'][process_desc['printer_id']] = True
        if process_desc['modem_req'] == 1:
            self.resources_dict['modem'] = True
        if process_desc['disk_id'] != 0:
            self.resources_dict['drivers'][process_desc['disk_id']] = True
