class DiskManager:
	"""Pseudo OS disk manager

    Args:
        n_blocks 	(`int`) Number of available blocks
        files		(`list`) Pre-allocated blocks
        operations	(`list`) operations to be processed
    """
	def __init__(self, n_blocks, files, operations):
		self.blocks = ['0']*n_blocks
		self.owner  = ['0']*n_blocks
		self.size 	= [0]*n_blocks


		for file in files:
			for i in range(int(file[1]), int(file[1])+int(file[2])):
				self.blocks[i] =  file[0]
				self.size[int(file[1])] = int(file[2])
		self.operations = operations

	def create(self, op):
		space = ''
		for j in range(0,int(op[3])):
			space = space + '0'

		allocation_add = ''.join(self.blocks).find(space)
		if (allocation_add != -1):
			
			self.size[allocation_add] = int(op[3])
			add = ''
			for k in range(allocation_add, allocation_add+int(op[3])):
				add = add + str(k) + ', '
				self.blocks[k] 	= op[2]
				self.owner[k]	= op[0]
			return 1, add

		else:
			return 2, ''
	
	def delete(self, op):		
		delete_add = ''.join(self.blocks).find(op[2])
		if (delete_add!= -1):
			if (self.owner[delete_add]=='0' or self.owner[delete_add]==op[0]):
				for l in range(delete_add, delete_add+self.size[delete_add]):
					self.blocks[l] 	= '0'
					self.owner[l]	= '0'
				self.size[delete_add] = 0
				return 4, ''

			else: 
				return 5, ''
		else:
			return 6

	def process(self, op):
		if (op[1]=='0'):
			if (op[2] in self.blocks):
				return 0,''
			else:	
				return self.create(op)

		elif (op[1] == '1'):
			if (op[2] not in self.blocks):
				return 3, ''
			else:
				return self.delete(op)	
		else:
			return 7, ''
		return 0,''		