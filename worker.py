from threading import Thread
from fetcher import fetch
from evaluator import get_all_links, get_all_feeds
from collector import collect
from urllib2 import HTTPError
import logging

class Worker(Thread):
	def __init__(self, queue, visited_urls, mutex, collection, collection_mutex):
		Thread.__init__(self)
		self.queue = queue
		self.visited_urls = visited_urls
		self.mutex = mutex
		self.collection = collection
		self.collection_mutex = collection_mutex
		self.logger = logging.getLogger('data_big_bang.focused_web_crawler')

	def run(self):
		item = self.queue.get()

		while item != None:
			try:
				url = item['url']
				key = item['key']
				constraint = item['constraint']
				data = fetch(url)

				if data == None:
					self.logger.info('Not fetched: %s because type != text/html', url)
				else:
					links = get_all_links(data, base = url)
					feeds = get_all_feeds(data, base = url)
					interesting = collect(links)
	
					if interesting:
						self.collection_mutex.acquire()
						if key not in self.collection:
							self.collection[key] = {'feeds':{}}

						if feeds:
							for feed in feeds:
								self.collection[key]['feeds'][feed['href']] = feed['type']

						for service, accounts in interesting.items():
							if service not in self.collection[key]:
								self.collection[key][service]  = {}

							for a,u in accounts.items():
								self.collection[key][service][a] = {'url': u, 'depth':constraint.depth}
						self.collection_mutex.release()


					for l in links:
						new_constraint = constraint.inherit(url, l)
						if new_constraint == None:
							continue
	
						self.mutex.acquire()
						if l not in self.visited_urls:
							self.queue.put({'url':l, 'key':key, 'constraint': new_constraint})
							self.visited_urls.add(l)
						self.mutex.release()

			except HTTPError:
				self.logger.info('HTTPError exception on url: %s', url)

			self.queue.task_done()

			item = self.queue.get()

		self.queue.task_done() # task_done on None

#		self.queue.put(None) # leave a None for the next Worker
