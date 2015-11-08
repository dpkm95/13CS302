import multiprocessing, os

#C - scheduler is invoked every C page requests
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
			while self.run_scheduler:
				self.run_scheduler.wait()
				#round robin algorithm
				dequeue = self.apps.pop(0)
				dequeue.app_lock.acquire()
				self.apps.append(dequeue)
				self.apps[0].app_lock.release()
				self.mmu.scheduler_free.release()

	def schedule_one(self):
		if len(apps) != 0:
			self.apps[1].release()
			return self.apps[0]
		else:
			return -1

	def admit_app(self, app_id, app_lock):
		self.apps.append((app_id,app_lock))

	def release_app(self, app_id):
		for app in self.apps:
			if app[0] == app_id:
				self.apps.remove(app)
		self.run_scheduler.notify()

	def display(self):
		print('Scheduler log: Scheduler details(C):',self.C)