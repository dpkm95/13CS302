import multiprocessing, os

#P - no of physical pages in memory
#Phit - time taken to access RAM
#Pmiss - time taken to access 
#T - no of entries in page table
#Taccess - time taken to access TLB
class MMU(multiprocessing.Process):
	def __init__(self, scheduler, **kwargs):
		super().__init__(self)
		self.P = kwargs['P']
		self.Phit = kwargs['Phit']
		self.Pmiss = kwargs['Pmiss']
		self.T = kwargs['T']
		self.Taccess = kwargs['Taccess']
		self.scheduler = scheduler

		self.manager = multiprocessing.Manager()
		self.page_fetched = manager.Condition()
		self.request_queue = manager.Queue()
		self.scheduler_free = manager.Lock()

		self.request_count = 0
		self.hit_count = 0
		self.miss_count = 0

		print('MMU log: MMU started, pid', os.getpid())
		self.display()		
		self.start()

	def run(self):
		while True:
			target_page = self.request_queue.get()			
			get_page_log(target_page)
			if self.check_tlb(target_page)
				self.task_tlb_access(target_page)
				self.generate_physical_address(target_page)
				if self.request_count % self.scheduler.C == 0:
					self.flush_tlb()
					self.scheduler_free.acquire()
					self.scheduler.run_scheduler.notify()
			else self.check_ram(target_page):						
				self.task_ram_access(target_page)
				self.update_tlb(target_page)
				self.generate_physical_address(target_page)
				if self.request_count % self.scheduler.C == 0:
					self.flush_tlb()
					self.scheduler_free.acquire()
					self.scheduler.run_scheduler.notify()
			else:
				self.task_disk_access(target_page)
				self.update_page_table(target_page)
				self.request_queue.put(target_page)

	def get_page_log(self, target_page):
		# self.request_count += 1
		print('MMU log:','servicing page request',target_page)

	def generate_physical_address(self, target_page):
		print('MMU log:','serviced page request',target_page)
		self.page_fetched.notify()

	def display(self):
		print('MMU log: MMU details(P, Phit, Pmiss, T, Taccess):', self.P, self.Phit, self.Pmiss, self.T, self.Taccess)