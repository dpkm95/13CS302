import multiprocessing, os, random
import Scheduler

#App - app name
#V 	 - total no of unique virtual pages
#N 	 - number of page requests made by the App
class App(multiprocessing.Process):
	def __init__(self, app_lock, app_release, run_scheduler, scheduler_free, 
					request_queue, page_fetched, **kwargs):
		super().__init__()
		self.app_lock = app_lock
		self.name = kwargs['App']
		self.V = kwargs['V']
		self.N = kwargs['N']

		self.request_count = 0

		self.run_scheduler = run_scheduler
		self.scheduler_free = scheduler_free
		self.request_queue = request_queue
		self.page_fetched = page_fetched
		self.app_release = app_release
		
		self.display()		
		self.start()

	def run(self):
		release_app = False
		# print('app log(',self.pid,'): app',self.name,'started')
		while True:	
			self.app_lock.acquire()
			self.scheduler_free.release()		
			if self.request_count < self.N:
				self.generate_page_request()			
			else:				
				self.scheduler_free.acquire()				
				release_app = True										
			self.app_lock.release()
			self.app_release.release()
			if release_app:
				release_app = False
				self.run_scheduler.put(self.pid)
				# print('app log(',self.pid,'): stopping app',self.name)
				break
			self.scheduler_free.acquire()
		# print('app log(',self.pid,'): app',self.name,'terminated')

	def generate_page_request(self):
		self.request_count += 1
		page = random.randint(0,self.V)
		# print('app log(',self.pid,'): page',page,'requested; request count', self.request_count)
		with self.page_fetched:			
			self.request_queue.put(page)
			self.request_queue.put(self.pid)
			self.page_fetched.wait()
			# print('app log(',self.pid,'): page',page,'recieved')

	def display(self):
		# print('app log: App Details(App name, V, N):',self.name, self.V, self.N)
		pass