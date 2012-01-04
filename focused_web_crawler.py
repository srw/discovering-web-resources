from threading import Thread, Lock
from worker import Worker
from Queue import Queue
import logging

class FocusedWebCrawler(Thread):
	NWORKERS = 10
	def __init__(self, nworkers = NWORKERS):
		Thread.__init__(self)
		self.nworkers = nworkers
		#self.queue = DualQueue()
		self.queue = Queue()
		self.visited_urls = set()
		self.mutex = Lock()
		self.workers = []
		self.logger = logging.getLogger('data_big_bang.focused_web_crawler')
		sh = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		sh.setFormatter(formatter)
		self.logger.addHandler(sh)
		self.logger.setLevel(logging.INFO)
		self.collection = {}
		self.collection_mutex = Lock()


	def run(self):
		self.logger.info('Focused Web Crawler launched')
		self.logger.info('Starting workers')
		for i in xrange(self.nworkers):
			worker = Worker(self.queue, self.visited_urls, self.mutex, self.collection, self.collection_mutex)
			self.workers.append(worker)
			worker.start()

		self.queue.join() # Wait until all items are consumed

		for i in xrange(self.nworkers): # send a 'None signal' to finish workers
			self.queue.put(None)

		self.queue.join() # Wait until all workers are notified

#		for worker in self.workers:
#			worker.join()

		self.logger.info('Finished workers')
		self.logger.info('Focused Web Crawler finished')
