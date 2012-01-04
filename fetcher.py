import urllib2
import logging


def fetch(uri):
	fetch.logger.info('Fetching: %s', uri)
	#logger = logging.getLogger('data_big_bang.focused_web_crawler')
	print uri
	

	h = urllib2.urlopen(uri)
	if h.headers.type == 'text/html':
		data = h.read()
	else:
		data = None

	return data

fetch.logger = logging.getLogger('data_big_bang.focused_web_crawler')
#fetch.logger.setLevel(logging.INFO)
#fetch.logger.info('Test')
#fetch.logger.info('test %s', 'ddd')
