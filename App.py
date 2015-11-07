import multiprocessing,os
import Scheduler

#App - app name
#V 	 - total no of unique virtual pages
#N 	 - number of page references made by the App
class App(multiprocessing.Process):
	def __init__(self, **kwargs):
		super().__init__(self)
		self.name = kwargs['App']
		self.V = kwargs['V']
		self.N = kwargs['N']
		print('App',self.App,'started, pid:',os.getpid())
		self.display()		
		self.start()

	def display(self):
		print('App Details(App name, V, N):',self.App, self.V, self.N)
