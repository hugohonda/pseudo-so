class FileSystem:
    """File system manager from pseudo operating system.

    Args:
        filename (`str`) Filename with relative path. The file contains
                         operations descriptions to be perfomed in the OS.
    """
    def __init__(self, filename):
        self.filename = filename

    def start(self):
        """Starts file system.
        """
        with open(self.filename, 'r') as f:
            cont = f.readlines()

        cont = [l.strip() for l in cont]
        self.system_blocks = l[0]
        self.blocks_allocated = l[1]
        for b in self.blocks_allocated:
            self.allocate_file(b.replace(',', '').split(' '))
