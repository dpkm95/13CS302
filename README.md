##About:
Process Synchronization and Memory Management python simulator
This is a simple python simulation of memory management in a paging system using python multiprocessing module. There are three modules implemented as processes:
  * App
    It makes N page requests to MMU randomly from among V unique virtual pages. Number of apps spawned equals number of entries in config file.
  * Scheduler
    It implements Round-Robin algorithm. It is called for every C page requests to MMU.
  * MMU
    It implements a TLB, which uses LRU algorithm. Taccess(TLB access time), Phit(page fetch time on TLB hit), Pmiss(page fetch time on TLB miss), P(frames in ram), T(entries in TLB) are set in config file.

##Objectives:
  * To find page fault rate of the system
  * To find effective memory access time
  * To find number of TLB misses

##Assumptions:
  * App
    - App makes random page requests.
    - App ends after N page requests.
  * Scheduler
	- Scheduler is called for every C page requests/ on release of an App.
  * MMU
    - Page tables of all processes is located in page-1 in ram.