class ResourceManager:
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if ResourceManager.__instance == None:
            ResourceManager()
        return ResourceManager.__instance

    def __init__(self, resources={}):
        if ResourceManager.__instance == None:
            self.resources = {'scanner': 0,
                              'printers': [0, 0],
                              'modem': 0,
                              'drivers': [0, 0]}
            ResourceManager.__instance = self

    def resources_avaliable(self, process_desc):
        """Verify if every resource requested by the process is avaliable

        Args:
            process_desc (`dictionary`) dictionary with process atributs
        """
        if process_desc['scanner_req'] == 1:
            if self.resources['scanner'] == 1:
                raise ValueError(f'Resource scanner alredy in use')
        if process_desc['printer_id'] != 0:
            if self.resources['printers'][process_desc.printer_id] == 1:
                raise ValueError(f'Resource printer {process_desc.printer_id} alredy in use')
        if process_desc['modem_req'] == 1:
            if self.resources['modem'] == 1:
                raise ValueError(f'Resource modem alredy in use')
        if process_desc['disk_id'] != 0:
            if self.resources['drivers'][process_desc.disk_id] == 1:
                raise ValueError(f'Resource drive {process_desc.disk_id} alredy in use')

    def free_resources(self, process):
        if process.scanner_req == 1:
            self.resources['scanner'] = 0
        if process.printer_id != 0:
            self.resources['printers'][process.printer_id] = 0
        if process.modem_req == 1:
            self.resources['modem'] = 0
        if process.disk_id != 0:
            self.resources['drivers'][process.disk_id] = 0

    def get_resources(self, process):
        if process.scanner_req == 1:
            self.resources['scanner'] = 1
        if process.printer_id != 0:
            self.resources['printers'][process.printer_id] = 1
        if process.modem_req == 1:
            self.resources['modem'] = 1
        if process.disk_id != 0:
            self.resources['drivers'][process.disk_id] = 1
