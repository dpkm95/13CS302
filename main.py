import re, os
import App
import Scheduler
import MMU

if __name__ == '__main__':
	scheduler = None
	mmu = None
	apps = []
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
		mmu = MMU.MMU(**config_mmu)

	#configure apps
	for app in open('config_app.txt'):
		config_app = {}
		for header,value in re.findall(r'(\w+)=(["\w+]+)',app):
			config_app[header]=eval(value)
		apps.append(App.App(**config_app))
		# print(app[0].get_ident())
		# scheduler.admit_app(app.get_ident())