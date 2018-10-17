import uuid

class Resource:
    def __init__(self, rid=None, type='generic'):
        if rid == None:
            rid = uuid.uuid4()
        self.rid = rid
        self.type = type
        self.pid = None
        self.allocated = False

class ResourceManager:
    def __init__(self, resources=[]):
        self.resources = resources
    
    def newResource(self, rid=None, type='generic'):
        new = Resource(rid, type)
        self.resources.append(new)
    
    def getCounts(self):
        counts = {}
        for resource in self.resources:
            if resource.type not in counts:
                counts[resource.type] = 1
            else:
                counts[resource.type] = counts[resource.type] + 1
        return counts
            