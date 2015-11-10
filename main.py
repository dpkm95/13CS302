import re
import os
import multiprocessing
import App
import Scheduler
import MMU

if __name__ == '__main__':
	apps = []
	scheduler = None
	mmu = None	

	run_scheduler = multiprocessing.Queue()
	page_fetched = multiprocessing.Condition()
	request_queue = multiprocessing.Queue()
	scheduler_free = multiprocessing.Semaphore(1)
	scheduler_free.acquire()

	#configure apps
	for app in open('config_app.txt'):
		config_app = {}
		app_lock = multiprocessing.Semaphore(1)
		app_lock.acquire()
		for header,value in re.findall(r'(\w+)=(["\w+]+)',app):
			config_app[header]=eval(value)
		new_app = App.App(app_lock, run_scheduler, scheduler_free, 
							request_queue, page_fetched, **config_app)
		apps.append((new_app.pid, app_lock))

	#configure scheduler
	with open('config_scheduler.txt') as f:
		config_scheduler = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_scheduler[header]=eval(value)
		scheduler = Scheduler.Scheduler(run_scheduler, scheduler_free,
											apps, **config_scheduler)

	#configure mmu
	with open('config_mmu.txt') as f:
		config_mmu = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_mmu[header]=eval(value)
		mmu = MMU.MMU(scheduler.C, page_fetched, request_queue,
						 scheduler_free, **config_mmu)

	#schedule first app
	scheduler.schedule_one()