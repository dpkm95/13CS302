import multiprocessing,os
import Scheduler

#App - app name
#V 	 - total no of unique virtual pages
#N 	 - number of page references made by the App
class App(multiprocessing.Process):
	# app_count = 0
	def __init__(self, app_lock, **kwargs):
		super().__init__(self)
		# App.app_count += 1
		# self.app_id = App.app_count
		self.app_lock = app_lock
		self.name = kwargs['App']
		self.V = kwargs['V']
		self.N = kwargs['N']
		self.references_count = 0
		print('App',self.App,'started, pid:',os.getpid())
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
		print('Page request(count, page):',self.references_count+1,page)

	def display(self):
		print('App Details(App name, V, N):',self.App, self.V, self.N)
