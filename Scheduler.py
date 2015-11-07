import multiprocessing, os

#C-scheduler is invoked every C page requests
class Scheduler(multiprocessing.Process):
	apps = []
	scheduler = None
	def __init__(self,**kwargs):
		super().__init__(self)
		self.C = kwargs['C']
		print('Scheduler started, pid:',os.getpid())
		self.display()		
		self.start()

	def admit_app(self,app):
		self.app.append(app)

	def display(self):
		print('Scheduler details(C):',self.C)