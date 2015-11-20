import re
import os, time
import multiprocessing
import App
import Scheduler
import MMU

if __name__ == '__main__':
	apps = []
	scheduler = None
	mmu = None	

	run_scheduler = multiprocessing.Queue() # Used by Scheduler
	page_fetched = multiprocessing.Condition()
	request_queue = multiprocessing.Queue() # Used by MMU
	scheduler_free = multiprocessing.Semaphore(1)
	scheduler_free.acquire()
	app_release = multiprocessing.Semaphore(1)

	#configure apps
	for app in open('config_app.txt'):
		config_app = {}
		app_lock = multiprocessing.Semaphore(1)
		app_lock.acquire()
		for header,value in re.findall(r'(\w+)=(["\w+]+)',app):
			config_app[header]=eval(value)
		new_app = App.App(app_lock, app_release, run_scheduler, scheduler_free, 
							request_queue, page_fetched, **config_app)
		apps.append((new_app.pid, app_lock))

	#configure scheduler
	with open('config_scheduler.txt') as f:
		config_scheduler = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_scheduler[header]=eval(value)
		scheduler = Scheduler.Scheduler(app_release, run_scheduler, scheduler_free, 
											request_queue, apps, **config_scheduler)

	#configure mmu
	with open('config_mmu.txt') as f:
		config_mmu = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_mmu[header]=eval(value)
		mmu = MMU.MMU(scheduler.C, app_release, page_fetched, request_queue,
						 scheduler_free, run_scheduler, **config_mmu)

	#schedule first app
	scheduler.schedule_one()