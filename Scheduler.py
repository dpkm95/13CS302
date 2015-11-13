import multiprocessing

#C - scheduler is invoked every C page requests
class Scheduler(multiprocessing.Process):
	def __init__(self, app_release, run_scheduler, scheduler_free, request_queue, apps, **kwargs):
		super().__init__()
		self.C = kwargs['C']
		self.run_scheduler = run_scheduler
		self.scheduler_free = scheduler_free
		self.request_queue = request_queue
		self.app_release = app_release
		self.ready_apps = apps

		self.display()		
		self.start()	

	def run(self):
		while True:
			call = self.run_scheduler.get()
			if call == -1: #run round robin scheduling algorithm				
				self.app_release.acquire()
				# print('sch log:------------running scheduling algorithm------------')
				self.ready_apps[0][1].acquire()
				dequeue = self.ready_apps.pop(0)
				self.ready_apps.append(dequeue)
				self.ready_apps[0][1].release()
				self.scheduler_free.release()
				self.app_release.release()
			else: #release app
				# print('sch log: -------------------releasing app-------------------')
				app_id = call
				for i,app in enumerate(self.ready_apps):
					if app[0] == app_id:
						app[1].acquire()
						self.ready_apps.pop(i)
				if len(self.ready_apps) == 0:
					# print('All jobs are completed')
					self.request_queue.put(-2)
					self.request_queue.put(self.pid)
					# print('sch log: stopping scheduler')
					break
				else:
					self.ready_apps[0][1].release()

	def schedule_one(self):
		if len(self.ready_apps) != 0:
			self.ready_apps[0][1].release()
			# print('sch log: first app ',self.ready_apps[0][0],'scheduled')
		else:
			# print('sch log: no apps to schedule')
			pass

	def admit_app(self, app_id, app_lock):
		self.ready_apps.append((app_id,app_lock))

	def display(self):
		# print('sch log: Scheduler details(C):',self.C)
		pass