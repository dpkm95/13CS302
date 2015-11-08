import re, os, multiprocessing
import App
import Scheduler
import MMU

if __name__ == '__main__':
	scheduler = None
	mmu = None
	apps = []
	app_locks = []
	#configure scheduler
	with open('config_scheduler.txt') as f:
		config_scheduler = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_scheduler[header]=eval(value)
		scheduler = Scheduler.Scheduler(**config_scheduler)

	#configure mmu
	with open('config_mmu.txt') as f:
		config_mmu = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',f.read()):
			config_mmu[header]=eval(value)
		mmu = MMU.MMU(scheduler, **config_mmu)		

	#configure apps
	for app in open('config_app.txt'):
		config_app = {}
		app_lock = multiprocessing.Lock()
		app_lock.acquire()
		app_locks.append(app_lock)
		for header,value in re.findall(r'(\w+)=(["\w+]+)',app):
			config_app[header]=eval(value)
		apps.append(App.App(app_lock, mmu, **config_app))
		scheduler.admit_app(app.get_ident(), app_lock)