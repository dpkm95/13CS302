import multiprocessing,os
import Scheduler

#App - app name
#V 	 - total no of unique virtual pages
#N 	 - number of page references made by the App
class App(multiprocessing.Process):
	# app_count = 0
	def __init__(self, app_lock, mmu, **kwargs):
		super().__init__(self)
		# App.app_count += 1
		# self.app_id = App.app_count
		self.app_lock = app_lock
		self.name = kwargs['App']
		self.V = kwargs['V']
		self.N = kwargs['N']
		self.mmu = mmu
		self.references_count = 0
		print('App log: App',self.App,'started, pid:',os.getpid())
		self.display()		
		self.start()

	def run(self):
		while True:
			app_lock.acquire()
			if self.references_count < self.N:
				generate_page_request()
			app_lock.release()				

	def generate_page_request(self):
		page = random.rand(self.V)
		print('App log: page requested-',page,'; request count-',self.references_count+1)
		while self.mmu.page_fetched:			
			self.mmu.request_queue.put(page)
			self.mmu.page_fetched.wait()
			print('App log: recieved page',page)

	def display(self):
		print('App log: App Details(App name, V, N):',self.App, self.V, self.N)
