import multiprocessing, os

#C-scheduler is invoked every C page requests
class Scheduler(multiprocessing.Process):
	apps = []
	scheduler = None
	def __init__(self,**kwargs):
		super().__init__(self)
		self.C = kwargs['C']

		self.manager = multiprocessing.Manager()
		self.run_scheduler = self.manager.Condition()

		print('Scheduler log: Scheduler started, pid:',os.getpid())
		self.display()		
		self.start()

	def run(self):
		while True:
			'''
				on run_scheduler() call from mmu
					ready.enqueue(ready.dequeue())
					ready.top()
			'''
			while self.run_scheduler:
				self.run_scheduler.wait()
				#scheculer functionality - round robin algorithm
				pass

	def admit_app(self, app_id, app_lock):
		self.apps.append((app_id,app_lock))

	def display(self):
		print('Scheduler log: Scheduler details(C):',self.C)