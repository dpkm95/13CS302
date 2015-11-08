import multiprocessing, os

#P - no of physical pages in memory
#Phit - time taken to access RAM
#Pmiss - time taken to access 
#T - no of entries in page table
#Taccess - time taken to access TLB
class MMU(multiprocessing.Process):
	def __init__(self, C, **kwargs):
		super().__init__(self)
		self.P = kwargs['P']
		self.Phit = kwargs['Phit']
		self.Pmiss = kwargs['Pmiss']
		self.T = kwargs['T']
		self.Taccess = kwargs['Taccess']
		self.C = C

		self.request_count = 0
		self.hit_count = 0
		self.miss_count = 0

		print('MMU started, pid', os.getpid())
		self.display()		
		self.start()

	def run(self):
		while True:
			'''
				on request
					def get_page(page):
						request_count+=1
						if check_tlb(page):
							task_tlb_access(page)
							generate_physical_address()
							if self.request_count == self.C:
								flush_tlb()
								run_scheduler()
						else check_ram(page):						
							task_ram_access(page)
							update_tlb(page)
							generate_physical_address()
							if self.request_count == self.C:
								flush_tlb()
								run_scheduler()
						else:
							task_disk_access(page)
							update_page_table()
							get_page(page)
			'''
			pass

	def display(self):
		print('MMU details(P, Phit, Pmiss, T, Taccess):', self.P, self.Phit, self.Pmiss, self.T, self.Taccess)