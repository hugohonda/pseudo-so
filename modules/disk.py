STATUS_OP = lambda id, status, info: f'Operação {id} => {status}\n{info}\n'


class DiskManager:
	"""Pseudo OS disk manager.

	Args:
		disk_info (`dict`) Disk status and processes operations. Contains
		number of available blocks, pre-allocated blocks and operations to
		be processed.
		pm (:obj: ProcessManager) ProcessManager entity.
	"""
	def __init__(self, disk_info, pm):
		self.pm = pm
		self.disk = [0]*disk_info['blocks']
		self.disk_length = disk_info['blocks']
		self.operations = disk_info['operations']
		self.logging = {}

		for f in disk_info['files']:
			f_block, blocks = int(f[1]), int(f[2])
			self.disk_length -= blocks
			base = lambda n: {'owner': -1, 'name': n}
			self.disk[f_block:f_block+blocks] = blocks*[base(f[0])]

	def empty(self):
		"""Checks if all operations was executed.

		Returns:
			``True`` if there are no operation to operate anymore,
			``False`` otherwise.
		"""
		return len(self.operations) == 0

	def find_owner(self, filename):
		"""Finds file's creator if file exists on disk.

		Args:
			filename (`str`) Name of the file to be fetched on disk.
		Returns:
			-1 file's creator was not found, otherwise file's creator pid.
		"""
		for d in self.disk:
			if d and d['name'] == filename:
				return d['owner']
		return -1

	def check_permissions(self, op, priority):
		"""Check process permissions.

		Real-time processes can create/delete any file. User processes can
		delete only processes that were created by them.

		Args:
			op (`dict`) Operation details.
			priority (`int`) Process priority.
		Returns:
			``True`` if process can operate on the disk, ``False`` otherwise.
		"""
		# user process delete operation
		if priority != 0 and op['op'] and \
		   self.find_owner(op['filename']) != op['pid']:
			return False
		return True

	def file_exists(self, filename):
		"""Checks if file already exists in disk.

		Args:
			filename (`str`) Name of the file to be fetched on disk.
		Returns:
			``True`` if file exists, ``False`` otherwise.
		"""
		for d in self.disk:
			if d and d['name'] == filename:
				return True
		return False

	def log(self, oid, info, fail=True):
		"""Push log message.

		Args:
			oid (`int`) Operation id.
			info (`str`) Operation detail.
			fail (`bool`) Indicates if operation has failed.
		"""
		status = 'Falha' if fail else 'Sucesso'
		self.logging[oid] = STATUS_OP(oid, status, info)

	def run(self):
		"""Run disk operations.

		Every operation status is logged. At the end of pseudo OS simulation
		the logging will be shown.
		"""
		all_processes = self.pm.old_procs

		for curr_op in self.operations:
			if curr_op['pid'] not in all_processes.keys():
				info = 	f"Não existe o processo {curr_op['pid']}."
				self.log(curr_op['id'], info)
				continue
			if not all_processes[curr_op['pid']]['itr']:
				info = 	f"O processo {curr_op['pid']} já encerrou o seu tempo " \
						 "de processamento.."
				self.log(curr_op['id'], info)
				continue

			# process is running, checks its permissions
			if not self.check_permissions(curr_op,
										  all_processes[curr_op['pid']]['priority']):
				info = 	f"O processo {curr_op['pid']} não pode deletar o arquivo" \
						f" {curr_op['filename']}."
				self.log(curr_op['id'], info)
				all_processes[curr_op['pid']]['itr'] -= 1
				continue

			if not curr_op['op']:  # create file operation
				if self.file_exists(curr_op['filename']):
					info = 	f"O arquivo {curr_op['filename']} já existe.."
					self.log(curr_op['id'], info)
					all_processes[curr_op['pid']]['itr'] -= 1
					continue

				# checks if there are space to allocate the file
				first_block = self.is_space(curr_op)
				if curr_op['blocks'] > self.disk_length or first_block == -1:
					info = 	f"O processo {curr_op['pid']} não pode criar o " \
							f"arquivo {curr_op['filename']} (falta de espaço)."
					self.log(curr_op['id'], info)
					all_processes[curr_op['pid']]['itr'] -= 1
					continue

				blocks = self.allocate(curr_op, first_block)
				info = 	f"O processo {curr_op['pid']} criou o arquivo " \
						f"{curr_op['filename']} (blocos {' ,'.join(blocks)})."
				self.log(curr_op['id'], info, fail=False)
				all_processes[curr_op['pid']]['itr'] -= 1
				continue

			if curr_op['op']:  # delete file operation
				if not self.file_exists(curr_op['filename']):
					info = 	f"O arquivo {curr_op['filename']} não existe para " \
							 "ser deletado.."
					self.log(curr_op['id'], info)
					all_processes[curr_op['pid']]['itr'] -= 1
					continue

				self.free(curr_op)
				info = 	f"O processo {curr_op['pid']} deletou o arquivo " \
						f"{curr_op['filename']}."
				self.log(curr_op['id'], info, fail=False)
				all_processes[curr_op['pid']]['itr'] -= 1

	def is_space(self, op):
		"""Check if there are contiguous space to allocate the file.

		First fit technique.

		Args:
			op (`dict`) Operation details.
		Returns:
			``int`` that indicates the first block to allocate that file.
			-1 if there are no contiguous space to allocate that file.
		"""
		base, limit = 0, len(self.disk)-1
		# try to find place to allocate the file
		while base <= limit:
			free_b = 0  # possible blocks to allocation
			last_base = base
			while not self.disk[base]:
				free_b += 1
				if base >= limit:
					break
				base += 1
				if free_b == op['blocks']:
					break

			# enough blocks to allocate the process
			if free_b == op['blocks']:
				return last_base

			if base <= limit:
				base += 1
		return -1

	def allocate(self, op, first_block):
		"""Allocate file in the disk.

		First fit technique.

		Args:
			op (`dict`) Operation details.
			first_block (`int`) First block to start allocate the file.
		Returns:
			``list`` of ``int`` that indicates the blocks positions allocated
			to that file.
		"""
		info = {'owner': op['pid'], 'name': op['filename']}
		self.disk_length -= op['blocks']
		self.disk[first_block:first_block+op['blocks']] = [info]*op['blocks']
		return list(map(lambda x: str(x),
						range(first_block, first_block+op['blocks'])))

	def free(self, op):
		"""Delete file.

		Args:
			op (`dict`) Operation details.
		"""
		idxs = []
		for i, d in enumerate(self.disk):
			if d and d['name'] == op['filename']:
				idxs.append(i)
		self.disk[idxs[0]:idxs[-1]+1] = [0]*len(idxs)
		self.disk_length += op['blocks']

	def show_logging(self):
		"""Show disk manager logging.
		"""
		for lid, msg in self.logging.items():
			print(msg)

	def show_disk(self):
		"""Show disk allocation.
		"""
		msg = ''
		for d in self.disk:
			if not d:
				msg += '| 0 '
			else:
				msg += f"| {d['name']} "
		print(f'{msg}|\n')
