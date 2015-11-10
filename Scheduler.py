import multiprocessing

#C - scheduler is invoked every C page requests
class Scheduler(multiprocessing.Process):
	def __init__(self, run_scheduler, scheduler_free, apps, **kwargs):
		super().__init__()
		self.C = kwargs['C']
		self.run_scheduler = run_scheduler
		self.scheduler_free = scheduler_free

		self.scheduler = self
		self.ready_apps = apps

		self.display()		
		self.start()	

	def run(self):
		while True:
			call = self.run_scheduler.get()
			if call == -1: #run round robin scheduling algorithm
				dequeue = self.ready_apps.pop(0)
				self.ready_apps.append(dequeue)
				self.ready_apps[0][1].release()
				self.scheduler_free.release()
			else: #release app
				app_id = call
				for i,app in enumerate(self.ready_apps):
					if app[0] == app_id:
						app[1].acquire()
						self.ready_apps.pop(i)
				if len(self.ready_apps) == 0:
					print('All jobs are completed')
					break
				else:
					self.run_scheduler.put(-1)

	def schedule_one(self):
		if len(self.ready_apps) != 0:
			self.ready_apps[0][1].release()
			print('sch log: first app ',self.ready_apps[0][0],'scheduled')
		else:
			print('sch log: no apps to schedule')

	def admit_app(self, app_id, app_lock):
		self.ready_apps.append((app_id,app_lock))

	def display(self):
		print('sch log: Scheduler details(C):',self.C)