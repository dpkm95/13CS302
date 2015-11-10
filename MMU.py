import multiprocessing

#P - no of physical pages in memory
#Phit - time taken to access RAM
#Pmiss - time taken to access 
#T - no of entries in page table
#Taccess - time taken to access TLB
class MMU(multiprocessing.Process):
	def __init__(self, C, page_fetched, request_queue, scheduler_free, **kwargs):
		super().__init__()
		self.P = kwargs['P']
		self.Phit = kwargs['Phit']
		self.Pmiss = kwargs['Pmiss']
		self.T = kwargs['T']
		self.Taccess = kwargs['Taccess']
		self.C = C

		self.page_fetched = page_fetched
		self.request_queue = request_queue
		self.scheduler_free = scheduler_free

		self.request_count = 0
		self.hit_count = 0
		
		self.display()		
		self.start()

	def run(self):
		print('mmu log: MMU started, pid', self.pid)
		while True:
			target_page = self.request_queue.get()
			self.get_page_log(target_page)
			self.generate_physical_address(target_page)
			# if self.check_tlb(target_page):
			# 	self.task_tlb_access(target_page)
			# 	self.generate_physical_address(target_page)
			# 	if self.request_count % self.C == 0:
			# 		self.flush_tlb()
			# 		self.scheduler_free.acquire()
			# 		self.scheduler.run_scheduler.put(-1)
			# elif self.check_ram(target_page):						
			# 	self.task_ram_access(target_page)
			# 	self.update_tlb(target_page)
			# 	self.generate_physical_address(target_page)
			# 	if self.request_count % self.C == 0:
			# 		self.flush_tlb()
			# 		self.scheduler_free.acquire()
			# 		self.scheduler.run_scheduler.put(-1)
			# else:
			# 	self.task_disk_access(target_page)
			# 	self.update_page_table(target_page)
			# 	self.request_queue.put(target_page)

	def get_page_log(self, target_page):
		self.request_count += 1
		print('mmu log:','servicing page request',target_page)

	def generate_physical_address(self, target_page):
		print('mmu log:','serviced page request',target_page)
		with self.page_fetched:
			self.page_fetched.notify()

	def display(self):
		print('mmu log: MMU details(P, Phit, Pmiss, T, Taccess):', self.P, 
				self.Phit, self.Pmiss, self.T, self.Taccess)