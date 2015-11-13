import multiprocessing, time
import collections

#P - no of physical pages in memory
#Phit - time taken to access RAM
#Pmiss - time taken to access 
#T - no of entries in page table
#Taccess - time taken to access TLB

'''
TLB functioning:
	-> if tlb-hit
		total_access_time += Taccess (to access TLB) + Phit (to access page)
	-> if page-table-hit
		total_access_time += Taccess (to access TLB; miss) + Phit (to access page-table) + Phit (to access page)
	-> if page-table-miss
		total_access_time += Taccess (to access TLB; miss) + Phit (to access page-table; miss) + 
								Pmiss (to access disk) + Taccess (to access TLB; miss) + 
								Phit (to access page-table) + Phit (to access page)
'''
class MMU(multiprocessing.Process):
	def __init__(self, C, app_release, page_fetched, request_queue, scheduler_free, run_scheduler, **kwargs):
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
		self.run_scheduler = run_scheduler
		self.app_release = app_release

		self.request_count = 0
		self.tlb_miss_count = 0
		self.page_fault_count = 0
		self.total_access_time = 0
		self.service_start_time = 0
		self.updated_count = False

		self.tlb_hashmap = dict()
		self.ram_hashmap = dict()
		
		self.display()		
		self.start()

	def run(self):
		# print('mmu log: MMU started, pid', self.pid)
		while True:			
			target_page = self.request_queue.get()
			app_id = self.request_queue.get()
			if target_page == -1:
				self.flush_tlb()
			elif target_page == -2:
				self.print_result()
				break
			else:
				if not self.updated_count:
					self.update_counts(target_page)
					self.updated_count = True
				#tlb-hit
				if self.check_tlb(target_page):
					self.task_tlb_access(target_page)
					if self.request_count % self.C == 0:
						self.scheduler_free.acquire()
						self.app_release.acquire()				
						self.flush_tlb()
						self.generate_physical_address(target_page)						
						self.run_scheduler.put(-1)
					else:
						self.generate_physical_address(target_page)
				#page-table-hit
				elif self.check_page_table(target_page, app_id):	
					self.task_ram_access(target_page, app_id)
					self.update_tlb(target_page)
					self.generate_physical_address(target_page)
				#page-table-miss
				else:					
					self.task_disk_access(target_page)
					self.update_page_table(target_page, app_id)
					self.request_queue.put(target_page)
					self.request_queue.put(app_id)

	def print_result(self):
		print('mmu log: stopping mmu')
		print('\nResults:\n')
		print('page faults recorded         =',self.page_fault_count)
		print('page requests recorded       =',self.request_count)
		print('total access time recorded   =',self.total_access_time,'us')
		print('\n')
		print('page fault rate              =',round((self.page_fault_count)/self.request_count,2),'faults/request')
		print('effective memory access time =',round(self.total_access_time/self.request_count,2),'us')
		print('number of TLB misses         =',self.tlb_miss_count)

	def check_tlb(self,target_page):
		self.total_access_time += self.Taccess
		if target_page in self.tlb_hashmap:
			# print('mmu log: tlb hit on page',target_page)		
			return True			
		else: 
			# print('mmu log: tlb miss on page',target_page)
			return False

	def check_page_table(self,target_page, app_id):
		self.total_access_time += self.Phit
		if (target_page, app_id) in self.ram_hashmap:
			# print('mmu log: page table hit on page',target_page)		
			return True			
		else: 
			# print('mmu log: page table miss on page',target_page)
			return False

	def task_tlb_access(self, target_page):					
		self.tlb_hashmap[target_page] = time.time()
		# print('mmu log: tlb accessed; total_access_time =',self.total_access_time)	

	def task_ram_access(self, target_page, app_id):
		self.tlb_miss_count += 1
		self.ram_hashmap[(target_page, app_id)] = time.time()
		# print('mmu log: ram accessed by',app_id,'; total_access_time =',self.total_access_time)

	def flush_tlb(self):
		# print('mmu log: tlb flushed')
		self.tlb_hashmap = dict()

	def task_disk_access(self, target_page):
		self.page_fault_count += 1
		self.total_access_time += self.Pmiss
		# print('mmu log: disk accessed; total_access_time =',self.total_access_time)		

	def update_tlb(self, target_page):		
		if len(self.tlb_hashmap) < self.T:
			self.tlb_hashmap[target_page] = time.time()
		else:
			evicted_entry = collections.OrderedDict(sorted(self.tlb_hashmap.items(), reverse = True)).popitem()
			del self.tlb_hashmap[evicted_entry[0]]
			self.tlb_hashmap[target_page] = time.time()
		# print('mmu log: updated tlb with page',target_page)

	def update_page_table(self, target_page, app_id):
		#page-table resides in page-1
		if len(self.ram_hashmap) < self.P - 1:
			self.ram_hashmap[(target_page, app_id)] = time.time()
		else:
			evicted_entry = collections.OrderedDict(sorted(self.ram_hashmap.items(), reverse = True)).popitem()
			del self.ram_hashmap[evicted_entry[0]]
			self.ram_hashmap[(target_page, app_id)] = time.time()
		# print('mmu log: updated page table with page',target_page)

	def update_counts(self,target_page):
		# print('mmu log: servicing request for page',target_page)		
		self.service_start_time = self.total_access_time
		self.request_count += 1

	def generate_physical_address(self, target_page):
		self.total_access_time += self.Phit
		# print('mmu log: serviced page request',target_page,'in',self.total_access_time-self.service_start_time,'us')		
		self.updated_count = False
		with self.page_fetched:
			self.page_fetched.notify()

	def display(self):
		# print('mmu log: MMU details(P, Phit, Pmiss, T, Taccess):', self.P, self.Phit, self.Pmiss, self.T, self.Taccess)
		pass